from __future__ import annotations
from typing import Any

from backend.semantic.symbols import Scope
from .helpers import getClassName
from backend.semantic.typesys import BaseType


class ProgramFlowMixin:
    def checkProgram(self, programNode: Any) -> None:
        globalDeclarations = getattr(programNode, "globalDeclarations", []) or []

        for globalDeclaration in globalDeclarations:
            declarationKind = getClassName(globalDeclaration)

            if declarationKind == "VariableDeclaration":
                self.checkVariableDeclarationInitialValues(globalDeclaration)

            elif declarationKind == "SacredDeclaration":
                self.checkSacredDeclarationInitialValues(globalDeclaration)

            elif declarationKind == "OrdainDeclaration":
                self.checkOrdainDeclarationInitialValues(globalDeclaration)

        entryRite = getattr(programNode, "entryRite", None)

        if entryRite is not None:
            self.checkRite(entryRite)

        riteDeclarations = getattr(programNode, "riteDeclarations", []) or []

        for riteDeclaration in riteDeclarations:
            self.checkRite(riteDeclaration)

    def blockGuaranteesDismiss(self, statementList: list[Any]) -> bool:
        for statementNode in statementList or []:
            if self.statementGuaranteesDismiss(statementNode):
                return True

        return False

    def statementGuaranteesDismiss(self, statementNode: Any) -> bool:
        if statementNode is None:
            return False

        statementKind = getClassName(statementNode)

        if statementKind == "DismissStatement":
            return True

        if statementKind == "DecreeStatement":
            decreeBody = getattr(statementNode, "bodyStatements", []) or []
            edictClauses = getattr(statementNode, "edictClauses", []) or []
            absolutionClause = getattr(statementNode, "absolutionClause", None)

            if absolutionClause is None:
                return False

            if not self.blockGuaranteesDismiss(decreeBody):
                return False

            for edictClause in edictClauses:
                if not self.statementGuaranteesDismiss(edictClause):
                    return False

            if not self.statementGuaranteesDismiss(absolutionClause):
                return False

            return True

        if statementKind == "EdictClause":
            edictBody = getattr(statementNode, "bodyStatements", []) or []

            return self.blockGuaranteesDismiss(edictBody)

        if statementKind == "AbsolutionClause":
            absolutionBody = getattr(statementNode, "bodyStatements", []) or []

            return self.blockGuaranteesDismiss(absolutionBody)

        return False

    def checkRite(self, riteNode: Any) -> None:
        if getClassName(riteNode) != "RiteDeclaration":
            return

        riteName = getattr(riteNode, "name", "")
        riteSymbol = self.functions.get(riteName)
        self.currentFunction = riteSymbol

        previousScope = self.currentScope
        self.currentScope = Scope(self.globalScope)

        try:
            if riteSymbol:
                seenParameterNames = set()

                for parameterSymbol in riteSymbol.parameters:
                    if parameterSymbol.name in seenParameterNames:
                        self.addError(
                            parameterSymbol.position,
                            f"Duplicate parameter '{parameterSymbol.name}' in rite '{riteName}'."
                        )

                    seenParameterNames.add(parameterSymbol.name)
                    self.currentScope.define(parameterSymbol)

            localDeclarations = getattr(riteNode, "localDeclarations", []) or []

            for localDeclaration in localDeclarations:
                declarationKind = getClassName(localDeclaration)

                if declarationKind == "VariableDeclaration":
                    self.declareVariableDeclaration(localDeclaration, isGlobal=False)
                    self.checkVariableDeclarationInitialValues(localDeclaration)

                elif declarationKind == "SacredDeclaration":
                    self.declareVariableDeclaration(
                        localDeclaration,
                        isGlobal=False,
                        forceConstant=True
                    )
                    self.checkSacredDeclarationInitialValues(localDeclaration)

                elif declarationKind == "OrdainDeclaration":
                    self.declareOrdainDeclaration(localDeclaration, isGlobal=False)
                    self.checkOrdainDeclarationInitialValues(localDeclaration)

                elif declarationKind == "OrderDeclaration":
                    self.addError(
                        localDeclaration,
                        "Order declarations are not allowed inside rites."
                    )

            bodyStatements = getattr(riteNode, "bodyStatements", []) or []

            for statementNode in bodyStatements:
                self.checkStatement(statementNode)

            dismissStatement = getattr(riteNode, "dismissStatement", None)

            if dismissStatement is not None:
                self.checkStatement(dismissStatement)

            if (
                riteSymbol is not None
                and not riteSymbol.returnType.isBaseType(BaseType.HOLLOW)
            ):
                bodyGuaranteesDismiss = self.blockGuaranteesDismiss(bodyStatements)
                finalDismissExists = dismissStatement is not None
                riteGuaranteesDismiss = bodyGuaranteesDismiss or finalDismissExists

                if not riteGuaranteesDismiss:
                    self.addError(
                        riteNode,
                        f"Rite '{riteName}' must dismiss a value of type {riteSymbol.returnType}."
                    )

        finally:
            self.currentScope = previousScope
            self.currentFunction = None