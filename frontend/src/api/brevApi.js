async function sendJsonRequest(url, requestBody, abortSignal) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
        signal: abortSignal,
    });

    const responseData = await response.json().catch(() => ({}));

    return {
        response,
        responseData,
    };
}

export async function runLexicalAnalysis(sourceCode, abortSignal) {
    return sendJsonRequest(
        "/api/lex",
        { source_code: sourceCode },
        abortSignal
    );
}

export async function runSyntaxAnalysis(sourceCode, abortSignal) {
    return sendJsonRequest(
        "/api/syntax",
        { source_code: sourceCode },
        abortSignal
    );
}

export async function runSemanticAnalysis(sourceCode, abortSignal) {
    return sendJsonRequest(
        "/api/sem",
        { source_code: sourceCode },
        abortSignal
    );
}

export async function startExecution(sourceCode, abortSignal) {
    return sendJsonRequest(
        "/api/run/start",
        { source_code: sourceCode },
        abortSignal
    );
}

export async function sendRuntimeInput(sessionId, inputValue, abortSignal) {
    return sendJsonRequest(
        "/api/run/input",
        {
            session_id: sessionId,
            value: inputValue,
        },
        abortSignal
    );
}