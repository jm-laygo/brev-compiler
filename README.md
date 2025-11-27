# Brev

A simple lexer for the **Brev programming language**.  
It tokenizes reserved words, identifiers, literals, and symbols, with proper error handling for invalid delimiters or oversized identifiers.

---

<!-- ## **Features**

- Recognizes **Brev reserved words**:
  - `receive`, `proclaim`, `divine`, `tally`, `sigil`, `hollow`, `verity`, etc.
- Supports **identifiers** with maximum length (`16` characters)
- Detects **invalid delimiters** and other lexical errors
- Supports basic **symbols/operators**: `+`, `-`, `*`, `/`, `%`, `&&`, `||`, `!`, `~`, parentheses, commas, etc.
- Easy **CLI testing** (type Brev code, see tokens and errors)

--- -->

## **Setup**

1. Clone or download the project

```bash
git clone <the url>
cd brev-lexer

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment
Windows (cmd): venv\Scripts\activate
Windows (PowerShell): venv\Scripts\Activate.ps1
Mac/Linux: source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt
