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
            self.checkFunction(entryRite)

        riteDeclarations = getattr(programNode, "riteDeclarations", []) or []

        for riteDeclaration in riteDeclarations:
            self.checkFunction(riteDeclaration)

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

    def checkFunction(self, functionNode: Any) -> None:
        if getClassName(functionNode) != "RiteDeclaration":
            return

        functionName = getattr(functionNode, "name", "")
        functionSymbol = self.functions.get(functionName)
        self.currentFunction = functionSymbol

        previousScope = self.currentScope
        self.currentScope = Scope(self.globalScope)

        try:
            if functionSymbol:
                seenParameterNames = set()

                for parameterSymbol in functionSymbol.parameters:
                    if parameterSymbol.name in seenParameterNames:
                        self.addError(
                            parameterSymbol.position,
                            f"Duplicate parameter '{parameterSymbol.name}' in function '{functionName}'."
                        )

                    seenParameterNames.add(parameterSymbol.name)
                    self.currentScope.define(parameterSymbol)

            localDeclarations = getattr(functionNode, "localDeclarations", []) or []

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
                        "Order declarations are not allowed inside functions."
                    )

            bodyStatements = getattr(functionNode, "bodyStatements", []) or []

            for statementNode in bodyStatements:
                self.checkStatement(statementNode)

            dismissStatement = getattr(functionNode, "dismissStatement", None)

            if dismissStatement is not None:
                self.checkStatement(dismissStatement)

            if (
                functionSymbol is not None
                and not functionSymbol.returnType.isBaseType(BaseType.HOLLOW)
            ):
                bodyGuaranteesDismiss = self.blockGuaranteesDismiss(bodyStatements)
                finalDismissExists = dismissStatement is not None
                functionGuaranteesDismiss = bodyGuaranteesDismiss or finalDismissExists

                if not functionGuaranteesDismiss:
                    self.addError(
                        functionNode,
                        f"Function '{functionName}' must dismiss a value of type {functionSymbol.returnType}."
                    )

        finally:
            self.currentScope = previousScope
            self.currentFunction = None