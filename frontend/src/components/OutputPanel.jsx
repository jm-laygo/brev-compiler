import React, { useEffect, useMemo, useRef } from "react";

function parseLineColumnFromText(text) {
    const normalizedText = String(text ?? "");
    const matchedLocation = normalizedText.match(/Ln\s*(\d+)\s*,\s*Col\s*(\d+)/i);

    if (!matchedLocation) {
        return null;
    }

    return {
        lineNumber: Number(matchedLocation[1]),
        columnNumber: Number(matchedLocation[2]),
        matchedText: matchedLocation[0],
        matchedIndex: matchedLocation.index ?? -1,
    };
}

function splitClickableLineParts(lineObject) {
    const lineText = String(lineObject?.text ?? "");
    const parsedLocation = parseLineColumnFromText(lineText);

    if (!parsedLocation || parsedLocation.matchedIndex < 0) {
        return {
            beforeText: lineText,
            locationLink: null,
            afterText: "",
        };
    }

    const startIndex = parsedLocation.matchedIndex;
    const endIndex = startIndex + parsedLocation.matchedText.length;

    return {
        beforeText: lineText.slice(0, startIndex),
        locationLink: {
            label: lineText.slice(startIndex, endIndex),
            lineNumber: parsedLocation.lineNumber,
            columnNumber: parsedLocation.columnNumber,
        },
        afterText: lineText.slice(endIndex),
    };
}

function renderExpectedDelimiters(text) {
    const normalizedText = String(text ?? "");
    const expectedMatch = normalizedText.match(/(Expected:\s*)(.*)$/i);

    if (!expectedMatch) {
        return normalizedText;
    }

    const prefixText = normalizedText.slice(0, expectedMatch.index ?? 0) + expectedMatch[1];
    const delimiterListText = expectedMatch[2];
    const delimiterParts = delimiterListText.split(/(\s*,\s*)/);

    return (
        <>
            <span>{prefixText}</span>

            {delimiterParts.map((delimiterPart, delimiterIndex) => {
                const isCommaSeparator = /^\s*,\s*$/.test(delimiterPart);

                if (isCommaSeparator) {
                    return <span key={delimiterIndex}>{delimiterPart}</span>;
                }

                return (
                    <span key={delimiterIndex} className="term-delim">
                        {delimiterPart}
                    </span>
                );
            })}
        </>
    );
}

export default function OutputPanel({
    terminalLines = [],
    outputOpen,
    panelStyle,
    onStartResize,
    isResizing = false,
    onJumpToPosition,
    runtimePrompt = null,
    onSubmitRuntimeInput,
}) {
    const bottomElementRef = useRef(null);
    const runtimeInputRef = useRef(null);

    useEffect(() => {
        if (!outputOpen) {
            return;
        }

        bottomElementRef.current?.scrollIntoView({
            block: "end",
        });
    }, [terminalLines, outputOpen, runtimePrompt]);

    useEffect(() => {
        if (!runtimePrompt) {
            return;
        }

        setTimeout(() => {
            runtimeInputRef.current?.focus();
        }, 0);
    }, [runtimePrompt]);

    const renderedLines = useMemo(() => {
        return (Array.isArray(terminalLines) ? terminalLines : []).map((lineObject) => {
            const clickableParts = splitClickableLineParts(lineObject);

            return {
                lineObject,
                clickableParts,
            };
        });
    }, [terminalLines]);

    const handleRuntimeInputSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData(event.currentTarget);
        const inputValue = String(formData.get("runtime_input") ?? "");

        if (inputValue.trim() === "") {
            runtimeInputRef.current?.focus();
            return;
        }

        onSubmitRuntimeInput?.(inputValue);
        event.currentTarget.reset();
    };

    return (
        <div
            className={`panel output-panel ${outputOpen ? "open" : "closed"}`}
            style={panelStyle}
        >
            {outputOpen && (
                <div
                    className={`output-resize-grip ${isResizing ? "dragging" : ""}`}
                    role="separator"
                    aria-orientation="vertical"
                    aria-label="Resize editor and output panels"
                    onPointerDown={onStartResize}
                />
            )}

            <div className="panel-head">
                <h3 className="panel-title">Output</h3>

                <div className="output-right">
                    <div className="panel-hint">
                        {terminalLines.length} lines
                    </div>
                </div>
            </div>

            <div id="terminal" role="log" aria-live="polite">
                {renderedLines.map(({ lineObject, clickableParts }) => {
                    const lineLevel = lineObject.level || "info";

                    const afterNode =
                        lineLevel === "error"
                            ? renderExpectedDelimiters(clickableParts.afterText)
                            : clickableParts.afterText;

                    return (
                        <div
                            key={lineObject.id}
                            className={`term-line ${lineLevel}`}
                        >
                            <span>{clickableParts.beforeText}</span>

                            {clickableParts.locationLink && (
                                <button
                                    type="button"
                                    className="term-loc-link"
                                    onClick={() =>
                                        onJumpToPosition?.(
                                            clickableParts.locationLink.lineNumber,
                                            clickableParts.locationLink.columnNumber
                                        )
                                    }
                                    title="Jump to this location"
                                >
                                    {clickableParts.locationLink.label}
                                </button>
                            )}

                            <span>{afterNode}</span>
                        </div>
                    );
                })}

                {runtimePrompt && (
                    <form
                        className="terminal-stdin-line"
                        onSubmit={handleRuntimeInputSubmit}
                        onClick={() => runtimeInputRef.current?.focus()}
                    >
                        <span className="terminal-stdin-prefix">
                            {runtimePrompt.prefix ?? ""}
                        </span>

                        <input
                            key={runtimePrompt?.id ?? "runtime-input"}
                            ref={runtimeInputRef}
                            name="runtime_input"
                            type="text"
                            className="terminal-stdin-input"
                            defaultValue=""
                            autoComplete="off"
                            spellCheck={false}
                        />
                    </form>
                )}

                <div ref={bottomElementRef} />
            </div>
        </div>
    );
}