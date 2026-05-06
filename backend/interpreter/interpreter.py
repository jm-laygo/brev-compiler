from __future__ import annotations
from typing import Dict, List

from backend.ast.ast_nodes import *
from backend.errors import RuntimeErrorBase
from backend.interpreter.environment import Environment
from backend.interpreter.input_request import InputRequest
from backend.interpreter.runtime.output_writer import bindOutputMethods
from backend.interpreter.runtime.type_conversion import bindCoercionMethods
from backend.interpreter.runtime.program_runner import bindProgramMethods
from backend.interpreter.runtime.functions import bindFunctionMethods
from backend.interpreter.runtime.statements import bindStatementMethods
from backend.interpreter.runtime.expressions import bindExpressionMethods
from backend.interpreter.runtime.declarations import bindDeclarationMethods
from backend.interpreter.runtime.references import bindReferenceMethods
from backend.interpreter.runtime.input_conversion import bindInputConversionMethods


class Interpreter:
    def __init__(self, *, inputProvider=None):
        self.globalEnvironment = Environment()
        self.outputLines: List[str] = []
        self.riteDeclarations: Dict[str, RiteDeclaration] = {}
        self.orderDeclarations: Dict[str, OrderDeclaration] = {}
        self.inputProvider = inputProvider or self.defaultInputProvider
        self.currentLine = ""

bindOutputMethods(Interpreter)
bindCoercionMethods(Interpreter)
bindProgramMethods(Interpreter)
bindFunctionMethods(Interpreter)
bindStatementMethods(Interpreter)
bindExpressionMethods(Interpreter)
bindDeclarationMethods(Interpreter)
bindReferenceMethods(Interpreter)
bindInputConversionMethods(Interpreter)

def runInterpreter(programNode, *, inputProvider=None):
    interpreter = Interpreter(inputProvider=inputProvider)

    try:
        executionResult = interpreter.run(programNode)
        interpreter.flushOutput()

        return {
            "result": executionResult,
            "output": list(interpreter.outputLines),
        }

    except InputRequest as inputRequest:
        interpreter.flushOutput()
        inputRequest.interpreterOutput = list(interpreter.outputLines)

        raise

    except RuntimeErrorBase as runtimeError:
        interpreter.flushOutput()
        runtimeError.interpreterOutput = list(interpreter.outputLines)

        raise