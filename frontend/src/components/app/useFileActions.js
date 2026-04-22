import { useRef, useCallback } from "react";

export default function useFileActions({
    getCode,
    editorRef,
    editorApiRef,
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

            const lowerName = file.name.toLowerCase();

            if (!lowerName.endsWith(".brev")) {
                setTerminal("Only .brev files are allowed.", "error");
                if (fileInputRef.current) fileInputRef.current.value = "";
                return;
            }

            const text = await file.text();

            if (editorApiRef?.current?.openFileAsTab) {
                editorApiRef.current.openFileAsTab(file.name, text);
            } else {
                setInitialCode(text);
                setSource(text);
                if (editorRef.current) editorRef.current.setValue(text);
            }

            setTerminal(`Loaded: ${file.name}`, "info");

            if (isRunning && runningPhase) {
                runLiveOnce(runningPhase, text, false);
            }

            if (fileInputRef.current) fileInputRef.current.value = "";
        },
        [
            editorApiRef,
            editorRef,
            isRunning,
            runningPhase,
            runLiveOnce,
            setInitialCode,
            setSource,
            setTerminal,
        ]
    );

    const saveFile = useCallback(async () => {
        const code = getCode();

        let fileName = "main.brev";
        const editor = editorRef.current;
        const model = editor?.getModel();

        if (model?.__fileName) {
            fileName = model.__fileName;
        }

        if (!fileName.toLowerCase().endsWith(".brev")) {
            fileName += ".brev";
        }

        try {
            if ("showSaveFilePicker" in window) {
                const handle = await window.showSaveFilePicker({
                    suggestedName: fileName,
                    types: [
                        {
                            description: "Brev Source File",
                            accept: {
                                "text/plain": [".brev"],
                            },
                        },
                    ],
                });

                const writable = await handle.createWritable();
                await writable.write(code);
                await writable.close();

                setTerminal(`Saved as: ${handle.name}`, "success");
                return;
            }
        } catch (err) {
            if (err?.name === "AbortError") {
                setTerminal("Save cancelled.", "warn");
                return;
            }

            setTerminal(`Save As failed: ${err.message}`, "error");
            return;
        }

        const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = fileName;
        a.click();
        URL.revokeObjectURL(a.href);

        setTerminal(`Downloaded: ${fileName}`, "success");
    }, [editorRef, getCode, setTerminal]);

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