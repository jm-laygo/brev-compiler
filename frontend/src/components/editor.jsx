import Editor from "@monaco-editor/react";
import { brevLanguage, brevTheme } from "../editor/brevMonaco";
import { useCallback, useEffect, useRef, useState } from "react";

let isBrevLanguageInstalled = false;

function installBrevLanguage(monaco) {
    if (isBrevLanguageInstalled) return;

    isBrevLanguageInstalled = true;

    monaco.languages.register({ id: "brev" });
    monaco.languages.setMonarchTokensProvider("brev", brevLanguage);
    monaco.editor.defineTheme("brevTheme", brevTheme);

    monaco.languages.registerCompletionItemProvider("brev", {
        provideCompletionItems: () => {
            const keywordList = brevLanguage.keywords.concat(
                brevLanguage.decl,
                brevLanguage.types,
                brevLanguage.builtins,
                brevLanguage.booleans
            );

            return {
                suggestions: keywordList.map((keyword) => ({
                    label: keyword,
                    kind: monaco.languages.CompletionItemKind.Keyword,
                    insertText: keyword,
                })),
            };
        },
    });

    const hoverDescriptions = {
        receive: "Input statement.",
        proclaim: "Output statement.",
        decree: "Declare a variable.",
        absolution: "Delete or clear a value.",
        edict: "Declare a constant.",
        discern: "Conditional statement.",
        verse: "Function definition.",
        grace: "Exception handling.",
        absolve: "Release a resource.",
        proceed: "Continue execution.",
        fall: "Break or exit.",
        procession: "Loop construct.",
        endure: "Loop construct.",
        ritual: "Block of code.",
        rite: "Function or block.",
        dismiss: "Return or exit.",
        sacred: "Modifier for declarations.",
        order: "Modifier for declarations.",
        ordain: "Modifier for declarations.",
        genesis: "Entry point or initializer.",
        sigil: "Type: sigil.",
        tally: "Type: tally.",
        divine: "Type: divine.",
        scripture: "Type: scripture.",
        hollow: "Type: hollow.",
        verity: "Type: verity.",
        verseof: "Builtin function.",
        holy: "Boolean true.",
        unholy: "Boolean false.",
    };

    monaco.languages.registerHoverProvider("brev", {
        provideHover(editorModel, cursorPosition) {
            const currentWord = editorModel.getWordAtPosition(cursorPosition);

            if (currentWord && hoverDescriptions[currentWord.word]) {
                return {
                    range: new monaco.Range(
                        cursorPosition.lineNumber,
                        currentWord.startColumn,
                        cursorPosition.lineNumber,
                        currentWord.endColumn
                    ),
                    contents: [
                        {
                            value: `**${currentWord.word}**\n\n${hoverDescriptions[currentWord.word]}`,
                        },
                    ],
                };
            }

            return null;
        },
    });

    monaco.languages.registerDocumentFormattingEditProvider("brev", {
        provideDocumentFormattingEdits(editorModel) {
            const lineList = editorModel.getLinesContent();
            let indentationLevel = 0;

            const formattedLines = lineList.map((lineText) => {
                const trimmedLine = lineText.trim();

                if (trimmedLine.endsWith("}")) {
                    indentationLevel = Math.max(0, indentationLevel - 1);
                }

                const formattedLine = "    ".repeat(indentationLevel) + trimmedLine;

                if (trimmedLine.endsWith("{")) {
                    indentationLevel += 1;
                }

                return formattedLine;
            });

            return [
                {
                    range: editorModel.getFullModelRange(),
                    text: formattedLines.join("\n"),
                },
            ];
        },
    });
}

function createEditorTab(tabId, fileName) {
    return {
        id: tabId,
        name: fileName,
        path: `inmemory://model/${tabId}/${fileName}`,
    };
}

export default function BrevEditor({
    initialValue,
    onChange,
    editorRef,
    editorApiRef,
    onReady,
}) {
    const localEditorRef = useRef(null);
    const monacoInstanceRef = useRef(null);
    const editorModelsRef = useRef(new Map());
    const editorViewStatesRef = useRef(new Map());
    const nextTabNumberRef = useRef(2);
    const tabScrollContainerRef = useRef(null);

    const [editorTabs, setEditorTabs] = useState([
        createEditorTab("main-tab", "main.brev"),
    ]);

    const [activeTabId, setActiveTabId] = useState("main-tab");
    const [renamingTabId, setRenamingTabId] = useState(null);
    const [renamingFileName, setRenamingFileName] = useState("");

    const getEditorTabById = useCallback(
        (tabId, sourceTabs = editorTabs) => {
            return sourceTabs.find((editorTab) => editorTab.id === tabId);
        },
        [editorTabs]
    );

    const createModelForTab = useCallback((monaco, editorTab, fileContent = "") => {
        const existingModel = editorModelsRef.current.get(editorTab.id);

        if (existingModel) {
            return existingModel;
        }

        const editorModel = monaco.editor.createModel(
            fileContent,
            "brev",
            monaco.Uri.parse(editorTab.path)
        );

        editorModel.__fileName = editorTab.name;
        editorModelsRef.current.set(editorTab.id, editorModel);

        return editorModel;
    }, []);

    const switchToTab = useCallback(
        (tabId, sourceTabs = editorTabs) => {
            const editorInstance = localEditorRef.current;
            const monacoInstance = monacoInstanceRef.current;

            if (!editorInstance || !monacoInstance) {
                setActiveTabId(tabId);
                return;
            }

            const currentTab = getEditorTabById(activeTabId, sourceTabs);

            if (currentTab) {
                editorViewStatesRef.current.set(
                    currentTab.id,
                    editorInstance.saveViewState()
                );
            }

            const nextTab = getEditorTabById(tabId, sourceTabs);

            if (!nextTab) {
                return;
            }

            const nextModel =
                editorModelsRef.current.get(nextTab.id) ||
                createModelForTab(monacoInstance, nextTab, "");

            editorInstance.setModel(nextModel);

            const savedViewState = editorViewStatesRef.current.get(nextTab.id);

            if (savedViewState) {
                editorInstance.restoreViewState(savedViewState);
            }

            editorInstance.focus();
            setActiveTabId(tabId);
        },
        [activeTabId, createModelForTab, getEditorTabById, editorTabs]
    );

    const openFileAsTab = useCallback(
        (fileName, fileContent) => {
            const safeFileName =
                fileName?.trim() || `file${nextTabNumberRef.current}.brev`;

            const existingTab = editorTabs.find(
                (editorTab) => editorTab.name === safeFileName
            );

            if (existingTab) {
                const existingModel = editorModelsRef.current.get(existingTab.id);

                if (existingModel) {
                    existingModel.setValue(fileContent);
                    existingModel.__fileName = safeFileName;
                }

                requestAnimationFrame(() => {
                    switchToTab(existingTab.id, editorTabs);
                });

                return;
            }

            const newTabId = `tab-${Date.now()}`;
            const newTab = createEditorTab(newTabId, safeFileName);
            const monacoInstance = monacoInstanceRef.current;

            if (!monacoInstance) {
                return;
            }

            createModelForTab(monacoInstance, newTab, fileContent);

            setEditorTabs((previousTabs) => {
                const nextTabs = [...previousTabs, newTab];

                requestAnimationFrame(() => {
                    switchToTab(newTabId, nextTabs);
                });

                return nextTabs;
            });
        },
        [createModelForTab, switchToTab, editorTabs]
    );

    const addEditorTab = useCallback(() => {
        const nextTabNumber = nextTabNumberRef.current;
        nextTabNumberRef.current += 1;

        const newTabId = `tab-${Date.now()}`;
        const newFileName = `file${nextTabNumber}.brev`;
        const newTab = createEditorTab(newTabId, newFileName);

        setEditorTabs((previousTabs) => {
            const nextTabs = [...previousTabs, newTab];
            const monacoInstance = monacoInstanceRef.current;

            if (monacoInstance) {
                createModelForTab(monacoInstance, newTab, "");
            }

            requestAnimationFrame(() => {
                switchToTab(newTabId, nextTabs);
            });

            return nextTabs;
        });
    }, [createModelForTab, switchToTab]);

    const closeEditorTab = useCallback(
        (tabId) => {
            if (editorTabs.length === 1) {
                return;
            }

            const closingTabIndex = editorTabs.findIndex(
                (editorTab) => editorTab.id === tabId
            );

            const remainingTabs = editorTabs.filter(
                (editorTab) => editorTab.id !== tabId
            );

            const tabModel = editorModelsRef.current.get(tabId);

            if (tabModel) {
                tabModel.dispose();
                editorModelsRef.current.delete(tabId);
            }

            editorViewStatesRef.current.delete(tabId);

            let nextActiveTabId = activeTabId;

            if (activeTabId === tabId) {
                const fallbackTab =
                    remainingTabs[closingTabIndex] ||
                    remainingTabs[closingTabIndex - 1] ||
                    remainingTabs[0];

                nextActiveTabId = fallbackTab.id;
            }

            setEditorTabs(remainingTabs);

            requestAnimationFrame(() => {
                switchToTab(nextActiveTabId, remainingTabs);
            });
        },
        [activeTabId, switchToTab, editorTabs]
    );

    const startRenamingTab = useCallback((editorTab) => {
        setRenamingTabId(editorTab.id);
        setRenamingFileName(editorTab.name);
    }, []);

    const commitRenamingTab = useCallback(
        (tabId) => {
            const rawFileName = renamingFileName.trim();

            const nextFileName =
                rawFileName === ""
                    ? "untitled.brev"
                    : rawFileName.endsWith(".brev")
                    ? rawFileName
                    : `${rawFileName}.brev`;

            setEditorTabs((previousTabs) =>
                previousTabs.map((editorTab) =>
                    editorTab.id === tabId
                        ? {
                              ...editorTab,
                              name: nextFileName,
                              path: `inmemory://model/${editorTab.id}/${nextFileName}`,
                          }
                        : editorTab
                )
            );

            const editorModel = editorModelsRef.current.get(tabId);

            if (editorModel) {
                editorModel.__fileName = nextFileName;
            }

            setRenamingTabId(null);
            setRenamingFileName("");
        },
        [renamingFileName]
    );

    useEffect(() => {
        if (!editorApiRef) {
            return;
        }

        editorApiRef.current = {
            openFileAsTab,
        };

        return () => {
            editorApiRef.current = null;
        };
    }, [editorApiRef, openFileAsTab]);

    useEffect(() => {
        const tabScrollContainer = tabScrollContainerRef.current;

        if (!tabScrollContainer) {
            return;
        }

        const activeTabElement = tabScrollContainer.querySelector(
            ".brev-editor-tab.active"
        );

        if (!activeTabElement) {
            return;
        }

        activeTabElement.scrollIntoView({
            behavior: "smooth",
            inline: "center",
            block: "nearest",
        });
    }, [activeTabId, editorTabs]);

    return (
        <div className="brev-editor-shell">
            <div className="brev-editor-tabs-bar">
                <div
                    ref={tabScrollContainerRef}
                    className="brev-editor-tabs-scroll"
                    role="tablist"
                    aria-label="Editor tabs"
                >
                    {editorTabs.map((editorTab) => (
                        <button
                            key={editorTab.id}
                            type="button"
                            role="tab"
                            aria-selected={activeTabId === editorTab.id}
                            className={`brev-editor-tab ${
                                activeTabId === editorTab.id ? "active" : ""
                            }`}
                            onClick={() => switchToTab(editorTab.id)}
                            onDoubleClick={() => startRenamingTab(editorTab)}
                        >
                            {renamingTabId === editorTab.id ? (
                                <input
                                    className="brev-editor-tab-input"
                                    value={renamingFileName}
                                    autoFocus
                                    onChange={(event) =>
                                        setRenamingFileName(event.target.value)
                                    }
                                    onBlur={() => commitRenamingTab(editorTab.id)}
                                    onClick={(event) => event.stopPropagation()}
                                    onKeyDown={(event) => {
                                        if (event.key === "Enter") {
                                            commitRenamingTab(editorTab.id);
                                        }

                                        if (event.key === "Escape") {
                                            setRenamingTabId(null);
                                            setRenamingFileName("");
                                        }
                                    }}
                                />
                            ) : (
                                <span className="brev-editor-tab-label">
                                    {editorTab.name}
                                </span>
                            )}

                            {renamingTabId !== editorTab.id && (
                                <span
                                    className={`brev-editor-tab-close ${
                                        editorTabs.length > 1
                                            ? "is-visible"
                                            : "is-hidden"
                                    }`}
                                    onClick={(event) => {
                                        event.stopPropagation();

                                        if (editorTabs.length > 1) {
                                            closeEditorTab(editorTab.id);
                                        }
                                    }}
                                    title="Close tab"
                                >
                                    ×
                                </span>
                            )}
                        </button>
                    ))}
                </div>

                <div className="brev-editor-tabs-actions">
                    <button
                        type="button"
                        className="brev-editor-tab-add"
                        onClick={addEditorTab}
                        title="Add tab"
                        aria-label="Add tab"
                    >
                        +
                    </button>
                </div>
            </div>

            <div className="brev-editor-content">
                <Editor
                    height="100%"
                    defaultLanguage="brev"
                    defaultValue=""
                    theme="brevTheme"
                    beforeMount={(monaco) => {
                        installBrevLanguage(monaco);
                    }}
                    onMount={(editorInstance, monacoInstance) => {
                        monacoInstanceRef.current = monacoInstance;
                        localEditorRef.current = editorInstance;

                        if (editorRef) {
                            editorRef.current = editorInstance;
                        }

                        const firstTab = createEditorTab("main-tab", "main.brev");

                        const firstModel = createModelForTab(
                            monacoInstance,
                            firstTab,
                            initialValue ?? ""
                        );

                        editorInstance.setModel(firstModel);

                        if (typeof onReady === "function") {
                            onReady({
                                editor: editorInstance,
                                monaco: monacoInstance,
                            });
                        }
                    }}
                    onChange={(value) => onChange?.(value ?? "")}
                    saveViewState={true}
                    keepCurrentModel={true}
                    options={{
                        automaticLayout: true,
                        minimap: { enabled: false },
                        fontSize: 14,
                        renderWhitespace: "all",
                        tabSize: 4,
                        insertSpaces: false,
                        detectIndentation: false,
                        scrollBeyondLastLine: false,
                        padding: { top: 6, bottom: 6 },
                        fixedOverflowWidgets: true,
                        scrollbar: {
                            verticalScrollbarSize: 5,
                            horizontalScrollbarSize: 3,
                            alwaysConsumeMouseWheel: false,
                        },
                    }}
                />
            </div>
        </div>
    );
}