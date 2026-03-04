import React, { useState } from "react";
import BrevEditor from "./components/editor.jsx";
import ErrorBoundary from "./components/ErrorBoundary.jsx";
import TokenPanel from "./components/TokenPanel.jsx";
import Toolbar from "./components/Toolbar.jsx";
import OutputPanel from "./components/OutputPanel.jsx";
import useTerminal from "./hooks/useTerminal.js";

import useEditorBridge from "./components/app/useEditorBridge.js";
import useFileActions from "./components/app/useFileActions.js";
import useLiveRunner from "./components/app/useLiveRunner.js";
import useEditorLayoutEffect from "./components/app/useEditorLayoutEffect.js";

export default function App() {
    const { terminalLines, logError, logWarn, setTerminal } = useTerminal(800);

    const [initialCode, setInitialCode] = useState("");
    const [tokens, setTokens] = useState([]);
    const [tokensOpen, setTokensOpen] = useState(false);
    const [outputOpen, setOutputOpen] = useState(true);

    const {
        editorRef,
        getCode,
        setSource,
        onEditorReady,
        clearAllEditorMarkers,
        setMarkersFromErrors,
        jumpToToken,
        jumpToPosition,
    } = useEditorBridge();

    const {
        isRunning,
        runningPhase,
        runLiveOnce,
        toggleLiveLex,
        toggleLiveSyn,
        toggleLiveSem,
        onEditorChange,
    } = useLiveRunner({
        getCode,
        clearAllEditorMarkers,
        setMarkersFromErrors,
        setTerminal,
        logError,
        logWarn,
        setTokens,
        setTokensOpen,
    });

    const {
        fileInputRef,
        openFile,
        onFilePicked,
        saveFile,
        clearEditor,
    } = useFileActions({
        getCode,
        editorRef,
        setInitialCode,
        setSource,
        setTerminal,
        isRunning,
        runningPhase,
        runLiveOnce,
    });

    useEditorLayoutEffect({ editorRef, tokensOpen });

    return (
        <>
            <main id="brev-container">
                <section id="brev-inner-container">
                    <Toolbar
                        fileInputRef={fileInputRef}
                        onFilePicked={onFilePicked}
                        openFile={openFile}
                        saveFile={saveFile}
                        clearEditor={clearEditor}
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
                                    onChange={(v) => {
                                        setSource(v);
                                        onEditorChange(v);
                                    }}
                                />
                            </div>

                            <OutputPanel
                                terminalLines={terminalLines}
                                outputOpen={outputOpen}
                                toggleOutput={() => setOutputOpen((v) => !v)}
                                onJumpToPosition={jumpToPosition}
                            />
                        </div>

                        <aside className="tokens-dock" aria-hidden={!tokensOpen}>
                            <ErrorBoundary>
                                <TokenPanel
                                    tokens={tokens}
                                    onTokenClick={jumpToToken}
                                />
                            </ErrorBoundary>
                        </aside>
                    </div>
                </section>
            </main>
        </>
    );
}