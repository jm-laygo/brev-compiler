import React, { useEffect, useRef } from "react";

export default function OutputPanel({ terminalLines = [] }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ block: "end" });
    }, [terminalLines]);

    return (
        <section className="output-panel">
            <div className="output-head">
                <div className="output-title">Output</div>
                <div className="output-count">{terminalLines.length} lines</div>
            </div>

            <div className="output-body" role="log" aria-live="polite">
                {terminalLines.map((l) => (
                    <div key={l.id} className={`term-line ${l.level || "info"}`}>
                        {l.text}
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
        </section>
    );
}