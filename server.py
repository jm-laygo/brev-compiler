from flask import Flask, request, jsonify

from backend.errors import *
from backend.tokens import *
from backend.lexer.lexer import Lexer
from backend.parser.parser import Parser
from backend.semantic.semantic import run_semantic
from backend.interpreter.interpreter import run_interpreter
from backend.errors import RuntimeErrorBase

SKIP_TYPES = {TK_SYM_SPACE, TK_SYM_TAB, TK_SYM_NEWLINE, TK_COMMENT, TK_COMMENT_BLOCK}

def tokens_for_parser(token_list):
    return [token for token in token_list if token.type not in SKIP_TYPES]

app = Flask(__name__)

@app.get("/api/ping")
def ping():
    return jsonify({"ok": True, "msg": "Flask API is running"}), 200

@app.post("/api/lex")
def api_lex():
    request_data = request.get_json(silent=True) or {}
    source_code = request_data.get("source_code", "")

    try:
        lexer = Lexer(source_code)
        token_list, lexer_errors = lexer.make_tokens()

        return jsonify({
            "tokens": [token.to_dict() for token in token_list],
            "errors": [error.as_string() for error in lexer_errors]
        }), 200

    except Exception as exception_obj:
        return jsonify({"error": f"Lexer crashed: {str(exception_obj)}"}), 500

@app.post("/api/syntax")
def api_syntax():
    request_data = request.get_json(silent=True) or {}
    source_code = request_data.get("source_code", "")

    try:
        lexer = Lexer(source_code)
        token_list, lexer_errors = lexer.make_tokens()

    except Exception as exception_obj:
        return jsonify({"error": f"Lexer crashed: {str(exception_obj)}"}), 500

    if lexer_errors:
        return jsonify({
            "syntax_valid": False,
            "errors": ["Syntax analysis not performed because lexical errors exist."]
                      + [error.as_string() for error in lexer_errors]
        }), 200

    try:
        parser = Parser(tokens_for_parser(token_list))
        program_ast = parser.parse()

        if parser.current_type(0) != TK_EOF:
            raise ParserError(
                parser.peek(0),
                expected=[TK_EOF],
                details="Trailing tokens"
            )

        return jsonify({
            "syntax_valid": True,
            "errors": []
        }), 200

    except ParserError as parser_error:
        return jsonify({
            "syntax_valid": False,
            "errors": [parser_error.as_string()]
        }), 200

    except Exception as exception_obj:
        return jsonify({"error": f"Parser crashed: {str(exception_obj)}"}), 500

@app.post("/api/sem")
def api_sem():
    request_data = request.get_json(silent=True) or {}
    source_code = request_data.get("source_code", "")

    try:
        lexer = Lexer(source_code)
        token_list, lexer_errors = lexer.make_tokens()

    except Exception as exception_obj:
        return jsonify({"error": f"Lexer crashed: {str(exception_obj)}"}), 500

    if lexer_errors:
        return jsonify({
            "semantic_valid": False,
            "errors": ["Semantic analysis not performed because lexical errors exist."]
                      + [error.as_string() for error in lexer_errors]
        }), 200

    try:
        parser = Parser(tokens_for_parser(token_list))
        program_ast = parser.parse()

        if parser.current_type(0) != TK_EOF:
            raise ParserError(
                parser.peek(0),
                expected=[TK_EOF],
                details="Trailing tokens"
            )

    except ParserError as parser_error:
        return jsonify({
            "semantic_valid": False,
            "errors": [
                "Semantic analysis not performed because syntax errors exist.",
                parser_error.as_string()
            ]
        }), 200

    except Exception as exception_obj:
        return jsonify({"error": f"Parser crashed: {str(exception_obj)}"}), 500

    try:
        checked_ast, semantic_errors = run_semantic(program_ast)

        formatted_errors = []

        for semantic_error in semantic_errors:
            if hasattr(semantic_error, "as_string"):
                formatted_errors.append(semantic_error.as_string())
            else:
                error_position = getattr(semantic_error, "pos", None)
                error_message = getattr(semantic_error, "message", str(semantic_error))

                if error_position and hasattr(error_position, "line") and hasattr(error_position, "col"):
                    formatted_errors.append(
                        f"Ln {error_position.line}, Col {error_position.col} Semantic Error: {error_message}"
                    )
                else:
                    formatted_errors.append(f"Semantic Error: {error_message}")

        return jsonify({
            "semantic_valid": len(formatted_errors) == 0,
            "errors": formatted_errors,
        }), 200

    except Exception as exception_obj:
        return jsonify({"error": f"Semantic analyzer crashed: {str(exception_obj)}"}), 500

@app.post("/api/run")
def api_run():
    request_data = request.get_json(silent=True) or {}
    source_code = request_data.get("source_code", "")
    runtime_inputs = request_data.get("inputs", [])

    try:
        lexer = Lexer(source_code)
        token_list, lexer_errors = lexer.make_tokens()
    except Exception as exception_obj:
        return jsonify({"error": f"Lexer crashed: {str(exception_obj)}"}), 500

    if lexer_errors:
        return jsonify({
            "ran": False,
            "output": [],
            "errors": ["Execution not performed because lexical errors exist."] + [error.as_string() for error in lexer_errors]
        }), 200

    try:
        parser = Parser(tokens_for_parser(token_list))
        program_ast = parser.parse()

        if parser.current_type(0) != TK_EOF:
            raise ParserError(
                parser.peek(0),
                expected=[TK_EOF],
                details="Trailing tokens"
            )
    except ParserError as parser_error:
        return jsonify({
            "ran": False,
            "output": [],
            "errors": [
                "Execution not performed because syntax errors exist.",
                parser_error.as_string()
            ]
        }), 200
    except Exception as exception_obj:
        return jsonify({"error": f"Parser crashed: {str(exception_obj)}"}), 500

    try:
        checked_ast, semantic_errors = run_semantic(program_ast)
        if semantic_errors:
            formatted_errors = [err.as_string() if hasattr(err, "as_string") else str(err) for err in semantic_errors]
            return jsonify({
                "ran": False,
                "output": [],
                "errors": ["Execution not performed because semantic errors exist."] + formatted_errors
            }), 200
    except Exception as exception_obj:
        return jsonify({"error": f"Semantic analyzer crashed: {str(exception_obj)}"}), 500

    inputs_queue = list(runtime_inputs)

    def input_provider(_target_node=None):
        if not inputs_queue:
            raise RuntimeErrorBase(_target_node, "receive requested input, but no runtime input was provided.")
        return inputs_queue.pop(0)

    try:
        result = run_interpreter(checked_ast, input_provider=input_provider)
        return jsonify({
            "ran": True,
            "output": result["output"],
            "result": result["result"],
            "errors": []
        }), 200
    except RuntimeErrorBase as runtime_error:
        return jsonify({
            "ran": False,
            "output": [],
            "errors": [runtime_error.as_string()]
        }), 200
    except Exception as exception_obj:
        return jsonify({"error": f"Interpreter crashed: {str(exception_obj)}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)