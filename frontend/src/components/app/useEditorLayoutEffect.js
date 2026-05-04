import { useEffect } from "react";

export default function useEditorLayoutEffect({ editorRef, isTokenPanelOpen }) {
    useEffect(() => {
        const updateEditorLayout = () => {
            editorRef.current?.layout?.();
        };

        requestAnimationFrame(updateEditorLayout);

        const firstLayoutTimer = setTimeout(updateEditorLayout, 80);
        const secondLayoutTimer = setTimeout(updateEditorLayout, 380);

        return () => {
            clearTimeout(firstLayoutTimer);
            clearTimeout(secondLayoutTimer);
        };
    }, [editorRef, isTokenPanelOpen]);
}