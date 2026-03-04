export function parseLnCol(message) {
    if (!message) return null;

    const m = String(message).match(/Ln\s*(\d+)\s*,\s*Col\s*(\d+)/i);
    if (!m) return null;

    return {
        line: Number(m[1]),
        col: Number(m[2]),
    };
}

function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
}

function inferRangeLength(msg) {
    const s = String(msg);

    const ident = s.match(/identifier\s+'([^']+)'/i);
    if (ident?.[1]) return Math.max(1, ident[1].length);

    const quoted = s.match(/'([^']+)'/);
    if (quoted?.[1]) return Math.max(1, quoted[1].length);

    const didYouMean = s.match(/Did you mean\s+'([^']+)'/i);
    if (didYouMean?.[1]) return Math.max(1, didYouMean[1].length);

    if (/Expected/i.test(s)) return 2;
    if (/Trailing tokens/i.test(s)) return 2;
    if (/unknown|invalid|unexpected/i.test(s)) return 2;

    return 1;
}

export function buildMarkers(errors, monaco, editor) {
    const list = Array.isArray(errors) ? errors : [];
    const model = editor?.getModel?.();

    const getLineMaxCol = (line) => {
        if (!model) return 1000000;
        const lc = model.getLineContent(line) || "";
        return Math.max(1, lc.length + 1);
    };

    return list
        .map((msg) => {
            const pos = parseLnCol(msg);
            if (!pos) return null;

            const s = String(msg);
            const line = Math.max(1, pos.line);
            const maxCol = getLineMaxCol(line);

            const startColumn = clamp(Math.max(1, pos.col), 1, maxCol);
            const len = inferRangeLength(s);
            const endColumn = clamp(startColumn + len, startColumn + 1, maxCol);

            return {
                severity: monaco.MarkerSeverity.Error,
                message: s,
                startLineNumber: line,
                startColumn,
                endLineNumber: line,
                endColumn,
            };
        })
        .filter(Boolean);
}

export function applyMarkers(editor, monaco, errors, owner = "brev") {
    if (!editor || !monaco) return;

    const model = editor.getModel();
    if (!model) return;

    const markers = buildMarkers(errors, monaco, editor);
    monaco.editor.setModelMarkers(model, owner, markers);
}

export function clearMarkers(editor, monaco, owner = "brev") {
    if (!editor || !monaco) return;

    const model = editor.getModel();
    if (!model) return;

    monaco.editor.setModelMarkers(model, owner, []);
}

export function jumpToFirstMarker(editor, monaco) {
    if (!editor || !monaco) return;

    const model = editor.getModel();
    if (!model) return;

    const markers = monaco.editor.getModelMarkers({ resource: model.uri }) || [];
    if (!markers.length) return;

    markers.sort((a, b) => {
        if (a.startLineNumber !== b.startLineNumber) return a.startLineNumber - b.startLineNumber;
        return a.startColumn - b.startColumn;
    });

    const m = markers[0];

    editor.revealPositionInCenter({ lineNumber: m.startLineNumber, column: m.startColumn });
    editor.setPosition({ lineNumber: m.startLineNumber, column: m.startColumn });
    editor.focus();
}