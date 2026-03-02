import { useRef, useState } from "react";
import BrevEditor from "../src/components/editor.jsx";

export default function App() {
  const fileInputRef = useRef(null);
  const editorRef = useRef(null);
  const sourceRef = useRef("");
  const [initialCode, setInitialCode] = useState("");
  const [tokens, setTokens] = useState([]);
  const [terminal, setTerminal] = useState("");
  const getCode = () => {
    return editorRef.current ? editorRef.current.getValue() : (sourceRef.current || "");
  };
  
  const openFile = () => fileInputRef.current?.click();
  const onFilePicked = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    setInitialCode(text);
    sourceRef.current = text;
    if (editorRef.current) editorRef.current.setValue(text);
    setTerminal(`Loaded: ${file.name}`);
  };

  const saveFile = () => {
    const code = getCode();
    const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "brev.txt";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const clearAll = () => {
    sourceRef.current = "";
    setInitialCode("");
    setTokens([]);
    setTerminal("");
    if (editorRef.current) editorRef.current.setValue("");
  };

  const runLex = async () => {
    const sourceCode = getCode();
    setTerminal("Running lexical analysis...\n");

    try {
      const res = await fetch("/api/lex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_code: sourceCode }),
      });

      const data = await res.json();

      if (!res.ok) {
        setTerminal((prev) => prev + `Lex API error (HTTP ${res.status}): ${data.error || "Unknown error"}\n`);
        return;
      }

      const toks = Array.isArray(data.tokens) ? data.tokens : [];
      const errs = Array.isArray(data.errors) ? data.errors : [];

      setTokens(toks.filter(t => !t.hidden));
      setTerminal((prev) => prev + (errs.length ? errs.join("\n") + "\n" : "Lexical analysis successful!\n"));
    } catch (e) {
      setTerminal((prev) => prev + `Network error: ${e.message}\n`);
    }
  };

  const runSyn = async () => {
    const sourceCode = getCode();
    setTerminal("Running syntax analysis...\n");

    try {
      const res = await fetch("/api/syntax", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_code: sourceCode }),
      });

      const data = await res.json();

      if (!res.ok) {
        setTerminal((prev) => prev + `Syntax API error (HTTP ${res.status}): ${data.error || "Unknown error"}\n`);
        return;
      }

      const errs = Array.isArray(data.errors) ? data.errors : [];
      setTerminal((prev) => prev + (errs.length ? errs.join("\n") + "\n" : "Syntax analysis successful!\n"));
    } catch (e) {
      setTerminal((prev) => prev + `Network error: ${e.message}\n`);
    }
  };

  const runSem = async () => {
    const sourceCode = getCode();
    setTerminal("Running semantic analysis...\n");

    try {
      const res = await fetch("/api/sem", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_code: sourceCode }),
      });

      const data = await res.json();

      if (!res.ok) {
        setTerminal((prev) => prev + `Sem API error (HTTP ${res.status}): ${data.error || "Unknown error"}\n`);
        return;
      }

      const errs = Array.isArray(data.errors) ? data.errors : [];
      setTerminal((prev) => prev + (errs.length ? errs.join("\n") + "\n" : "Semantic analysis successful!\n"));
    } catch (e) {
      setTerminal((prev) => prev + `Network error: ${e.message}\n`);
    }
  };

  const renderLexeme = (v) => {
    if (v === null || v === undefined) return "";
    if (v === " ") return " ";
    if (v === "\n") return "\\n";
    if (v === "\t") return "\\t";
    return String(v);
  };

  return (
    <>
      <div id="brev-background"></div>

      <main id="brev-container">
        <section id="brev-inner-container">
          <header id="header-row">
            <div className="header-left">
              <button onClick={openFile} className="command-btn">Open</button>
              <input
                ref={fileInputRef}
                type="file"
                style={{ display: "none" }}
                onChange={onFilePicked}
              />
              <button onClick={saveFile} className="command-btn">Save</button>
            </div>

            <div className="header-title-box">
              <h2 className="header-title-text">Brev Compiler</h2>
            </div>

            <div className="header-right">
              <button onClick={runLex} className="command-btn">Run Lexical</button>
              <button onClick={runSyn} className="command-btn">Run Syntax</button>
              <button onClick={runSem} className="command-btn">Run Semantics</button>
              <button onClick={clearAll} className="command-btn">Clear</button>
            </div>
          </header>

          <div id="brev-inner-content">
            <div id="brev-pane">
              <BrevEditor
                initialValue={initialCode}
                editorRef={editorRef}
                onChange={(v) => { sourceRef.current = v; }}
              />
            </div>

            <div id="table-terminal">
              <div className="panel">
                <h3 className="panel-title">Tokens</h3>
                <table id="tokenTable">
                  <thead>
                    <tr>
                      <th>Lexeme</th>
                      <th>Token</th>
                      <th>Type</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tokens.map((t, idx) => (
                      <tr key={idx}>
                        <td style={{ whiteSpace: "pre" }}>{renderLexeme(t.value)}</td>
                        <td>{t.token}</td>
                        <td>{t.type}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="panel">
                <h3 className="panel-title">Output</h3>
                <pre id="terminal">{terminal}</pre>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}