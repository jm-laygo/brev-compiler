document.getElementById('runLex').addEventListener('click', async () => {
  const source = document.getElementById('code').value;
  const term = document.getElementById('terminal');
  term.textContent += "\nRunning lexical analysis...\n";

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

    const mapToken = (type) => {
    if (!type) return "";
    if (type === " ") return "space"; // TK_SYM_SPACE
    if (type === ",") return "comma"; // TK_SYM_COMMA
    if (type.startsWith("TK_LIT_")) return type.replace("TK_LIT_", "").toLowerCase();
    if (type.startsWith("TK_OP_")) return type.replace("TK_OP_", "").toLowerCase();
    if (type === "TK_IDENTIFIER") return "identifier";
    return type.toLowerCase();
    };


    data.tokens.forEach(tok => {
      const value = tok.value;
      const row = `
        <tr>
          <td>${value}</td>
          <td>${mapToken(tok.type)}</td>
        </tr>`;
      tbody.innerHTML += row;
    });

    if (data.errors.length) {
      term.textContent += "Lexical Errors:\n" + data.errors.join("\n") + "\n";
    } else {
      term.textContent += "Lexical analysis successful!\n";
    }

  } catch (err) {
    term.textContent += "Error: " + err + "\n";
  }
});

document.getElementById('runProg')?.addEventListener('click', async () => {
  const source = document.getElementById('code').value;
  const term = document.getElementById('terminal');
  term.textContent += "\nRunning program...\n";

  try {
    const res = await fetch('/api/output', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source_code: source })
    });

    if (!res.ok) throw new Error("Server error: " + res.status);

    const data = await res.json();
    term.textContent += (data.output || "Program finished.\n");

  } catch (err) {
    term.textContent += "Error: " + err + "\n";
  }
});
