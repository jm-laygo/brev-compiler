import { useCallback, useState } from "react";

export default function useTerminal(maximumLineCount = 800) {
    const [terminalLines, setTerminalLines] = useState([]);

    const addTerminalLine = useCallback(
        (lineLevel, lineText) => {
            const terminalLine = {
                id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
                level: lineLevel,
                text: String(lineText ?? ""),
            };

            setTerminalLines((previousLines) => {
                const nextLines =
                    previousLines.length >= maximumLineCount
                        ? previousLines.slice(
                              previousLines.length - (maximumLineCount - 1)
                          )
                        : previousLines.slice();

                nextLines.push(terminalLine);

                return nextLines;
            });
        },
        [maximumLineCount]
    );

    const log = useCallback(
        (lineText) => {
            addTerminalLine("info", lineText);
        },
        [addTerminalLine]
    );

    const logSuccess = useCallback(
        (lineText) => {
            addTerminalLine("success", lineText);
        },
        [addTerminalLine]
    );

    const logError = useCallback(
        (lineText) => {
            addTerminalLine("error", lineText);
        },
        [addTerminalLine]
    );

    const logWarning = useCallback(
        (lineText) => {
            addTerminalLine("warn", lineText);
        },
        [addTerminalLine]
    );

    const setTerminalOutput = useCallback((text, lineLevel = "info") => {
        const outputLines = String(text ?? "")
            .split("\n")
            .filter((lineText) => lineText.length > 0);

        setTerminalLines(
            outputLines.map((lineText) => ({
                id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
                level: lineLevel,
                text: lineText,
            }))
        );
    }, []);

    return {
        terminalLines,
        log,
        logSuccess,
        logError,
        logWarning,
        setTerminalOutput,
    };
}