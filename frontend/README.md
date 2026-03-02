# Brev (Breviary) — Frontend

<p align="center">
    <img src="public/background/readmebanner.svg" alt="Brev Logo" width="6000" />
</p>

<p align="center">
    <b>A general-purpose imperative programming language for learning and structured problem-solving wrapped in a medieval liturgical theme.</b>
    <br/>
    <sub>Write programs like a ritual: readable, deterministic, and supported by precise diagnostics.</sub>
</p>

## Frontend (React + Vite)

This folder contains the **Brev Compiler UI**:
- Code editor (BrevEditor / Monaco, if you’re using it)
- Buttons to run Lexical / Syntax / Semantic analysis
- Token table + output terminal panel
- Sends requests to the backend API endpoints (e.g., `/api/lex`, `/api/syntax`, `/api/sem`)

---

## Requirements
- Node.js (LTS recommended)
- npm (or pnpm/yarn)

---

## Run locally

```bash
cd frontend
npm install
npm run dev