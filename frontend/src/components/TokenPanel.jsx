/* eslint-disable react-hooks/incompatible-library */
import React, { useEffect, useLayoutEffect, useMemo, useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import TokenRow from "./TokenRow.jsx";

export default function TokenPanel({
    tokens = [],
    onTokenClick,
    selectedRange,
    activeHeadIndex = -1,
}) {
    const safeTokens = useMemo(() => {
        return Array.isArray(tokens) ? tokens : [];
    }, [tokens]);

    const parentRef = useRef(null);

    const rowVirtualizer = useVirtualizer({
        count: safeTokens.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 60,
        overscan: 12,
        getItemKey: (index) => {
            const t = safeTokens[index];
            const p = t?.pos ?? t?.position ?? {};
            return `${index}-${t?.type ?? ""}-${t?.value ?? ""}-${p?.ln ?? ""}:${p?.col ?? ""}`;
        },
    });

    const start = Number(selectedRange?.start ?? -1);
    const end = Number(selectedRange?.end ?? -1);
    const lo = start >= 0 && end >= 0 ? Math.min(start, end) : -1;
    const hi = start >= 0 && end >= 0 ? Math.max(start, end) : -1;

    useLayoutEffect(() => {
        const head = Number(activeHeadIndex);

        const target =
            head >= 0 && head < safeTokens.length
                ? head
                : end >= 0 && end < safeTokens.length
                    ? end
                    : -1;

        if (target < 0) return;

        const vis = rowVirtualizer.getVirtualItems();
        const first = vis?.[0]?.index ?? 0;
        const last = vis?.[vis.length - 1]?.index ?? 0;

        const align = target < first ? "start" : target > last ? "end" : "center";

        rowVirtualizer.scrollToIndex(target, { align, behavior: "auto" });

        requestAnimationFrame(() => {
            const vis2 = rowVirtualizer.getVirtualItems();
            const first2 = vis2?.[0]?.index ?? 0;
            const last2 = vis2?.[vis2.length - 1]?.index ?? 0;
            const align2 = target < first2 ? "start" : target > last2 ? "end" : "center";

            rowVirtualizer.scrollToIndex(target, { align: align2, behavior: "auto" });
        });
    }, [activeHeadIndex, end, safeTokens.length, rowVirtualizer]);

    useEffect(() => {
        rowVirtualizer.measure();
    }, [safeTokens.length, rowVirtualizer]);

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
                            width: "100%",
                        }}
                    >
                        {items.map((v) => {
                            const hasRange = lo >= 0 && hi >= 0 && lo <= hi;
                            const isSelected = hasRange ? v.index >= lo && v.index <= hi : false;

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