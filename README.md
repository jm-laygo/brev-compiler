# Brev (Breviary)

<p align="center">
  <img src="frontend\public\background\readmebanner.svg" alt="Brev Logo" width="6000" />
</p>

<p align="center">
  <b>A general-purpose imperative programming language for learning and structured problem-solving wrapped in medieval liturgical theme.</b>
  <br/>
  <sub>Write programs like a ritual: readable, deterministic, and supported by precise diagnostics.</sub>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#language-highlights">Highlights</a> •
  <a href="#tooling--compiler-pipeline">Compiler Pipeline</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#license">License</a> •
</p>

---

## Overview

**Brev**, short for **Breviary**, is a **general-purpose imperative programming language** designed for learning and structured problem-solving while blending the practical power of computation with the thematic elements of medieval religious tradition.

Inspired by the structure and solemnity of Catholic liturgical texts, **Brev transforms coding into a ceremonial and narrative experience** without sacrificing clarity or correctness. Every construct, reserved word, and operation is named to evoke the mystique of sacred rituals, ecclesiastical decrees, and divine judgment—giving the programmer the feeling of performing a “prayer” as they craft their programs.

Brev prioritizes **readable structure**, **deterministic behavior**, and **consistent rules**, with diagnostics that report errors using **line and column positions** to support debugging and learning. Keywords in Brev are **reserved** and cannot be used as identifiers, and whitespace is generally insignificant except for separating tokens. The language includes fundamental features such as typed declarations, expressions, assignments, control flow, and functions with a required entry point. Advanced features like concurrency or extensive libraries are considered out of scope unless defined later in the specification.

---

## Language Highlights

- **Learning-first design**: strict structure.
- **Deterministic execution**: predictable rules and behavior.
- **Precise diagnostics**: errors include **line** and **column** for fast debugging.
- **Reserved keywords**: cannot be used as identifiers.
- **Whitespace-insignificant**: whitespace is only used to separate tokens.
- **Core imperative features**:
  - typed declarations
  - expressions & assignments
  - control flow (conditional branches, loops if applicable)
  - functions
  - required entry point

---

## Tooling & Compiler Pipeline

This repository contains the implementation of Brev’s **front-to-back language toolchain**, typically including:

1. **Lexer**  
   Converts source code into tokens (keywords, identifiers, literals, operators, symbols).

2. **Parser (LL(1) / CFG-based)**  
   Validates syntax using a formal grammar (FIRST/FOLLOW/PREDICT sets if applicable).

3. **Semantic Analysis**  
   Performs checks such as:
   - declaration rules / ordering constraints
   - type checking
   - duplicate identifiers
   - scope rules

4. **Interpreter / Executor**
   Evaluates Brev programs according to the language rules.

---

## Getting Started

### Prerequisites
- **Python** `>= 3.10` (recommended)  
- **Node.js** `>= 18`
- Git

### Clone
```bash
git clone https://github.com/jm-laygo/brev-compiler
cd brev-compiler
```

### Backend (Python)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python server.py
```
### Frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev
```

---

Then open:
- `http://localhost:5173/`



## Usage

### Web UI
1. Paste/write Brev code in the editor
2. Run **Lexical / Syntax / Semantic**
3. Review tokens, syntax validation, semantic diagnostics, and/or output

---


## License

MIT License

Copyright (c) [2026] [Jhon Michael Laygo]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Authors / Credits

- **jm-laygo** — [GitHub](https://github.com/jm-laygo)  
- Inspiration: Medieval Catholic liturgical structure
