from .array_initializers import ArrayInitializerMixin
from .struct_initializers import OrdainInitializerMixin
from .constant_initializers import SacredInitializerMixin
from .variable_initializers import VariableInitializerMixin


class InitializersMixin(
    SacredInitializerMixin,
    OrdainInitializerMixin,
    VariableInitializerMixin,
    ArrayInitializerMixin,
):
    pass