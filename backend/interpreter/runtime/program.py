from __future__ import annotations
from backend.ast.ast_nodes import OrderDecl, SacredDecl, VarDecl, OrdainDecl, Program
from backend.errors import RuntimeErrorBase, InputConversionRuntimeError

def run(self, program_node: Program):
    self._register_program(program_node)

    entry_rite = getattr(program_node, "entry", None)
    if entry_rite is None:
        raise RuntimeErrorBase(program_node, "No entry function was found.")

    entry_rite_name = getattr(entry_rite, "name", None)
    if not entry_rite_name:
        raise RuntimeErrorBase(program_node, "Entry function has no valid name.")

    return self._call_rite(entry_rite_name, [], call_node=entry_rite)

def _default_input_provider(self, target_node=None):
    raise InputConversionRuntimeError(
        target_node,
        "Input was requested during execution, but no runtime input provider was supplied.",
    )

def _register_program(self, program_node: Program):
    global_declarations = getattr(program_node, "globals", []) or []

    for global_declaration in global_declarations:
        if isinstance(global_declaration, OrderDecl):
            self.orders[global_declaration.name] = global_declaration

    entry_rite = getattr(program_node, "entry", None)
    if entry_rite is not None:
        self.rites[entry_rite.name] = entry_rite

    function_rites = getattr(program_node, "functions", []) or []
    for function_rite in function_rites:
        self.rites[function_rite.name] = function_rite

    for global_declaration in global_declarations:
        if isinstance(global_declaration, SacredDecl):
            self._exec_sacred_decl(global_declaration, self.globals)
        elif isinstance(global_declaration, VarDecl):
            self._exec_var_decl(global_declaration, self.globals)
        elif isinstance(global_declaration, OrdainDecl):
            self._exec_ordain_decl(global_declaration, self.globals)
        elif isinstance(global_declaration, OrderDecl):
            pass

def bind_program_methods(cls):
    cls.run = run
    cls._default_input_provider = _default_input_provider
    cls._register_program = _register_program