# Brev Compiler

<p align="center">
  <img src="frontend/public/background/readmebanner.svg" alt="Brev Compiler Banner" width="100%" />
</p>

<p align="center">
  <b>A compiler and interpreter for Brev, a general-purpose imperative programming language with a medieval liturgical naming style.</b>
  <br/>
  <sub>Built for language design, compiler construction, syntax analysis, semantic validation, and structured program execution.</sub>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#language-features">Language Features</a> •
  <a href="#compiler-pipeline">Compiler Pipeline</a> •
  <a href="#sample-code">Sample Code</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#authors--credits">Credits</a>
</p>

---

## Overview

**Brev** is a general-purpose imperative programming language designed as part of a compiler construction project. The language uses a medieval Catholic liturgical naming style for its keywords while keeping the underlying programming rules practical, structured, and deterministic.

The project includes a working compiler pipeline that performs lexical analysis, syntax analysis, semantic analysis, and interpretation. Brev supports typed declarations, constants, arrays, user-defined structures, functions, conditional statements, loops, input/output operations, expressions, and runtime execution through an interpreter.

The language is designed to demonstrate the major stages of compiler development, including tokenization, grammar-based parsing, abstract syntax tree construction, type checking, scope validation, and controlled execution.

---

## Language Features

Brev includes the following core language features:

### Program Structure

- A Brev program requires exactly one `genesis()` function as the entry point.
- Global declarations must appear before function definitions.
- Local declarations must appear before executable statements inside a function.
- Functions are declared using the `rite` keyword.
- Non-`hollow` functions return values using `dismiss`.

### Data Types

Brev supports the following primitive types:

| Brev Type | Meaning |
|---|---|
| `tally` | integer |
| `divine` | double / decimal |
| `sigil` | character |
| `scripture` | string |
| `verity` | boolean |
| `hollow` | no return value |

Boolean values use:

| Value | Meaning |
|---|---|
| `holy` | true |
| `unholy` | false |

### Constants

Constants are declared using `sacred`.

```brev
sacred tally MAX_COUNT = 10;
sacred scripture TITLE = "Brev Compiler";
sacred verity ENABLED = holy;
```

Sacred declarations must be initialized at declaration and cannot be reassigned.

### Variables and Arrays

Brev supports primitive variables, arrays, and multidimensional arrays.

```brev
tally count = 0;
divine rate = 2.50;
scripture name = "Brev";

tally scores[3] = {90, 85, 88};
tally matrix[2][3] = {
    {1, 2, 3},
    {4, 5, 6}
};
```

Array indices start at `0`. Array sizes must be compile-time constants, such as tally literals or `sacred tally` constants.

### Orders and Ordain

Brev uses `order` to define structured data types and `ordain` to create instances.

```brev
order Record {
    tally id;
    scripture name;
    verity active;
};

rite tally genesis() {
    ordain Record rec;

    rec.id = 1;
    rec.name = "Alpha";
    rec.active = holy;

    dismiss 0;
}
```

Order definitions are declared globally. Order instances are created locally using `ordain`.

### Control Flow

Brev supports conditional branching through:

- `decree` for if
- `edict` for else-if
- `absolution` for else
- `discern` for switch-like branching
- `verse` for cases
- `grace` for default case

Example:

```brev
decree(score >= 75) {
    proclaim("Passed");
} edict(score >= 50) {
    proclaim("Needs review");
} absolution {
    proclaim("Failed");
}
```

### Loops

Brev supports three loop structures:

| Keyword | Meaning |
|---|---|
| `procession` | for loop |
| `endure` | while loop |
| `ritual` | do-while loop |

Example:

```brev
procession(tally i = 0; i < 5; i++) {
    proclaim(i);
}

endure(count < 10) {
    count++;
}

ritual {
    count--;
} endure(count > 0);
```

Loop control statements:

| Keyword | Meaning |
|---|---|
| `proceed` | continue |
| `absolve` | break |
| `fall` | fall-through inside `discern` verse |

### Input and Output

Brev uses:

| Keyword | Purpose |
|---|---|
| `receive` | input |
| `proclaim` | output |

```brev
tally age;

proclaim("Enter age:");
receive(age);

proclaim("Age:", age);
```

### Operators

Brev supports:

- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`
- Relational: `>`, `<`, `>=`, `<=`
- Equality: `==`, `!=`
- Logical: `&&`, `||`, `!!`
- Increment/decrement: `++`, `--`
- String concatenation: `&`
- Member access: `.`
- Indexing: `[]`
- String length: `verseof()`

---

## Compiler Pipeline

The Brev compiler follows a staged pipeline. Each stage receives the result of the previous stage, validates a specific part of the program, and prepares the program for the next level of analysis.

---

### 1. Lexical Analysis

<p align="left">
  <img src="frontend/public/images/lexical_analyzer_window.svg" alt="Lexical Analyzer Window" width="520" height="500" />
</p>

The lexical analyzer, or lexer, reads the raw Brev source code and converts it into a stream of tokens. Tokens are the smallest meaningful units of the program, such as keywords, identifiers, literals, operators, and symbols.

**Main responsibilities:**

- Recognizes reserved words such as `rite`, `genesis`, `sacred`, `decree`, `procession`, and `proclaim`.
- Identifies primitive data types such as `tally`, `divine`, `sigil`, `scripture`, and `verity`.
- Detects identifiers, numeric literals, character literals, string literals, and boolean values.
- Tokenizes operators such as `+`, `-`, `*`, `/`, `%`, `**`, `=`, `==`, `&&`, `||`, and `!!`.
- Handles delimiters such as parentheses, brackets, braces, commas, colons, and semicolons.
- Skips whitespace and comments while preserving accurate line and column tracking.
- Reports lexical errors such as invalid symbols, malformed literals, unclosed strings, unclosed comments, and overlong identifiers.

**Output of this stage:**

```text
Source Code → Token Stream
```

The token stream is passed to the syntax analyzer.

---

### 2. Syntax Analysis

<p align="center">
  <img src="frontend/public/images/syntax_analyzer_window.svg" alt="Syntax Analyzer Window" width="520" />
</p>

The syntax analyzer, or parser, checks whether the token stream follows the formal grammar of Brev. This stage validates the structure of the program before any deeper meaning is checked.

Brev uses an LL(1)-style parsing approach supported by CFG productions, FIRST sets, FOLLOW sets, and PREDICT sets. The parser also constructs the abstract syntax tree used by semantic analysis and interpretation.

**Main responsibilities:**

- Validates the required program structure and the `genesis()` entry point.
- Checks global declarations, function definitions, local declarations, and statement order.
- Ensures declarations, assignments, function calls, loops, and conditionals follow the grammar.
- Validates required symbols such as semicolons, parentheses, brackets, braces, and commas.
- Parses expressions according to precedence rules for arithmetic, relational, equality, logical, unary, and postfix operations.
- Rejects structurally invalid code before semantic analysis begins.

**Examples of syntax-level checks:**

```brev
sacred tally LIMIT = 10;

rite tally genesis() {
    tally x = 0;
    dismiss 0;
}
```

The parser ensures that the code is structurally valid, but it does not yet decide whether every operation is semantically meaningful. That responsibility belongs to the semantic analyzer.

**Output of this stage:**

```text
Token Stream → Abstract Syntax Tree
```

---

### 3. Semantic Analysis

<p align="center">
  <img src="frontend/public/images/semantic_analyzer_window.svg" alt="Semantic Analyzer Window" width="520" />
</p>

The semantic analyzer checks whether a syntactically valid Brev program follows the meaning and type rules of the language. This stage catches errors that cannot be fully detected by grammar alone.

**Main responsibilities:**

- Validates declarations and prevents duplicate identifiers in the same scope.
- Checks that identifiers are declared before they are used.
- Enforces type compatibility in assignments, expressions, function calls, and return statements.
- Ensures `sacred` constants are initialized and cannot be reassigned.
- Validates array dimensions, array initializers, and constant out-of-bounds indices.
- Checks that `order` definitions and `ordain` instances are used correctly.
- Rejects invalid operations such as comparing order instances directly.
- Validates condition expressions for `decree`, `edict`, `procession`, `endure`, and `ritual`.
- Checks loop-control and discern-control statements such as `proceed`, `absolve`, and `fall`.
- Ensures non-`hollow` functions return compatible values using `dismiss`.

**Examples of semantic-level checks:**

```brev
sacred tally LIMIT = 3;

rite tally genesis() {
    tally nums[LIMIT];
    nums[0] = 10;
    dismiss 0;
}
```

The syntax may be correct, but the semantic analyzer verifies whether the types, scopes, constants, arrays, and control-flow rules are valid according to the Brev specification.

**Output of this stage:**

```text
Abstract Syntax Tree → Validated Program
```

---

### 4. Interpretation

After a program passes lexical, syntax, and semantic analysis, the interpreter executes it.

**Main responsibilities:**

- Executes statements in program order.
- Evaluates expressions and assignments.
- Manages global and local scopes.
- Handles function calls and return values.
- Processes arrays, orders, and member access.
- Runs conditionals, loops, and discern blocks.
- Produces output through `proclaim` and handles input through `receive`.

**Output of this stage:**

```text
Validated Program → Runtime Output
```

---

## Sample Code

```brev
sacred tally LIMIT = 3;

order Record {
    tally id;
    scripture name;
    verity active;
};

rite tally add(tally a, tally b) {
    tally result = 0;

    result = a + b;

    dismiss result;
}

rite tally genesis() {
    ordain Record rec;
    tally total = 0;
    tally i = 0;

    rec.id = 1;
    rec.name = "Archive";
    rec.active = holy;

    procession(tally index = 0; index < LIMIT; index++) {
        total += add(index, rec.id);
    }

    decree(rec.active) {
        proclaim(rec.name, total);
    } absolution {
        proclaim("Inactive record");
    }

    dismiss 0;
}
```

---

## Project Structure

```text
brev-compiler/
├── backend/
│   ├── lexer/
│   ├── parser/
│   ├── semantic/
│   ├── interpreter/
│   ├── ast/
│   ├── tokens.py
│   └── server.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
│
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.10 or later
- Node.js 18 or later
- Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jm-laygo/brev-compiler
cd brev-compiler
```

### 2. Set Up the Backend

```bash
python -m venv .venv
```

Activate the virtual environment.

For Windows:

```bash
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend server:

```bash
python server.py
```

### 3. Set Up the Frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173/
```

---

## Usage

Through the web interface, users can:

1. Write or paste Brev source code.
2. Run lexical analysis.
3. Run syntax analysis.
4. Run semantic analysis.
5. Execute valid Brev programs.
6. View tokens, diagnostics, and output.

The compiler reports errors with line and column information to make debugging easier.

---

## Example Diagnostics

Example syntax error:

```text
Ln 4, Col 12 Syntax Error: Expected ; but found identifier.
```

Example semantic error:

```text
Ln 8, Col 5 Semantic Error: Cannot assign scripture to tally.
```

---

## Current Scope

Brev currently focuses on the core requirements of a compiler construction project:

- lexical analysis
- LL(1)-style parsing
- semantic checking
- AST-based interpretation
- structured language documentation
- web-based compiler interface

Advanced runtime libraries, concurrency, optimization, and machine-code generation are outside the current scope.

---

## License

MIT License

Copyright (c) 2026 Jhon Michael Laygo

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

- **Jhon Michael Laygo** — [GitHub](https://github.com/jm-laygo)
- Language theme inspired by medieval Catholic liturgical terminology
- Blizzard Entertainment for its human user interface border
- Paradox Interactive for its medieval icons
- Built as a compiler construction project for Brev
