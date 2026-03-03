import { useEffect, useState } from "react";

export default function useElementSize(ref) {
    const [size, setSize] = useState({ width: 0, height: 0 });

    useEffect(() => {
        if (!ref.current) return;

        const ro = new ResizeObserver(() => {
            const r = ref.current.getBoundingClientRect();
            setSize({
                width: Math.max(0, Math.floor(r.width)),
                height: Math.max(0, Math.floor(r.height)),
            });
        });

        ro.observe(ref.current);
        return () => ro.disconnect();
    }, [ref]);

    return size;
}