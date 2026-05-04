from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union


# base node
@dataclass
class Node:
    position: Any = None


# program
@dataclass
class Program(Node):
    globalDeclarations: List[Node] = field(default_factory=list)
    riteDeclarations: List["RiteDeclaration"] = field(default_factory=list)
    entryRite: Optional["RiteDeclaration"] = None


# rite
@dataclass
class RiteDeclaration(Node):
    name: str = ""
    returnType: str = ""
    parameters: List["Parameter"] = field(default_factory=list)
    localDeclarations: List[Node] = field(default_factory=list)
    bodyStatements: List["Statement"] = field(default_factory=list)
    dismissStatement: Optional["DismissStatement"] = None


@dataclass
class Parameter(Node):
    typeName: str = ""
    name: str = ""
    dimensions: List[Optional["Expression"]] = field(default_factory=list)


# sacred declaration
@dataclass
class SacredDeclaration(Node):
    typeName: str = ""
    items: List["SacredItem"] = field(default_factory=list)


@dataclass
class SacredItem(Node):
    name: str = ""
    value: Optional["Expression"] = None


# variable declaration
@dataclass
class VariableDeclaration(Node):
    typeName: str = ""
    items: List["VariableItem"] = field(default_factory=list)


@dataclass
class VariableItem(Node):
    name: str = ""
    dimensions: List["Expression"] = field(default_factory=list)
    initialValue: Optional["Expression"] = None


# order declaration
@dataclass
class OrderDeclaration(Node):
    name: str = ""
    members: List["OrderMember"] = field(default_factory=list)


@dataclass
class OrderMember(Node):
    typeName: str = ""
    name: str = ""
    dimensions: List["Expression"] = field(default_factory=list)
    initialValue: Optional["Expression"] = None


# ordain declaration
@dataclass
class OrdainDeclaration(Node):
    name: str = ""
    items: List["OrdainItem"] = field(default_factory=list)


@dataclass
class OrdainItem(Node):
    name: str = ""
    dimensions: List["Expression"] = field(default_factory=list)
    initialValue: Optional["Expression"] = None


# statements
@dataclass
class Statement(Node):
    pass


@dataclass
class FunctionCallStatement(Statement):
    calleeName: str = ""
    arguments: List["Expression"] = field(default_factory=list)
    accessChain: Optional["LeftHandValue"] = None


@dataclass
class VariableDeclarationStatement(Statement):
    declaration: VariableDeclaration = None


@dataclass
class OrderDeclarationStatement(Statement):
    declaration: OrderDeclaration = None


@dataclass
class OrdainDeclarationStatement(Statement):
    declaration: OrdainDeclaration = None


# input output statements
@dataclass
class InputOutputStatement(Statement):
    pass


@dataclass
class ReceiveStatement(InputOutputStatement):
    target: "LeftHandValue" = None


@dataclass
class ProclaimStatement(InputOutputStatement):
    arguments: List["Expression"] = field(default_factory=list)


@dataclass
class AssignmentStatement(Statement):
    target: "LeftHandValue" = None
    operator: str = "="
    value: "Expression" = None


@dataclass
class IncrementDecrementStatement(Statement):
    target: "LeftHandValue" = None
    operator: str = "++"
    isPrefix: bool = True


# jump statements
@dataclass
class JumpStatement(Statement):
    pass


@dataclass
class DismissStatement(JumpStatement):
    value: Optional["Expression"] = None


@dataclass
class ProceedStatement(JumpStatement):
    pass


@dataclass
class AbsolveStatement(JumpStatement):
    pass


@dataclass
class FallStatement(JumpStatement):
    pass


# condition statements
@dataclass
class ConditionStatement(Statement):
    pass


# decree statement
@dataclass
class DecreeStatement(ConditionStatement):
    condition: "Expression" = None
    bodyStatements: List[Statement] = field(default_factory=list)
    edictClauses: List["EdictClause"] = field(default_factory=list)
    absolutionClause: Optional["AbsolutionClause"] = None


@dataclass
class EdictClause(Node):
    condition: "Expression" = None
    bodyStatements: List[Statement] = field(default_factory=list)


@dataclass
class AbsolutionClause(Node):
    bodyStatements: List[Statement] = field(default_factory=list)


# discern statement
@dataclass
class DiscernStatement(ConditionStatement):
    expression: "Expression" = None
    verseCases: List["VerseCase"] = field(default_factory=list)
    graceDefault: Optional["GraceDefault"] = None


@dataclass
class VerseCase(Node):
    matchValue: Union["Expression", "IdentifierReference"] = None
    bodyStatements: List[Statement] = field(default_factory=list)
    verseEnd: Optional["VerseEnd"] = None


@dataclass
class VerseEnd(Node):
    kind: str = ""


@dataclass
class GraceDefault(Node):
    bodyStatements: List[Statement] = field(default_factory=list)
    verseEnd: Optional["VerseEnd"] = None


# loop statements
@dataclass
class LoopStatement(Statement):
    pass


@dataclass
class EndureStatement(LoopStatement):
    condition: "Expression" = None
    bodyStatements: List[Statement] = field(default_factory=list)


@dataclass
class ProcessionStatement(LoopStatement):
    initializerStatement: Optional[Statement] = None
    condition: Optional["Expression"] = None
    updateStatement: Optional[Statement] = None
    bodyStatements: List[Statement] = field(default_factory=list)


@dataclass
class RitualStatement(LoopStatement):
    bodyStatements: List[Statement] = field(default_factory=list)
    condition: "Expression" = None


# left hand values
@dataclass
class LeftHandValue(Node):
    pass


@dataclass
class NameReference(LeftHandValue):
    name: str = ""


@dataclass
class IndexReference(LeftHandValue):
    baseReference: LeftHandValue = None
    indexExpression: "Expression" = None


@dataclass
class MemberReference(LeftHandValue):
    baseReference: LeftHandValue = None
    memberName: str = ""


@dataclass
class IdentifierReference(Node):
    name: str = ""


# expressions
@dataclass
class Expression(Node):
    inferredType: Optional[str] = None


@dataclass
class LiteralExpression(Expression):
    value: Any = None
    literalType: str = ""


@dataclass
class UnaryExpression(Expression):
    operator: str = ""
    operand: Expression = None
    isPrefix: bool = True


@dataclass
class BinaryExpression(Expression):
    leftExpression: Expression = None
    operator: str = ""
    rightExpression: Expression = None


@dataclass
class GroupExpression(Expression):
    expression: Expression = None


@dataclass
class FunctionCallExpression(Expression):
    calleeName: str = ""
    arguments: List[Expression] = field(default_factory=list)
    accessChain: Optional[LeftHandValue] = None


@dataclass
class VerseOfExpression(Expression):
    expression: Expression = None


@dataclass
class ArrayInitializationExpression(Expression):
    items: List[Expression] = field(default_factory=list)


@dataclass
class VariableExpression(Expression):
    reference: LeftHandValue = None