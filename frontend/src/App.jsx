import React, { useEffect, useRef, useState } from "react";
import BrevEditor from "./components/editor.jsx";
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
    const [isTokenPanelOpen, setIsTokenPanelOpen] = useState(false);
    const [outputWidthPixels, setOutputWidthPixels] = useState(650);
    const [isResizingPanels, setIsResizingPanels] = useState(false);

    const [, setActiveTokenRange] = useState({
        start: -1,
        end: -1,
    });

    const [, setActiveTokenHeadIndex] = useState(-1);

    const workspaceRef = useRef(null);
    const editorApiRef = useRef(null);

    useEffect(() => {
        if (!isResizingPanels) {
            return;
        }

        const MINIMUM_OUTPUT_WIDTH = 320;
        const MINIMUM_EDITOR_WIDTH = 380;

        const handlePointerMove = (event) => {
            const workspaceElement = workspaceRef.current;

            if (!workspaceElement) {
                return;
            }

            const workspaceRectangle = workspaceElement.getBoundingClientRect();
            const pointerLeftOffset = event.clientX - workspaceRectangle.left;
            const nextOutputWidth = workspaceRectangle.width - pointerLeftOffset;

            const maximumOutputWidth = Math.max(
                MINIMUM_OUTPUT_WIDTH,
                workspaceRectangle.width - MINIMUM_EDITOR_WIDTH
            );

            const clampedOutputWidth = Math.max(
                MINIMUM_OUTPUT_WIDTH,
                Math.min(nextOutputWidth, maximumOutputWidth)
            );

            setOutputWidthPixels(clampedOutputWidth);
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
        toggleRunProgram,
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
        tokensOpen: isTokenPanelOpen,
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
                    toggleRunProgram={toggleRunProgram}
                    isRunning={isRunning}
                    runningPhase={runningPhase}
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
                                "--output-width": `${outputWidthPixels}px`,
                            }}
                            onStartResize={startPanelResize}
                            isResizing={isResizingPanels}
                            onJumpToPosition={jumpToPosition}
                            runtimePrompt={runtimePrompt}
                            onSubmitRuntimeInput={submitRuntimeInput}
                            onCancelRuntimeInput={cancelRuntimeInput}
                        />
                    </div>
                </div>
            </section>
        </main>
    );
}