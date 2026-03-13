from __future__ import annotations
from typing import Any

from backend.semantic.symbols import MemberSymbol, OrderSymbol
from backend.semantic.typesys import Type

from ..helpers import _class, _pos


class OrderDeclarationsMixin:
    def _declare_orders(self, program_node: Any) -> None:
        global_declarations = getattr(program_node, "globals", []) or []

        for global_declaration in global_declarations:
            if _class(global_declaration) != "OrderDecl":
                continue

            order_name = getattr(global_declaration, "name", None)
            if not order_name:
                self._error(global_declaration, "Order declaration missing name.")
                continue

            if order_name in self.orders:
                self._error(global_declaration, f"Order '{order_name}' already declared.")
                continue

            order_symbol = OrderSymbol(
                name=order_name,
                typ=Type.order(order_name),
                pos=_pos(global_declaration)
            )

            member_declarations = getattr(global_declaration, "members", []) or []

            for member_declaration in member_declarations:
                member_name = getattr(member_declaration, "name", None)

                if not member_name:
                    self._error(member_declaration, f"Order '{order_name}' member missing name.")
                    continue

                if member_name in order_symbol.members:
                    self._error(member_declaration, f"Duplicate member '{member_name}' in order '{order_name}'.")
                    continue

                member_type = self._type_from_decl(member_declaration)
                order_symbol.members[member_name] = MemberSymbol(
                    name=member_name,
                    typ=member_type,
                    pos=_pos(member_declaration)
                )

            self.orders[order_name] = order_symbol