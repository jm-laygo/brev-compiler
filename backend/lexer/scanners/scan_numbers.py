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

    # handle negative sign
    if lexer.current_char == "~":
        num_str += "~"
        lexer.advance()
        if lexer.current_char is None or lexer.current_char not in DIGITS:
            raise LexicalError(pos, f"Invalid number literal '{num_str}'")

    # must start with digit
    if lexer.current_char not in DIGITS:
        return None

    # scan digits and decimal point
    while lexer.current_char is not None:
        ch = lexer.current_char

        if ch in DIGITS:
            num_str += ch
            lexer.advance()
            continue

        if ch == ".":
            if has_dot:
                raise LexicalError(pos, f"Multiple decimal points in '{num_str + ch}'")
            has_dot = True
            num_str += "."
            lexer.advance()
            if lexer.current_char is None or lexer.current_char not in DIGITS:
                raise LexicalError(pos, f"Invalid decimal literal '{num_str}'")
            continue

        if ch in int_decdelim:
            break

        # anything else is illegal
        raise LexicalError(pos, f"Invalid character '{ch}' after number '{num_str}'")

    # **require delimiter after number**
    if lexer.current_char is None or lexer.current_char not in int_decdelim:
        raise LexicalError(pos, f"Missing delimiter after number '{num_str}'")

    # determine token type
    tok_type = TK_LIT_INT if not has_dot else TK_LIT_DECIMAL
    tok = Token(tok_type, num_str, pos)

    # integer checks
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

    # decimal checks
    if has_dot:
        clean = num_str.replace("~", "")
        whole, frac = clean.split(".")
        if len(whole) > 9:
            raise LexicalError(pos, f"Too many digits before decimal in '{num_str}'")
        if len(frac) > 9:
            raise LexicalError(pos, f"Too many digits after decimal in '{num_str}'")
        try:
            val = float(num_str.replace("~", "-"))
        except:
            raise LexicalError(pos, f"Invalid decimal literal '{num_str}'")
        if val < MIN_FLOAT or val > MAX_FLOAT:
            raise LexicalError(pos, f"Decimal literal out of range '{num_str}'")

    return tok
