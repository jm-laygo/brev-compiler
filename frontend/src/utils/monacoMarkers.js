export function parseLineColumn(message) {
    if (!message) {
        return null;
    }

    const matchedLocation = String(message).match(/Ln\s*(\d+)\s*,\s*Col\s*(\d+)/i);

    if (!matchedLocation) {
        return null;
    }

    return {
        lineNumber: Number(matchedLocation[1]),
        columnNumber: Number(matchedLocation[2]),
    };
}

function clampNumber(numberValue, minimumValue, maximumValue) {
    return Math.max(
        minimumValue,
        Math.min(maximumValue, numberValue)
    );
}

function inferMarkerRangeLength(message) {
    const messageText = String(message);

    const identifierMatch = messageText.match(/identifier\s+'([^']+)'/i);

    if (identifierMatch?.[1]) {
        return Math.max(1, identifierMatch[1].length);
    }

    const quotedTextMatch = messageText.match(/'([^']+)'/);

    if (quotedTextMatch?.[1]) {
        return Math.max(1, quotedTextMatch[1].length);
    }

    const suggestionMatch = messageText.match(/Did you mean\s+'([^']+)'/i);

    if (suggestionMatch?.[1]) {
        return Math.max(1, suggestionMatch[1].length);
    }

    if (/Expected/i.test(messageText)) {
        return 2;
    }

    if (/Trailing tokens/i.test(messageText)) {
        return 2;
    }

    if (/unknown|invalid|unexpected/i.test(messageText)) {
        return 2;
    }

    return 1;
}

export function buildEditorMarkers(errors, monaco, editor) {
    const errorList = Array.isArray(errors) ? errors : [];
    const editorModel = editor?.getModel?.();

    const getLineMaximumColumn = (lineNumber) => {
        if (!editorModel) {
            return 1000000;
        }

        const lineContent = editorModel.getLineContent(lineNumber) || "";

        return Math.max(1, lineContent.length + 1);
    };

    return errorList
        .map((errorMessage) => {
            const parsedPosition = parseLineColumn(errorMessage);

            if (!parsedPosition) {
                return null;
            }

            const markerMessage = String(errorMessage);
            const markerLineNumber = Math.max(1, parsedPosition.lineNumber);
            const maximumColumn = getLineMaximumColumn(markerLineNumber);

            const startColumn = clampNumber(
                Math.max(1, parsedPosition.columnNumber),
                1,
                maximumColumn
            );

            const rangeLength = inferMarkerRangeLength(markerMessage);

            const endColumn = clampNumber(
                startColumn + rangeLength,
                startColumn + 1,
                maximumColumn
            );

            return {
                severity: monaco.MarkerSeverity.Error,
                message: markerMessage,
                startLineNumber: markerLineNumber,
                startColumn,
                endLineNumber: markerLineNumber,
                endColumn,
            };
        })
        .filter(Boolean);
}

export function applyEditorMarkers(editor, monaco, errors, markerOwner = "brev") {
    if (!editor || !monaco) {
        return;
    }

    const editorModel = editor.getModel();

    if (!editorModel) {
        return;
    }

    const editorMarkers = buildEditorMarkers(errors, monaco, editor);

    monaco.editor.setModelMarkers(
        editorModel,
        markerOwner,
        editorMarkers
    );
}

export function clearEditorMarkers(editor, monaco, markerOwner = "brev") {
    if (!editor || !monaco) {
        return;
    }

    const editorModel = editor.getModel();

    if (!editorModel) {
        return;
    }

    monaco.editor.setModelMarkers(
        editorModel,
        markerOwner,
        []
    );
}

export function jumpToFirstEditorMarker(editor, monaco) {
    if (!editor || !monaco) {
        return;
    }

    const editorModel = editor.getModel();

    if (!editorModel) {
        return;
    }

    const editorMarkers = monaco.editor.getModelMarkers({
        resource: editorModel.uri,
    }) || [];

    if (!editorMarkers.length) {
        return;
    }

    editorMarkers.sort((firstMarker, secondMarker) => {
        if (firstMarker.startLineNumber !== secondMarker.startLineNumber) {
            return firstMarker.startLineNumber - secondMarker.startLineNumber;
        }

        return firstMarker.startColumn - secondMarker.startColumn;
    });

    const firstMarker = editorMarkers[0];

    editor.revealPositionInCenter({
        lineNumber: firstMarker.startLineNumber,
        column: firstMarker.startColumn,
    });

    editor.setPosition({
        lineNumber: firstMarker.startLineNumber,
        column: firstMarker.startColumn,
    });

    editor.focus();
}