import React from "react";
import renderLexeme from "../utils/renderLexeme.js";

function getLnCol(token) {
    const p = token?.pos ?? token?.position ?? null;

    const ln = Number(p?.ln ?? p?.line ?? token?.ln ?? token?.line ?? 0);
    const col = Number(p?.col ?? p?.column ?? token?.col ?? token?.column ?? 0);

    const lnTxt = ln > 0 ? ln : "-";
    const colTxt = col > 0 ? col : "-";
    return `${lnTxt},${colTxt}`;
}

export default function TokenRow({ token }) {
    if (!token) return null;

    const posText = getLnCol(token);
    const lex = renderLexeme(token.value);
    const tok = token.token ?? "";
    const type = token.type ?? "";

    return (
    <>
        <div className="token-cell pos" role="cell" title={`Ln ${posText.split(",")[0]}, Col ${posText.split(",")[1]}`}>
        {posText}
        </div>

        <div className="token-cell lexeme" role="cell" title={lex}>{lex}</div>
        <div className="token-cell token" role="cell" title={tok}>{tok}</div>
        <div className="token-cell type" role="cell" title={type}>{type}</div>
    </>
    );
}