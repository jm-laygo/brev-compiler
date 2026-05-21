import React from "react";

export default function Toolbar({
    fileInputRef,
    onFilePicked,
    openFile,
    saveFile,
    clearEditor,
    toggleLiveLexical,
    toggleLiveSyntax,
    toggleLiveSemantic,
    toggleExecute,
    isRunning,
    runningPhase,
    tokensOpen,
    toggleTokens,
}) {
    const isLexRunning = isRunning && runningPhase === "lex";
    const isSynRunning = isRunning && runningPhase === "syn";
    const isSemRunning = isRunning && runningPhase === "sem";
    const isExecRunning = isRunning && runningPhase === "run";

    return (
        <header id="header-row">
            <div className="toolbar-left">
                <button
                    onClick={toggleLiveLexical}
                    className={`command-btn command-btn-lexical ${isLexRunning ? "active-btn" : ""}`}
                    aria-label={isLexRunning ? "Stop lexical analysis" : "Lexical analysis"}
                    title={isLexRunning ? "Stop lexical analysis" : "Lexical analysis"}
                >
                    {isLexRunning ? "Stop Lexical" : "Lexical"}
                </button>

                <button
                    onClick={toggleLiveSyntax}
                    className={`command-btn command-btn-syntax ${isSynRunning ? "active-btn" : ""}`}
                    aria-label={isSynRunning ? "Stop syntax analysis" : "Syntax analysis"}
                    title={isSynRunning ? "Stop syntax analysis" : "Syntax analysis"}
                >
                    {isSynRunning ? "Stop Syntax" : "Syntax"}
                </button>

                <button
                    onClick={toggleLiveSemantic}
                    className={`command-btn command-btn-semantics ${isSemRunning ? "active-btn" : ""}`}
                    aria-label={isSemRunning ? "Stop semantic analysis" : "Semantic analysis"}
                    title={isSemRunning ? "Stop semantic analysis" : "Semantic analysis"}
                >
                    {isSemRunning ? "Stop Semantics" : "Semantics"}
                </button>

                <button
                    onClick={toggleExecute}
                    className={`command-btn command-btn-execution ${isExecRunning ? "active-btn" : ""}`}
                    aria-label={isExecRunning ? "Stop execution" : "Execution"}
                    title={isExecRunning ? "Stop execution" : "Execution"}
                >
                    {isExecRunning ? "Stop Execution" : "Execution"}
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
                    accept=".brev"
                    onChange={onFilePicked}
                    hidden
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

                <button
                    onClick={toggleTokens}
                    className={`command-btn command-btn-tokens ${tokensOpen ? "command-btn-token-close" : "command-btn-token-show"} ${tokensOpen ? "active-btn" : ""}`}
                    aria-label={tokensOpen ? "Hide token table" : "Show token table"}
                    title={tokensOpen ? "Hide token table" : "Show token table"}
                >
                    {tokensOpen ? "Hide Tokens" : "Show Tokens"}
                </button>
            </div>
        </header>
    );
}