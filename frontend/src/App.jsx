import React, { useEffect, useRef, useState } from "react";
import BrevEditor from "./components/editor.jsx";
import ErrorBoundary from "./components/ErrorBoundary.jsx";
import TokenPanel from "./components/TokenPanel.jsx";
import Toolbar from "./components/Toolbar.jsx";
import OutputPanel from "./components/OutputPanel.jsx";

import useTerminal from "./hooks/useTerminal.js";
import { runLexical, runSyntax, runSemantic } from "./api/brevApi.js";
import { applyMarkers, clearMarkers, jumpToFirstError } from "./utils/monacoMarkers.js";

export default function App() {
    const fileInputRef = useRef(null);
    const editorRef = useRef(null);
    const editorApiRef = useRef(null);
    const sourceRef = useRef("");

    const [initialCode, setInitialCode] = useState("");
    const [tokens, setTokens] = useState([]);
    const [tokensOpen, setTokensOpen] = useState(false);

    const { terminalLines, log, setTerminal } = useTerminal(800);

    const getCode = () => {
        return editorRef.current ? editorRef.current.getValue() : sourceRef.current || "";
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

    const onEditorReady = ({ editor, monaco }) => {
        editorApiRef.current = { editor, monaco };
    };

    const clearAllEditorMarkers = () => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;
        clearMarkers(api.editor, api.monaco, "brev");
    };

    const markErrorsAndJump = (errors) => {
        const api = editorApiRef.current;
        if (!api?.editor || !api?.monaco) return;
        applyMarkers(api.editor, api.monaco, errors, "brev");
        jumpToFirstError(api.editor, errors);
    };

    const runLex = async () => {
        const sourceCode = getCode();
        setTerminal("Running lexical analysis...");
        clearAllEditorMarkers();

        try {
            const { res, data } = await runLexical(sourceCode);

            if (!res.ok) {
                const msg = `Lex API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                log(msg);
                markErrorsAndJump([msg]);
                return;
            }

            const toks = Array.isArray(data.tokens) ? data.tokens : [];
            const errs = Array.isArray(data.errors) ? data.errors : [];

            const filtered = toks.filter((t) => !t.hidden);
            setTokens(filtered);

            if (errs.length) {
                log("Lexical analysis failed:");
                errs.forEach((e) => log(e));
                markErrorsAndJump(errs);
            } else {
                log("Lexical analysis successful!");
            }

            if (filtered.length > 0) setTokensOpen(true);
        } catch (e) {
            const msg = `Network error: ${e.message}`;
            log(msg);
            markErrorsAndJump([msg]);
        }
    };

    const runSyn = async () => {
        const sourceCode = getCode();
        setTerminal("Running syntax analysis...");
        clearAllEditorMarkers();

        try {
            const { res, data } = await runSyntax(sourceCode);

            if (!res.ok) {
                const msg = `Syntax API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                log(msg);
                markErrorsAndJump([msg]);
                return;
            }

            const errs = Array.isArray(data.errors) ? data.errors : [];
            if (errs.length) {
                log("Syntax analysis failed:");
                errs.forEach((e) => log(e));
                markErrorsAndJump(errs);
            } else {
                log("Syntax analysis successful!");
            }
        } catch (e) {
            const msg = `Network error: ${e.message}`;
            log(msg);
            markErrorsAndJump([msg]);
        }
    };

    const runSem = async () => {
        const sourceCode = getCode();
        setTerminal("Running semantic analysis...");
        clearAllEditorMarkers();

        try {
            const { res, data } = await runSemantic(sourceCode);

            if (!res.ok) {
                const msg = `Semantic API error (HTTP ${res.status}): ${data.error || "Unknown error"}`;
                log(msg);
                markErrorsAndJump([msg]);
                return;
            }

            const errs = Array.isArray(data.errors) ? data.errors : [];
            if (data.semantic_valid && errs.length === 0) {
                log("Semantic analysis successful!");
            } else {
                const stage = data.stage ? ` (${data.stage})` : "";
                log(`Semantic analysis failed${stage}:`);
                if (errs.length) errs.forEach((e) => log(e));
                else log("Unknown semantic error");
                if (errs.length) markErrorsAndJump(errs);
            }
        } catch (e) {
            const msg = `Network error: ${e.message}`;
            log(msg);
            markErrorsAndJump([msg]);
        }
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
                        runLex={runLex}
                        runSyn={runSyn}
                        runSem={runSem}
                        tokensOpen={tokensOpen}
                        toggleTokens={() => setTokensOpen((v) => !v)}
                    />

                    <div id="brev-dock" className={tokensOpen ? "tokens-open" : ""}>
                        <div id="brev-workspace">
                            <div id="brev-pane">
                                <BrevEditor
                                    initialValue={initialCode}
                                    editorRef={editorRef}
                                    onReady={onEditorReady}
                                    onChange={(v) => {
                                        sourceRef.current = v;
                                    }}
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