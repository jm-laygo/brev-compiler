import React from "react";

export default function Toolbar({
    fileInputRef,
    onFilePicked,
    openFile,
    saveFile,
    // openHelp,
    // openSettings,
    runLex,
    runSyn,
    runSem,
    tokensOpen,
    toggleTokens,
}) {
    return (
        <header id = "header-row">
            <div className = "toolbar-left">
                <button onClick = {openFile} className = "command-btn">
                    Open
                </button>

                <input
                    ref = {fileInputRef}
                    type = "file"
                    style = {{ display: "none" }}
                    onChange = {onFilePicked}
                />

                <button onClick = {saveFile} className = "command-btn">
                    Save
                </button>

                {/* <button onClick = {openHelp} className = "command-btn">
                    Help
                </button>

                <button onClick = {openSettings} className = "command-btn">
                    Settings
                </button> */}
            </div>

            <div className = "header-title-box">
                <h2 className = "header-title-text">Brev Compiler</h2>
            </div>

            <div className = "toolbar-right">
                <button onClick = {runLex} className = "command-btn">
                    Run Lexical
                </button>
                <button onClick = {runSyn} className = "command-btn">
                    Run Syntax
                </button>
                <button onClick = {runSem} className = "command-btn">
                    Run Semantics
                </button>

                <button
                    onClick = {toggleTokens}
                    className = {`command-btn ${tokensOpen ? "active-btn" : ""}`}
                    title = {tokensOpen ? "Hide tokens" : "Show tokens"}
                >
                    Tokens {tokensOpen ? "«" : "»"}
                </button>
            </div>
        </header>
    );
}