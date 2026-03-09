async function postJson(url, body, signal) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal,
    });

    const data = await res.json().catch(() => ({}));
    return { res, data };
}

export async function runLexical(source_code, signal) {
    return postJson("/api/lex", { source_code }, signal);
}

export async function runSyntax(source_code, signal) {
    return postJson("/api/syntax", { source_code }, signal);
}

export async function runSemantic(source_code, signal) {
    return postJson("/api/sem", { source_code }, signal);
}

export async function runStartExecute(source_code, signal) {
    return postJson("/api/run/start", { source_code }, signal);
}

export async function runSendInput(session_id, value, signal) {
    return postJson("/api/run/input", { session_id, value }, signal);
}