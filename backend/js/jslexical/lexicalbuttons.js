const openFileBtn = document.getElementById("openFileBtn");
const fileInput = document.getElementById("fileInput");
const codeArea = document.getElementById("code");

openFileBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        codeArea.value = e.target.result;
        highlight();
    };
    reader.readAsText(file);
});

document.getElementById("saveFileBtn").addEventListener("click", () => {
    const code = textarea.value;
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "brev.txt";
    a.click();
    URL.revokeObjectURL(url);
});

document.getElementById("clearBtn").addEventListener("click", () => {
    textarea.value = "";
    lineNumbers.innerHTML = "1";
    document.querySelector("#tokenTable tbody").innerHTML = "";
    term.textContent = "";
});
