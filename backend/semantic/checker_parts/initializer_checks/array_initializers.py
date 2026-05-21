from __future__ import annotations
from typing import Any, List, Optional

from backend.semantic.typesys import Type, canAssign
from ..helper_functions import getClassName


class ArrayInitializerMixin:
    def convertDimensionsToSizes(
        self,
        dimensionNodes: List[Any],
        ownerNode: Any
    ) -> Optional[List[int]]:
        dimensionSizes: List[int] = []

        for dimensionNode in dimensionNodes:
            dimensionValue = self.getConstantIntegerValue(dimensionNode)

            if dimensionValue is None:
                self.addError(
                    ownerNode,
                    "Array size must be a positive tally literal, constant expression, or sacred tally constant."
                )
                return None

            if dimensionValue <= 0:
                self.addError(
                    ownerNode,
                    f"Array size must be > 0, got {dimensionValue}."
                )
                return None

            dimensionSizes.append(dimensionValue)

        return dimensionSizes

    def checkArrayInitializationShape(
        self,
        initializerNode: Any,
        dimensionSizes: List[int],
        level: int,
        ownerNode: Any
    ) -> None:
        initializerItems = getattr(initializerNode, "items", []) or []
        expectedItemCount = dimensionSizes[level]

        # too many items
        if len(initializerItems) > expectedItemCount:
            self.addError(
                initializerNode,
                f"Too many initializer elements at dimension {level + 1}: max {expectedItemCount}, got {len(initializerItems)}."
            )

        isLastDimension = level == len(dimensionSizes) - 1

        # last dimension
        if isLastDimension:
            for initializerItem in initializerItems[:expectedItemCount]:
                if getClassName(initializerItem) == "ArrayInitializationExpression":
                    self.addError(
                        initializerItem,
                        f"Too many nested braces: array is {len(dimensionSizes)}D but initializer nests deeper."
                    )

            return

        # nested dimensions
        for itemIndex, initializerItem in enumerate(initializerItems[:expectedItemCount]):
            if getClassName(initializerItem) != "ArrayInitializationExpression":
                self.addError(
                    initializerItem,
                    f"Missing nested braces at dimension {level + 1}: element {itemIndex + 1} must be a brace group."
                )

                continue

            self.checkArrayInitializationShape(
                initializerItem,
                dimensionSizes,
                level + 1,
                ownerNode
            )

    def checkArrayInitializationTypes(
        self,
        initializerNode: Any,
        targetType: Type,
        level: int,
        sizes: List[int],
        ownerNode: Any
    ) -> None:
        initializerItems = getattr(initializerNode, "items", []) or []
        expectedItemCount = sizes[level]

        if not initializerItems:
            return

        isLastDimension = level == len(sizes) - 1

        # check final values
        if isLastDimension:
            elementType = targetType

            while elementType.arrayElementType is not None:
                elementType = elementType.arrayElementType

            for initializerItem in initializerItems[:expectedItemCount]:
                if getClassName(initializerItem) == "ArrayInitializationExpression":
                    self.addError(
                        initializerItem,
                        "Unexpected nested brace at last dimension."
                    )

                    continue

                initializerItemType = self.getExpressionType(initializerItem)

                if not canAssign(elementType, initializerItemType):
                    self.addError(
                        initializerItem,
                        f"Cannot assign {initializerItemType} to {elementType} in array initializer."
                    )

            return

        childTargetType = (
            targetType.arrayElementType
            if targetType.arrayElementType is not None
            else targetType
        )

        # check nested values
        for initializerItem in initializerItems[:expectedItemCount]:
            if getClassName(initializerItem) != "ArrayInitializationExpression":
                continue

            self.checkArrayInitializationTypes(
                initializerItem,
                childTargetType,
                level + 1,
                sizes,
                ownerNode
            )