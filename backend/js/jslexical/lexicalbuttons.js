const term = document.getElementById('terminal');
const openFileBtn = document.getElementById("openFileBtn");
const fileInput = document.getElementById("fileInput");
const runBtn = document.getElementById('runLex');

// open file
openFileBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        editor.innerText = e.target.result;
        sanitizeEditor();
        normalizeLines();
        updateLineNumbers();
    };

    reader.readAsText(file);
});

// save file
document.getElementById("saveFileBtn").addEventListener("click", () => {
    // Extract clean plain text
    const code = editor.innerText;

    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "brev.txt";
    a.click();
    URL.revokeObjectURL(url);
});

runBtn.addEventListener('click', async () => {
    const source = getEditorLines().join('\n');
    term.textContent = "Running lexical analysis...\n";

    try {
        const res = await fetch('/api/lex', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: source })
        });

        if (!res.ok) throw new Error("Server error: " + res.status);

        const data = await res.json();

        // clear token table and re-populate
        const tbody = document.querySelector('#tokenTable tbody');
        tbody.innerHTML = '';

        const mapToken = (type) => {
            if (!type) return "";
            if (type === " ") return "space";
            if (type === ",") return "comma";
            if (type.startsWith("TK_LIT_")) return type.replace("TK_LIT_", "").toLowerCase();
            if (type.startsWith("TK_OP_")) return type.replace("TK_OP_", "").toLowerCase();
            if (type === "TK_IDENTIFIER") return "identifier";
            return type.toLowerCase();
        };

        data.tokens.forEach(tok => {
            const row = `
                <tr>
                    <td>${escapeHtml(tok.value)}</td>
                    <td>${mapToken(tok.type)}</td>
                </tr>`;
            tbody.innerHTML += row;
        });

        if (data.errors && data.errors.length) {
            term.textContent += "Lexical Errors:\n";
            data.errors.forEach(err => term.textContent += err + "\n");
        } else {
            term.textContent += "Lexical analysis successful!\n";
        }

    } catch (err) {
        term.textContent += "Error: " + err + "\n";
    }
});

// clear button
document.getElementById("clearBtn").addEventListener("click", () => {
    editor.innerText = "";
    lineNumbers.innerHTML = "1";
    document.querySelector("#tokenTable tbody").innerHTML = "";
    term.textContent = "";
    if (typeof sanitizeEditorNodes === "function") sanitizeEditorNodes();
});

function escapeHtml(unsafe) {
    return (unsafe + '')
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

