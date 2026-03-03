import { useCallback, useState } from "react";

export default function useTerminal(maxLines = 800) {
    const [terminalLines, setTerminalLines] = useState([]);

    const log = useCallback((line) => {
        setTerminalLines((prev) => {
            const next = [...prev, line];
            return next.length > maxLines ? next.slice(-maxLines) : next;
        });
    }, [maxLines]);

    const setTerminal = useCallback((text) => {
        setTerminalLines(text ? text.split("\n") : []);
    }, []);

    return { terminalLines, log, setTerminal };
}