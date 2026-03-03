/* eslint-disable react-hooks/incompatible-library */
import React, { useMemo, useRef } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import TokenRow from "./TokenRow.jsx";

export default function TokenPanel({ tokens = [] }) {
    const safeTokens = useMemo(() => (
        Array.isArray(tokens) ? tokens : []
    ), [tokens]);

    const parentRef = useRef(null);

    const rowVirtualizer = useVirtualizer({
        count: safeTokens.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 44,
        overscan: 10,
        measureElement: (el) => el.getBoundingClientRect().height
    });

    const items = rowVirtualizer.getVirtualItems();

    const paddingTop = items.length > 0 ? items[0].start : 0;
    const paddingBottom = items.length > 0
        ? rowVirtualizer.getTotalSize() - items[items.length - 1].end
        : 0;

    return (
        <div className="tokens-panel">
            <div className="tokens-head">
                <div className="tokens-title">Tokens</div>
                <div className="tokens-count">{safeTokens.length} rows</div>
            </div>

            <div ref={parentRef} className="tokens-list-wrap tanstack">
                <table className="tokens-table">
                    <thead className="token-thead">
                        <tr>
                            <th className="token-hcell">LEXEME</th>
                            <th className="token-hcell">TOKEN</th>
                            <th className="token-hcell">TYPE</th>
                        </tr>
                    </thead>

                    <tbody className="token-tbody">
                        {paddingTop > 0 && (
                            <tr aria-hidden="true">
                                <td colSpan={3} style={{ height: paddingTop }} />
                            </tr>
                        )}

                        {items.map((v) => (
                            <tr
                                key={v.key}
                                data-index={v.index}
                                ref={rowVirtualizer.measureElement}
                                className={`token-row ${v.index % 2 === 0 ? "even" : "odd"}`}
                            >
                                <TokenRow token={safeTokens[v.index]} />
                            </tr>
                        ))}

                        {paddingBottom > 0 && (
                            <tr aria-hidden="true">
                                <td colSpan={3} style={{ height: paddingBottom }} />
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}