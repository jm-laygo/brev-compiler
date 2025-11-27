document.addEventListener('DOMContentLoaded', () => {

    const term = document.getElementById('terminal');
    const openFileBtn = document.getElementById("openFileBtn");
    const fileInput = document.getElementById("fileInput");
    const runBtn = document.getElementById('runLex');
    const saveBtn = document.getElementById("saveFileBtn");
    const clearBtn = document.getElementById("clearBtn");

    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs' }});

    require(['vs/editor/editor.main'], () => {
        const reservedWords = [
            "receive", "proclaim",
            "sigil", "tally", "divine", "scripture", "hollow", "verity",
            "decree", "absolution", "edict", "discern", "verse", "grace",
            "absolve", "proceed", "procession", "endure", "rite", "ritual",
            "dismiss", "sacred", "genesis", "holy", "unholy", "order",
            "ordain", "massof", "verseof"
        ];

        monaco.languages.register({ id: 'brev' });

        monaco.languages.setMonarchTokensProvider('brev', {
            tokenizer: {
                root: [
                    [/\b(receive|proclaim)\b/, 'keyword'],
                    [/\b(sigil|tally|divine|scripture|hollow|verity)\b/, 'type'],
                    [/\b(decree|absolution|edict|discern|verse|grace|absolve|proceed|procession|endure|ritual|rite|dismiss)\b/, 'control'],
                    [/\b(sacred|genesis|holy|unholy|order|ordain|massof|verseof)\b/, 'constant'],
                    [/\d+\.\d+|\d+/, 'number'],
                    [/".*?"/, 'string'],
                    [/\/\/.*$/, 'comment'],
                    [/[+\-*\/%=<>!&|]+/, 'operator'],
                    [/[a-zA-Z_]\w*/, 'identifier']
                ]
            }
        });

        monaco.languages.setLanguageConfiguration('brev', {
            comments: { lineComment: '//', blockComment: ['/*','*/'] },
            brackets: [['{','}'],['[',']'],['(',')']],
            autoClosingPairs: [
                { open: '{', close: '}' },
                { open: '[', close: ']' },
                { open: '(', close: ')' },
                { open: '"', close: '"' },
                { open: "'", close: "'" }
            ],
            surroundingPairs: [
                { open: '{', close: '}' },
                { open: '[', close: ']' },
                { open: '(', close: ')' },
                { open: '"', close: '"' },
                { open: "'", close: "'" }
            ],
            indentationRules: {
                increaseIndentPattern: /^\s*(decree|absolution|edict|discern|verse|grace|absolve|proceed|procession|endure|ritual|rite|dismiss|order|ordain|massof|verseof|{\s*)$/,
                decreaseIndentPattern: /^\s*}\s*$/
            }
        });

        // theme
        monaco.editor.defineTheme('brevTheme', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: 'keyword', foreground: '0000FF' },
                { token: 'type', foreground: '800080' },
                { token: 'control', foreground: 'FFA500' },
                { token: 'constant', foreground: 'FF0000' },
                { token: 'number', foreground: '00FFFF' },
                { token: 'string', foreground: 'A52A2A' },
                { token: 'comment', foreground: '808080' },
                { token: 'operator', foreground: 'FFD700' },
                { token: 'identifier', foreground: 'FFFFFF' }
            ],
            colors: {
                "editor.foreground": "#FFFFFF",
                "editor.background": "#101010",
                "editorRuler.foreground": "#FFD700",
                "editorLineNumber.foreground": "#00FF00",
                "editorLineNumber.activeForeground": "#FFFF00"
            }
        });

        // editor
        window.editor = monaco.editor.create(document.getElementById('editor'), {
            language: 'brev',
            theme: 'brevTheme',
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            suggestOnTriggerCharacters: true,
            tabSize: 4,
            insertSpaces: true,
            // rulers: [
            //     { column: 0, color: '#FFD700', lineStyle: 'solid', margin: 20 }
            // ],
            padding: { top: 5, bottom: 5, left: 5, right: 5 },
            scrollbar: {
                alwaysConsumeMouseWheel: true,
                vertical: 'auto',
                horizontal: 'auto',
                handleMouseWheel: true,
                useShadows: false,
                verticalScrollbarSize: 6,
                horizontalScrollbarSize: 6,
                color: 'FFF'
            }
        });

        // autocomplete
        monaco.languages.registerCompletionItemProvider('brev', {
            triggerCharacters: 'abcdefghijklmnopqrstuvwxyz'.split(''),
            provideCompletionItems: (model, position) => {
                const wordUntil = model.getWordUntilPosition(position);
                const range = {
                    startLineNumber: position.lineNumber,
                    endLineNumber: position.lineNumber,
                    startColumn: wordUntil.startColumn,
                    endColumn: wordUntil.endColumn
                };

                const suggestions = reservedWords
                    .filter(word => word.startsWith(wordUntil.word))
                    .map(word => ({
                        label: word,
                        kind: monaco.languages.CompletionItemKind.Keyword,
                        insertText: word,
                        range: range
                    }));

                return { suggestions: suggestions };
            }
        });

        // buttons
        editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Space, () => {
            editor.trigger('keyboard', 'editor.action.triggerSuggest', {});
        });

        openFileBtn.addEventListener("click", () => fileInput.click());
        fileInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => window.editor.setValue(e.target.result);
            reader.readAsText(file);
        });

        saveBtn.addEventListener("click", () => {
            const code = window.editor.getValue();
            const blob = new Blob([code], { type: "text/plain" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "brev.txt";
            a.click();
            URL.revokeObjectURL(url);
        });

        runBtn.addEventListener("click", async () => {
            const source = window.editor.getValue();
            term.textContent = "Running lexical analysis...\n";
            try {
                const res = await fetch('/api/lex', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ source_code: source })
                });

                if (!res.ok) throw new Error("Server error: " + res.status);

                const data = await res.json();
                const tbody = document.querySelector('#tokenTable tbody');
                tbody.innerHTML = '';

                data.tokens.forEach(tok => {
                    const displayToken = tok.value === "\n" ? "\\n" : tok.value === " " ? "space" : tok.value;
                    tbody.innerHTML += `
                        <tr>
                            <td>${tok.value === " " ? "" : escapeHtml(tok.value)}</td>
                            <td>${escapeHtml(displayToken)}</td>
                            <td>${tok.type}</td>
                        </tr>`;
                });

                if (data.errors && data.errors.length) {
                    term.textContent += "Lexical Errors:\n" + data.errors.join("\n");
                } else {
                    term.textContent += "Lexical analysis successful!\n";
                }

            } catch (err) {
                term.textContent += "Error: " + err + "\n";
            }
        });

        clearBtn.addEventListener("click", () => {
            window.editor.setValue("");
            document.querySelector("#tokenTable tbody").innerHTML = "";
            term.textContent = "";
        });

        function escapeHtml(unsafe) {
            return (unsafe + '')
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

    });

});
