export const brevLanguage = {
  tokenizer: {
    root: [
      [/\b(receive|proclaim)\b/, "keyword"],
      [/\b(sigil|tally|divine|scripture|hollow|verity)\b/, "type"],
      [/\b(decree|absolution|edict|discern|verse|grace|absolve|proceed|fall|procession|endure|ritual|rite|dismiss)\b/, "control"],
      [/\b(sacred|genesis|holy|unholy|order|ordain|verseof)\b/, "constant"],
      [/\d+(\.\d+)?/, "number"],
      [/".*?"/, "string"],
      [/\/\*/, "comment", "@comment"],
      [/\/\/.*$/, "comment"],
     [ /[+\-*/%=<>!&|$]+/, "operator" ],
      [/[a-zA-Z_]\w*/, "identifier"],
    ],
    comment: [
      [/[^/*]+/, "comment"],
      [/\*\//, "comment", "@pop"],
      [/[/*]/, "comment"],
    ],
  },
};

export const brevTheme = {
  base: "vs-dark",
  inherit: true,
  rules: [
    { token: "keyword", foreground: "0000FF" },
    { token: "type", foreground: "800080" },
    { token: "control", foreground: "FFA500" },
    { token: "constant", foreground: "FF0000" },
    { token: "number", foreground: "00FFFF" },
    { token: "string", foreground: "A52A2A" },
    { token: "comment", foreground: "808080" },
  ],
  colors: {
    "editor.background": "#101010",
    "editor.foreground": "#FFFFFF",
  },
};