export default function renderLexeme(v) {
    if (v === null || v === undefined) return "";
    if (v === " ") return "␠";
    if (v === "\n") return "\\n";
    if (v === "\t") return "\\t";
    return String(v);
}