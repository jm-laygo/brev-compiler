import Editor from "@monaco-editor/react";
import { brevLanguage, brevTheme } from "../editor/brevMonaco";
import { useCallback, useEffect, useRef, useState } from "react";

let brevInstalled = false;

function installBrev(monaco) {
    if (brevInstalled) return;
    brevInstalled = true;

    monaco.languages.register({ id: "brev" });
    monaco.languages.setMonarchTokensProvider("brev", brevLanguage);
    monaco.editor.defineTheme("brevTheme", brevTheme);

    monaco.languages.registerCompletionItemProvider("brev", {
        provideCompletionItems: () => {
            const keywords = brevLanguage.keywords.concat(
                brevLanguage.decl,
                brevLanguage.types,
                brevLanguage.builtins,
                brevLanguage.booleans
            );

            return {
                suggestions: keywords.map((word) => ({
                    label: word,
                    kind: monaco.languages.CompletionItemKind.Keyword,
                    insertText: word,
                })),
            };
        },
    });

    const hoverDocs = {
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
        provideHover(model, position) {
            const word = model.getWordAtPosition(position);
            if (word && hoverDocs[word.word]) {
                return {
                    range: new monaco.Range(
                        position.lineNumber,
                        word.startColumn,
                        position.lineNumber,
                        word.endColumn
                    ),
                    contents: [{ value: `**${word.word}**\n\n${hoverDocs[word.word]}` }],
                };
            }
            return null;
        },
    });

    monaco.languages.registerDocumentFormattingEditProvider("brev", {
        provideDocumentFormattingEdits(model) {
            const lines = model.getLinesContent();
            let indent = 0;

            const formatted = lines.map((line) => {
                const trimmed = line.trim();
                if (trimmed.endsWith("}")) indent = Math.max(0, indent - 1);
                const result = "    ".repeat(indent) + trimmed;
                if (trimmed.endsWith("{")) indent++;
                return result;
            });

            return [
                {
                    range: model.getFullModelRange(),
                    text: formatted.join("\n"),
                },
            ];
        },
    });
}

function makeTab(id, name) {
    return {
        id,
        name,
        path: `inmemory://model/${id}/${name}`,
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
    const monacoRef = useRef(null);
    const modelsRef = useRef(new Map());
    const viewStatesRef = useRef(new Map());
    const nextTabNumberRef = useRef(2);

    const [tabs, setTabs] = useState([makeTab("main-tab", "main.brev")]);
    const [activeTabId, setActiveTabId] = useState("main-tab");
    const [editingTabId, setEditingTabId] = useState(null);
    const [editingName, setEditingName] = useState("");
    const tabsScrollRef = useRef(null);

    const getTabById = useCallback(
        (tabId, sourceTabs = tabs) => sourceTabs.find((tab) => tab.id === tabId),
        [tabs]
    );

    const createModelForTab = useCallback((monaco, tab, value = "") => {
        const existing = modelsRef.current.get(tab.id);
        if (existing) return existing;

        const model = monaco.editor.createModel(
            value,
            "brev",
            monaco.Uri.parse(tab.path)
        );
        model.__fileName = tab.name;
        modelsRef.current.set(tab.id, model);
        return model;
    }, []);

    const switchToTab = useCallback(
        (tabId, sourceTabs = tabs) => {
            const editor = localEditorRef.current;
            const monaco = monacoRef.current;

            if (!editor || !monaco) {
                setActiveTabId(tabId);
                return;
            }

            const currentTab = getTabById(activeTabId, sourceTabs);
            if (currentTab) {
                viewStatesRef.current.set(currentTab.id, editor.saveViewState());
            }

            const nextTab = getTabById(tabId, sourceTabs);
            if (!nextTab) return;

            const nextModel =
                modelsRef.current.get(nextTab.id) ||
                createModelForTab(monaco, nextTab, "");

            editor.setModel(nextModel);

            const savedViewState = viewStatesRef.current.get(nextTab.id);
            if (savedViewState) {
                editor.restoreViewState(savedViewState);
            }

            editor.focus();
            setActiveTabId(tabId);
        },
        [activeTabId, createModelForTab, getTabById, tabs]
    );

    const openFileAsTab = useCallback(
        (fileName, fileText) => {
            const safeName =
                fileName?.trim() || `file${nextTabNumberRef.current}.brev`;

            const existingTab = tabs.find((tab) => tab.name === safeName);
            if (existingTab) {
                const model = modelsRef.current.get(existingTab.id);
                if (model) {
                    model.setValue(fileText);
                    model.__fileName = safeName;
                }

                requestAnimationFrame(() => {
                    switchToTab(existingTab.id, tabs);
                });
                return;
            }

            const newId = `tab-${Date.now()}`;
            const newTab = makeTab(newId, safeName);

            const monaco = monacoRef.current;
            if (!monaco) return;

            createModelForTab(monaco, newTab, fileText);

            setTabs((prev) => {
                const nextTabs = [...prev, newTab];

                requestAnimationFrame(() => {
                    switchToTab(newId, nextTabs);
                });

                return nextTabs;
            });
        },
        [createModelForTab, switchToTab, tabs]
    );

    const addTab = useCallback(() => {
        const nextNumber = nextTabNumberRef.current++;
        const newId = `tab-${Date.now()}`;
        const newName = `file${nextNumber}.brev`;
        const newTab = makeTab(newId, newName);

        setTabs((prev) => {
            const nextTabs = [...prev, newTab];

            const monaco = monacoRef.current;
            if (monaco) {
                createModelForTab(monaco, newTab, "");
            }

            requestAnimationFrame(() => {
                switchToTab(newId, nextTabs);
            });

            return nextTabs;
        });
    }, [createModelForTab, switchToTab]);

    const closeTab = useCallback(
        (tabId) => {
            if (tabs.length === 1) return;

            const closingIndex = tabs.findIndex((tab) => tab.id === tabId);
            const nextTabs = tabs.filter((tab) => tab.id !== tabId);

            const model = modelsRef.current.get(tabId);
            if (model) {
                model.dispose();
                modelsRef.current.delete(tabId);
            }
            viewStatesRef.current.delete(tabId);

            let nextActiveId = activeTabId;
            if (activeTabId === tabId) {
                const fallbackTab =
                    nextTabs[closingIndex] || nextTabs[closingIndex - 1] || nextTabs[0];
                nextActiveId = fallbackTab.id;
            }

            setTabs(nextTabs);

            requestAnimationFrame(() => {
                switchToTab(nextActiveId, nextTabs);
            });
        },
        [activeTabId, switchToTab, tabs]
    );

    const startRenameTab = useCallback((tab) => {
        setEditingTabId(tab.id);
        setEditingName(tab.name);
    }, []);

    const commitRenameTab = useCallback(
        (tabId) => {
            const nextNameRaw = editingName.trim();
            const nextName =
                nextNameRaw === ""
                    ? "untitled.brev"
                    : nextNameRaw.endsWith(".brev")
                    ? nextNameRaw
                    : `${nextNameRaw}.brev`;

            setTabs((prev) =>
                prev.map((tab) =>
                    tab.id === tabId
                        ? {
                              ...tab,
                              name: nextName,
                              path: `inmemory://model/${tab.id}/${nextName}`,
                          }
                        : tab
                )
            );

            const model = modelsRef.current.get(tabId);
            if (model) {
                model.__fileName = nextName;
            }

            setEditingTabId(null);
            setEditingName("");
        },
        [editingName]
    );

    useEffect(() => {
        if (!editorApiRef) return;

        editorApiRef.current = {
            openFileAsTab,
        };

        return () => {
            editorApiRef.current = null;
        };
    }, [editorApiRef, openFileAsTab]);

    useEffect(() => {
        const container = tabsScrollRef.current;
        if (!container) return;

        const activeTabEl = container.querySelector(".brev-editor-tab.active");
        if (!activeTabEl) return;

        activeTabEl.scrollIntoView({
            behavior: "smooth",
            inline: "center",
            block: "nearest",
        });
    }, [activeTabId, tabs]);

    return (
        <div className="brev-editor-shell">
            <div className="brev-editor-tabs-bar">
    <div
        ref={tabsScrollRef}
        className="brev-editor-tabs-scroll"
        role="tablist"
        aria-label="Editor tabs"
    >
        {tabs.map((tab) => (
            <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTabId === tab.id}
                className={`brev-editor-tab ${activeTabId === tab.id ? "active" : ""}`}
                onClick={() => switchToTab(tab.id)}
                onDoubleClick={() => startRenameTab(tab)}
            >
                {editingTabId === tab.id ? (
                    <input
                        className="brev-editor-tab-input"
                        value={editingName}
                        autoFocus
                        onChange={(e) => setEditingName(e.target.value)}
                        onBlur={() => commitRenameTab(tab.id)}
                        onClick={(e) => e.stopPropagation()}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") commitRenameTab(tab.id);
                            if (e.key === "Escape") {
                                setEditingTabId(null);
                                setEditingName("");
                            }
                        }}
                    />
                ) : (
                    <span className="brev-editor-tab-label">{tab.name}</span>
                )}

                {editingTabId !== tab.id && (
                    <span
                        className={`brev-editor-tab-close ${tabs.length > 1 ? "is-visible" : "is-hidden"}`}
                        onClick={(e) => {
                            e.stopPropagation();
                            if (tabs.length > 1) closeTab(tab.id);
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
            onClick={addTab}
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
                        installBrev(monaco);
                    }}
                    onMount={(editor, monaco) => {
                        monacoRef.current = monaco;
                        localEditorRef.current = editor;
                        if (editorRef) editorRef.current = editor;

                        const firstTab = makeTab("main-tab", "main.brev");
                        const firstModel = createModelForTab(
                            monaco,
                            firstTab,
                            initialValue ?? ""
                        );
                        editor.setModel(firstModel);

                        if (typeof onReady === "function") {
                            onReady({ editor, monaco });
                        }
                    }}
                    onChange={(v) => onChange?.(v ?? "")}
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