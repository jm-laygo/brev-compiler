import { useCallback, useState } from "react";

export default function useTerminal(maxLines = 800) {
    const [terminalLines, setTerminalLines] = useState([]);

    const push = useCallback((level, text) => {
        const line = {
            id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
            level,
            text: String(text ?? ""),
        };

        setTerminalLines((prev) => {
            const next = prev.length >= maxLines ? prev.slice(prev.length - (maxLines - 1)) : prev.slice();
            next.push(line);
            return next;
        });
    }, [maxLines]);

    const log = useCallback((text) => {
        push("info", text);
    }, [push]);

    const logSuccess = useCallback((text) => {
        push("success", text);
    }, [push]);

    const logError = useCallback((text) => {
        push("error", text);
    }, [push]);

    const logWarn = useCallback((text) => {
        push("warn", text);
    }, [push]);

    const setTerminal = useCallback((text, level = "info") => {
        const lines = String(text ?? "").split("\n").filter((x) => x.length > 0);

        setTerminalLines(
            lines.map((t) => ({
                id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
                level,
                text: t,
            }))
        );
    }, []);

    return { terminalLines, log, logSuccess, logError, logWarn, setTerminal };
}