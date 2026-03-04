import React from "react";
import renderLexeme from "../utils/renderLexeme.js";

export default function TokenRow({ token }) {
    if (!token) return null;

    const lex = renderLexeme(token.value);
    const tok = token.token ?? "";
    const type = token.type ?? "";

    return (
        <>
            <div className="token-cell lexeme" role="cell" title={lex}>{lex}</div>
            <div className="token-cell token" role="cell" title={tok}>{tok}</div>
            <div className="token-cell type" role="cell" title={type}>{type}</div>
        </>
    );
}