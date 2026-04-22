import React from "react";

export default function Toolbar({
    fileInputRef,
    onFilePicked,
    openFile,
    saveFile,
    clearEditor,
    // toggleLiveLex,
    // toggleLiveSyn,
    // toggleLiveSem,
    // toggleExecute,
    toggleRunProgram,
    isRunning,
    runningPhase,
    // tokensOpen,
    // toggleTokens,
}) {
    // const isLexRunning = isRunning && runningPhase === "lex";
    // const isSynRunning = isRunning && runningPhase === "syn";
    // const isSemRunning = isRunning && runningPhase === "sem";
    // const isExecRunning = isRunning && runningPhase === "run";
    const isProgramRunning = isRunning && runningPhase === "program";

    return (
        <header id="header-row">
            <div className="toolbar-left">
                {/*
                <button
                    onClick={toggleLiveLex}
                    className={`command-btn ${isLexRunning ? "active-btn" : ""}`}
                >
                    {isLexRunning ? "Stop Running" : "Run Lexical"}
                </button>

                <button
                    onClick={toggleLiveSyn}
                    className={`command-btn ${isSynRunning ? "active-btn" : ""}`}
                >
                    {isSynRunning ? "Stop Running" : "Run Syntax"}
                </button>

                <button
                    onClick={toggleLiveSem}
                    className={`command-btn ${isSemRunning ? "active-btn" : ""}`}
                >
                    {isSemRunning ? "Stop Running" : "Run Semantics"}
                </button>

                <button
                    onClick={toggleExecute}
                    className={`command-btn ${isExecRunning ? "active-btn" : ""}`}
                >
                    {isExecRunning ? "Stop Running" : "Run Execute"}
                </button>
                */}

                <button
                    onClick={toggleRunProgram}
                    className={`command-btn command-btn-run ${isProgramRunning ? "active-btn" : ""}`}
                    aria-label={isProgramRunning ? "Stop running program" : "Run program"}
                    title={isProgramRunning ? "Stop running program" : "Run program"}
                >
                    {isProgramRunning ? "Stop Running" : "Run Program"}
                </button>
            </div>

            <div className="header-title-box">
                <h2 className="header-title-text">Brev Compiler</h2>
            </div>

            <div className="toolbar-right">
                <button
                    onClick={openFile}
                    className="command-btn command-btn-open"
                    aria-label="Open file"
                    title="Open file"
                >
                    Open
                </button>

                <input
                    ref={fileInputRef}
                    type="file"
                    style={{ display: "none" }}
                    onChange={onFilePicked}
                />

                <button
                    onClick={saveFile}
                    className="command-btn command-btn-save"
                    aria-label="Save file"
                    title="Save file"
                >
                    Save
                </button>

                <button
                    onClick={clearEditor}
                    className="command-btn command-btn-clear"
                    aria-label="Clear editor"
                    title="Clear editor"
                >
                    Clear
                </button>
                {/*
                <button
                    onClick={toggleTokens}
                    className={`command-btn ${tokensOpen ? "active-btn" : ""}`}
                    title={tokensOpen ? "Hide tokens" : "Show tokens"}
                >
                    Tokens {tokensOpen ? "«" : "»"}
                </button>
                */}
            </div>
        </header>
    );
}