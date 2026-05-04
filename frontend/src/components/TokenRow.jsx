import React from "react";
import renderLexeme from "../utils/renderLexeme.js";

function getLineColumnText(token) {
    const tokenPosition = token?.position ?? token?.pos ?? null;

    const lineNumber = Number(
        tokenPosition?.lineNumber ??
            tokenPosition?.ln ??
            tokenPosition?.line ??
            token?.lineNumber ??
            token?.ln ??
            token?.line ??
            0
    );

    const columnNumber = Number(
        tokenPosition?.columnNumber ??
            tokenPosition?.col ??
            tokenPosition?.column ??
            token?.columnNumber ??
            token?.col ??
            token?.column ??
            0
    );

    const lineText = lineNumber > 0 ? lineNumber : "-";
    const columnText = columnNumber > 0 ? columnNumber : "-";

    return `${lineText},${columnText}`;
}

export default function TokenRow({ token }) {
    if (!token) {
        return null;
    }

    const positionText = getLineColumnText(token);
    const [lineText, columnText] = positionText.split(",");

    const lexemeText = renderLexeme(token.value);
    const tokenName = token.token ?? "";
    const tokenType = token.type ?? "";

    return (
        <>
            <div
                className="token-cell pos"
                role="cell"
                title={`Ln ${lineText}, Col ${columnText}`}
            >
                {positionText}
            </div>

            <div
                className="token-cell lexeme"
                role="cell"
                title={lexemeText}
            >
                {lexemeText}
            </div>

            <div
                className="token-cell token"
                role="cell"
                title={tokenName}
            >
                {tokenName}
            </div>

            <div
                className="token-cell type"
                role="cell"
                title={tokenType}
            >
                {tokenType}
            </div>
        </>
    );
}