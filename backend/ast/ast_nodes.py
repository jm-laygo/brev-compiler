from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

# Base Node
@dataclass
class Node:
    pos: Any = None

# Program / Functions
@dataclass
class Program(Node):
    # global_dec_list (sacred / var / order / ordain)
    globals: List[Node] = field(default_factory=list)

    # rite_seq non-entry
    functions: List["RiteDecl"] = field(default_factory=list)

    # genesis() rite (entry)
    entry: Optional["RiteDecl"] = None

@dataclass
class RiteDecl(Node):
    name: str = ""
    return_type: str = ""
    params: List["Param"] = field(default_factory=list)

    local_decls: List[Node] = field(default_factory=list)
    body: List["Statement"] = field(default_factory=list)
    dismiss: Optional["DismissStmt"] = None

@dataclass
class Param(Node):
    type_name: str = ""
    name: str = ""
    dims: List[Optional["Expr"]] = field(default_factory=list)

# Global / Local Decls
@dataclass
class SacredDecl(Node):
    type_name: str = ""
    items: List["SacredItem"] = field(default_factory=list)

@dataclass
class SacredItem(Node):
    name: str = ""
    value: Optional["Expr"] = None   # const_expr

@dataclass
class VarDecl(Node):
    type_name: str = ""
    items: List["VarItem"] = field(default_factory=list)

@dataclass
class VarItem(Node):
    name: str = ""
    dims: List["Expr"] = field(default_factory=list)
    init: Optional["Expr"] = None

@dataclass
class OrderDecl(Node):
    name: str = ""
    members: List["OrderMember"] = field(default_factory=list)

@dataclass
class OrderMember(Node):
    type_name: str = ""
    name: str = ""
    dims: List["Expr"] = field(default_factory=list)
    init: Optional["Expr"] = None

@dataclass
class OrdainDecl(Node):
    name: str = ""
    items: List["OrdainItem"] = field(default_factory=list)

@dataclass
class OrdainItem(Node):
    name: str = ""
    dims: List["Expr"] = field(default_factory=list)
    init: Optional["Expr"] = None

# Statements
@dataclass
class Statement(Node):
    pass

@dataclass
class CallStmt(Statement):
    callee: str = ""
    args: List["Expr"] = field(default_factory=list)
    access: Optional["LValue"] = None

@dataclass
class VarDeclStmt(Statement):
    decl: VarDecl = None

@dataclass
class OrderStmt(Statement):
    decl: OrderDecl = None

@dataclass
class OrdainStmt(Statement):
    decl: OrdainDecl = None

@dataclass
class IOStmt(Statement):
    pass

@dataclass
class ReceiveStmt(IOStmt):
    target: "LValue" = None

@dataclass
class ProclaimStmt(IOStmt):
    args: List["Expr"] = field(default_factory=list)

@dataclass
class AssignStmt(Statement):
    target: "LValue" = None
    op: str = "="
    value: "Expr" = None

@dataclass
class IncDecStmt(Statement):
    target: "LValue" = None
    op: str = "++" 
    prefix: bool = True

@dataclass
class JumpStmt(Statement):
    pass

@dataclass
class DismissStmt(JumpStmt):
    value: Optional["Expr"] = None

@dataclass
class ProceedStmt(JumpStmt):
    pass

@dataclass
class AbsolveStmt(JumpStmt):
    pass

# Conditions (decree / discern)
@dataclass
class CondStmt(Statement):
    pass

# Decree
@dataclass
class DecreeStmt(CondStmt):
    expr: "Expr" = None
    body: List[Statement] = field(default_factory=list)
    edicts: List["EdictClause"] = field(default_factory=list)
    absolution: Optional["AbsolutionClause"] = None

@dataclass
class EdictClause(Node):
    expr: "Expr" = None
    body: List[Statement] = field(default_factory=list)

@dataclass
class AbsolutionClause(Node):
    body: List[Statement] = field(default_factory=list)

# Discern
@dataclass
class DiscernStmt(CondStmt):
    expr: "Expr" = None
    verses: List["VerseCase"] = field(default_factory=list)
    grace: Optional["GraceDefault"] = None

@dataclass
class VerseCase(Node):
    match: Union["Expr", "IdentifierRef"] = None
    body: List[Statement] = field(default_factory=list)
    end: Optional["VerseEnd"] = None

@dataclass
class VerseEnd(Node):
    kind: str = ""

@dataclass
class GraceDefault(Node):
    body: List[Statement] = field(default_factory=list)
    end: Optional["VerseEnd"] = None

@dataclass
class FallStmt(JumpStmt):
    pass

# Loops
@dataclass
class LoopStmt(Statement):
    pass

@dataclass
class EndureStmt(LoopStmt):
    condition: "Expr" = None
    body: List[Statement] = field(default_factory=list)

@dataclass
class ProcessionStmt(LoopStmt):
    init: Optional[Statement] = None
    condition: Optional["Expr"] = None
    update: Optional[Statement] = None
    body: List[Statement] = field(default_factory=list)

@dataclass
class RitualStmt(LoopStmt):
    body: List[Statement] = field(default_factory=list)
    condition: "Expr" = None

@dataclass
class LValue(Node):
    pass

@dataclass
class NameRef(LValue):
    name: str = ""

@dataclass
class IndexRef(LValue):
    base: LValue = None
    index: "Expr" = None

@dataclass
class MemberRef(LValue):
    base: LValue = None
    member: str = ""

@dataclass
class IdentifierRef(Node):
    name: str = ""

# Expressions
@dataclass
class Expr(Node):
    inferred_type: Optional[str] = None


@dataclass
class LiteralExpr(Expr):
    value: Any = None
    literal_type: str = ""

@dataclass
class UnaryExpr(Expr):
    op: str = ""
    operand: Expr = None
    prefix: bool = True

@dataclass
class BinaryExpr(Expr):
    left: Expr = None
    op: str = ""
    right: Expr = None

@dataclass
class GroupExpr(Expr):
    expr: Expr = None

@dataclass
class CallExpr(Expr):
    callee: str = ""
    args: List[Expr] = field(default_factory=list)
    access: Optional[LValue] = None

@dataclass
class VerseOfExpr(Expr):
    expr: Expr = None

@dataclass
class ArrayInit(Expr):
    items: List[Expr] = field(default_factory=list)

@dataclass
class VarExpr(Expr):
    ref: LValue = None