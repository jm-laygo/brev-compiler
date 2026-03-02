from backend.tokens import Token, TK_LIT_INT, TK_LIT_DECIMAL
from backend.errors import LexicalError
from backend.delimiters import int_decdelim, format_expected_delims

MAX_INT_DIGITS = 9
MAX_FRAC_DIGITS = 9

def accept_number(lexer, tokens, errors, start_pos, raw_value, allowed_delims, has_dot):
    if isinstance(allowed_delims, str):
        allowed_delims = {allowed_delims}

    ch = lexer.current_char
    if ch == "\r":
        ch = "\n"

    expected = format_expected_delims(allowed_delims)

    if ch is None and None not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Missing delimiter after number '{raw_value}'. Expected: {expected}"))
        return True

    if ch is not None and ch not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after number '{raw_value}'. Expected: {expected}"))
        return True

    tok_type = TK_LIT_DECIMAL if has_dot else TK_LIT_INT
    tokens.append(Token(tok_type, raw_value, start_pos))
    return True

def _consume_number_tail(lexer):
    while lexer.current_char is not None and (
        lexer.current_char.isalnum()
        or lexer.current_char in {".", "_", "~"}
    ):
        lexer.advance()

def scan_numbers(lexer, tokens, errors):
    ch = lexer.current_char
    if ch is None:
        return False

    if not (ch.isdigit() or (ch == "~" and (lexer.peek() or "").isdigit())):
        return False

    start_pos = lexer.pos.copy()
    text = ""
    has_dot = False
    int_digits = 0
    frac_digits = 0
    saw_digit_after_dot = False

    if lexer.current_char == "~":
        text += "~"
        lexer.advance()
        if lexer.current_char is None or not lexer.current_char.isdigit():
            errors.append(LexicalError(start_pos, "Invalid number literal '~' (expected digit after ~)"))
            return True

    while lexer.current_char is not None:
        ch = lexer.current_char

        if ch.isdigit():
            if not has_dot:
                int_digits += 1
                if int_digits > MAX_INT_DIGITS:
                    _consume_number_tail(lexer)
                    errors.append(LexicalError(start_pos, f"Integer part exceeds {MAX_INT_DIGITS} digits"))
                    return True
            else:
                frac_digits += 1
                saw_digit_after_dot = True
                if frac_digits > MAX_FRAC_DIGITS:
                    _consume_number_tail(lexer)
                    errors.append(LexicalError(start_pos, f"Fractional part exceeds {MAX_FRAC_DIGITS} digits"))
                    return True

            text += ch
            lexer.advance()
            continue

        if ch == ".":
            if has_dot:
                _consume_number_tail(lexer)
                errors.append(LexicalError(start_pos, f"Multiple decimal points in number '{text + ch}'"))
                return True
            if int_digits == 0:
                _consume_number_tail(lexer)
                errors.append(LexicalError(start_pos, "Decimal must have integer part before '.'"))
                return True
            has_dot = True
            text += ch
            lexer.advance()
            continue

        if ch.isalpha() or ch == "_":
            _consume_number_tail(lexer)
            errors.append(LexicalError(start_pos, f"Invalid identifier starting with digit '{text + ch}'"))
            return True

        if ch in int_decdelim:
            break

        _consume_number_tail(lexer)
        errors.append(LexicalError(start_pos, f"Invalid character '{ch}' in number '{text}'"))
        return True

    if has_dot and not saw_digit_after_dot:
        errors.append(LexicalError(start_pos, f"Decimal point requires digits after '.' in '{text}'"))
        return True

    return accept_number(lexer, tokens, errors, start_pos, text, int_decdelim, has_dot)