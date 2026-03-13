from .arrays import ArrayInitializerMixin
from .ordain import OrdainInitializerMixin
from .sacred import SacredInitializerMixin
from .variables import VariableInitializerMixin


class InitializersMixin(
    SacredInitializerMixin,
    OrdainInitializerMixin,
    VariableInitializerMixin,
    ArrayInitializerMixin,
):
    pass