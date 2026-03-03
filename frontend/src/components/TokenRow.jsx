import React, { memo } from "react";
import renderLexeme from "../utils/renderLexeme.js";

const TokenRow = memo(function TokenRow({ index, style, token }) {
  const t = token;
  if (!t) return null;

  return (
    <div className={`token-row ${index % 2 === 0 ? "even" : "odd"}`} style={style}>
      <div className="token-cell lexeme" title={renderLexeme(t.value)}>
        {renderLexeme(t.value)}
      </div>
      <div className="token-cell token" title={t.token ?? ""}>
        {t.token ?? ""}
      </div>
      <div className="token-cell type" title={t.type ?? ""}>
        {t.type ?? ""}
      </div>
    </div>
  );
});

export default TokenRow;