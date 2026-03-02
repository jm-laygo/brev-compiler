import Editor from "@monaco-editor/react";
import { brevLanguage, brevTheme } from "../editor/brevMonaco";

export default function BrevEditor({ value, onChange }) {
  return (
    <Editor
      height="100%"
      defaultLanguage="brev"
      value={value}
      onChange={(v) => onChange(v ?? "")}
      theme="brevTheme"
      beforeMount={(monaco) => {
        monaco.languages.register({ id: "brev" });
        monaco.languages.setMonarchTokensProvider("brev", brevLanguage);
        monaco.editor.defineTheme("brevTheme", brevTheme);
      }}
    options={{
      automaticLayout: true,
      minimap: { enabled: false },
      fontSize: 14,
      renderWhitespace: "all",
      tabSize: 4,
      insertSpaces: false,  
      detectIndentation: false
    }}
    />
  );
}