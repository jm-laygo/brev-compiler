from __future__ import annotations
from typing import Dict, List
from backend.ast.ast_nodes import *
from backend.errors import RuntimeErrorBase
from backend.interpreter.environment import Environment
from backend.interpreter.input_request import InputRequest
from backend.interpreter.runtime.output import bind_output_methods
from backend.interpreter.runtime.coercion import bind_coercion_methods
from backend.interpreter.runtime.program import bind_program_methods
from backend.interpreter.runtime.functions import bind_function_methods
from backend.interpreter.runtime.statements import bind_statement_methods
from backend.interpreter.runtime.expressions import bind_expression_methods
from backend.interpreter.runtime.declarations import bind_declaration_methods
from backend.interpreter.runtime.references import bind_reference_methods
from backend.interpreter.runtime.input_conversion import bind_input_conversion_methods

class Interpreter:
    def __init__(self, *, input_provider=None):
        self.globals = Environment()
        self.output: List[str] = []
        self.rites: Dict[str, RiteDecl] = {}
        self.orders: Dict[str, OrderDecl] = {}
        self.input_provider = input_provider or self._default_input_provider

        self.output = []
        self.current_line = ""

bind_output_methods(Interpreter)
bind_coercion_methods(Interpreter)
bind_program_methods(Interpreter)
bind_function_methods(Interpreter)
bind_statement_methods(Interpreter)
bind_expression_methods(Interpreter)
bind_declaration_methods(Interpreter)
bind_reference_methods(Interpreter)
bind_input_conversion_methods(Interpreter)

def run_interpreter(program_node, *, input_provider=None):
    interpreter = Interpreter(input_provider=input_provider)

    try:
        execution_result = interpreter.run(program_node)
        interpreter._flush_output()
        return {
            "result": execution_result,
            "output": list(interpreter.output),
        }
    except InputRequest as input_request:
        interpreter._flush_output()
        input_request.interpreter_output = list(interpreter.output)
        raise
    except RuntimeErrorBase as runtime_error:
        interpreter._flush_output()
        runtime_error.interpreter_output = list(interpreter.output)
        raise