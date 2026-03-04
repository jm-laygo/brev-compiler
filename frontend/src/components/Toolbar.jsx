import React from "react";

export default function Toolbar({
    fileInputRef,
    onFilePicked,
    openFile,
    saveFile,
    toggleLiveLex,
    toggleLiveSyn,
    toggleLiveSem,
    isRunning,
    runningPhase,
    tokensOpen,
    toggleTokens,
}) {
    const isLexRunning = isRunning && runningPhase === "lex";
    const isSynRunning = isRunning && runningPhase === "syn";
    const isSemRunning = isRunning && runningPhase === "sem";

    return (
        <header id="header-row">
            <div className="toolbar-left">
                <button onClick={openFile} className="command-btn">
                    Open
                </button>

                <input
                    ref={fileInputRef}
                    type="file"
                    style={{ display: "none" }}
                    onChange={onFilePicked}
                />

                <button onClick={saveFile} className="command-btn">
                    Save
                </button>
            </div>

            <div className="header-title-box">
                <h2 className="header-title-text">Brev Compiler</h2>
            </div>

            <div className="toolbar-right">
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
                    onClick={toggleTokens}
                    className={`command-btn ${tokensOpen ? "active-btn" : ""}`}
                    title={tokensOpen ? "Hide tokens" : "Show tokens"}
                >
                    Tokens {tokensOpen ? "«" : "»"}
                </button>
            </div>
        </header>
    );
}