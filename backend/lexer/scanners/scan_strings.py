from backend.tokens import Token, TK_LIT_STRING
from backend.errors import LexicalError
from backend.delimiters import str_delim, format_expected_delims

def accept_string(lexer, tokens, errors, start_pos, value, allowed_delims):
    ch = lexer.current_char
    expected = format_expected_delims(allowed_delims)

    if ch is None and None not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Missing delimiter after string literal. Expected: {expected}"))
        return True

    if ch is not None and ch not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after string literal. Expected: {expected}"))
        return True

    # Store interpreted value (no extra quotes)
    tokens.append(Token(TK_LIT_STRING, value, start_pos))
    return True

def recover_string_literal(lexer):
    while lexer.current_char is not None and lexer.current_char not in {'"', "\n"}:
        lexer.advance()
    if lexer.current_char == '"':
        lexer.advance()

def scan_string(lexer, tokens, errors):
    if lexer.current_char != '"':
        return False

    start_pos = lexer.pos.copy()
    value = ""
    lexer.advance()

    while lexer.current_char is not None:
        ch = lexer.current_char

        if ch == "\n":
            errors.append(LexicalError(start_pos, "Unterminated string literal"))
            return True

        if ch == "\\":
            lexer.advance()
            esc = lexer.current_char

            if esc is None:
                errors.append(LexicalError(start_pos, "Unterminated escape sequence"))
                return True

            if esc == "n":
                value += "\n"
            elif esc == "t":
                value += "\t"
            elif esc == "\\":
                value += "\\"
            elif esc == '"':
                value += '"'
            else:
                errors.append(LexicalError(start_pos, f"Invalid escape sequence '\\{esc}'"))
                lexer.advance()
                recover_string_literal(lexer)
                return True

            lexer.advance()
            continue

        if ch == '"':
            lexer.advance()
            return accept_string(lexer, tokens, errors, start_pos, value, str_delim)

        value += ch
        lexer.advance()

    errors.append(LexicalError(start_pos, "Unterminated string literal"))
    return True