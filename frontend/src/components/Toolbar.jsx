import React from "react";

export default function Toolbar({
    fileInputRef,
    onFilePicked,
    openFile,
    saveFile,
    clearEditor,
    toggleRunProgram,
    isRunning,
    runningPhase,
}) {
    const isProgramRunning = isRunning && runningPhase === "program";

    return (
        <header id="header-row">
            <div className="toolbar-left">
                <button
                    onClick={toggleRunProgram}
                    className={`command-btn command-btn-run ${
                        isProgramRunning ? "active-btn" : ""
                    }`}
                    aria-label={
                        isProgramRunning ? "Stop running program" : "Run program"
                    }
                    title={
                        isProgramRunning ? "Stop running program" : "Run program"
                    }
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
            </div>
        </header>
    );
}