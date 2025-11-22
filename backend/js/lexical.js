const term = document.getElementById('terminal');
const textarea = document.getElementById("code");
const lineNumbers = document.getElementById("lineNumbers");

// for text numbe

textarea.addEventListener("input", updateLines);
textarea.addEventListener("scroll", syncScroll);

function updateLines() {
    const lines = textarea.value.split("\n").length;
    let numberHtml = "";
    for (let i = 1; i <= lines; i++) {
        numberHtml += i + "<br>";
    }
    lineNumbers.innerHTML = numberHtml;
}

function syncScroll() {
    lineNumbers.scrollTop = textarea.scrollTop;
}

document.getElementById('runLex').addEventListener('click', async () => {
    const source = document.getElementById('code').value;
    term.textContent = "Running lexical analysis...\n";

    try {
        const res = await fetch('/api/lex', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: source })
        });

        if (!res.ok) throw new Error("Server error: " + res.status);

        const data = await res.json();

        // Clear previous tokens
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

        // Populate tokens table
        data.tokens.forEach(tok => {
            const row = `
                <tr>
                    <td>${tok.value}</td>
                    <td>${mapToken(tok.type)}</td>
                </tr>`;
            tbody.innerHTML += row;
        });

        // Display errors line by line
        if (data.errors.length) {
            term.textContent += "Lexical Errors:\n";
            data.errors.forEach(err => {
                term.textContent += err + "\n";
            });
        } else {
            term.textContent += "Lexical analysis successful!\n";
        }

    } catch (err) {
        term.textContent += "Error: " + err + "\n";
    }
});

// document.getElementById('runProg')?.addEventListener('click', async () => {
//     const source = document.getElementById('code').value;

//     // Clear terminal
//     term.textContent = "Running program...\n";

//     try {
//         const res = await fetch('/api/output', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ source_code: source })
//         });

//         if (!res.ok) throw new Error("Server error: " + res.status);

//         const data = await res.json();
//         term.textContent += (data.output || "Program finished.\n");

//     } catch (err) {
//         term.textContent += "Error: " + err + "\n";
//     }
// });
