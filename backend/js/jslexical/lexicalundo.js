const editor = document.getElementById("code");

let undoStack = [];
let redoStack = [];
const MAX_STACK = 100;

function saveState() {
    const state = Array.from(editor.children).map(div => div.textContent);
    undoStack.push(state);
    if (undoStack.length > MAX_STACK) undoStack.shift();
    redoStack = [];
}

function restoreState(state) {
    editor.innerHTML = "";
    state.forEach(line => {
        const div = document.createElement("div");
        div.textContent = line === "\u200B" ? "" : line;
        editor.appendChild(div);
    });

    const lastLine = editor.lastElementChild;
    if (lastLine) {
        const sel = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(lastLine);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
    }

    if (typeof updateLineNumbers === "function") updateLineNumbers();
}

// Undo
function undo() {
    if (!undoStack.length) return;
    const currentState = Array.from(editor.children).map(div => div.textContent);
    redoStack.push(currentState);

    const prevState = undoStack.pop();
    restoreState(prevState);
}

// Redo
function redo() {
    if (!redoStack.length) return;
    const currentState = Array.from(editor.children).map(div => div.textContent);
    undoStack.push(currentState);

    const nextState = redoStack.pop();
    restoreState(nextState);
}

editor.addEventListener("input", () => {
    saveState();
});

document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
        e.preventDefault();
        undo();
    } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") {
        e.preventDefault();
        redo();
    }
});

saveState();
