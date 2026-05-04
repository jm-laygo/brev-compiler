import { useCallback, useEffect, useRef } from "react";
import {
    applyEditorMarkers,
    clearEditorMarkers,
} from "../../utils/monacoMarkers.js";

function getTokenStartPosition(token) {
    const tokenPosition = token?.position ?? token?.pos ?? null;

    const lineNumber = Number(
        tokenPosition?.lineNumber ??
            tokenPosition?.ln ??
            tokenPosition?.line ??
            token?.lineNumber ??
            token?.ln ??
            token?.line ??
            0
    );

    const columnNumber = Number(
        tokenPosition?.columnNumber ??
            tokenPosition?.col ??
            tokenPosition?.column ??
            token?.columnNumber ??
            token?.col ??
            token?.column ??
            0
    );

    return {
        lineNumber,
        columnNumber,
    };
}

function compareTokenPositions(firstPosition, secondPosition) {
    if (firstPosition.lineNumber !== secondPosition.lineNumber) {
        return firstPosition.lineNumber - secondPosition.lineNumber;
    }

    return firstPosition.columnNumber - secondPosition.columnNumber;
}

function pickTokenIndexFromCursor(tokens, cursorLineNumber, cursorColumnNumber) {
    const cursorPosition = {
        lineNumber: Number(cursorLineNumber) || 1,
        columnNumber: Number(cursorColumnNumber) || 1,
    };

    let bestTokenIndex = -1;
    let bestTokenDistance = Infinity;

    for (let tokenIndex = 0; tokenIndex < tokens.length; tokenIndex += 1) {
        const tokenItem = tokens[tokenIndex];

        if (!tokenItem || tokenItem.hidden) {
            continue;
        }

        const tokenStartPosition = getTokenStartPosition(tokenItem);

        if (
            tokenStartPosition.lineNumber <= 0 ||
            tokenStartPosition.columnNumber <= 0
        ) {
            continue;
        }

        const positionComparison = compareTokenPositions(
            tokenStartPosition,
            cursorPosition
        );

        if (positionComparison > 0) {
            continue;
        }

        const tokenDistance =
            (cursorPosition.lineNumber - tokenStartPosition.lineNumber) * 100000 +
            (cursorPosition.columnNumber - tokenStartPosition.columnNumber);

        if (tokenDistance >= 0 && tokenDistance < bestTokenDistance) {
            bestTokenDistance = tokenDistance;
            bestTokenIndex = tokenIndex;
        }
    }

    return bestTokenIndex;
}

export default function useEditorBridge({
    tokens = [],
    onActiveTokenRangeChange,
    onActiveTokenHeadIndexChange,
} = {}) {
    const editorRef = useRef(null);
    const editorApiRef = useRef(null);
    const sourceCodeRef = useRef("");

    const getCode = useCallback(() => {
        if (editorRef.current) {
            return editorRef.current.getValue();
        }

        return sourceCodeRef.current || "";
    }, []);

    const setSource = useCallback((sourceCode) => {
        sourceCodeRef.current = sourceCode ?? "";
    }, []);

    const onEditorReady = useCallback(({ editor, monaco }) => {
        editorApiRef.current = {
            editor,
            monaco,
        };
    }, []);

    const clearAllEditorMarkers = useCallback(() => {
        const editorApi = editorApiRef.current;

        if (!editorApi?.editor || !editorApi?.monaco) {
            return;
        }

        clearEditorMarkers(
            editorApi.editor,
            editorApi.monaco,
            "brev"
        );
    }, []);

    const setMarkersFromErrors = useCallback((errors) => {
        const editorApi = editorApiRef.current;

        if (!editorApi?.editor || !editorApi?.monaco) {
            return;
        }

        clearEditorMarkers(
            editorApi.editor,
            editorApi.monaco,
            "brev"
        );

        const errorList = Array.isArray(errors) ? errors : [];

        if (errorList.length) {
            applyEditorMarkers(
                editorApi.editor,
                editorApi.monaco,
                errorList,
                "brev"
            );
        }
    }, []);

    const jumpToPosition = useCallback((lineNumber, columnNumber) => {
        const editorApi = editorApiRef.current;

        if (!editorApi?.editor) {
            return;
        }

        const safeLineNumber = Math.max(1, Number(lineNumber) || 1);
        const safeColumnNumber = Math.max(1, Number(columnNumber) || 1);

        editorApi.editor.revealPositionInCenter({
            lineNumber: safeLineNumber,
            column: safeColumnNumber,
        });

        editorApi.editor.setPosition({
            lineNumber: safeLineNumber,
            column: safeColumnNumber,
        });

        editorApi.editor.focus();
    }, []);

    const jumpToToken = useCallback((token) => {
        const editorApi = editorApiRef.current;

        if (!editorApi?.editor || !editorApi?.monaco) {
            return;
        }

        if (!token) {
            return;
        }

        const editor = editorApi.editor;
        const monaco = editorApi.monaco;
        const tokenPosition = token.position ?? token.pos ?? null;

        const lineNumber = Math.max(
            1,
            Number(
                tokenPosition?.lineNumber ??
                    tokenPosition?.ln ??
                    tokenPosition?.line ??
                    token.lineNumber ??
                    token.ln ??
                    token.line ??
                    1
            )
        );

        const columnNumber = Math.max(
            1,
            Number(
                tokenPosition?.columnNumber ??
                    tokenPosition?.col ??
                    tokenPosition?.column ??
                    token.columnNumber ??
                    token.col ??
                    token.column ??
                    1
            )
        );

        const editorModel = editor.getModel();

        if (!editorModel) {
            return;
        }

        const lineText = editorModel.getLineContent(lineNumber);
        const remainingLineText = lineText.slice(Math.max(0, columnNumber - 1));
        const wordMatch = remainingLineText.match(/^[A-Za-z_]\w*/);

        let endColumnNumber = columnNumber + 1;

        if (wordMatch && wordMatch[0]) {
            endColumnNumber = columnNumber + wordMatch[0].length;
        }

        const tokenRange = new monaco.Range(
            lineNumber,
            columnNumber,
            lineNumber,
            endColumnNumber
        );

        editor.setSelection(tokenRange);
        editor.revealRangeInCenter(tokenRange);
        editor.focus();
    }, []);

    useEffect(() => {
        const editorApi = editorApiRef.current;

        if (!editorApi?.editor || !editorApi?.monaco) {
            return;
        }

        const editor = editorApi.editor;
        const monaco = editorApi.monaco;
        const rightToLeftDirection = monaco?.SelectionDirection?.RTL;

        function adjustExclusivePosition(lineNumber, columnNumber) {
            let adjustedLineNumber = Number(lineNumber) || 1;
            let adjustedColumnNumber = Number(columnNumber) || 1;

            if (adjustedColumnNumber <= 1) {
                if (adjustedLineNumber > 1) {
                    adjustedLineNumber -= 1;

                    try {
                        const editorModel = editor.getModel?.();

                        if (editorModel) {
                            const lineLength = editorModel.getLineLength(
                                adjustedLineNumber
                            );

                            return {
                                lineNumber: adjustedLineNumber,
                                columnNumber: Math.max(1, lineLength + 1),
                            };
                        }
                    } catch {
                        // ignore
                    }

                    return {
                        lineNumber: adjustedLineNumber,
                        columnNumber: 1000000,
                    };
                }

                return {
                    lineNumber: 1,
                    columnNumber: 1,
                };
            }

            return {
                lineNumber: adjustedLineNumber,
                columnNumber: adjustedColumnNumber - 1,
            };
        }

        const cursorSelectionSubscription = editor.onDidChangeCursorSelection(
            (event) => {
                const selection = event?.selection ?? editor.getSelection?.();

                if (!selection) {
                    return;
                }

                const safeTokenList = Array.isArray(tokens) ? tokens : [];

                const selectionStartPosition = selection.getStartPosition?.();
                const selectionEndPosition = selection.getEndPosition?.();

                if (!selectionStartPosition || !selectionEndPosition) {
                    return;
                }

                const isSelectionEmpty =
                    typeof selection.isEmpty === "function"
                        ? selection.isEmpty()
                        : true;

                const selectionDirection =
                    typeof selection.getDirection === "function"
                        ? selection.getDirection()
                        : null;

                const isRightToLeftSelection =
                    selectionDirection === rightToLeftDirection;

                const activeRawPosition =
                    (typeof selection.getPosition === "function"
                        ? selection.getPosition()
                        : null) ||
                    (isRightToLeftSelection
                        ? selectionStartPosition
                        : selectionEndPosition);

                const startLineNumber = selectionStartPosition.lineNumber;
                const startColumnNumber = selectionStartPosition.column;

                let endLineNumber = selectionEndPosition.lineNumber;
                let endColumnNumber = selectionEndPosition.column;

                let headLineNumber = activeRawPosition.lineNumber;
                let headColumnNumber = activeRawPosition.column;

                if (!isSelectionEmpty) {
                    const adjustedEndPosition = adjustExclusivePosition(
                        endLineNumber,
                        endColumnNumber
                    );

                    endLineNumber = adjustedEndPosition.lineNumber;
                    endColumnNumber = adjustedEndPosition.columnNumber;

                    if (!isRightToLeftSelection) {
                        const adjustedHeadPosition = adjustExclusivePosition(
                            headLineNumber,
                            headColumnNumber
                        );

                        headLineNumber = adjustedHeadPosition.lineNumber;
                        headColumnNumber = adjustedHeadPosition.columnNumber;
                    }
                }

                const rawStartTokenIndex = pickTokenIndexFromCursor(
                    safeTokenList,
                    startLineNumber,
                    startColumnNumber
                );

                const rawEndTokenIndex = pickTokenIndexFromCursor(
                    safeTokenList,
                    endLineNumber,
                    endColumnNumber
                );

                const headTokenIndex = pickTokenIndexFromCursor(
                    safeTokenList,
                    headLineNumber,
                    headColumnNumber
                );

                if (typeof onActiveTokenRangeChange === "function") {
                    if (rawStartTokenIndex < 0 && rawEndTokenIndex < 0) {
                        onActiveTokenRangeChange({
                            start: -1,
                            end: -1,
                        });
                    } else if (rawStartTokenIndex < 0) {
                        onActiveTokenRangeChange({
                            start: rawEndTokenIndex,
                            end: rawEndTokenIndex,
                        });
                    } else if (rawEndTokenIndex < 0) {
                        onActiveTokenRangeChange({
                            start: rawStartTokenIndex,
                            end: rawStartTokenIndex,
                        });
                    } else {
                        onActiveTokenRangeChange({
                            start: Math.min(rawStartTokenIndex, rawEndTokenIndex),
                            end: Math.max(rawStartTokenIndex, rawEndTokenIndex),
                        });
                    }
                }

                if (typeof onActiveTokenHeadIndexChange === "function") {
                    onActiveTokenHeadIndexChange(headTokenIndex);
                }
            }
        );

        return () => {
            try {
                cursorSelectionSubscription?.dispose?.();
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