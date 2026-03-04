import { useEffect } from "react";

export default function useEditorLayoutEffect({ editorRef, tokensOpen }) {
    useEffect(() => {
        const layout = () => editorRef.current?.layout?.();
        requestAnimationFrame(layout);
        const t1 = setTimeout(layout, 80);
        const t2 = setTimeout(layout, 380);
        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, [editorRef, tokensOpen]);
}