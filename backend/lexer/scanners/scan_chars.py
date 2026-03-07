from backend.tokens import Token, TK_LIT_CHAR
from backend.errors import LexicalError
from backend.delimiters import chr_delim, format_expected_delims

def accept_char(lexer, tokens, errors, start_pos, display_value, allowed_delims):
    ch = lexer.current_char
    expected = format_expected_delims(allowed_delims)

    if ch is None and None not in allowed_delims:
        errors.append(
            LexicalError(start_pos, f"Missing delimiter after char literal {display_value}. Expected: {expected}")
        )
        return True

    if ch is not None and ch not in allowed_delims:
        errors.append(
            LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after char literal {display_value}. Expected: {expected}")
        )
        return True

    tokens.append(Token(TK_LIT_CHAR, display_value, start_pos))
    return True

def recover_char_literal(lexer):
    while lexer.current_char is not None and lexer.current_char not in {"'", "\n"}:
        lexer.advance()
    if lexer.current_char == "'":
        lexer.advance()

def scan_char(lexer, tokens, errors):
    if lexer.current_char != "'":
        return False

    start_pos = lexer.pos.copy()
    lexer.advance()

    if lexer.current_char is None:
        errors.append(LexicalError(start_pos, "Unterminated char literal"))
        return True

    if lexer.current_char == "\n":
        errors.append(LexicalError(start_pos, "Unterminated char literal (newline in char literal)"))
        return True

    # empty char ''
    if lexer.current_char == "'":
        lexer.advance()
        return accept_char(lexer, tokens, errors, start_pos, "''", chr_delim)

    # read one character (escaped or normal)
    if lexer.current_char == "\\":
        lexer.advance()
        if lexer.current_char is None:
            errors.append(LexicalError(start_pos, "Unterminated escape sequence in char literal"))
            return True

        escape_map = {
            "n": "\n",
            "t": "\t",
            "0": "\0",
            "'": "'",
            "\\": "\\",
        }

        esc = lexer.current_char
        if esc not in escape_map:
            errors.append(LexicalError(start_pos, f"Unknown escape sequence '\\{esc}'"))
            lexer.advance()
            recover_char_literal(lexer)
            return True

        ch = escape_map[esc]
        lexer.advance()
    else:
        ch = lexer.current_char
        lexer.advance()

    if lexer.current_char != "'":
        errors.append(LexicalError(start_pos, "Char literal must contain exactly one character"))
        recover_char_literal(lexer)
        return True

    lexer.advance()

    if ord(ch) > 127:
        errors.append(LexicalError(start_pos, f"Non-ASCII character '{ch}' is not allowed in char literal"))
        return True

    if ch == "\n":
        display = "\\n"
    elif ch == "\t":
        display = "\\t"
    elif ch == "\0":
        display = "\\0"
    else:
        display = ch

    return accept_char(lexer, tokens, errors, start_pos, f"'{display}'", chr_delim)