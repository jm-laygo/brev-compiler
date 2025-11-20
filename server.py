from flask import Flask, request, jsonify, send_from_directory
from lexer.lexer import Lexer
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


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
