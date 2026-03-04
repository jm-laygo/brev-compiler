import React, { useEffect, useRef, useState } from "react";
import BrevEditor from "./components/editor.jsx";
import ErrorBoundary from "./components/ErrorBoundary.jsx";
import TokenPanel from "./components/TokenPanel.jsx";
import Toolbar from "./components/Toolbar.jsx";
import OutputPanel from "./components/OutputPanel.jsx";

import useTerminal from "./hooks/useTerminal.js";
import { runLexical, runSyntax, runSemantic } from "./api/brevApi.js";
import { applyMarkers, clearMarkers } from "./utils/monacoMarkers.js";

export default function App() {
    const fileInputRef = useRef(null);
    const editorRef = useRef(null);
    const editorApiRef = useRef(null);
    const sourceRef = useRef("");

    const [initialCode, setInitialCode] = useState("");
    const [tokens, setTokens] = useState([]);
    const [tokensOpen, setTokensOpen] = useState(false);

    const [isRunning, setIsRunning] = useState(false);
    const [runningPhase, setRunningPhase] = useState("");

    const liveAbortRef = useRef(null);
    const liveReqIdRef = useRef(0);
    const liveDebounceRef = useRef(null);

    const { terminalLines, log, setTerminal } = useTerminal(800);

    const getCode = () => {
        return editorRef.current ? editorRef.current.getValue() : sourceRef.current || "";
    };

    const onEditorReady = ({ editor, monaco }) => {
        editorApiRef.current = { editor, monaco };
    };

    const clearAllEditorMarkers = () => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;
        clearMarkers(api.editor, api.monaco, "brev");
    };

    const setMarkersFromErrors = (errors) => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;

        clearMarkers(api.editor, api.monaco, "brev");

        const errs = Array.isArray(errors) ? errors : [];
        if (errs.length) applyMarkers(api.editor, api.monaco, errs, "brev");
    };

    const openFile = () => fileInputRef.current?.click();

    const onFilePicked = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const text = await file.text();
        setInitialCode(text);
        sourceRef.current = text;

        if (editorRef.current) editorRef.current.setValue(text);
        setTerminal(`Loaded: ${file.name}`);

        if (isRunning && runningPhase) {
            runLiveOnce(runningPhase, text, false);
        }
    };

    const saveFile = () => {
        const code = getCode();
        const blob = new Blob([code], { type: "text/plain;charset=utf-8" });

        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "brev.txt";
        a.click();
        URL.revokeObjectURL(a.href);
    };

    useEffect(() => {
        const layout = () => editorRef.current?.layout?.();
        requestAnimationFrame(layout);
        const t1 = setTimeout(layout, 80);
        const t2 = setTimeout(layout, 380);
        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, [tokensOpen]);

    useEffect(() => {
        return () => {
            if (liveDebounceRef.current) clearTimeout(liveDebounceRef.current);
            if (liveAbortRef.current) liveAbortRef.current.abort();
        };
    }, []);

    const stopLive = () => {
        if (liveDebounceRef.current) {
            clearTimeout(liveDebounceRef.current);
            liveDebounceRef.current = null;
        }

        if (liveAbortRef.current) {
            liveAbortRef.current.abort();
            liveAbortRef.current = null;
        }

        liveReqIdRef.current += 1;

        setIsRunning(false);
        setRunningPhase("");
        log("Stopped.");
    };

    const startLive = (phase) => {
        if (isRunning && runningPhase === phase) return;

        stopLive();

        setIsRunning(true);
        setRunningPhase(phase);

        const code = getCode();
        runLiveOnce(phase, code, true);
    };

    const toggleLiveLex = () => {
        if (isRunning && runningPhase === "lex") {
            stopLive();
            return;
        }
        startLive("lex");
    };

    const toggleLiveSyn = () => {
        if (isRunning && runningPhase === "syn") {
            stopLive();
            return;
        }
        startLive("syn");
    };

    const toggleLiveSem = () => {
        if (isRunning && runningPhase === "sem") {
            stopLive();
            return;
        }
        startLive("sem");
    };

    const runLiveOnce = async (phase, sourceCode, openTokens) => {
        if (liveAbortRef.current) liveAbortRef.current.abort();
        const controller = new AbortController();
        liveAbortRef.current = controller;

        const reqId = ++liveReqIdRef.current;

        try {
            clearAllEditorMarkers();

            if (phase === "lex") {
                setTerminal("Running lexical analysis...");

                const { res, data } = await runLexical(sourceCode, controller.signal);
                if (reqId !== liveReqIdRef.current) return;

                if (!res.ok) {
                    const msg = `Lex API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                    setTerminal("Lexical analysis failed:");
                    log(msg);
                    setMarkersFromErrors([msg]);
                    return;
                }

                const toks = Array.isArray(data.tokens) ? data.tokens : [];
                const errs = Array.isArray(data.errors) ? data.errors : [];

                const filtered = toks.filter((t) => !t.hidden);
                setTokens(filtered);

                if (errs.length) {
                    setTerminal("Lexical analysis failed:");
                    errs.forEach((e) => log(e));
                    setMarkersFromErrors(errs);
                } else {
                    setTerminal("Lexical analysis successful!");
                    setMarkersFromErrors([]);
                }

                if (openTokens && filtered.length > 0) setTokensOpen(true);
                return;
            }

            if (phase === "syn") {
                setTerminal("Running syntax analysis...");

                const { res, data } = await runSyntax(sourceCode, controller.signal);
                if (reqId !== liveReqIdRef.current) return;

                if (!res.ok) {
                    const msg = `Syntax API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                    setTerminal("Syntax analysis failed:");
                    log(msg);
                    setMarkersFromErrors([msg]);
                    return;
                }

                const errs = Array.isArray(data.errors) ? data.errors : [];

                if (errs.length) {
                    setTerminal("Syntax analysis failed:");
                    errs.forEach((e) => log(e));
                    setMarkersFromErrors(errs);
                } else {
                    setTerminal("Syntax analysis successful!");
                    setMarkersFromErrors([]);
                }

                return;
            }

            if (phase === "sem") {
                setTerminal("Running semantic analysis...");

                const { res, data } = await runSemantic(sourceCode, controller.signal);
                if (reqId !== liveReqIdRef.current) return;

                if (!res.ok) {
                    const msg = `Semantic API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                    setTerminal("Semantic analysis failed:");
                    log(msg);
                    setMarkersFromErrors([msg]);
                    return;
                }

                const errs = Array.isArray(data.errors) ? data.errors : [];

                if (data.semantic_valid && errs.length === 0) {
                    setTerminal("Semantic analysis successful!");
                    setMarkersFromErrors([]);
                } else {
                    setTerminal("Semantic analysis failed:");
                    if (errs.length) errs.forEach((e) => log(e));
                    else log("Unknown semantic error");
                    if (errs.length) setMarkersFromErrors(errs);
                }

                return;
            }
        } catch (e) {
            if (e?.name === "AbortError") return;
            const msg = `Network error: ${e.message}`;
            setTerminal("Run failed:");
            log(msg);
            setMarkersFromErrors([msg]);
        }
    };

    const onEditorChange = (v) => {
        sourceRef.current = v;

        if (!isRunning || !runningPhase) return;

        if (liveDebounceRef.current) clearTimeout(liveDebounceRef.current);

        liveDebounceRef.current = setTimeout(() => {
            runLiveOnce(runningPhase, v, false);
        }, 600);
    };

    return (
        <>
            <main id="brev-container">
                <section id="brev-inner-container">
                    <Toolbar
                        fileInputRef={fileInputRef}
                        onFilePicked={onFilePicked}
                        openFile={openFile}
                        saveFile={saveFile}
                        toggleLiveLex={toggleLiveLex}
                        toggleLiveSyn={toggleLiveSyn}
                        toggleLiveSem={toggleLiveSem}
                        isRunning={isRunning}
                        runningPhase={runningPhase}
                        tokensOpen={tokensOpen}
                        toggleTokens={() => setTokensOpen((x) => !x)}
                    />

                    <div id="brev-dock" className={tokensOpen ? "tokens-open" : ""}>
                        <div id="brev-workspace">
                            <div id="brev-pane">
                                <BrevEditor
                                    initialValue={initialCode}
                                    editorRef={editorRef}
                                    onReady={onEditorReady}
                                    onChange={onEditorChange}
                                />
                            </div>

                            <OutputPanel terminalLines={terminalLines} />
                        </div>

                        <aside className="tokens-dock" aria-hidden={!tokensOpen}>
                            <ErrorBoundary>
                                <TokenPanel tokens={tokens} />
                            </ErrorBoundary>
                        </aside>
                    </div>
                </section>
            </main>
        </>
    );
}