async function postJson(url, body) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => ({}));

    const errors = Array.isArray(data.errors) ? data.errors : [];
    const fatal = typeof data.error === "string" ? [data.error] : [];

    return { res, data, errors: [...fatal, ...errors] };
}

export async function runLexical(source_code) {
    return postJson("/api/lex", { source_code });
}

export async function runSyntax(source_code) {
    return postJson("/api/syntax", { source_code });
}

export async function runSemantic(source_code) {
    return postJson("/api/sem", { source_code });
}