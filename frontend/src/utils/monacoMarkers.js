export function parseLnCol(message) {
    if (!message) return null;

    const m = String(message).match(/Ln\s*(\d+)\s*,\s*Col\s*(\d+)/i);
    if (!m) return null;

    return {
        line: Number(m[1]),
        col: Number(m[2]),
    };
}

export function buildMarkers(errors, monaco) {
    const list = Array.isArray(errors) ? errors : [];

    return list
        .map((msg) => {
            const pos = parseLnCol(msg);
            if (!pos) return null;

            const line = Math.max(1, pos.line);
            const col = Math.max(1, pos.col);

            const s = String(msg);

            let length = 1;

            const ident = s.match(/identifier\s+'([^']+)'/i);
            if (ident && ident[1]) {
                length = Math.max(1, ident[1].length);
            } else {
                const quoted = s.match(/'([^']+)'/);
                if (quoted && quoted[1]) {
                    length = Math.max(1, quoted[1].length);
                }
            }

            return {
                severity: monaco.MarkerSeverity.Error,
                message: s,
                startLineNumber: line,
                startColumn: col,
                endLineNumber: line,
                endColumn: col + length,
            };
        })
        .filter(Boolean);
}

export function applyMarkers(editor, monaco, errors, owner = "brev") {
    if (!editor || !monaco) return;

    const model = editor.getModel();
    if (!model) return;

    const markers = buildMarkers(errors, monaco);
    monaco.editor.setModelMarkers(model, owner, markers);
}

export function clearMarkers(editor, monaco, owner = "brev") {
    if (!editor || !monaco) return;

    const model = editor.getModel();
    if (!model) return;

    monaco.editor.setModelMarkers(model, owner, []);
}

export function jumpToFirstError(editor, errors) {
    if (!editor) return;

    const list = Array.isArray(errors) ? errors : [];
    if (list.length === 0) return;

    const pos = parseLnCol(list[0]);
    if (!pos) return;

    editor.revealPositionInCenter({ lineNumber: pos.line, column: pos.col });
    editor.setPosition({ lineNumber: pos.line, column: pos.col });
    editor.focus();
}