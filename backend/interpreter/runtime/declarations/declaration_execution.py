from __future__ import annotations

from backend.ast.ast_nodes import OrdainDeclaration, SacredDeclaration, VariableDeclaration
from backend.errors import RuntimeErrorBase
from backend.interpreter.environment import Environment


# variable declaration
def executeVariableDeclaration(
    self,
    declarationNode: VariableDeclaration,
    currentEnvironment: Environment
):
    declaredTypeName = getattr(declarationNode, "typeName", "")
    declaredItems = getattr(declarationNode, "items", []) or []

    for declaredItem in declaredItems:
        materializedValue = self.materializeVariableItem(
            declaredTypeName,
            declaredItem,
            currentEnvironment
        )

        dimensionNodes = getattr(declaredItem, "dimensions", None) or []

        if dimensionNodes:
            coercedValue = materializedValue
        else:
            coercedValue = self.coerceValueToType(
                declaredTypeName,
                materializedValue,
                declaredItem
            )

        currentEnvironment.declare(
            declaredItem.name,
            coercedValue,
            isConstant=False,
            node=declaredItem,
            declaredType=declaredTypeName
        )


# sacred declaration
def executeSacredDeclaration(
    self,
    declarationNode: SacredDeclaration,
    currentEnvironment: Environment
):
    declaredTypeName = getattr(declarationNode, "typeName", "")
    declaredItems = getattr(declarationNode, "items", []) or []

    for declaredItem in declaredItems:
        valueNode = getattr(declaredItem, "value", None)

        if valueNode is not None:
            evaluatedValue = self.evaluateExpression(
                valueNode,
                currentEnvironment
            )
        else:
            evaluatedValue = self.getDefaultValueForType(declaredTypeName)

        coercedValue = self.coerceValueToType(
            declaredTypeName,
            evaluatedValue,
            declaredItem
        )

        currentEnvironment.declare(
            declaredItem.name,
            coercedValue,
            isConstant=True,
            node=declaredItem,
            declaredType=declaredTypeName
        )


# ordain declaration
def executeOrdainDeclaration(
    self,
    declarationNode: OrdainDeclaration,
    currentEnvironment: Environment
):
    orderName = declarationNode.name
    orderDeclaration = self.orderDeclarations.get(orderName)

    if orderDeclaration is None:
        raise RuntimeErrorBase(
            declarationNode,
            f"Unknown order type '{orderName}'."
        )

    declaredItems = getattr(declarationNode, "items", []) or []

    for declaredItem in declaredItems:
        dimensionNodes = getattr(declaredItem, "dimensions", None) or []
        initializerNode = getattr(declaredItem, "initialValue", None)

        if dimensionNodes:
            evaluatedShape = []

            for dimensionNode in dimensionNodes:
                evaluatedShape.extend([
                    self.requireIntegerDimension(
                        dimensionNode,
                        currentEnvironment,
                        declaredItem
                    )
                ])

            runtimeValue = self.makeArrayOf(
                lambda: self.makeOrderInstance(orderDeclaration),
                evaluatedShape
            )

        elif initializerNode is not None:
            runtimeValue = self.evaluateExpression(
                initializerNode,
                currentEnvironment
            )

        else:
            runtimeValue = self.makeOrderInstance(orderDeclaration)

        currentEnvironment.declare(
            declaredItem.name,
            runtimeValue,
            isConstant=False,
            node=declaredItem,
            declaredType=orderName
        )