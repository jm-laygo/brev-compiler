import { useCallback, useEffect, useRef } from "react";
import { applyMarkers, clearMarkers } from "../../utils/monacoMarkers.js";

function getTokenStart(token) {
    const p = token?.pos ?? token?.position ?? null;
    const ln = Number(p?.ln ?? p?.line ?? token?.ln ?? token?.line ?? 0);
    const col = Number(p?.col ?? p?.column ?? token?.col ?? token?.column ?? 0);
    return { ln, col };
}

function comparePos(a, b) {
    if (a.ln !== b.ln) return a.ln - b.ln;
    return a.col - b.col;
}

function pickTokenIndexFromCursor(tokens, cursorLn, cursorCol) {
    const cursor = { ln: Number(cursorLn) || 1, col: Number(cursorCol) || 1 };

    let bestIdx = -1;
    let bestDist = Infinity;

    for (let i = 0; i < tokens.length; i += 1) {
        const t = tokens[i];
        if (!t || t.hidden) continue;

        const start = getTokenStart(t);
        if (start.ln <= 0 || start.col <= 0) continue;

        const c = comparePos(start, cursor);
        if (c > 0) continue;

        const dist = (cursor.ln - start.ln) * 100000 + (cursor.col - start.col);
        if (dist >= 0 && dist < bestDist) {
            bestDist = dist;
            bestIdx = i;
        }
    }

    return bestIdx;
}

export default function useEditorBridge({
    tokens = [],
    onActiveTokenRangeChange,
    onActiveTokenHeadIndexChange,
} = {}) {
    const editorRef = useRef(null);
    const editorApiRef = useRef(null);
    const sourceRef = useRef("");

    const getCode = useCallback(() => {
        return editorRef.current ? editorRef.current.getValue() : sourceRef.current || "";
    }, []);

    const setSource = useCallback((v) => {
        sourceRef.current = v ?? "";
    }, []);

    const onEditorReady = useCallback(({ editor, monaco }) => {
        editorApiRef.current = { editor, monaco };
    }, []);

    const clearAllEditorMarkers = useCallback(() => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;
        clearMarkers(api.editor, api.monaco, "brev");
    }, []);

    const setMarkersFromErrors = useCallback((errors) => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;

        clearMarkers(api.editor, api.monaco, "brev");

        const errs = Array.isArray(errors) ? errors : [];
        if (errs.length) applyMarkers(api.editor, api.monaco, errs, "brev");
    }, []);

    const jumpToPosition = useCallback((line, col) => {
        const api = editorApiRef.current;
        if (!api?.editor) return;

        const lineNumber = Math.max(1, Number(line) || 1);
        const column = Math.max(1, Number(col) || 1);

        api.editor.revealPositionInCenter({ lineNumber, column });
        api.editor.setPosition({ lineNumber, column });
        api.editor.focus();
    }, []);

    const jumpToToken = useCallback((token) => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;
        if (!token) return;

        const editor = api.editor;
        const monaco = api.monaco;

        const pos = token.pos ?? token.position ?? null;

        const lineNumber = Math.max(
            1,
            Number(pos?.ln ?? pos?.line ?? token.ln ?? token.line ?? 1)
        );
        const column = Math.max(
            1,
            Number(pos?.col ?? pos?.column ?? token.col ?? token.column ?? 1)
        );

        const model = editor.getModel();
        if (!model) return;

        const lineText = model.getLineContent(lineNumber);

        let endColumn = column + 1;
        const rest = lineText.slice(Math.max(0, column - 1));
        const m = rest.match(/^[A-Za-z_]\w*/);
        if (m && m[0]) endColumn = column + m[0].length;

        const range = new monaco.Range(lineNumber, column, lineNumber, endColumn);

        editor.setSelection(range);
        editor.revealRangeInCenter(range);
        editor.focus();
    }, []);

    useEffect(() => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;

        const editor = api.editor;
        const monaco = api.monaco;

        const RTL = monaco?.SelectionDirection?.RTL;

        function adjustExclusivePosition(ln, col) {
            let outLn = Number(ln) || 1;
            let outCol = Number(col) || 1;

            if (outCol <= 1) {
                if (outLn > 1) {
                    outLn -= 1;

                    try {
                        const model = editor.getModel?.();
                        if (model) {
                            const lineLen = model.getLineLength(outLn);
                            return { ln: outLn, col: Math.max(1, lineLen + 1) };
                        }
                    } catch {
                        // ignore
                    }

                    return { ln: outLn, col: 1_000_000 };
                }
                return { ln: 1, col: 1 };
            }

            return { ln: outLn, col: outCol - 1 };
        }

        const sub = editor.onDidChangeCursorSelection((evt) => {
            const sel = evt?.selection ?? editor.getSelection?.();
            if (!sel) return;

            const safeTokens = Array.isArray(tokens) ? tokens : [];

            const sp = sel.getStartPosition?.();
            const ep = sel.getEndPosition?.();
            if (!sp || !ep) return;

            const isEmpty = typeof sel.isEmpty === "function" ? sel.isEmpty() : true;

            const dir = typeof sel.getDirection === "function" ? sel.getDirection() : null;
            const isRTL = dir === RTL;

            const activeRaw =
                (typeof sel.getPosition === "function" ? sel.getPosition() : null) ||
                (isRTL ? sp : ep);

            const sLn = sp.lineNumber;
            const sCol = sp.column;

            let eLn = ep.lineNumber;
            let eCol = ep.column;

            let hLn = activeRaw.lineNumber;
            let hCol = activeRaw.column;

            if (!isEmpty) {
                const endAdj = adjustExclusivePosition(eLn, eCol);
                eLn = endAdj.ln;
                eCol = endAdj.col;

                if (!isRTL) {
                    const headAdj = adjustExclusivePosition(hLn, hCol);
                    hLn = headAdj.ln;
                    hCol = headAdj.col;
                }
            }

            const startIdxRaw = pickTokenIndexFromCursor(safeTokens, sLn, sCol);
            const endIdxRaw = pickTokenIndexFromCursor(safeTokens, eLn, eCol);
            const headIdx = pickTokenIndexFromCursor(safeTokens, hLn, hCol);

            if (typeof onActiveTokenRangeChange === "function") {
                if (startIdxRaw < 0 && endIdxRaw < 0) {
                    onActiveTokenRangeChange({ start: -1, end: -1 });
                } else if (startIdxRaw < 0) {
                    onActiveTokenRangeChange({ start: endIdxRaw, end: endIdxRaw });
                } else if (endIdxRaw < 0) {
                    onActiveTokenRangeChange({ start: startIdxRaw, end: startIdxRaw });
                } else {
                    onActiveTokenRangeChange({
                        start: Math.min(startIdxRaw, endIdxRaw),
                        end: Math.max(startIdxRaw, endIdxRaw),
                    });
                }
            }

            if (typeof onActiveTokenHeadIndexChange === "function") {
                onActiveTokenHeadIndexChange(headIdx);
            }
        });

        return () => {
            try {
                sub?.dispose?.();
            } catch {
                // ignore
            }
        };
    }, [tokens, onActiveTokenRangeChange, onActiveTokenHeadIndexChange]);

    return {
        editorRef,
        getCode,
        setSource,
        onEditorReady,
        clearAllEditorMarkers,
        setMarkersFromErrors,
        jumpToToken,
        jumpToPosition,
    };
}