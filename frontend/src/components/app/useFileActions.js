import { useRef, useCallback } from "react";

export default function useFileActions({
    getCode,
    editorRef,
    editorApiRef,
    setInitialCode,
    setSource,
    setTerminalOutput,
    isRunning,
    runningPhase,
    runLiveOnce,
}) {
    const fileInputRef = useRef(null);

    const openFile = useCallback(() => {
        fileInputRef.current?.click();
    }, []);

    const onFilePicked = useCallback(
        async (event) => {
            const selectedFile = event.target.files?.[0];

            if (!selectedFile) {
                return;
            }

            const lowerFileName = selectedFile.name.toLowerCase();

            if (!lowerFileName.endsWith(".brev")) {
                setTerminalOutput("Only .brev files are allowed.", "error");

                if (fileInputRef.current) {
                    fileInputRef.current.value = "";
                }

                return;
            }

            const fileText = await selectedFile.text();

            if (editorApiRef?.current?.openFileAsTab) {
                editorApiRef.current.openFileAsTab(
                    selectedFile.name,
                    fileText
                );
            } else {
                setInitialCode(fileText);
                setSource(fileText);

                if (editorRef.current) {
                    editorRef.current.setValue(fileText);
                }
            }

            setTerminalOutput(`Loaded: ${selectedFile.name}`, "info");

            if (isRunning && runningPhase) {
                runLiveOnce(
                    runningPhase,
                    fileText,
                    false
                );
            }

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        },
        [
            editorApiRef,
            editorRef,
            isRunning,
            runningPhase,
            runLiveOnce,
            setInitialCode,
            setSource,
            setTerminalOutput,
        ]
    );

    const saveFile = useCallback(async () => {
        const sourceCode = getCode();

        let fileName = "main.brev";
        const editor = editorRef.current;
        const editorModel = editor?.getModel();

        if (editorModel?.__fileName) {
            fileName = editorModel.__fileName;
        }

        if (!fileName.toLowerCase().endsWith(".brev")) {
            fileName += ".brev";
        }

        try {
            if ("showSaveFilePicker" in window) {
                const fileHandle = await window.showSaveFilePicker({
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

                const writableFile = await fileHandle.createWritable();

                await writableFile.write(sourceCode);
                await writableFile.close();

                setTerminalOutput(`Saved as: ${fileHandle.name}`, "success");

                return;
            }
        } catch (errorObject) {
            if (errorObject?.name === "AbortError") {
                setTerminalOutput("Save cancelled.", "warn");
                return;
            }

            setTerminalOutput(
                `Save As failed: ${errorObject.message}`,
                "error"
            );

            return;
        }

        const fileBlob = new Blob(
            [sourceCode],
            {
                type: "text/plain;charset=utf-8",
            }
        );

        const downloadLink = document.createElement("a");

        downloadLink.href = URL.createObjectURL(fileBlob);
        downloadLink.download = fileName;
        downloadLink.click();

        URL.revokeObjectURL(downloadLink.href);

        setTerminalOutput(`Downloaded: ${fileName}`, "success");
    }, [editorRef, getCode, setTerminalOutput]);

    const clearEditor = useCallback(() => {
        const editor = editorRef.current;

        if (!editor) {
            return;
        }

        const editorModel = editor.getModel();

        if (!editorModel) {
            return;
        }

        editor.pushUndoStop();

        const fullEditorRange = editorModel.getFullModelRange();

        editor.executeEdits("brev-clear", [
            {
                range: fullEditorRange,
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