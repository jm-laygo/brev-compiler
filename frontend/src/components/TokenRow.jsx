import React, { memo } from "react";
import renderLexeme from "../utils/renderLexeme.js";

const TokenRow = memo(function TokenRow({ token }) {
    if (!token) return null;

    const lex = renderLexeme(token.value);
    const tok = token.token ?? "";
    const type = token.type ?? "";

    return (
        <>
            <td className="token-cell lexeme" title={lex}>{lex}</td>
            <td className="token-cell token" title={tok}>{tok}</td>
            <td className="token-cell type" title={type}>{type}</td>
        </>
    );
});

export default TokenRow;