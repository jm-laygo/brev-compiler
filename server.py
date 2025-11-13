from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from lexer import Lexer
import io
import contextlib
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# --- Serve index.html ---
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# --- Lexical Analyzer Route ---
@app.route('/api/lex', methods=['POST'])
def lexical_analysis():
    data = request.get_json()
    source_code = data.get('source_code', '')

    lexer = Lexer(source_code)
    tokens, errors = lexer.make_tokens()

    token_list = [
        {"type": t.type, "value": t.value, "line": t.line} for t in tokens
    ]

    return jsonify({
        "tokens": token_list,
        "errors": [e.as_string() for e in errors]
    })


# --- Run Program Route ---
@app.route('/api/output', methods=['POST'])
def run_program():
    data = request.get_json()
    source_code = data.get('source_code', '')

    try:
        output_buffer = io.StringIO()
        local_vars = {}

        with contextlib.redirect_stdout(output_buffer):
            exec(source_code, {}, local_vars)

        printed_output = output_buffer.getvalue()
        output_buffer.close()

        vars_output = "\n".join(f"{k} = {v}" for k, v in local_vars.items())
        final_output = printed_output + vars_output

        return jsonify({"output": final_output or "✅ Program finished successfully."})
    except Exception as e:
        return jsonify({"output": f"❌ Runtime Error: {str(e)}"}), 400


if __name__ == '__main__':
    print("🚀 Server running on http://127.0.0.1:5000")
    app.run(debug=True)
