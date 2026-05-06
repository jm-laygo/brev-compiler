from flask import Flask, request, jsonify
import traceback
import uuid

from backend.errors import *
from backend.tokens import *
from backend.lexer.lexer import Lexer
from backend.parser.parser import Parser
from backend.semantic.semantic import runSemanticAnalysis
from backend.interpreter.interpreter import runInterpreter
from backend.interpreter.input_request import InputRequest


SKIPPED_TOKEN_TYPES = {
    TK_SYM_SPACE,
    TK_SYM_TAB,
    TK_SYM_NEWLINE,
    TK_COMMENT,
    TK_COMMENT_BLOCK,
}


def getParserTokens(tokenList):
    return [
        token
        for token in tokenList
        if token.type not in SKIPPED_TOKEN_TYPES
    ]


app = Flask(__name__)
RUNNING_SESSIONS = {}


def getOutputDelta(previousOutput, currentOutput):
    previousOutput = list(previousOutput or [])
    currentOutput = list(currentOutput or [])

    sharedLineCount = min(len(previousOutput), len(currentOutput))
    matchingLineCount = 0

    while (
        matchingLineCount < sharedLineCount
        and previousOutput[matchingLineCount] == currentOutput[matchingLineCount]
    ):
        matchingLineCount += 1

    if matchingLineCount == len(previousOutput):
        return currentOutput[matchingLineCount:]

    if (
        matchingLineCount == len(previousOutput) - 1
        and matchingLineCount < len(currentOutput)
    ):
        previousTail = previousOutput[matchingLineCount]
        currentTail = currentOutput[matchingLineCount]

        if (
            isinstance(previousTail, str)
            and isinstance(currentTail, str)
            and currentTail.startswith(previousTail)
        ):
            outputDelta = []
            tailDelta = currentTail[len(previousTail):]

            if tailDelta:
                outputDelta.extend([tailDelta])

            outputDelta.extend(currentOutput[matchingLineCount + 1:])

            return outputDelta

    return currentOutput


@app.get("/api/ping")
def ping():
    return jsonify({
        "ok": True,
        "message": "Flask API is running"
    }), 200


def analyzeSource(sourceCode):
    lexer = Lexer(sourceCode)
    tokenList, lexicalErrors = lexer.makeTokens()

    if lexicalErrors:
        return None, {
            "ok": False,
            "errors": ["Execution not performed because lexical errors exist."]
            + [error.asString() for error in lexicalErrors]
        }

    parser = Parser(getParserTokens(tokenList))
    programAst = parser.parse()

    if parser.currentType(0) != TK_EOF:
        raise ParserError(
            parser.peek(0),
            [TK_EOF],
            details="Trailing tokens"
        )

    checkedProgram, semanticErrors = runSemanticAnalysis(programAst)

    if semanticErrors:
        formattedErrors = [
            error.asString() if hasattr(error, "asString") else str(error)
            for error in semanticErrors
        ]

        return None, {
            "ok": False,
            "errors": ["Execution not performed because semantic errors exist."]
            + formattedErrors
        }

    return checkedProgram, {"ok": True}


def executeSessionUntilPause(session):
    providedInputs = list(session["inputs"])
    consumedInputIndex = 0

    def inputProvider(targetNode=None):
        nonlocal consumedInputIndex

        if consumedInputIndex < len(providedInputs):
            inputValue = providedInputs[consumedInputIndex]
            consumedInputIndex += 1

            return inputValue

        raise InputRequest(targetNode)

    try:
        result = runInterpreter(
            session["checkedProgram"],
            inputProvider=inputProvider
        )

        fullOutput = result["output"]
        deltaOutput = getOutputDelta(
            session["emittedOutput"],
            fullOutput
        )

        session["emittedOutput"] = list(fullOutput)

        return {
            "status": "finished",
            "session_id": session["id"],
            "output": deltaOutput,
            "result": result["result"],
            "errors": [],
        }

    except InputRequest as inputRequest:
        fullOutput = getattr(inputRequest, "interpreterOutput", [])
        deltaOutput = getOutputDelta(
            session["emittedOutput"],
            fullOutput
        )

        session["emittedOutput"] = list(fullOutput)

        return {
            "status": "waiting_input",
            "session_id": session["id"],
            "output": deltaOutput,
            "result": None,
            "errors": [],
        }

    except RuntimeErrorBase as runtimeError:
        fullOutput = getattr(runtimeError, "interpreterOutput", [])
        deltaOutput = getOutputDelta(
            session["emittedOutput"],
            fullOutput
        )

        session["emittedOutput"] = list(fullOutput)

        return {
            "status": "error",
            "session_id": session["id"],
            "output": deltaOutput,
            "result": None,
            "errors": [runtimeError.asString()],
        }


@app.post("/api/lex")
def apiLex():
    requestData = request.get_json(silent=True) or {}
    sourceCode = requestData.get("source_code", "")

    try:
        lexer = Lexer(sourceCode)
        tokenList, lexicalErrors = lexer.makeTokens()

        return jsonify({
            "tokens": [token.toDictionary() for token in tokenList],
            "errors": [error.asString() for error in lexicalErrors]
        }), 200

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Lexer crashed: {str(exceptionObject)}"
        }), 500


@app.post("/api/syntax")
def apiSyntax():
    requestData = request.get_json(silent=True) or {}
    sourceCode = requestData.get("source_code", "")

    try:
        lexer = Lexer(sourceCode)
        tokenList, lexicalErrors = lexer.makeTokens()

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Lexer crashed: {str(exceptionObject)}"
        }), 500

    if lexicalErrors:
        return jsonify({
            "syntax_valid": False,
            "errors": ["Syntax analysis not performed because lexical errors exist."]
            + [error.asString() for error in lexicalErrors]
        }), 200

    try:
        parser = Parser(getParserTokens(tokenList))
        parser.parse()

        if parser.currentType(0) != TK_EOF:
            raise ParserError(
                parser.peek(0),
                [TK_EOF],
                details="Trailing tokens"
            )

        return jsonify({
            "syntax_valid": True,
            "errors": []
        }), 200

    except ParserError as parserError:
        return jsonify({
            "syntax_valid": False,
            "errors": [parserError.asString()]
        }), 200

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Parser crashed: {str(exceptionObject)}"
        }), 500


@app.post("/api/sem")
def apiSemantic():
    requestData = request.get_json(silent=True) or {}
    sourceCode = requestData.get("source_code", "")

    try:
        lexer = Lexer(sourceCode)
        tokenList, lexicalErrors = lexer.makeTokens()

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Lexer crashed: {str(exceptionObject)}"
        }), 500

    if lexicalErrors:
        return jsonify({
            "semantic_valid": False,
            "errors": ["Semantic analysis not performed because lexical errors exist."]
            + [error.asString() for error in lexicalErrors]
        }), 200

    try:
        parser = Parser(getParserTokens(tokenList))
        programAst = parser.parse()

        if parser.currentType(0) != TK_EOF:
            raise ParserError(
                parser.peek(0),
                [TK_EOF],
                details="Trailing tokens"
            )

    except ParserError as parserError:
        return jsonify({
            "semantic_valid": False,
            "errors": [
                "Semantic analysis not performed because syntax errors exist.",
                parserError.asString()
            ]
        }), 200

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Parser crashed: {str(exceptionObject)}"
        }), 500

    try:
        checkedProgram, semanticErrors = runSemanticAnalysis(programAst)
        formattedErrors = []

        for semanticError in semanticErrors:
            if hasattr(semanticError, "asString"):
                formattedErrors.extend([semanticError.asString()])

            elif hasattr(semanticError, "as_string"):
                formattedErrors.extend([semanticError.as_string()])

            else:
                errorPosition = getattr(semanticError, "position", None)
                errorMessage = getattr(
                    semanticError,
                    "message",
                    str(semanticError)
                )

                if (
                    errorPosition
                    and hasattr(errorPosition, "lineNumber")
                    and hasattr(errorPosition, "columnNumber")
                ):
                    formattedErrors.extend([
                        f"Ln {errorPosition.lineNumber}, Col {errorPosition.columnNumber} Semantic Error: {errorMessage}"
                    ])

                else:
                    formattedErrors.extend([
                        f"Semantic Error: {errorMessage}"
                    ])

        return jsonify({
            "semantic_valid": len(formattedErrors) == 0,
            "errors": formattedErrors,
        }), 200

    except Exception as exceptionObject:
        return jsonify({
            "error": f"Semantic analyzer crashed: {str(exceptionObject)}"
        }), 500


@app.post("/api/run/start")
def apiRunStart():
    requestData = request.get_json(silent=True) or {}
    sourceCode = requestData.get("source_code", "")

    try:
        checkedProgram, analysisResult = analyzeSource(sourceCode)

        if not analysisResult["ok"]:
            return jsonify({
                "status": "error",
                "session_id": None,
                "output": [],
                "result": None,
                "errors": analysisResult["errors"],
            }), 200

        sessionId = str(uuid.uuid4())

        session = {
            "id": sessionId,
            "sourceCode": sourceCode,
            "checkedProgram": checkedProgram,
            "inputs": [],
            "emittedOutput": [],
        }

        RUNNING_SESSIONS[sessionId] = session
        response = executeSessionUntilPause(session)

        if response["status"] in ("finished", "error"):
            RUNNING_SESSIONS.pop(sessionId, None)

        return jsonify(response), 200

    except ParserError as parserError:
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [
                "Execution not performed because syntax errors exist.",
                parserError.asString()
            ],
        }), 200

    except Exception as exceptionObject:
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [
                f"Interpreter internal crash: {exceptionObject.__class__.__name__}"
            ],
        }), 500


@app.post("/api/run/input")
def apiRunInput():
    requestData = request.get_json(silent=True) or {}
    sessionId = requestData.get("session_id")
    inputValue = requestData.get("value", "")

    session = RUNNING_SESSIONS.get(sessionId)

    if not session:
        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": ["Runtime session expired or does not exist."],
        }), 200

    session["inputs"].extend([inputValue])

    try:
        response = executeSessionUntilPause(session)

        if response["status"] in ("finished", "error"):
            RUNNING_SESSIONS.pop(sessionId, None)

        return jsonify(response), 200

    except Exception as exceptionObject:
        traceback.print_exc()
        RUNNING_SESSIONS.pop(sessionId, None)

        return jsonify({
            "status": "error",
            "session_id": None,
            "output": [],
            "result": None,
            "errors": [
                f"Interpreter internal crash: {exceptionObject.__class__.__name__}"
            ],
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )