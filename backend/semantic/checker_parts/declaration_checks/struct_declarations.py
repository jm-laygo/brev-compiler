from __future__ import annotations
from typing import Any

from backend.semantic.symbols import MemberSymbol, OrderSymbol
from backend.semantic.typesys import Type

from ..helper_functions import getClassName, getNodePosition


class OrderDeclarationsMixin:
    def declareOrders(self, programNode: Any) -> None:
        globalDeclarations = getattr(programNode, "globalDeclarations", []) or []

        for globalDeclaration in globalDeclarations:
            if getClassName(globalDeclaration) != "OrderDeclaration":
                continue

            orderName = getattr(globalDeclaration, "name", None)

            if not orderName:
                self.addError(
                    globalDeclaration,
                    "Order declaration missing name."
                )

                continue

            if orderName in self.orders:
                self.addError(
                    globalDeclaration,
                    f"Order '{orderName}' already declared."
                )

                continue

            orderSymbol = OrderSymbol(
                name=orderName,
                symbolType=Type.fromOrder(orderName),
                position=getNodePosition(globalDeclaration)
            )

            memberDeclarations = getattr(globalDeclaration, "members", []) or []

            for memberDeclaration in memberDeclarations:
                memberName = getattr(memberDeclaration, "name", None)

                if not memberName:
                    self.addError(
                        memberDeclaration,
                        f"Order '{orderName}' member missing name."
                    )

                    continue

                if memberName in orderSymbol.members:
                    self.addError(
                        memberDeclaration,
                        f"Duplicate member '{memberName}' in order '{orderName}'."
                    )

                    continue

                memberType = self.getTypeFromDeclaration(memberDeclaration)

                orderSymbol.members[memberName] = MemberSymbol(
                    name=memberName,
                    symbolType=memberType,
                    position=getNodePosition(memberDeclaration)
                )

            self.orders[orderName] = orderSymbol