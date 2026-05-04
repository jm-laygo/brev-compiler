import React from "react";

export default class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            hasError: false,
            errorMessage: "",
        };
    }

    static getDerivedStateFromError(errorObject) {
        return {
            hasError: true,
            errorMessage: errorObject?.message || String(errorObject),
        };
    }

    componentDidCatch(errorObject, errorInfo) {
        console.error("UI crash:", errorObject, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: 12, color: "gold" }}>
                    <div style={{ fontWeight: 800, marginBottom: 6 }}>
                        Tokens panel crashed:
                    </div>

                    <pre
                        style={{
                            whiteSpace: "pre-wrap",
                            margin: 0,
                            opacity: 0.9,
                        }}
                    >
                        {this.state.errorMessage}
                    </pre>
                </div>
            );
        }

        return this.props.children;
    }
}