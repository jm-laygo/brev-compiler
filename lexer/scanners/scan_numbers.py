from lexer.tokens import Token, TK_LIT_INT, TK_LIT_DECIMAL
from lexer.errors import LexicalError
from lexer.delimiters import *
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

    # Negative sign
    if lexer.current_char == "~":
        negative = True
        num_str += "~"
        lexer.advance()
        if lexer.current_char is None or lexer.current_char not in DIGITS:
            raise LexicalError(pos, f"Invalid number literal '{num_str}'")

    if lexer.current_char not in DIGITS:
        return None

    num_str += lexer.current_char
    lexer.advance()

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

        if ch in ALPHABET or ch == "_":
            raise LexicalError(pos, f"Invalid character '{ch}' inside number '{num_str}'")
        
        if ch in idnt_delim:
            break

        raise LexicalError(pos, f"Invalid character '{ch}' after number '{num_str}'")

    if not has_dot:
        try:
            val = int(num_str.replace("~", "-"))
        except:
            raise LexicalError(pos, f"Invalid integer literal '{num_str}'")
        if val < MIN_INT or val > MAX_INT:
            raise LexicalError(pos, f"Integer literal out of range '{num_str}'")
        return Token(TK_LIT_INT, num_str, pos)

    try:
        val = float(num_str.replace("~", "-"))
    except:
        raise LexicalError(pos, f"Invalid decimal literal '{num_str}'")
    if val < MIN_FLOAT or val > MAX_FLOAT:
        raise LexicalError(pos, f"Decimal literal out of range '{num_str}'")
    if "." not in num_str:
        raise LexicalError(pos, f"Decimal literal must have decimal point '{num_str}'")
    return Token(TK_LIT_DECIMAL, num_str, pos)
