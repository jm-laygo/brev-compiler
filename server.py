from flask import Flask, request, jsonify
import traceback
import uuid

from backend.errors import *
from backend.tokens import *
from backend.lexer.lexer import Lexer
from backend.parser.parser import Parser
from backend.semantic.semantic import run_semantic
from backend.interpreter.interpreter import run_interpreter
from backend.interpreter.input_request import InputRequest

SKIP_TYPES = {TK_SYM_SPACE, TK_SYM_TAB, TK_SYM_NEWLINE, TK_COMMENT, TK_COMMENT_BLOCK}


def tokens_for_parser(token_list):
    return [token for token in token_list if token.type not in SKIP_TYPES]


app = Flask(__name__)
RUN_SESSIONS = {}


@app.get("/api/ping")
def ping():
    return jsonify({"ok": True, "msg": "Flask API is running"}), 200


def analyze_source(source_code):
    lexer = Lexer(source_code)
    token_list, lexer_errors = lexer.make_tokens()

    if lexer_errors:
        return None, {
            "ok": False,
            "errors": ["Execution not performed because lexical errors exist."] +
                      [error.as_string() for error in lexer_errors]
        }

    parser = Parser(tokens_for_parser(token_list))
    program_ast = parser.parse()

    if parser.current_type(0) != TK_EOF:
        raise ParserError(
            parser.peek(0),
            expected=[TK_EOF],
            details="Trailing tokens"
        )

    checked_ast, semantic_errors = run_semantic(program_ast)
    if semantic_errors:
        formatted_errors = [
            err.as_string() if hasattr(err, "as_string") else str(err)
            for err in semantic_errors
        ]
        return None, {
            "ok": False,
            "errors": ["Execution not performed because semantic errors exist."] + formatted_errors
        }

    return checked_ast, {"ok": True}


def execute_session_until_pause(session):
    provided_inputs = list(session["inputs"])
    consumed_index = 0

    def input_provider(_target_node=None):
        nonlocal consumed_index
        if consumed_index < len(provided_inputs):
            value = provided_inputs[consumed_index]
            consumed_index += 1
            return value
        raise InputRequest(_target_node)

    try:
        result = run_interpreter(session["checked_ast"], input_provider=input_provider)
        full_output = result["output"]
        old_len = session["emitted_output_len"]
        delta_output = full_output[old_len:]
        session["emitted_output_len"] = len(full_output)

        return {
            "status": "finished",
            "session_id": session["id"],
            "output": delta_output,
            "result": result["result"],
            "errors": [],
        }

    except InputRequest as input_request:
        full_output = getattr(input_request, "interpreter_output", [])
        old_len = session["emitted_output_len"]
        delta_output = full_output[old_len:]
        session["emitted_output_len"] = len(full_output)

        return {
            "status": "waiting_input",
            "session_id": session["id"],
            "output": delta_output,
            "result": None,
            "errors": [],
        }

    except RuntimeErrorBase as runtime_error:
        full_output = getattr(runtime_error, "interpreter_output", [])
        old_len = session["emitted_output_len"]
        delta_output = full_output[old_len:]
        session["emitted_output_len"] = len(full_output)

        return {
            "status": "error",
            "session_id": session["id"],
            "output": delta_output,
            "result": None,
            "errors": [runtime_error.as_string()],
        }


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


@app.post("/api/run/start")
def api_run_start():
    request_data = request.get_json(silent=True) or {}
    source_code = request_data.get("source_code", "")

    try:
        checked_ast, analysis = analyze_source(source_code)
        if not analysis["ok"]:
            return jsonify({
                "status": "error",
                "session_id": None,
                "output": [],
                "result": None,
                "errors": analysis["errors"],
            }), 200

        session_id = str(uuid.uuid4())
        session = {
            "id": session_id,
            "source_code": source_code,
            "checked_ast": checked_ast,
            "inputs": [],
            "emitted_output_len": 0,
        }
        RUN_SESSIONS[session_id] = session

        response = execute_session_until_pause(session)

        if response["status"] in ("finished", "error"):
            RUN_SESSIONS.pop(session_id, None)

        return jsonify(response), 200

    except ParserError as parser_error:
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [
                "Execution not performed because syntax errors exist.",
                parser_error.as_string()
            ],
        }), 200

    except Exception as exception_obj:
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [f"Interpreter internal crash: {exception_obj.__class__.__name__}"],
        }), 500


@app.post("/api/run/input")
def api_run_input():
    request_data = request.get_json(silent=True) or {}
    session_id = request_data.get("session_id")
    value = request_data.get("value", "")

    session = RUN_SESSIONS.get(session_id)
    if not session:
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": ["Runtime session expired or does not exist."],
        }), 200

    session["inputs"].append(value)

    try:
        response = execute_session_until_pause(session)

        if response["status"] in ("finished", "error"):
            RUN_SESSIONS.pop(session_id, None)

        return jsonify(response), 200

    except Exception as exception_obj:
        traceback.print_exc()
        RUN_SESSIONS.pop(session_id, None)
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [f"Interpreter internal crash: {exception_obj.__class__.__name__}"],
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)