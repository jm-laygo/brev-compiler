// main.js
const socket = io.connect(window.location.origin, { transports: ['polling'] });

socket.on('output', data => {
  const term = document.getElementById('terminal');
  term.textContent += data.output + "\n";
  term.scrollTop = term.scrollHeight;
});

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

    data.tokens.forEach(tok => {
      const row = `<tr>
        <td>${tok.type}</td>
        <td>${tok.value || ''}</td>
        <td>${tok.line}</td>
      </tr>`;
      tbody.innerHTML += row;
    });

    if (data.errors.length) {
      term.textContent += "❌ Lexical Errors:\n" + data.errors.join("\n") + "\n";
    } else {
      term.textContent += "✅ Lexical analysis successful!\n";
    }
  } catch (err) {
    term.textContent += "Error: " + err + "\n";
  }
});


document.getElementById('runProg').addEventListener('click', async () => {
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

    term.textContent += data.output + "\n";
  } catch (err) {
    term.textContent += "Error: " + err + "\n";
  }
});
