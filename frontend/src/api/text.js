export function renderLexemeText(v) {
  if (v === null || v === undefined) return "";
  if (v === " ") return "␠";     // clearer than &nbsp;
  if (v === "\n") return "\\n";
  if (v === "\t") return "\\t";
  return String(v);
}