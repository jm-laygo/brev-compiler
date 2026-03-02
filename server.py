from flask import Flask, request, jsonify
from backend.errors import *
from backend.tokens import *
from backend.lexer.lexer import Lexer
from backend.parser.parser import parse_ast
from backend.semantic.semantic import run_semantic

SKIP_TYPES = {TK_SYM_SPACE, TK_SYM_TAB, TK_SYM_NEWLINE, TK_COMMENT, TK_COMMENT_BLOCK}

def tokens_for_parser(tokens):
    return [t for t in tokens if t.type not in SKIP_TYPES]

app = Flask(__name__)

@app.get("/api/ping")
def ping():
    return jsonify({"ok": True, "msg": "Flask API is running"}), 200

@app.post("/api/lex")
def api_lex():
    data = request.get_json(silent=True) or {}
    code = data.get("source_code", "")

    try:
        lexer = Lexer(code)
        tokens, errors = lexer.make_tokens()
        return jsonify({
            "tokens": [t.to_dict() for t in tokens],
            "errors": [e.as_string() for e in errors]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Lexer crashed: {str(e)}"}), 500

@app.post("/api/syntax")
def api_syntax():
    data = request.get_json(silent=True) or {}
    code = data.get("source_code", "")

    try:
        lexer = Lexer(code)
        tokens, lex_errors = lexer.make_tokens()
    except Exception as e:
        return jsonify({"error": f"Lexer crashed: {str(e)}"}), 500

    if lex_errors:
        return jsonify({
            "syntax_valid": False,
            "errors": ["Syntax analysis not performed because lexical errors exist."]
                      + [e.as_string() for e in lex_errors]
        }), 200

    try:
        parse_ast(tokens_for_parser(tokens))
        return jsonify({"syntax_valid": True, "errors": []}), 200
    except ParserError as e:
        return jsonify({"syntax_valid": False, "errors": [e.as_string()]}), 200
    except Exception as e:
        return jsonify({"error": f"Parser crashed: {str(e)}"}), 500

@app.post("/api/sem")
def api_sem():
    data = request.get_json(silent=True) or {}
    code = data.get("source_code", "")

    try:
        lexer = Lexer(code)
        tokens, lex_errors = lexer.make_tokens()
    except Exception as e:
        return jsonify({"error": f"Lexer crashed: {str(e)}"}), 500

    if lex_errors:
        return jsonify({
            "semantic_valid": False,
            "stage": "lex",
            "errors": [e.as_string() for e in lex_errors],
        }), 200

    try:
        ast = parse_ast(tokens_for_parser(tokens))
    except ParserError as e:
        return jsonify({
            "semantic_valid": False,
            "stage": "syntax",
            "errors": [e.as_string()],
        }), 200
    except Exception as e:
        return jsonify({"error": f"Parser crashed: {str(e)}"}), 500

    try:
        sem_result = run_semantic(ast)
        sem_errors = sem_result.errors or []
        return jsonify({
            "semantic_valid": len(sem_errors) == 0,
            "stage": "semantic",
            "errors": [err.as_string() if hasattr(err, "as_string") else str(err) for err in sem_errors],
        }), 200
    except Exception as e:
        return jsonify({"error": f"Semantic crashed: {str(e)}"}), 500

@app.post("/api/tac")
def tac_placeholder():
    return jsonify({"errors": ["Codegen not wired yet"], "tac": []}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)