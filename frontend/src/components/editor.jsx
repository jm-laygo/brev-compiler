import Editor from "@monaco-editor/react";
import { brevLanguage, brevTheme } from "../editor/brevMonaco";
import { useRef } from "react";

let brevInstalled = false;

export default function BrevEditor({ initialValue, onChange, editorRef }) {
  const localEditorRef = useRef(null);

  return (
    <Editor
      height="100%"
      language="brev"
      theme="brevTheme"
      defaultValue={initialValue || ""}
      path="main.brev"
      beforeMount={(monaco) => {
        if (brevInstalled) return;
        brevInstalled = true;

        monaco.languages.register({ id: "brev" });
        monaco.languages.setMonarchTokensProvider("brev", brevLanguage);
        monaco.editor.defineTheme("brevTheme", brevTheme);
      }}

      onMount={(editor) => {
        localEditorRef.current = editor;
        if (editorRef) editorRef.current = editor;
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
      }}
    />
  );
}