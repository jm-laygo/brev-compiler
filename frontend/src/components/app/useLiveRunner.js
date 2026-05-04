import { useCallback, useEffect, useRef, useState } from "react";
import {
    runLexicalAnalysis,
    runSyntaxAnalysis,
    runSemanticAnalysis,
    startExecution,
    sendRuntimeInput,
} from "../../api/brevApi.js";

export default function useLiveRunner({
    getCode,
    clearAllEditorMarkers,
    setMarkersFromErrors,
    setTerminalOutput,
    logError,
    logWarning,
    logSuccess,
    setTokens,
    setTokensOpen,
}) {
    const [isRunning, setIsRunning] = useState(false);
    const [runningPhase, setRunningPhase] = useState("");
    const [runtimePrompt, setRuntimePrompt] = useState(null);
    const [runtimeSessionId, setRuntimeSessionId] = useState(null);

    const abortControllerRef = useRef(null);
    const requestIdRef = useRef(0);
    const debounceTimerRef = useRef(null);

    useEffect(() => {
        return () => {
            if (debounceTimerRef.current) {
                clearTimeout(debounceTimerRef.current);
            }

            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, []);

    const appendRuntimeOutput = useCallback(
        (outputLines) => {
            const safeOutputLines = Array.isArray(outputLines) ? outputLines : [];

            safeOutputLines.forEach((outputLine) => {
                if (outputLine === "" || outputLine == null) {
                    logWarning("");
                } else {
                    logWarning(String(outputLine));
                }
            });
        },
        [logWarning]
    );

    const finishRuntimeState = useCallback(() => {
        setRuntimePrompt(null);
        setRuntimeSessionId(null);
    }, []);

    const resetRunState = useCallback(() => {
        finishRuntimeState();
        setIsRunning(false);
        setRunningPhase("");
    }, [finishRuntimeState]);

    const stopLive = useCallback(() => {
        if (debounceTimerRef.current) {
            clearTimeout(debounceTimerRef.current);
            debounceTimerRef.current = null;
        }

        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
        }

        requestIdRef.current += 1;
        resetRunState();
        logWarning("Stopped.");
    }, [logWarning, resetRunState]);

    const handleApiError = useCallback(
        (phaseName, response, responseData) => {
            const errorMessage = `${phaseName} API error (HTTP ${
                response?.status ?? "?"
            }): ${responseData?.error || "Unknown error"}`;

            setTerminalOutput(`${phaseName} failed:`, "error");
            logError(errorMessage);
            setMarkersFromErrors([errorMessage]);
        },
        [logError, setMarkersFromErrors, setTerminalOutput]
    );

    const runLiveOnce = useCallback(
        async (phase, sourceCode, shouldOpenTokens) => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }

            const abortController = new AbortController();
            abortControllerRef.current = abortController;

            const currentRequestId = requestIdRef.current + 1;
            requestIdRef.current = currentRequestId;

            try {
                clearAllEditorMarkers();

                if (phase === "lex") {
                    setTerminalOutput("Running lexical analysis...", "info");

                    const { response, responseData } = await runLexicalAnalysis(
                        sourceCode,
                        abortController.signal
                    );

                    if (currentRequestId !== requestIdRef.current) {
                        return;
                    }

                    if (!response.ok) {
                        handleApiError("Lexical analysis", response, responseData);
                        return;
                    }

                    const tokenList = Array.isArray(responseData.tokens)
                        ? responseData.tokens
                        : [];

                    const lexicalErrors = Array.isArray(responseData.errors)
                        ? responseData.errors
                        : [];

                    const visibleTokens = tokenList.filter((token) => !token.hidden);
                    setTokens(visibleTokens);

                    if (lexicalErrors.length) {
                        setTerminalOutput("Lexical analysis failed:", "error");
                        lexicalErrors.forEach((errorText) => logError(errorText));
                        setMarkersFromErrors(lexicalErrors);
                    } else {
                        setTerminalOutput("Lexical analysis successful!", "success");
                        setMarkersFromErrors([]);
                    }

                    if (shouldOpenTokens && visibleTokens.length > 0) {
                        setTokensOpen(true);
                    }

                    return;
                }

                if (phase === "syn") {
                    setTerminalOutput("Running syntax analysis...", "info");

                    const { response, responseData } = await runSyntaxAnalysis(
                        sourceCode,
                        abortController.signal
                    );

                    if (currentRequestId !== requestIdRef.current) {
                        return;
                    }

                    if (!response.ok) {
                        handleApiError("Syntax analysis", response, responseData);
                        return;
                    }

                    const syntaxErrors = Array.isArray(responseData.errors)
                        ? responseData.errors
                        : [];

                    if (syntaxErrors.length) {
                        setTerminalOutput("Syntax analysis failed:", "error");
                        syntaxErrors.forEach((errorText) => logError(errorText));
                        setMarkersFromErrors(syntaxErrors);
                    } else {
                        setTerminalOutput("Syntax analysis successful!", "success");
                        setMarkersFromErrors([]);
                    }

                    return;
                }

                if (phase === "sem") {
                    setTerminalOutput("Running semantic analysis...", "info");

                    const { response, responseData } = await runSemanticAnalysis(
                        sourceCode,
                        abortController.signal
                    );

                    if (currentRequestId !== requestIdRef.current) {
                        return;
                    }

                    if (!response.ok) {
                        handleApiError("Semantic analysis", response, responseData);
                        return;
                    }

                    const semanticErrors = Array.isArray(responseData.errors)
                        ? responseData.errors
                        : [];

                    if (responseData.semantic_valid && semanticErrors.length === 0) {
                        setTerminalOutput("Semantic analysis successful!", "success");
                        setMarkersFromErrors([]);
                    } else {
                        setTerminalOutput("Semantic analysis failed:", "error");

                        if (semanticErrors.length) {
                            semanticErrors.forEach((errorText) => logError(errorText));
                            setMarkersFromErrors(semanticErrors);
                        } else {
                            logError("Unknown semantic error");
                        }
                    }

                    return;
                }

                if (phase === "run") {
                    setTerminalOutput("Running execution...", "info");

                    const { response, responseData } = await startExecution(
                        sourceCode,
                        abortController.signal
                    );

                    if (currentRequestId !== requestIdRef.current) {
                        return;
                    }

                    if (!response.ok) {
                        const errorMessage = `Execute API error (HTTP ${response.status}): ${
                            responseData.error || "Unknown error"
                        }`;

                        logError("Execution failed:");
                        logError(errorMessage);
                        setMarkersFromErrors([errorMessage]);
                        resetRunState();

                        return;
                    }

                    const outputLines = Array.isArray(responseData.output)
                        ? responseData.output
                        : [];

                    const runtimeErrors = Array.isArray(responseData.errors)
                        ? responseData.errors
                        : [];

                    appendRuntimeOutput(outputLines);

                    if (responseData.status === "waiting_input") {
                        setRuntimeSessionId(responseData.session_id);
                        setRuntimePrompt({
                            id: responseData.session_id,
                            prefix: "",
                        });

                        return;
                    }

                    if (responseData.status === "finished") {
                        logSuccess("Execution successful!");
                        setMarkersFromErrors([]);
                        resetRunState();

                        return;
                    }

                    logError("Execution failed:");

                    if (runtimeErrors.length) {
                        runtimeErrors.forEach((errorText) => logError(errorText));
                        setMarkersFromErrors(runtimeErrors);
                    } else {
                        logError("Unknown runtime error");
                    }

                    resetRunState();
                }
            } catch (errorObject) {
                if (errorObject?.name === "AbortError") {
                    resetRunState();
                    return;
                }

                const errorMessage = `Network error: ${errorObject.message}`;

                logError("Run failed:");
                logError(errorMessage);
                setMarkersFromErrors([errorMessage]);
                resetRunState();
            }
        },
        [
            appendRuntimeOutput,
            clearAllEditorMarkers,
            handleApiError,
            logError,
            logSuccess,
            resetRunState,
            setMarkersFromErrors,
            setTerminalOutput,
            setTokens,
            setTokensOpen,
        ]
    );

    const startLive = useCallback(
        (phase) => {
            if (phase === "run") {
                return;
            }

            if (isRunning && runningPhase === phase) {
                return;
            }

            stopLive();

            setIsRunning(true);
            setRunningPhase(phase);

            const sourceCode = getCode();
            runLiveOnce(phase, sourceCode, true);
        },
        [getCode, isRunning, runLiveOnce, runningPhase, stopLive]
    );

    const toggleLiveLexical = useCallback(() => {
        if (isRunning && runningPhase === "lex") {
            stopLive();
            return;
        }

        startLive("lex");
    }, [isRunning, runningPhase, startLive, stopLive]);

    const toggleLiveSyntax = useCallback(() => {
        if (isRunning && runningPhase === "syn") {
            stopLive();
            return;
        }

        startLive("syn");
    }, [isRunning, runningPhase, startLive, stopLive]);

    const toggleLiveSemantic = useCallback(() => {
        if (isRunning && runningPhase === "sem") {
            stopLive();
            return;
        }

        startLive("sem");
    }, [isRunning, runningPhase, startLive, stopLive]);

    const toggleExecute = useCallback(async () => {
        if (isRunning && runningPhase === "run") {
            stopLive();
            return;
        }

        stopLive();

        setIsRunning(true);
        setRunningPhase("run");

        const sourceCode = getCode();
        await runLiveOnce("run", sourceCode, true);
    }, [getCode, isRunning, runLiveOnce, runningPhase, stopLive]);

    const toggleRunProgram = useCallback(async () => {
        if (isRunning && runningPhase === "program") {
            stopLive();
            return;
        }

        stopLive();

        const sourceCode = getCode();

        setIsRunning(true);
        setRunningPhase("program");
        clearAllEditorMarkers();

        try {
            setTerminalOutput("Running lexical analysis...", "info");

            const lexicalResult = await runLexicalAnalysis(sourceCode);
            const lexicalData = lexicalResult?.responseData || {};

            if (!lexicalResult?.response?.ok) {
                const errorMessage = `Lex API error (HTTP ${
                    lexicalResult?.response?.status ?? "?"
                }): ${lexicalData.error || "Unknown error"}`;

                setTerminalOutput("Lexical analysis failed:", "error");
                logError(errorMessage);
                setMarkersFromErrors([errorMessage]);
                resetRunState();

                return;
            }

            const lexicalTokens = Array.isArray(lexicalData.tokens)
                ? lexicalData.tokens.filter((token) => !token.hidden)
                : [];

            const lexicalErrors = Array.isArray(lexicalData.errors)
                ? lexicalData.errors
                : [];

            setTokens(lexicalTokens);

            if (lexicalTokens.length > 0) {
                setTokensOpen(true);
            }

            if (lexicalErrors.length) {
                setTerminalOutput("Lexical analysis failed:", "error");
                lexicalErrors.forEach((errorText) => logError(errorText));
                setMarkersFromErrors(lexicalErrors);
                resetRunState();

                return;
            }

            setTerminalOutput("Running syntax analysis...", "info");

            const syntaxResult = await runSyntaxAnalysis(sourceCode);
            const syntaxData = syntaxResult?.responseData || {};

            if (!syntaxResult?.response?.ok) {
                const errorMessage = `Syntax API error (HTTP ${
                    syntaxResult?.response?.status ?? "?"
                }): ${syntaxData.error || "Unknown error"}`;

                setTerminalOutput("Syntax analysis failed:", "error");
                logError(errorMessage);
                setMarkersFromErrors([errorMessage]);
                resetRunState();

                return;
            }

            const syntaxErrors = Array.isArray(syntaxData.errors)
                ? syntaxData.errors
                : [];

            if (syntaxErrors.length) {
                setTerminalOutput("Syntax analysis failed:", "error");
                syntaxErrors.forEach((errorText) => logError(errorText));
                setMarkersFromErrors(syntaxErrors);
                resetRunState();

                return;
            }

            setTerminalOutput("Running semantic analysis...", "info");

            const semanticResult = await runSemanticAnalysis(sourceCode);
            const semanticData = semanticResult?.responseData || {};

            if (!semanticResult?.response?.ok) {
                const errorMessage = `Semantic API error (HTTP ${
                    semanticResult?.response?.status ?? "?"
                }): ${semanticData.error || "Unknown error"}`;

                setTerminalOutput("Semantic analysis failed:", "error");
                logError(errorMessage);
                setMarkersFromErrors([errorMessage]);
                resetRunState();

                return;
            }

            const semanticErrors = Array.isArray(semanticData.errors)
                ? semanticData.errors
                : [];

            if (!(semanticData.semantic_valid && semanticErrors.length === 0)) {
                setTerminalOutput("Semantic analysis failed:", "error");

                if (semanticErrors.length) {
                    semanticErrors.forEach((errorText) => logError(errorText));
                    setMarkersFromErrors(semanticErrors);
                } else {
                    logError("Unknown semantic error");
                }

                resetRunState();
                return;
            }

            setTerminalOutput("Running execution...", "info");

            const executionResult = await startExecution(sourceCode);
            const executionData = executionResult?.responseData || {};

            if (!executionResult?.response?.ok) {
                const errorMessage = `Execute API error (HTTP ${
                    executionResult?.response?.status ?? "?"
                }): ${executionData.error || "Unknown error"}`;

                logError("Execution failed:");
                logError(errorMessage);
                setMarkersFromErrors([errorMessage]);
                resetRunState();

                return;
            }

            const outputLines = Array.isArray(executionData.output)
                ? executionData.output
                : [];

            const executionErrors = Array.isArray(executionData.errors)
                ? executionData.errors
                : [];

            appendRuntimeOutput(outputLines);

            if (executionData.status === "waiting_input") {
                setRuntimeSessionId(executionData.session_id);
                setRuntimePrompt({
                    id: executionData.session_id,
                    prefix: "",
                });

                return;
            }

            if (executionData.status === "finished") {
                logSuccess("Execution successful!");
                setMarkersFromErrors([]);
                resetRunState();

                return;
            }

            logError("Execution failed:");

            if (executionErrors.length) {
                executionErrors.forEach((errorText) => logError(errorText));
                setMarkersFromErrors(executionErrors);
            } else {
                logError("Unknown runtime error");
            }

            resetRunState();
        } catch (errorObject) {
            if (errorObject?.name === "AbortError") {
                resetRunState();
                return;
            }

            const errorMessage = `Network error: ${errorObject.message}`;

            logError("Run failed:");
            logError(errorMessage);
            setMarkersFromErrors([errorMessage]);
            resetRunState();
        }
    }, [
        appendRuntimeOutput,
        clearAllEditorMarkers,
        getCode,
        isRunning,
        logError,
        logSuccess,
        resetRunState,
        runningPhase,
        setMarkersFromErrors,
        setTerminalOutput,
        setTokens,
        setTokensOpen,
        stopLive,
    ]);

    const submitRuntimeInput = useCallback(
        async (inputValue) => {
            if (!runtimeSessionId) {
                return;
            }

            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }

            const abortController = new AbortController();
            abortControllerRef.current = abortController;

            logWarning(String(inputValue ?? ""));
            setRuntimePrompt(null);

            try {
                const { response, responseData } = await sendRuntimeInput(
                    runtimeSessionId,
                    inputValue ?? "",
                    abortController.signal
                );

                if (!response.ok) {
                    const errorMessage = `Execute API error (HTTP ${response.status}): ${
                        responseData.error || "Unknown error"
                    }`;

                    logError("Execution failed:");
                    logError(errorMessage);
                    setMarkersFromErrors([errorMessage]);
                    resetRunState();

                    return;
                }

                const outputLines = Array.isArray(responseData.output)
                    ? responseData.output
                    : [];

                const runtimeErrors = Array.isArray(responseData.errors)
                    ? responseData.errors
                    : [];

                appendRuntimeOutput(outputLines);

                if (responseData.status === "waiting_input") {
                    setRuntimeSessionId(responseData.session_id);
                    setRuntimePrompt({
                        id: responseData.session_id,
                        prefix: "",
                    });

                    return;
                }

                if (responseData.status === "finished") {
                    logSuccess("Execution successful!");
                    setMarkersFromErrors([]);
                    resetRunState();

                    return;
                }

                logError("Execution failed:");

                if (runtimeErrors.length) {
                    runtimeErrors.forEach((errorText) => logError(errorText));
                    setMarkersFromErrors(runtimeErrors);
                } else {
                    logError("Unknown runtime error");
                }

                resetRunState();
            } catch (errorObject) {
                if (errorObject?.name === "AbortError") {
                    resetRunState();
                    return;
                }

                logError("Execution failed:");
                logError(`Network error: ${errorObject.message}`);
                resetRunState();
            }
        },
        [
            appendRuntimeOutput,
            logError,
            logSuccess,
            logWarning,
            resetRunState,
            runtimeSessionId,
            setMarkersFromErrors,
        ]
    );

    const cancelRuntimeInput = useCallback(() => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
        }

        requestIdRef.current += 1;
        resetRunState();
        logWarning("Execution cancelled.");
    }, [logWarning, resetRunState]);

    const onEditorChange = useCallback(
        (sourceCode) => {
            if (!isRunning || !runningPhase) {
                return;
            }

            if (runningPhase === "run") {
                return;
            }

            if (debounceTimerRef.current) {
                clearTimeout(debounceTimerRef.current);
            }

            debounceTimerRef.current = setTimeout(() => {
                runLiveOnce(runningPhase, sourceCode, false);
            }, 600);
        },
        [isRunning, runLiveOnce, runningPhase]
    );

    return {
        isRunning,
        runningPhase,
        runLiveOnce,
        stopLive,
        startLive,
        toggleLiveLexical,
        toggleLiveSyntax,
        toggleLiveSemantic,
        toggleExecute,
        toggleRunProgram,
        onEditorChange,
        runtimePrompt,
        runtimeSessionId,
        submitRuntimeInput,
        cancelRuntimeInput,
    };
}