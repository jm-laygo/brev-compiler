import { useCallback, useEffect, useRef, useState } from "react";
import {
    runLexical,
    runSyntax,
    runSemantic,
    runStartExecute,
    runSendInput,
} from "../../api/brevApi.js";

export default function useLiveRunner({
    getCode,
    clearAllEditorMarkers,
    setMarkersFromErrors,
    setTerminal,
    logError,
    logWarn,
    setTokens,
    setTokensOpen,
}) {
    const [isRunning, setIsRunning] = useState(false);
    const [runningPhase, setRunningPhase] = useState("");
    const [runtimePrompt, setRuntimePrompt] = useState(null);
    const [runtimeSessionId, setRuntimeSessionId] = useState(null);

    const liveAbortRef = useRef(null);
    const liveReqIdRef = useRef(0);
    const liveDebounceRef = useRef(null);

    useEffect(() => {
        return () => {
            if (liveDebounceRef.current) clearTimeout(liveDebounceRef.current);
            if (liveAbortRef.current) liveAbortRef.current.abort();
        };
    }, []);

    const appendRuntimeOutput = useCallback(
        (output) => {
            const lines = Array.isArray(output) ? output : [];
            lines.forEach((line) => {
                if (line === "" || line == null) logWarn("");
                else logWarn(String(line));
            });
        },
        [logWarn]
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
        if (liveDebounceRef.current) {
            clearTimeout(liveDebounceRef.current);
            liveDebounceRef.current = null;
        }

        if (liveAbortRef.current) {
            liveAbortRef.current.abort();
            liveAbortRef.current = null;
        }

        liveReqIdRef.current += 1;
        resetRunState();
        logWarn("Stopped.");
    }, [logWarn, resetRunState]);

    const runLiveOnce = useCallback(
        async (phase, sourceCode, openTokens) => {
            if (liveAbortRef.current) liveAbortRef.current.abort();

            const controller = new AbortController();
            liveAbortRef.current = controller;

            const reqId = ++liveReqIdRef.current;

            try {
                clearAllEditorMarkers();

                if (phase === "lex") {
                    setTerminal("Running lexical analysis...", "info");

                    const { res, data } = await runLexical(sourceCode, controller.signal);
                    if (reqId !== liveReqIdRef.current) return;

                    if (!res.ok) {
                        const msg = `Lex API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                        setTerminal("Lexical analysis failed:", "error");
                        logError(msg);
                        setMarkersFromErrors([msg]);
                        return;
                    }

                    const toks = Array.isArray(data.tokens) ? data.tokens : [];
                    const errs = Array.isArray(data.errors) ? data.errors : [];

                    const filtered = toks.filter((t) => !t.hidden);
                    setTokens(filtered);

                    if (errs.length) {
                        setTerminal("Lexical analysis failed:", "error");
                        errs.forEach((e) => logError(e));
                        setMarkersFromErrors(errs);
                    } else {
                        setTerminal("Lexical analysis successful!", "success");
                        setMarkersFromErrors([]);
                    }

                    if (openTokens && filtered.length > 0) setTokensOpen(true);
                    return;
                }

                if (phase === "syn") {
                    setTerminal("Running syntax analysis...", "info");

                    const { res, data } = await runSyntax(sourceCode, controller.signal);
                    if (reqId !== liveReqIdRef.current) return;

                    if (!res.ok) {
                        const msg = `Syntax API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                        setTerminal("Syntax analysis failed:", "error");
                        logError(msg);
                        setMarkersFromErrors([msg]);
                        return;
                    }

                    const errs = Array.isArray(data.errors) ? data.errors : [];

                    if (errs.length) {
                        setTerminal("Syntax analysis failed:", "error");
                        errs.forEach((e) => logError(e));
                        setMarkersFromErrors(errs);
                    } else {
                        setTerminal("Syntax analysis successful!", "success");
                        setMarkersFromErrors([]);
                    }

                    return;
                }

                if (phase === "sem") {
                    setTerminal("Running semantic analysis...", "info");

                    const { res, data } = await runSemantic(sourceCode, controller.signal);
                    if (reqId !== liveReqIdRef.current) return;

                    if (!res.ok) {
                        const msg = `Semantic API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                        setTerminal("Semantic analysis failed:", "error");
                        logError(msg);
                        setMarkersFromErrors([msg]);
                        return;
                    }

                    const errs = Array.isArray(data.errors) ? data.errors : [];

                    if (data.semantic_valid && errs.length === 0) {
                        setTerminal("Semantic analysis successful!", "success");
                        setMarkersFromErrors([]);
                    } else {
                        setTerminal("Semantic analysis failed:", "error");
                        if (errs.length) errs.forEach((e) => logError(e));
                        else logError("Unknown semantic error");
                        if (errs.length) setMarkersFromErrors(errs);
                    }

                    return;
                }

                if (phase === "run") {
                    setTerminal("Running execution...", "info");

                    const { res, data } = await runStartExecute(sourceCode, controller.signal);
                    if (reqId !== liveReqIdRef.current) return;

                    if (!res.ok) {
                        const msg = `Execute API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                        logError("Execution failed:");
                        logError(msg);
                        setMarkersFromErrors([msg]);
                        resetRunState();
                        return;
                    }

                    const output = Array.isArray(data.output) ? data.output : [];
                    const errs = Array.isArray(data.errors) ? data.errors : [];

                    appendRuntimeOutput(output);

                    if (data.status === "waiting_input") {
                        setRuntimeSessionId(data.session_id);
                        setRuntimePrompt({ id: data.session_id, prefix: "" });
                        return;
                    }

                    if (data.status === "finished") {
                        logWarn("Execution successful!");
                        setMarkersFromErrors([]);
                        resetRunState();
                        return;
                    }

                    logError("Execution failed:");
                    if (errs.length) errs.forEach((e) => logError(e));
                    else logError("Unknown runtime error");
                    if (errs.length) setMarkersFromErrors(errs);
                    resetRunState();
                    return;
                }
            } catch (e) {
                if (e?.name === "AbortError") {
                    resetRunState();
                    return;
                }

                const msg = `Network error: ${e.message}`;
                logError("Run failed:");
                logError(msg);
                setMarkersFromErrors([msg]);
                resetRunState();
            }
        },
        [
            appendRuntimeOutput,
            clearAllEditorMarkers,
            logError,
            logWarn,
            resetRunState,
            setMarkersFromErrors,
            setTerminal,
            setTokens,
            setTokensOpen,
        ]
    );

    const startLive = useCallback(
        (phase) => {
            if (phase === "run") return;

            if (isRunning && runningPhase === phase) return;

            stopLive();

            setIsRunning(true);
            setRunningPhase(phase);

            const code = getCode();
            runLiveOnce(phase, code, true);
        },
        [getCode, isRunning, runLiveOnce, runningPhase, stopLive]
    );

    const toggleLiveLex = useCallback(() => {
        if (isRunning && runningPhase === "lex") {
            stopLive();
            return;
        }
        startLive("lex");
    }, [isRunning, runningPhase, startLive, stopLive]);

    const toggleLiveSyn = useCallback(() => {
        if (isRunning && runningPhase === "syn") {
            stopLive();
            return;
        }
        startLive("syn");
    }, [isRunning, runningPhase, startLive, stopLive]);

    const toggleLiveSem = useCallback(() => {
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

        const code = getCode();
        await runLiveOnce("run", code, true);
    }, [getCode, isRunning, runLiveOnce, runningPhase, stopLive]);

    const submitRuntimeInput = useCallback(
        async (value) => {
            if (!runtimeSessionId) return;

            if (liveAbortRef.current) liveAbortRef.current.abort();

            const controller = new AbortController();
            liveAbortRef.current = controller;

            logWarn(String(value ?? ""));
            setRuntimePrompt(null);

            try {
                const { res, data } = await runSendInput(runtimeSessionId, value ?? "", controller.signal);

                if (!res.ok) {
                    const msg = `Execute API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                    logError("Execution failed:");
                    logError(msg);
                    setMarkersFromErrors([msg]);
                    resetRunState();
                    return;
                }

                const output = Array.isArray(data.output) ? data.output : [];
                const errs = Array.isArray(data.errors) ? data.errors : [];

                appendRuntimeOutput(output);

                if (data.status === "waiting_input") {
                    setRuntimeSessionId(data.session_id);
                    setRuntimePrompt({ id: data.session_id, prefix: "" });
                    return;
                }

                if (data.status === "finished") {
                    logWarn("Execution successful!");
                    setMarkersFromErrors([]);
                    resetRunState();
                    return;
                }

                logError("Execution failed:");
                if (errs.length) errs.forEach((e) => logError(e));
                else logError("Unknown runtime error");
                if (errs.length) setMarkersFromErrors(errs);
                resetRunState();
            } catch (e) {
                if (e?.name === "AbortError") {
                    resetRunState();
                    return;
                }

                logError("Execution failed:");
                logError(`Network error: ${e.message}`);
                resetRunState();
            }
        },
        [
            appendRuntimeOutput,
            logError,
            logWarn,
            resetRunState,
            runtimeSessionId,
            setMarkersFromErrors,
        ]
    );

    const cancelRuntimeInput = useCallback(() => {
        if (liveAbortRef.current) {
            liveAbortRef.current.abort();
            liveAbortRef.current = null;
        }

        liveReqIdRef.current += 1;
        resetRunState();
        logWarn("Execution cancelled.");
    }, [logWarn, resetRunState]);

    const onEditorChange = useCallback(
        (v) => {
            if (!isRunning || !runningPhase) return;
            if (runningPhase === "run") return;

            if (liveDebounceRef.current) clearTimeout(liveDebounceRef.current);

            liveDebounceRef.current = setTimeout(() => {
                runLiveOnce(runningPhase, v, false);
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
        toggleLiveLex,
        toggleLiveSyn,
        toggleLiveSem,
        toggleExecute,
        onEditorChange,
        runtimePrompt,
        runtimeSessionId,
        submitRuntimeInput,
        cancelRuntimeInput,
    };
}