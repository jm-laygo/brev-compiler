const editor = document.getElementById("code");
const lineNumbers = document.getElementById("lineNumbers");
const ZERO_WIDTH = "\u200B";

function getEditorLines() {
    return Array.from(editor.children).map(div => {
        let text = div.textContent || "";
        // Remove ZERO_WIDTH spaces everywhere
        text = text.replace(/\u200B/g, "");
        return text;
    });
}
const sourceCode = getEditorLines().join("\n");


function createLine(text = "") {
    const div = document.createElement("div");
    div.textContent = text || ZERO_WIDTH;
    return div;
}

function normalizeLines() {
    if (!editor.firstChild) editor.appendChild(createLine());
    const nodes = Array.from(editor.childNodes);
    for (let node of nodes) {
        if (node.nodeType === Node.TEXT_NODE) {
            const frag = document.createDocumentFragment();
            node.textContent.split("\n").forEach(t => frag.appendChild(createLine(t)));
            editor.replaceChild(frag, node);
        } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== "DIV") {
            editor.replaceChild(createLine(node.textContent), node);
        }
    }
}

function getLineForRange(range) {
    let node = range.startContainer;
    if (!node) return editor.firstElementChild || createLine();
    if (node.nodeType === 3 && node.parentNode.tagName === "DIV") return node.parentNode;
    while (node && node !== editor && node.tagName !== "DIV") node = node.parentNode;
    return node === editor ? editor.firstElementChild : node;
}

function getCaretOffset(line, range) {
    if (range.startContainer.nodeType === 3) {
        let offset = range.startOffset;
        let node = range.startContainer.previousSibling;
        while (node) { offset += node.textContent.length; node = node.previousSibling; }
        return offset;
    }
    let offset = 0;
    for (let i = 0; i < range.startOffset; i++) {
        const child = range.startContainer.childNodes[i];
        if (child) offset += child.textContent.length;
    }
    return offset;
}

function placeCaret(line, charOffset) {
    const sel = window.getSelection();
    const range = document.createRange();
    if (!line.firstChild) line.textContent = ZERO_WIDTH;

    let n = line.firstChild;
    while (n) {
        const len = n.textContent.length;
        if (charOffset <= len) {
            range.setStart(n, charOffset);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
            return;
        } else charOffset -= len;
        n = n.nextSibling;
    }
    range.selectNodeContents(line);
    range.collapse(false);
    sel.removeAllRanges();
    sel.addRange(range);
}

function updateLineNumbers() {
    normalizeLines();
    lineNumbers.innerHTML = Array.from(editor.children).map((_, i) => i + 1).join("<br>");
    lineNumbers.scrollTop = editor.scrollTop;
}

function sanitizeEditor() {
    Array.from(editor.querySelectorAll("*")).forEach(n => {
        if (n.hasAttribute("style")) n.removeAttribute("style");
        if (n.hasAttribute("color")) n.removeAttribute("color");
        if (n.tagName === "FONT") {
            const p = n.parentNode;
            while (n.firstChild) p.insertBefore(n.firstChild, n);
            n.remove();
        } else if (!["DIV", "SPAN"].includes(n.tagName)) {
            const p = n.parentNode;
            while (n.firstChild) p.insertBefore(n.firstChild, n);
            n.remove();
        }
    });
}

editor.addEventListener("input", () => { sanitizeEditor(); normalizeLines(); updateLineNumbers(); });
editor.addEventListener("scroll", () => { lineNumbers.scrollTop = editor.scrollTop; });
editor.addEventListener("paste", (e) => {
    e.preventDefault();
    const text = (e.clipboardData || window.clipboardData).getData("text/plain") || "";
    if (!text) return;

    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);

    normalizeLines();
    let lineDiv = getLineForRange(range);
    const offset = getCaretOffset(lineDiv, range);
    const fullText = lineDiv.textContent || "";
    let before = fullText.substring(0, offset);
    let after = fullText.substring(offset);

    const parent = editor;
    let referenceNode = lineDiv.nextSibling;

    if (offset === 0 && fullText === ZERO_WIDTH) {
        lineDiv.remove();
        referenceNode = parent.firstChild;
        before = "";
    } else {
        lineDiv.textContent = before || ZERO_WIDTH;
    }

    const lines = text.split(/\r?\n/);
    let lastInserted = null;
    lines.forEach(line => {
        const d = createLine(line);
        if (referenceNode) parent.insertBefore(d, referenceNode);
        else parent.appendChild(d);
        lastInserted = d;
    });

    if (after) {
        const afterDiv = createLine(after);
        if (referenceNode) parent.insertBefore(afterDiv, referenceNode);
        else parent.appendChild(afterDiv);
        lastInserted = afterDiv;
    }

    requestAnimationFrame(() => {
        placeCaret(lastInserted, 0);
        sanitizeEditor();
        normalizeLines();
        updateLineNumbers();
    });
});

editor.addEventListener("keydown", e => {
    if (e.key !== "Enter") return;
    e.preventDefault();

    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    let lineDiv = getLineForRange(range);
    const offset = getCaretOffset(lineDiv, range);
    const text = lineDiv.textContent;
    lineDiv.textContent = text.substring(0, offset) || ZERO_WIDTH;
    const newLine = createLine(text.substring(offset));
    editor.insertBefore(newLine, lineDiv.nextSibling || null);

    requestAnimationFrame(() => {
        placeCaret(newLine, 0);
        sanitizeEditor();
        updateLineNumbers();
    });
});

editor.addEventListener("keydown", e => {
    if (e.key !== "Tab") return;
    e.preventDefault();

    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    const text = range.toString();

    if (text.includes("\n")) {
        let lineDiv = getLineForRange(range);
        const offset = getCaretOffset(lineDiv, range);
        const before = lineDiv.textContent.substring(0, offset);
        const after = lineDiv.textContent.substring(offset + text.length);
        const indentedLines = text.split("\n").map(l => "\t" + l);
        const frag = document.createDocumentFragment();

        frag.appendChild(createLine(before));
        indentedLines.forEach(l => frag.appendChild(createLine(l)));
        frag.appendChild(createLine(after));
        editor.replaceChild(frag, lineDiv);

        placeCaret(frag.lastChild, frag.lastChild.textContent.length);
    } else {
        const tn = document.createTextNode("\t");
        range.insertNode(tn);
        range.setStartAfter(tn);
        range.collapse(true);
        const sel2 = window.getSelection();
        sel2.removeAllRanges();
        sel2.addRange(range);
    }

    sanitizeEditor();
    normalizeLines();
    updateLineNumbers();
});

normalizeLines();
sanitizeEditor();
updateLineNumbers();
editor.focus();
