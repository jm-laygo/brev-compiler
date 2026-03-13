from .arrays import DeclarationArrayMixin
from .functions import FunctionDeclarationsMixin
from .globals import GlobalDeclarationsMixin
from .orders import OrderDeclarationsMixin
from .variables import VariableDeclarationsMixin


class DeclarationsMixin(
    GlobalDeclarationsMixin,
    DeclarationArrayMixin,
    OrderDeclarationsMixin,
    FunctionDeclarationsMixin,
    VariableDeclarationsMixin,
):
    pass