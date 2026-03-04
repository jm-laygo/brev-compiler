/* eslint-disable react-hooks/incompatible-library */
import React, { useEffect, useMemo, useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import TokenRow from "./TokenRow.jsx";

export default function TokenPanel({ tokens = [], onTokenClick, selectedRange = { start: -1, end: -1 } }) {
    const safeTokens = useMemo(() => {
        return Array.isArray(tokens) ? tokens : [];
    }, [tokens]);

    const parentRef = useRef(null);

    const rowVirtualizer = useVirtualizer({
        count: safeTokens.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 44,
        overscan: 10,
        measureElement: (el) => el.getBoundingClientRect().height,
        getItemKey: (index) => {
            const t = safeTokens[index];
            if (!t) return `row-${index}`;
            return `${index}-${t.type ?? ""}-${t.token ?? ""}-${t.value ?? ""}`;
        },
    });

    const start = Number(selectedRange?.start ?? -1);
    const end = Number(selectedRange?.end ?? -1);

    useEffect(() => {
        if (start < 0) return;
        if (start >= safeTokens.length) return;
        rowVirtualizer.scrollToIndex(start, { align: "center" });
    }, [rowVirtualizer, safeTokens.length, start]);

    const items = rowVirtualizer.getVirtualItems();

    return (
        <div className="tokens-panel">
            <div className="tokens-head">
                <div className="tokens-title">Tokens</div>
                <div className="tokens-count">{safeTokens.length} rows</div>
            </div>

            <div className="tokens-table" role="table" aria-label="Tokens table">
                <div className="token-thead" role="rowgroup">
                    <div className="token-header-row" role="row">
                        <div className="token-hcell pos" role="columnheader">Ln, Cl</div>
                        <div className="token-hcell" role="columnheader">LEXEME</div>
                        <div className="token-hcell" role="columnheader">TOKEN</div>
                        <div className="token-hcell" role="columnheader">TYPE</div>
                    </div>
                </div>

                <div ref={parentRef} className="tokens-list-wrap" role="rowgroup">
                    <div
                        style={{
                            height: rowVirtualizer.getTotalSize(),
                            position: "relative",
                        }}
                    >
                        {items.map((v) => {
                            const isSelected = start >= 0 && end >= 0 && v.index >= start && v.index <= end;

                            return (
                                <div
                                    key={v.key}
                                    ref={rowVirtualizer.measureElement}
                                    data-index={v.index}
                                    className={`token-row ${v.index % 2 === 0 ? "even" : "odd"}${isSelected ? " selected" : ""}`}
                                    role="row"
                                    tabIndex={0}
                                    aria-selected={isSelected}
                                    onClick={() => onTokenClick?.(safeTokens[v.index])}
                                    onKeyDown={(e) => {
                                        if (e.key === "Enter" || e.key === " ") {
                                            e.preventDefault();
                                            onTokenClick?.(safeTokens[v.index]);
                                        }
                                    }}
                                    style={{
                                        position: "absolute",
                                        top: 0,
                                        left: 0,
                                        width: "100%",
                                        transform: `translateY(${v.start}px)`,
                                    }}
                                >
                                    <TokenRow token={safeTokens[v.index]} />
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}