export async function sendJsonRequest(url, requestBody) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
    });

    let responseData = null;

    try {
        responseData = await response.json();
    } catch {
        // ignore empty response
    }

    if (!response.ok) {
        const errorMessage = responseData?.error || `HTTP ${response.status}`;
        throw new Error(errorMessage);
    }

    return responseData;
}