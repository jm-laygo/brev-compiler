/* eslint-disable react-hooks/incompatible-library */

import React, { useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import TokenRow from "./TokenRow.jsx";

export default function TokenPanel({ tokens = [] }) {
  const safeTokens = Array.isArray(tokens) ? tokens : [];
  const parentRef = useRef(null);

  const rowVirtualizer = useVirtualizer({
    count: safeTokens.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 36,
    overscan: 8,
  });

  return (
    <div className="tokens-panel">
      <div className="tokens-head">
        <div className="tokens-title">Tokens</div>
        <div className="tokens-count">{safeTokens.length} rows</div>
      </div>

      <div className="token-header">
        <div className="token-hcell">LEXEME</div>
        <div className="token-hcell">TOKEN</div>
        <div className="token-hcell">TYPE</div>
      </div>

      <div className="tokens-list-wrap tanstack" ref={parentRef}>
        <div
          style={{
            height: rowVirtualizer.getTotalSize(),
            width: "100%",
            position: "relative",
          }}
        >
          {rowVirtualizer.getVirtualItems().map((v) => (
            <div
              key={v.key}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: v.size,
                transform: `translateY(${v.start}px)`,
              }}
            >
              <TokenRow index={v.index} token={safeTokens[v.index]} style={{ height: "100%" }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}