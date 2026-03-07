from backend.tokens import Token, TK_IDENTIFIER
from backend.errors import LexicalError
from backend.delimiters import idnt_delim, format_expected_delims, ALPHABET, ALPHA_DIG

MAX_IDENTIFIER_LENGTH = 48

def scan_identifier(lexer, tokens, errors):
    if lexer.current_char is None:
        return False

    start_pos = lexer.pos.copy()

    # invalid start: digit or underscore
    if lexer.current_char.isdigit() or lexer.current_char == "_":
        bad = ""
        while lexer.current_char is not None and (
            lexer.current_char in ALPHA_DIG or lexer.current_char == "_"
        ):
            bad += lexer.current_char
            lexer.advance()

        errors.append(
            LexicalError(start_pos, f"Invalid identifier starting with '{bad[0]}' '{bad}'")
        )
        return True

    # must start with a letter
    if lexer.current_char not in ALPHABET:
        return False

    text = ""
    while lexer.current_char is not None and (
        lexer.current_char in ALPHA_DIG or lexer.current_char == "_"
    ):
        # length limit
        if len(text) >= MAX_IDENTIFIER_LENGTH:
            # discard the rest of the identifier lexeme
            while lexer.current_char is not None and (
                lexer.current_char in ALPHA_DIG or lexer.current_char == "_"
            ):
                lexer.advance()

            errors.append(
                LexicalError(start_pos, f"Identifier too long (max {MAX_IDENTIFIER_LENGTH}).")
            )
            return True

        text += lexer.current_char
        lexer.advance()

    # delimiter validation
    ch = lexer.current_char
    expected = format_expected_delims(idnt_delim)

    if ch is None and None not in idnt_delim:
        errors.append(
            LexicalError(start_pos, f"Missing delimiter after identifier '{text}'. Expected: {expected}")
        )
        return True

    if ch is not None and ch not in idnt_delim:
        errors.append(
            LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after identifier '{text}'. Expected: {expected}")
        )
        return True

    tokens.append(Token(TK_IDENTIFIER, text, start_pos))
    return True