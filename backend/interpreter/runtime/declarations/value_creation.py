from __future__ import annotations

from backend.ast.ast_nodes import OrderDeclaration, VariableItem
from backend.errors import RuntimeErrorBase, RuntimeTypeError
from backend.interpreter.environment import Environment


def materializeVariableItem(
    self,
    declaredTypeName: str,
    declaredItem: VariableItem,
    currentEnvironment: Environment
):
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

        if initializerNode is not None:
            return self.evaluateExpression(
                initializerNode,
                currentEnvironment
            )

        return self.makeArrayOf(
            lambda: self.getDefaultValueForType(declaredTypeName),
            evaluatedShape
        )

    if initializerNode is not None:
        return self.evaluateExpression(
            initializerNode,
            currentEnvironment
        )

    return self.getDefaultValueForType(declaredTypeName)

def makeOrderInstance(self, orderDeclaration: OrderDeclaration):
    orderInstance = {"__order__": orderDeclaration.name}

    memberNodes = getattr(orderDeclaration, "members", []) or []

    for memberNode in memberNodes:
        memberDimensionNodes = getattr(memberNode, "dimensions", None) or []
        memberInitializerNode = getattr(memberNode, "initialValue", None)

        if memberDimensionNodes:
            evaluatedShape = []

            for dimensionNode in memberDimensionNodes:
                evaluatedShape.extend([
                    self.requireIntegerDimension(
                        dimensionNode,
                        self.globalEnvironment,
                        memberNode
                    )
                ])

            orderInstance[memberNode.name] = self.makeArrayOf(
                lambda: self.getDefaultValueForType(memberNode.typeName),
                evaluatedShape
            )

        elif memberInitializerNode is not None:
            orderInstance[memberNode.name] = self.evaluateExpression(
                memberInitializerNode,
                self.globalEnvironment
            )

        else:
            orderInstance[memberNode.name] = self.getDefaultValueForType(
                memberNode.typeName
            )

    return orderInstance

def makeArrayOf(self, valueFactory, shape):
    if not shape:
        return valueFactory()

    currentDimensionSize = shape[0]

    return [
        self.makeArrayOf(valueFactory, shape[1:])
        for _ in range(currentDimensionSize)
    ]

def requireIntegerDimension(self, dimensionExpression, currentEnvironment: Environment, node):
    evaluatedDimensionValue = self.evaluateExpression(
        dimensionExpression,
        currentEnvironment
    )

    if not isinstance(evaluatedDimensionValue, int):
        raise RuntimeTypeError(
            node,
            "Array dimensions must evaluate to tally values."
        )

    if evaluatedDimensionValue <= 0:
        raise RuntimeErrorBase(
            node,
            "Array dimensions must be positive."
        )

    return evaluatedDimensionValue

def getDefaultValueForType(self, declaredTypeName: str):
    loweredTypeName = (declaredTypeName or "").lower()

    if loweredTypeName == "tally":
        return 0

    if loweredTypeName == "divine":
        return 0.0

    if loweredTypeName == "sigil":
        return "\0"

    if loweredTypeName == "scripture":
        return ""

    if loweredTypeName == "verity":
        return False

    if loweredTypeName == "hollow":
        return None

    if declaredTypeName in self.orderDeclarations:
        return self.makeOrderInstance(
            self.orderDeclarations[declaredTypeName]
        )

    return None