import { useEffect, useState } from "react";

export default function useElementSize(elementRef) {
    const [elementSize, setElementSize] = useState({
        width: 0,
        height: 0,
    });

    useEffect(() => {
        const element = elementRef.current;

        if (!element) {
            return;
        }

        const resizeObserver = new ResizeObserver(() => {
            const elementRectangle = element.getBoundingClientRect();

            setElementSize({
                width: Math.max(0, Math.floor(elementRectangle.width)),
                height: Math.max(0, Math.floor(elementRectangle.height)),
            });
        });

        resizeObserver.observe(element);

        return () => {
            resizeObserver.disconnect();
        };
    }, [elementRef]);

    return elementSize;
}