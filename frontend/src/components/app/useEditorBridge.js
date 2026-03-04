import { useRef, useCallback } from "react";
import { applyMarkers, clearMarkers } from "../../utils/monacoMarkers.js";

export default function useEditorBridge() {
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

        const lineNumber = Math.max(1, Number(pos?.ln ?? pos?.line ?? token.ln ?? token.line ?? 1));
        const column = Math.max(1, Number(pos?.col ?? pos?.column ?? token.col ?? token.column ?? 1));

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