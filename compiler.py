from lexer import Lexer, LexicalError, Token


def run_code(source: str):
    lexer = Lexer(source)
    result = lexer.make_tokens()

    # Handle both (tokens, errors) tuple or None returns
    if not result or len(result) != 2:
        print("Lexer.make_tokens() did not return (tokens, errors).")
        return

    tokens, errors = result

    print("\n--- TOKENS ---")
    for token in tokens:
        print(f"{token.type:<25} | {token.value}")

    if errors:
        print("\n--- ERRORS ---")
        for error in errors:
            print(error.as_string())
    else:
        print("\nNo lexical errors found.")


def repl():
    """Simple interactive REPL for lexical analysis."""
    print("Type your code below. Type 'exit' to quit.\n")

    while True:
        source_lines = []
        print("Enter code (end with a blank line):")
        while True:
            try:
                line = input(">> ")
            except EOFError:
                print("\nGoodbye.")
                return

            if line.strip().lower() == "exit":
                print("Goodbye.")
                return
            if not line.strip():
                break
            source_lines.append(line)

        code = "\n".join(source_lines)
        run_code(code)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    repl()
