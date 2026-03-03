import React from "react";

export default class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, errorText: "" };
    }

    static getDerivedStateFromError(err) {
        return { hasError: true, errorText: err?.message || String(err) };
    }

    componentDidCatch(err, info) {
        console.error("UI crash:", err, info);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style = {{ padding: 12, color: "gold" }}>
                    <div style = {{ fontWeight: 800, marginBottom: 6 }}>
                        Tokens panel crashed:
                    </div>
                    <pre style = {{ whiteSpace: "pre-wrap", margin: 0, opacity: 0.9 }}>
                        {this.state.errorText}
                    </pre>
                </div>
            );
        }
        return this.props.children;
    }
}