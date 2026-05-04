export default function renderLexemeValue(lexemeValue) {
    if (lexemeValue === null || lexemeValue === undefined) {
        return "";
    }

    if (lexemeValue === " ") {
        return "";
    }

    if (lexemeValue === "\n") {
        return "\\n";
    }

    if (lexemeValue === "\t") {
        return "\\t";
    }

    return String(lexemeValue);
}