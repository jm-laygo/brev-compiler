from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Union

class BaseType(str, Enum):
    TALLY = "tally"
    DIVINE = "divine"
    SIGIL = "sigil"
    SCRIPTURE = "scripture"
    VERITY = "verity"
    HOLLOW = "hollow"
    UNKNOWN = "unknown"
    ERROR = "error"

@dataclass(frozen=True)
class Type:
    base: BaseType = BaseType.UNKNOWN
    array_of: Optional["Type"] = None
    order_name: Optional[str] = None

    @staticmethod
    def base_t(name: Union[str, BaseType]) -> "Type":
        if isinstance(name, BaseType):
            return Type(base=name)
        n = (name or "").lower()
        mapping = {
            "tally": BaseType.TALLY,
            "divine": BaseType.DIVINE,
            "sigil": BaseType.SIGIL,
            "scripture": BaseType.SCRIPTURE,
            "verity": BaseType.VERITY,
            "hollow": BaseType.HOLLOW,
        }
        return Type(base=mapping.get(n, BaseType.UNKNOWN))

    @staticmethod
    def array(elem: "Type", dims: int = 1) -> "Type":
        t = elem
        for _ in range(max(0, dims)):
            t = Type(base=BaseType.UNKNOWN, array_of=t)
        return t

    @staticmethod
    def order(name: str) -> "Type":
        return Type(base=BaseType.UNKNOWN, order_name=name)

    @staticmethod
    def unknown() -> "Type":
        return Type(base=BaseType.UNKNOWN)

    @staticmethod
    def error() -> "Type":
        return Type(base=BaseType.ERROR)

    def is_array(self) -> bool:
        return self.array_of is not None

    def is_order(self) -> bool:
        return self.order_name is not None

    def is_base(self, b: BaseType) -> bool:
        return self.array_of is None and self.order_name is None and self.base == b

    def __str__(self) -> str:
        if self.base == BaseType.ERROR:
            return "type-error"
        if self.is_array():
            # count dims
            dims = 0
            t = self
            while t.array_of is not None:
                dims += 1
                t = t.array_of
            return f"{t}[{dims}]"
        if self.is_order():
            return f"order {self.order_name}"
        return self.base.value

def is_numeric(t: Type) -> bool:
    return t.is_base(BaseType.TALLY) or t.is_base(BaseType.DIVINE)

def is_bool(t: Type) -> bool:
    return t.is_base(BaseType.VERITY)

def is_string(t: Type) -> bool:
    return t.is_base(BaseType.SCRIPTURE)

def is_char(t: Type) -> bool:
    return t.is_base(BaseType.SIGIL)

def promote_numeric(a: Type, b: Type) -> Type:
    if a.is_base(BaseType.DIVINE) or b.is_base(BaseType.DIVINE):
        return Type.base_t(BaseType.DIVINE)
    return Type.base_t(BaseType.TALLY)

def same_type(a: Type, b: Type) -> bool:
    return str(a) == str(b)

def can_assign(dst: Type, src: Type) -> bool:
    if dst.base == BaseType.ERROR or src.base == BaseType.ERROR:
        return True

    if same_type(dst, src):
        return True

    if is_numeric(dst) and is_numeric(src):
        return True

    if dst.is_base(BaseType.SCRIPTURE) and src.is_base(BaseType.SIGIL):
        return True
    
    if dst.is_array() and src.is_array():
        d = dst
        s = src
        while d.is_array() and s.is_array():
            d = d.array_of
            s = s.array_of
        if d.is_array() or s.is_array():
            return False
        return can_assign(d, s)

    return False

def can_concat(a: Type, b: Type, allow_coerce: bool = True) -> bool:
    if a.base == BaseType.ERROR or b.base == BaseType.ERROR:
        return True

    if is_string(a) and is_string(b):
        return True

    if not allow_coerce:
        return False

    if is_string(a) or is_string(b):
        return True

    return False

def result_of_binary(op: str, left: Type, right: Type) -> Type:
    if left.base == BaseType.ERROR or right.base == BaseType.ERROR:
        return Type.error()

    op = op or ""
    if op in ("&", "concat", "++"):
        if can_concat(left, right, allow_coerce=True):
            return Type.base_t(BaseType.SCRIPTURE)
        return Type.error()

    if op in ("+", "-", "*", "/", "%", "**", "^"):
        if is_numeric(left) and is_numeric(right):
            return promote_numeric(left, right)
        return Type.error()

    if op in ("==", "!="):
        if same_type(left, right) or (is_numeric(left) and is_numeric(right)):
            return Type.base_t(BaseType.VERITY)
        return Type.error()

    if op in (">", "<", ">=", "<="):
        if is_numeric(left) and is_numeric(right):
            return Type.base_t(BaseType.VERITY)
        if left.is_base(BaseType.SIGIL) and right.is_base(BaseType.SIGIL):
            return Type.base_t(BaseType.VERITY)
        return Type.error()

    if op in ("&&", "and"):
        if is_bool(left) and is_bool(right):
            return Type.base_t(BaseType.VERITY)
        return Type.error()

    if op in ("||", "or"):
        if is_bool(left) and is_bool(right):
            return Type.base_t(BaseType.VERITY)
        return Type.error()

    return Type.error()

def result_of_unary(op: str, operand: Type) -> Type:
    if operand.base == BaseType.ERROR:
        return Type.error()

    op = op or ""
    if op in ("!!", "!", "not"):
        return Type.base_t(BaseType.VERITY) if is_bool(operand) else Type.error()
    if op == "~":
        return operand if is_numeric(operand) else Type.error()
    if op in ("++", "--"):
        return operand if is_numeric(operand) else Type.error()
    return Type.error()