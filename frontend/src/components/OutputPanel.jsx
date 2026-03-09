import React, { useEffect, useMemo, useRef } from "react";

function parseLnColFromText(text) {
    const s = String(text ?? "");
    const m = s.match(/Ln\s*(\d+)\s*,\s*Col\s*(\d+)/i);
    if (!m) return null;

    return {
        line: Number(m[1]),
        col: Number(m[2]),
        matchText: m[0],
        matchIndex: m.index ?? -1,
    };
}

function splitLineClickableParts(lineObj) {
    const text = String(lineObj?.text ?? "");
    const pos = parseLnColFromText(text);
    if (!pos || pos.matchIndex < 0) {
        return { before: text, link: null, after: "" };
    }

    const start = pos.matchIndex;
    const end = start + pos.matchText.length;

    return {
        before: text.slice(0, start),
        link: {
            label: text.slice(start, end),
            line: pos.line,
            col: pos.col,
        },
        after: text.slice(end),
    };
}

function renderExpectedDelims(text) {
    const s = String(text ?? "");
    const m = s.match(/(Expected:\s*)(.*)$/i);
    if (!m) return s;

    const prefix = s.slice(0, m.index ?? 0) + m[1];
    const list = m[2];
    const parts = list.split(/(\s*,\s*)/);

    return (
        <>
            <span>{prefix}</span>
            {parts.map((p, i) => {
                const isComma = /^\s*,\s*$/.test(p);
                if (isComma) return <span key={i}>{p}</span>;
                return (
                    <span key={i} className="term-delim">
                        {p}
                    </span>
                );
            })}
        </>
    );
}

export default function OutputPanel({
    terminalLines = [],
    outputOpen,
    toggleOutput,
    onJumpToPosition,
    runtimePrompt = null,
    onSubmitRuntimeInput,
}) {
    const bottomRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        if (!outputOpen) return;
        bottomRef.current?.scrollIntoView({ block: "end" });
    }, [terminalLines, outputOpen, runtimePrompt]);

    useEffect(() => {
        if (!runtimePrompt) return;
        setTimeout(() => inputRef.current?.focus(), 0);
    }, [runtimePrompt]);

    const rendered = useMemo(() => {
        return (Array.isArray(terminalLines) ? terminalLines : []).map((l) => {
            const parts = splitLineClickableParts(l);
            return { lineObj: l, parts };
        });
    }, [terminalLines]);

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(e.currentTarget);
        const value = String(formData.get("runtime_input") ?? "");

        if (value.trim() === "") {
            inputRef.current?.focus();
            return;
        }

        onSubmitRuntimeInput?.(value);
        e.currentTarget.reset();
    };

    return (
        <div className={`panel output-panel ${outputOpen ? "open" : "closed"}`}>
            <div className="panel-head">
                <h3 className="panel-title">Output</h3>

                <div className="output-right">
                    <div className="panel-hint">{terminalLines.length} lines</div>

                    <button
                        type="button"
                        className="output-toggle-btn"
                        onClick={toggleOutput}
                        aria-label={outputOpen ? "Collapse output" : "Expand output"}
                        title={outputOpen ? "Collapse output" : "Expand output"}
                    >
                        {outputOpen ? "×" : "▲"}
                    </button>
                </div>
            </div>

            <div id="terminal" role="log" aria-live="polite">
                {rendered.map(({ lineObj, parts }) => {
                    const lvl = lineObj.level || "info";
                    const afterNode =
                        lvl === "error" ? renderExpectedDelims(parts.after) : parts.after;

                    return (
                        <div key={lineObj.id} className={`term-line ${lvl}`}>
                            <span>{parts.before}</span>

                            {parts.link && (
                                <button
                                    type="button"
                                    className="term-loc-link"
                                    onClick={() => onJumpToPosition?.(parts.link.line, parts.link.col)}
                                    title="Jump to this location"
                                >
                                    {parts.link.label}
                                </button>
                            )}

                            <span>{afterNode}</span>
                        </div>
                    );
                })}

                {runtimePrompt && (
                    <form className="terminal-stdin-line" onSubmit={handleSubmit}>
                        <span className="terminal-stdin-prefix">{runtimePrompt.prefix ?? ""}</span>

                        <input
                            key={runtimePrompt?.id ?? "runtime-input"}
                            ref={inputRef}
                            name="runtime_input"
                            type="text"
                            className="terminal-stdin-input"
                            defaultValue=""
                            autoComplete="off"
                            spellCheck={false}
                        />
                    </form>
                )}

                <div ref={bottomRef} />
            </div>
        </div>
    );
}