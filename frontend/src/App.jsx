import React, { useEffect, useRef, useState } from "react";
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
    const [outputHeightPx, setOutputHeightPx] = useState(220);
    const [isResizingPanels, setIsResizingPanels] = useState(false);
    const [activeTokenRange, setActiveTokenRange] = useState({ start: -1, end: -1 });
    const [activeTokenHeadIndex, setActiveTokenHeadIndex] = useState(-1);
    const workspaceRef = useRef(null);

    useEffect(() => {
        if (!isResizingPanels) return;

        const MIN_OUTPUT_HEIGHT = 120;
        const MIN_EDITOR_HEIGHT = 180;

        const onPointerMove = (event) => {
            const workspaceElement = workspaceRef.current;
            if (!workspaceElement) return;

            const workspaceRect = workspaceElement.getBoundingClientRect();
            const topOffset = event.clientY - workspaceRect.top;
            const nextOutputHeight = workspaceRect.height - topOffset;
            const maxOutputHeight = Math.max(MIN_OUTPUT_HEIGHT, workspaceRect.height - MIN_EDITOR_HEIGHT);
            const clampedOutputHeight = Math.max(MIN_OUTPUT_HEIGHT, Math.min(nextOutputHeight, maxOutputHeight));

            setOutputHeightPx(clampedOutputHeight);
        };

        const onPointerUp = () => setIsResizingPanels(false);

        window.addEventListener("pointermove", onPointerMove);
        window.addEventListener("pointerup", onPointerUp);

        return () => {
            window.removeEventListener("pointermove", onPointerMove);
            window.removeEventListener("pointerup", onPointerUp);
        };
    }, [isResizingPanels]);

    const startPanelResize = (event) => {
        event.preventDefault();
        setIsResizingPanels(true);
    };

    const {
        editorRef,
        getCode,
        setSource,
        onEditorReady,
        clearAllEditorMarkers,
        setMarkersFromErrors,
        jumpToToken,
        jumpToPosition,
    } = useEditorBridge({
        tokens,
        onActiveTokenRangeChange: setActiveTokenRange,
        onActiveTokenHeadIndexChange: setActiveTokenHeadIndex,
    });

    const {
        isRunning,
        runningPhase,
        runLiveOnce,
        toggleLiveLex,
        toggleLiveSyn,
        toggleLiveSem,
        toggleExecute,
        onEditorChange,
        runtimePrompt,
        submitRuntimeInput,
        cancelRuntimeInput,
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
                        toggleExecute={toggleExecute}
                        isRunning={isRunning}
                        runningPhase={runningPhase}
                        tokensOpen={tokensOpen}
                        toggleTokens={() => setTokensOpen((x) => !x)}
                    />

                    <div id="brev-dock" className={tokensOpen ? "tokens-open" : ""}>
                        <div id="brev-workspace" ref={workspaceRef}>
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
                                panelStyle={outputOpen ? { "--output-height": `${outputHeightPx}px` } : undefined}
                                onStartResize={startPanelResize}
                                isResizing={isResizingPanels}
                                onJumpToPosition={jumpToPosition}
                                runtimePrompt={runtimePrompt}
                                onSubmitRuntimeInput={submitRuntimeInput}
                                onCancelRuntimeInput={cancelRuntimeInput}
                            />
                        </div>

                        <aside className="tokens-dock" aria-hidden={!tokensOpen}>
                            <ErrorBoundary>
                                <TokenPanel
                                    tokens={tokens}
                                    onTokenClick={jumpToToken}
                                    selectedRange={activeTokenRange}
                                    activeHeadIndex={activeTokenHeadIndex}
                                />
                            </ErrorBoundary>
                        </aside>
                    </div>
                </section>
            </main>
        </>
    );
}