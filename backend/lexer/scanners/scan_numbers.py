from backend.lexer.tokens import Token, TK_LIT_INT, TK_LIT_DECIMAL
from backend.lexer.errors import LexicalError
from backend.lexer.delimiters import *
MAX_INT = 999_999_999
MIN_INT = -999_999_999
MAX_FLOAT = 999_999_999.999_999_999
MIN_FLOAT = -999_999_999.999_999_999

DIGITS = "0123456789"

def scan_number(lexer):
    pos = lexer.pos.copy()
    num_str = ""
    has_dot = False
    negative = False

    # negative sign
    if lexer.current_char == "~":
        negative = True
        num_str += "~"
        lexer.advance()

        if lexer.current_char is None or lexer.current_char not in DIGITS:
            raise LexicalError(pos, f"Invalid number literal '{num_str}'")

    # must start with a digit
    if lexer.current_char not in DIGITS:
        return None

    num_str += lexer.current_char
    lexer.advance()

    while lexer.current_char is not None:
        ch = lexer.current_char

        # integers
        if ch in DIGITS:
            num_str += ch
            lexer.advance()
            continue

        # doubles
        if ch == ".":
            if has_dot:
                raise LexicalError(pos, f"Multiple decimal points in '{num_str + ch}'")
            has_dot = True
            num_str += "."
            lexer.advance()

            # must be followed by digit
            if lexer.current_char is None or lexer.current_char not in DIGITS:
                raise LexicalError(pos, f"Invalid decimal literal '{num_str}'")
            continue

        if ch == ",":
            raise LexicalError(pos, f"Invalid character ',' in number '{num_str}'")

        # invalid characters
        if ch in ALPHABET or ch == "_":
            raise LexicalError(pos, f"Invalid character '{ch}' inside number '{num_str}'")

        if ch in idnt_delim:
            break

        raise LexicalError(pos, f"Invalid character '{ch}' after number '{num_str}'")

    # integers
    if not has_dot:
        digits = num_str.replace("~", "")
        if len(digits) > 9:
            raise LexicalError(pos, f"Integer literal too long '{num_str}' (max 9 digits)")

        try:
            val = int(num_str.replace("~", "-"))
        except:
            raise LexicalError(pos, f"Invalid integer literal '{num_str}'")

        if val < MIN_INT or val > MAX_INT:
            raise LexicalError(pos, f"Integer literal out of range '{num_str}'")

        return Token(TK_LIT_INT, num_str, pos)

    # double
    clean = num_str.replace("~", "")
    whole, frac = clean.split(".")
    if len(whole) > 9:
        raise LexicalError(pos, f"Too many digits before decimal point in '{num_str}' (max 9)")
    if len(frac) > 9:
        raise LexicalError(pos, f"Too many digits after decimal point in '{num_str}' (max 9)")

    try:
        val = float(num_str.replace("~", "-"))
    except:
        raise LexicalError(pos, f"Invalid decimal literal '{num_str}'")

    if val < MIN_FLOAT or val > MAX_FLOAT:
        raise LexicalError(pos, f"Decimal literal out of range '{num_str}'")

    return Token(TK_LIT_DECIMAL, num_str, pos)