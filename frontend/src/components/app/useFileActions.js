import { useRef, useCallback } from "react";

export default function useFileActions({
    getCode,
    editorRef,
    setInitialCode,
    setSource,
    setTerminal,
    isRunning,
    runningPhase,
    runLiveOnce,
}) {
    const fileInputRef = useRef(null);

    const openFile = useCallback(() => fileInputRef.current?.click(), []);

    const onFilePicked = useCallback(
        async (e) => {
            const file = e.target.files?.[0];
            if (!file) return;

            const text = await file.text();

            setInitialCode(text);
            setSource(text);

            if (editorRef.current) editorRef.current.setValue(text);

            setTerminal(`Loaded: ${file.name}`, "info");

            if (isRunning && runningPhase) {
                runLiveOnce(runningPhase, text, false);
            }
        },
        [editorRef, isRunning, runningPhase, runLiveOnce, setInitialCode, setSource, setTerminal]
    );

    const saveFile = useCallback(() => {
        const code = getCode();
        const blob = new Blob([code], { type: "text/plain;charset=utf-8" });

        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "brev.txt";
        a.click();
        URL.revokeObjectURL(a.href);
    }, [getCode]);

    const clearEditor = useCallback(() => {
        const editor = editorRef.current;
        if (!editor) return;

        const model = editor.getModel();
        if (!model) return;

        editor.pushUndoStop();

        const fullRange = model.getFullModelRange();
        editor.executeEdits("brev-clear", [
            {
                range: fullRange,
                text: "",
                forceMoveMarkers: true,
            },
        ]);

        editor.pushUndoStop();
        editor.focus();
    }, [editorRef]);

    return {
        fileInputRef,
        openFile,
        onFilePicked,
        saveFile,
        clearEditor,
    };
}