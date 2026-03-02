import { useRef, useState } from "react";
import BrevEditor from "../src/components/editor.jsx";

export default function App() {
  const fileInputRef = useRef(null);
  const [sourceCode, setSourceCode] = useState("");
  const [tokens, setTokens] = useState([]);
  const [terminal, setTerminal] = useState("");

  const openFile = () => fileInputRef.current?.click();

  const onFilePicked = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    setSourceCode(text);
    setTerminal(`Loaded: ${file.name}`);
  };

  const saveFile = () => {
    const blob = new Blob([sourceCode], { type: "text/plain;charset = utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "brev.txt";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const clearAll = () => {
    setSourceCode("");
    setTokens([]);
    setTerminal("");
  };

  // buttons for running lex/syn/sem analysis
  const runLex = async () => {
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

      setTokens(toks.filter(t => !t.hidden));  // show non-EOF tokens
      setTerminal((prev) => prev + (errs.length ? errs.join("\n") + "\n" : "Lexical analysis successful!\n"));
    } catch (e) {
      setTerminal((prev) => prev + `Network error: ${e.message}\n`);
    }
  };
  const runSyn = async () => {
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
      if (errs.length) {
        setTerminal((prev) => prev + errs.join("\n") + "\n");
      } else {
        setTerminal((prev) => prev + "Syntax analysis successful!\n");
      }
    } catch (e) {
      setTerminal((prev) => prev + `Network error: ${e.message}\n`);
    }
  };
  const runSem = async () => setTerminal("Run Semantics (not wired yet)");

  const renderLexeme = (v) => {
  if (v === null || v === undefined) return "";
  if (v === " ") return " ";     // visible space
  if (v === "\n") return "\\n";  // show newline token
  if (v === "\t") return "\\t";  // show tab token
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
              <BrevEditor value={sourceCode} onChange={setSourceCode} />
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