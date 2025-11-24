const editor = document.getElementById("code");
const lineNumbers = document.getElementById("lineNumbers");

function getEditorLines() {
    let html = editor.innerHTML || "";

    html = html.replace(/\r/g, "");
    html = html.replace(/<div><br><\/div>/gi, '\n');
    html = html.replace(/<div>/gi, '\n');
    html = html.replace(/<\/div>/gi, '');
    html = html.replace(/<br\s*\/?>/gi, '\n');

    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    const text = tmp.textContent || tmp.innerText || '';
    let lines = text.split('\n');

    if (lines.length > 1 && lines[lines.length - 1] === "") {
        lines.pop();
    }

    return lines;
}

function updateLineNumbers() {
    const lines = getEditorLines();
    let html = "";
    for (let i = 1; i <= lines.length; i++) {
        html += i + "<br>";
    }
    lineNumbers.innerHTML = html;
}

function updateLines() {
    updateLineNumbers();
    syncScroll();
}

function syncScroll() {
    lineNumbers.scrollTop = editor.scrollTop;
}

function sanitizeEditorNodes() {
    const walker = document.createTreeWalker(editor, NodeFilter.SHOW_ELEMENT, null);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    for (const n of nodes) {
        if (n.hasAttribute && n.hasAttribute('style')) n.removeAttribute('style');
        if (n.hasAttribute && n.hasAttribute('color')) n.removeAttribute('color');
        if (n.nodeName === 'FONT') {
            const parent = n.parentNode;
            while (n.firstChild) parent.insertBefore(n.firstChild, n);
            parent.removeChild(n);
        }
    }
}

editor.addEventListener('paste', (e) => {
    e.preventDefault();
    const clipboardData = (e.clipboardData || window.clipboardData);
    const text = clipboardData.getData('text/plain');

    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    range.deleteContents();
    const node = document.createTextNode(text);
    range.insertNode(node);

    range.setStartAfter(node);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);

    sanitizeEditorNodes();
    updateLines();
});

editor.addEventListener("input", () => {
    sanitizeEditorNodes();
    updateLines();
});
editor.addEventListener("scroll", syncScroll);

editor.addEventListener("keydown", function(e) {
    if (e.key === "Tab") {
        e.preventDefault();

        const sel = window.getSelection();
        if (!sel.rangeCount) return;
        const range = sel.getRangeAt(0);
        const selectedText = range.toString();

        if (selectedText.includes("\n")) {
            const lines = selectedText.split("\n");
            const indentedText = lines.map(line => "\t" + line).join("\n");

            range.deleteContents();
            const textNode = document.createTextNode(indentedText);
            range.insertNode(textNode);
            range.setStartAfter(textNode);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        } else {
            const tabNode = document.createTextNode("\t");
            range.insertNode(tabNode);

            range.setStartAfter(tabNode);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        }

        sanitizeEditorNodes();
        updateLines();
    }
});

function escapeHtml(unsafe) {
    return (unsafe + '')
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

updateLines();
