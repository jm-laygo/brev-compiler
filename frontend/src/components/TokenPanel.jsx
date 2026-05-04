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
    const safeTokenList = useMemo(() => {
        return Array.isArray(tokens) ? tokens : [];
    }, [tokens]);

    const tokenListContainerRef = useRef(null);

    const tokenRowVirtualizer = useVirtualizer({
        count: safeTokenList.length,
        getScrollElement: () => tokenListContainerRef.current,
        estimateSize: () => 60,
        overscan: 12,
        getItemKey: (index) => {
            const tokenItem = safeTokenList[index];
            const tokenPosition = tokenItem?.pos ?? tokenItem?.position ?? {};

            return `${index}-${tokenItem?.type ?? ""}-${tokenItem?.value ?? ""}-${tokenPosition?.ln ?? ""}:${tokenPosition?.col ?? ""}`;
        },
    });

    const selectedStartIndex = Number(selectedRange?.start ?? -1);
    const selectedEndIndex = Number(selectedRange?.end ?? -1);

    const selectedLowerIndex =
        selectedStartIndex >= 0 && selectedEndIndex >= 0
            ? Math.min(selectedStartIndex, selectedEndIndex)
            : -1;

    const selectedHigherIndex =
        selectedStartIndex >= 0 && selectedEndIndex >= 0
            ? Math.max(selectedStartIndex, selectedEndIndex)
            : -1;

    useLayoutEffect(() => {
        const activeTokenIndex = Number(activeHeadIndex);

        const targetTokenIndex =
            activeTokenIndex >= 0 && activeTokenIndex < safeTokenList.length
                ? activeTokenIndex
                : selectedEndIndex >= 0 && selectedEndIndex < safeTokenList.length
                ? selectedEndIndex
                : -1;

        if (targetTokenIndex < 0) {
            return;
        }

        const visibleRows = tokenRowVirtualizer.getVirtualItems();
        const firstVisibleIndex = visibleRows?.[0]?.index ?? 0;
        const lastVisibleIndex = visibleRows?.[visibleRows.length - 1]?.index ?? 0;

        const scrollAlignment =
            targetTokenIndex < firstVisibleIndex
                ? "start"
                : targetTokenIndex > lastVisibleIndex
                ? "end"
                : "center";

        tokenRowVirtualizer.scrollToIndex(targetTokenIndex, {
            align: scrollAlignment,
            behavior: "auto",
        });

        requestAnimationFrame(() => {
            const updatedVisibleRows = tokenRowVirtualizer.getVirtualItems();
            const updatedFirstVisibleIndex = updatedVisibleRows?.[0]?.index ?? 0;
            const updatedLastVisibleIndex =
                updatedVisibleRows?.[updatedVisibleRows.length - 1]?.index ?? 0;

            const updatedScrollAlignment =
                targetTokenIndex < updatedFirstVisibleIndex
                    ? "start"
                    : targetTokenIndex > updatedLastVisibleIndex
                    ? "end"
                    : "center";

            tokenRowVirtualizer.scrollToIndex(targetTokenIndex, {
                align: updatedScrollAlignment,
                behavior: "auto",
            });
        });
    }, [activeHeadIndex, selectedEndIndex, safeTokenList.length, tokenRowVirtualizer]);

    useEffect(() => {
        tokenRowVirtualizer.measure();
    }, [safeTokenList.length, tokenRowVirtualizer]);

    const virtualRows = tokenRowVirtualizer.getVirtualItems();

    return (
        <div className="tokens-panel">
            <div className="tokens-head">
                <div className="tokens-title">Tokens</div>
                <div className="tokens-count">
                    {safeTokenList.length} rows
                </div>
            </div>

            <div
                className="tokens-table"
                role="table"
                aria-label="Tokens table"
            >
                <div className="token-thead" role="rowgroup">
                    <div className="token-header-row" role="row">
                        <div className="token-hcell pos" role="columnheader">
                            Ln, Cl
                        </div>

                        <div className="token-hcell" role="columnheader">
                            LEXEME
                        </div>

                        <div className="token-hcell" role="columnheader">
                            TOKEN
                        </div>

                        <div className="token-hcell" role="columnheader">
                            TYPE
                        </div>
                    </div>
                </div>

                <div
                    ref={tokenListContainerRef}
                    className="tokens-list-wrap"
                    role="rowgroup"
                >
                    <div
                        style={{
                            height: tokenRowVirtualizer.getTotalSize(),
                            position: "relative",
                            width: "100%",
                        }}
                    >
                        {virtualRows.map((virtualRow) => {
                            const hasSelectedRange =
                                selectedLowerIndex >= 0 &&
                                selectedHigherIndex >= 0 &&
                                selectedLowerIndex <= selectedHigherIndex;

                            const isSelected =
                                hasSelectedRange
                                    ? virtualRow.index >= selectedLowerIndex &&
                                      virtualRow.index <= selectedHigherIndex
                                    : false;

                            return (
                                <div
                                    key={virtualRow.key}
                                    ref={tokenRowVirtualizer.measureElement}
                                    data-index={virtualRow.index}
                                    className={`token-row ${
                                        virtualRow.index % 2 === 0 ? "even" : "odd"
                                    }${isSelected ? " selected" : ""}`}
                                    role="row"
                                    tabIndex={0}
                                    aria-selected={isSelected}
                                    onClick={() =>
                                        onTokenClick?.(
                                            safeTokenList[virtualRow.index]
                                        )
                                    }
                                    onKeyDown={(event) => {
                                        if (
                                            event.key === "Enter" ||
                                            event.key === " "
                                        ) {
                                            event.preventDefault();

                                            onTokenClick?.(
                                                safeTokenList[virtualRow.index]
                                            );
                                        }
                                    }}
                                    style={{
                                        position: "absolute",
                                        top: 0,
                                        left: 0,
                                        width: "100%",
                                        transform: `translateY(${virtualRow.start}px)`,
                                    }}
                                >
                                    <TokenRow token={safeTokenList[virtualRow.index]} />
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}