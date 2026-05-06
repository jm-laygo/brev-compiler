from .array_declarations import DeclarationArrayMixin
from .function_declarations import FunctionDeclarationsMixin
from .global_declarations import GlobalDeclarationsMixin
from .struct_declarations import OrderDeclarationsMixin
from .variable_declarations import VariableDeclarationsMixin


class DeclarationsMixin(
    GlobalDeclarationsMixin,
    DeclarationArrayMixin,
    OrderDeclarationsMixin,
    FunctionDeclarationsMixin,
    VariableDeclarationsMixin,
):
    pass