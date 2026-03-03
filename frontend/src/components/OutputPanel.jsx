import React from "react";

export default function OutputPanel({ terminalLines }) {
    return (
        <div className = "panel output-panel">
            <div className = "panel-head">
                <h3 className = "panel-title">Output</h3>
                <div className = "panel-hint">Logs</div>
            </div>
            <pre id = "terminal">{terminalLines.join("\n")}</pre>
        </div>
    );
}