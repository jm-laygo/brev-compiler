from flask import Flask, request, jsonify, send_from_directory
from backend.lexer.lexer import Lexer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_JS_DIR = os.path.join(BASE_DIR, "backend", "js")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/frontend")

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "lexical.html")

@app.route('/backend/js/<path:filename>')
def backend_js(filename):
    return send_from_directory(BACKEND_JS_DIR, filename)

@app.route("/api/lex", methods=["POST"])
def lex_handler():
    data = request.json
    code = data.get("source_code", "")
    lexer = Lexer(code)
    try:
        tokens, errors = lexer.make_tokens()
        return jsonify({
            "tokens": [t.to_dict() for t in tokens],
            "errors": [e.as_string() for e in errors]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/output", methods=["POST"])
def output_handler():
    return jsonify({"output": "Program executed (parser not implemented yet)."})

if __name__ == "__main__":
    app.run(debug=True)
