export const brevLanguage = {
    defaultToken: "",
    tokenPostfix: ".brev",

    keywords: [
        "receive",
        "proclaim",
        "decree",
        "absolution",
        "edict",
        "discern",
        "verse",
        "grace",
        "absolve",
        "proceed",
        "fall",
        "procession",
        "endure",
        "ritual",
        "rite",
        "dismiss",
    ],

    dataTypes: [
        "sigil",
        "tally",
        "divine",
        "scripture",
        "hollow",
        "verity",
    ],

    declarationKeywords: [
        "sacred",
        "order",
        "ordain",
        "genesis",
    ],

    builtInFunctions: [
        "verseof",
    ],

    booleanLiterals: [
        "holy",
        "unholy",
    ],

    tokenizer: {
        root: [
            { include: "@whitespace" },

            [/"/, { token: "string.quote", bracket: "@open", next: "@string" }],
            [/'([^'\\]|\\.)'/, "string.char"],

            [
                /[a-zA-Z_]\w*/,
                {
                    cases: {
                        "@booleanLiterals": "constant.bool",
                        "@dataTypes": "type",
                        "@keywords": "keyword",
                        "@declarationKeywords": "keyword.decl",
                        "@builtInFunctions": "predefined",
                        "@default": "identifier",
                    },
                },
            ],

            [
                /([a-zA-Z_]\w*)(\s*)(\()/,
                ["function", "white", "delimiter.parenthesis"],
            ],

            [/\b\d+\.\d+\b/, "number.float"],
            [/\b\d+\b/, "number"],

            [/\*\*=/, "operator"],
            [/\+=|-=|\*=|\/=|%=|\*\*/, "operator"],
            [/==|!=|>=|<=|>|</, "operator.compare"],
            [/&&|\|\|/, "operator.logic"],
            [/=|\+|-|\*|\/|%|&|!/, "operator"],

            [/[{}()[\]]/, "@brackets"],
            [/[;,.:\]]/, "delimiter"],
        ],

        whitespace: [
            [/[ \t\r\n]+/, "white"],
            [/\/\/.*$/, "comment.line"],
            [/\/\*/, "comment.block", "@comment"],
        ],

        comment: [
            [/[^/*]+/, "comment.block"],
            [/\*\//, "comment.block", "@pop"],
            [/[/*]/, "comment.block"],
        ],

        string: [
            [/[^\\"]+/, "string"],
            [/\\./, "string.escape"],
            [/"/, { token: "string.quote", bracket: "@close", next: "@pop" }],
        ],
    },
};

export const brevTheme = {
    base: "vs-dark",
    inherit: true,

    rules: [
        { token: "keyword", foreground: "F2C14E", fontStyle: "bold" },
        { token: "keyword.decl", foreground: "FF9F1C", fontStyle: "bold" },
        { token: "type", foreground: "7BDFF2", fontStyle: "bold" },
        { token: "predefined", foreground: "B8F2E6" },
        { token: "constant.bool", foreground: "9B5DE5", fontStyle: "bold" },
        { token: "function", foreground: "00F5D4", fontStyle: "bold" },

        { token: "number", foreground: "4CC9F0" },
        { token: "number.float", foreground: "4CC9F0" },
        { token: "string", foreground: "90EE90" },
        { token: "string.char", foreground: "90EE90" },
        { token: "string.escape", foreground: "FFD6A5" },

        { token: "comment.line", foreground: "6C757D", fontStyle: "italic" },
        { token: "comment.block", foreground: "6C757D", fontStyle: "italic" },

        { token: "operator", foreground: "F8F9FA" },
        { token: "operator.compare", foreground: "F2C14E" },
        { token: "operator.logic", foreground: "FF6B6B" },
        { token: "delimiter", foreground: "ADB5BD" },
        { token: "delimiter.parenthesis", foreground: "ADB5BD" },
        { token: "delimiter.bracket", foreground: "ADB5BD" },
    ],

    colors: {
        "editor.background": "#0B0F14",
        "editor.foreground": "#E6EDF3",

        "editorLineNumber.foreground": "#3A4756",
        "editorLineNumber.activeForeground": "#F2C14E",

        "editorCursor.foreground": "#F2C14E",
        "editor.selectionBackground": "#22304A",
        "editor.inactiveSelectionBackground": "#1B2433",

        "editorIndentGuide.background": "#1A2433",
        "editorIndentGuide.activeBackground": "#2C3E59",

        "editorWhitespace.foreground": "#243447",

        "editorBracketMatch.background": "#1D2A3A",
        "editorBracketMatch.border": "#F2C14E",
    },
};