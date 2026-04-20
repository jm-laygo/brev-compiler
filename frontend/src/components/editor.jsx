import Editor from "@monaco-editor/react";
import { brevLanguage, brevTheme } from "../editor/brevMonaco";
import { useRef } from "react";

let brevInstalled = false;

export default function BrevEditor({ initialValue, onChange, editorRef, onReady }) {
    const localEditorRef = useRef(null);

    return (
        <Editor
            height="100%"
            language="brev"
            theme="brevTheme"
            value={initialValue ?? ""}
            path="main.brev"
            beforeMount={(monaco) => {
                if (!brevInstalled) {
                    brevInstalled = true;
                    monaco.languages.register({ id: "brev" });
                    monaco.languages.setMonarchTokensProvider("brev", brevLanguage);
                }
                monaco.editor.defineTheme("brevTheme", brevTheme);

                // --- Completion Provider ---
                monaco.languages.registerCompletionItemProvider("brev", {
                    provideCompletionItems: () => {
                        const keywords = brevLanguage.keywords.concat(brevLanguage.decl, brevLanguage.types, brevLanguage.builtins, brevLanguage.booleans);
                        return {
                            suggestions: keywords.map((word) => ({
                                label: word,
                                kind: monaco.languages.CompletionItemKind.Keyword,
                                insertText: word,
                            })),
                        };
                    },
                });

                // --- Hover Provider ---
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
                    provideHover: function (model, position) {
                        const word = model.getWordAtPosition(position);
                        if (word && hoverDocs[word.word]) {
                            return {
                                range: new monaco.Range(position.lineNumber, word.startColumn, position.lineNumber, word.endColumn),
                                contents: [{ value: `**${word.word}**\n\n${hoverDocs[word.word]}` }],
                            };
                        }
                        return null;
                    },
                });

                // --- Formatting Provider ---
                monaco.languages.registerDocumentFormattingEditProvider("brev", {
                    provideDocumentFormattingEdits: function (model) {
                        const lines = model.getLinesContent();
                        // Simple formatting: indent blocks by 4 spaces
                        let indent = 0;
                        const formatted = lines.map((line) => {
                            let trimmed = line.trim();
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
            }}
            onMount={(editor, monaco) => {
                localEditorRef.current = editor;
                if (editorRef) editorRef.current = editor;

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
            }}
        />
    );
}