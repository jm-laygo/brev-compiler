import React, { useEffect, useRef, useState } from "react";
import BrevEditor from "./components/Editor.jsx";
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
    const {
        terminalLines,
        logError,
        logWarning,
        logSuccess,
        setTerminalOutput,
    } = useTerminal(800);

    const DEFAULT_BREV_CODE = `rite tally genesis() {
    dismiss 0;
}`;

    const [initialCode, setInitialCode] = useState(DEFAULT_BREV_CODE);
    const [tokenList, setTokenList] = useState([]);
    const [isTokenPanelOpen, setIsTokenPanelOpen] = useState(true);
    const [outputHeightPx, setOutputHeightPx] = useState(220);
    const [isResizingPanels, setIsResizingPanels] = useState(false);

    const [activeTokenRange, setActiveTokenRange] = useState({
        start: -1,
        end: -1,
    });

    const [activeTokenHeadIndex, setActiveTokenHeadIndex] = useState(-1);

    const workspaceRef = useRef(null);
    const editorApiRef = useRef(null);

    useEffect(() => {
        if (!isResizingPanels) {
            return;
        }

        const MINIMUM_OUTPUT_HEIGHT = 120;
        const MINIMUM_EDITOR_HEIGHT = 180;

        const handlePointerMove = (event) => {
            const workspaceElement = workspaceRef.current;

            if (!workspaceElement) {
                return;
            }

            const workspaceRectangle = workspaceElement.getBoundingClientRect();
            const pointerTopOffset = event.clientY - workspaceRectangle.top;
            const nextOutputHeight = workspaceRectangle.height - pointerTopOffset;

            const maximumOutputHeight = Math.max(
                MINIMUM_OUTPUT_HEIGHT,
                workspaceRectangle.height - MINIMUM_EDITOR_HEIGHT
            );

            const clampedOutputHeight = Math.max(
                MINIMUM_OUTPUT_HEIGHT,
                Math.min(nextOutputHeight, maximumOutputHeight)
            );

            setOutputHeightPx(clampedOutputHeight);
        };

        const handlePointerUp = () => {
            setIsResizingPanels(false);
        };

        window.addEventListener("pointermove", handlePointerMove);
        window.addEventListener("pointerup", handlePointerUp);

        return () => {
            window.removeEventListener("pointermove", handlePointerMove);
            window.removeEventListener("pointerup", handlePointerUp);
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
        tokens: tokenList,
        onActiveTokenRangeChange: setActiveTokenRange,
        onActiveTokenHeadIndexChange: setActiveTokenHeadIndex,
    });

    const {
        isRunning,
        runningPhase,
        runLiveOnce,
        toggleLiveLexical,
        toggleLiveSyntax,
        toggleLiveSemantic,
        toggleExecute,
        onEditorChange,
        runtimePrompt,
        submitRuntimeInput,
        cancelRuntimeInput,
    } = useLiveRunner({
        getCode,
        clearAllEditorMarkers,
        setMarkersFromErrors,
        setTerminalOutput,
        logError,
        logWarning,
        logSuccess,
        setTokens: setTokenList,
        setTokensOpen: setIsTokenPanelOpen,
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
        editorApiRef,
        setInitialCode,
        setSource,
        setTerminalOutput,
        isRunning,
        runningPhase,
        runLiveOnce,
    });

    useEditorLayoutEffect({
        editorRef,
        isTokenPanelOpen,
    });

    return (
        <main id="brev-container">
            <section id="brev-inner-container">
                <Toolbar
                    fileInputRef={fileInputRef}
                    onFilePicked={onFilePicked}
                    openFile={openFile}
                    saveFile={saveFile}
                    clearEditor={clearEditor}
                    toggleLiveLexical={toggleLiveLexical}
                    toggleLiveSyntax={toggleLiveSyntax}
                    toggleLiveSemantic={toggleLiveSemantic}
                    toggleExecute={toggleExecute}
                    isRunning={isRunning}
                    runningPhase={runningPhase}
                    tokensOpen={isTokenPanelOpen}
                    toggleTokens={() => setIsTokenPanelOpen((value) => !value)}
                />

                <div
                    id="brev-dock"
                    className={isTokenPanelOpen ? "tokens-open" : ""}
                >
                    <div id="brev-workspace" ref={workspaceRef}>
                        <div id="brev-pane">
                            <BrevEditor
                                initialValue={initialCode}
                                editorRef={editorRef}
                                editorApiRef={editorApiRef}
                                onReady={onEditorReady}
                                onChange={(sourceCode) => {
                                    setSource(sourceCode);
                                    onEditorChange(sourceCode);
                                }}
                            />
                        </div>

                        <OutputPanel
                            terminalLines={terminalLines}
                            outputOpen={true}
                            panelStyle={{
                                "--output-height": `${outputHeightPx}px`,
                            }}
                            onStartResize={startPanelResize}
                            isResizing={isResizingPanels}
                            onJumpToPosition={jumpToPosition}
                            runtimePrompt={runtimePrompt}
                            onSubmitRuntimeInput={submitRuntimeInput}
                            onCancelRuntimeInput={cancelRuntimeInput}
                        />
                    </div>

                    <aside className="tokens-dock" aria-hidden={!isTokenPanelOpen}>
                        <ErrorBoundary>
                            <TokenPanel
                                tokens={tokenList}
                                onTokenClick={jumpToToken}
                                selectedRange={activeTokenRange}
                                activeHeadIndex={activeTokenHeadIndex}
                            />
                        </ErrorBoundary>
                    </aside>
                </div>
            </section>
        </main>
    );
}