from lexer.tokens import Token
from lexer.tokens import *
from lexer.delimiters import idnt_delim, ALPHA_DIG
from lexer.errors import LexicalError

def scan_alphabet_manual(lexer, tokens, errors, line):
    ident_str = ''
    pos = lexer.pos.copy()

    save_pos = lexer.pos.copy()
    save_char = lexer.current_char
    save_str = ident_str

    # LETTER A
    if lexer.current_char is not None and lexer.current_char == "a":
        ident_str = "a"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # ABSOLUTION
        if lexer.current_char is not None and lexer.current_char == "b":
            ident_str += lexer.current_char
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "s":
                ident_str += lexer.current_char
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "o":
                    ident_str += lexer.current_char
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "l":
                        ident_str += lexer.current_char
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "u":
                            ident_str += lexer.current_char
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "t":
                                ident_str += lexer.current_char
                                lexer.advance()

                                if lexer.current_char is not None and lexer.current_char == "i":
                                    ident_str += lexer.current_char
                                    lexer.advance()

                                    if lexer.current_char is not None and lexer.current_char == "o":
                                        ident_str += lexer.current_char
                                        lexer.advance()

                                        if lexer.current_char is not None and lexer.current_char == "n":
                                            ident_str += lexer.current_char
                                            lexer.advance()

                                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                                tokens.append(Token(TK_CF_ABSOLUTION, ident_str, line))
                                                return True
                                            else:
                                                errors.append(LexicalError(
                                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                                lexer.advance()
                                                return True

        # BACKTRACK FOR ABSOLVE
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str   # "a"

        # ABSOLVE
        if lexer.current_char is not None and lexer.current_char == "b":
            ident_str += lexer.current_char
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "s":
                ident_str += lexer.current_char
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "o":
                    ident_str += lexer.current_char
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "l":
                        ident_str += lexer.current_char
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "v":
                            ident_str += lexer.current_char
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "e":
                                ident_str += lexer.current_char
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_CF_ABSOLVE, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(pos,
                                        f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

    # LETTER D
    if lexer.current_char is not None and lexer.current_char == "d":
        ident_str = "d"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # DECREE
        if lexer.current_char is not None and lexer.current_char == "e":
            ident_str += "e"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "c":
                ident_str += "c"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "r":
                    ident_str += "r"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "e":
                            ident_str += "e"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_CF_DECREE, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # BACKTRACK FOR DISCERN / DISMISS / DIVINE
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str     # "d"

        if lexer.current_char is not None and lexer.current_char == "i":
            ident_str += "i"
            lexer.advance()

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str     # "di"

            # DISCERN
            if lexer.current_char is not None and lexer.current_char == "s":
                ident_str += "s"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "r":
                            ident_str += "r"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "n":
                                ident_str += "n"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_CF_DISCERN, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(
                                        pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

            # BACKTRACK FOR DISMISS
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str     # "di"

            if lexer.current_char is not None and lexer.current_char == "s":
                ident_str += "s"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "m":
                    ident_str += "m"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "i":
                        ident_str += "i"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "s":
                            ident_str += "s"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "s":
                                ident_str += "s"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_CF_DISMISS, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(
                                        pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

            # BACKTRACK FOR DIVINE
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str     # "di"

            if lexer.current_char is not None and lexer.current_char == "v":
                ident_str += "v"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "i":
                    ident_str += "i"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "n":
                        ident_str += "n"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "e":
                            ident_str += "e"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_DTYPE_DIVINE, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # IDENTIFIER
        ident_str = "d"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True


    # LETTER E
    if lexer.current_char is not None and lexer.current_char == "e":
        ident_str = "e"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # EDICT
        if lexer.current_char is not None and lexer.current_char == "d":
            ident_str += "d"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "i":
                ident_str += "i"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "t":
                        ident_str += "t"
                        lexer.advance()

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_CF_EDICT, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(
                                pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

        # BACKTRACK FOR ENDURE
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # ENDURE
        if lexer.current_char is not None and lexer.current_char == "n":
            ident_str += "n"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "d":
                ident_str += "d"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "u":
                    ident_str += "u"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "r":
                        ident_str += "r"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "e":
                            ident_str += "e"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_CF_ENDURE, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # IDENTIFIER
        ident_str = "e"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER G
    if lexer.current_char is not None and lexer.current_char == "g":
        ident_str = "g"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # GENESIS
        if lexer.current_char is not None and lexer.current_char == "e":
            ident_str += "e"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "n":
                ident_str += "n"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "e":
                    ident_str += "e"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "s":
                        ident_str += "s"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "i":
                            ident_str += "i"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "s":
                                ident_str += "s"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_OTHERS_MAIN, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(
                                        pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

        # BACKTRACK FOR GRACE
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str   # "g"

        # GRACE
        if lexer.current_char is not None and lexer.current_char == "r":
            ident_str += "r"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "a":
                ident_str += "a"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_CF_GRACE, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(
                                pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

        # IDENTIFIER
        ident_str = "g"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER H
    if lexer.current_char is not None and lexer.current_char == "h":
        ident_str = "h"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # HOLLOW
        if lexer.current_char is not None and lexer.current_char == "o":
            ident_str += "o"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "l":
                ident_str += "l"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "l":
                    ident_str += "l"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "o":
                        ident_str += "o"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "w":
                            ident_str += "w"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_DTYPE_HOLLOW, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # BACKTRACK FOR HOLY
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str   # "h"

        if lexer.current_char is not None and lexer.current_char == "o":
            ident_str += "o"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "l":
                ident_str += "l"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "y":
                    ident_str += "y"
                    lexer.advance()

                    if lexer.current_char is None or lexer.current_char in idnt_delim:
                        tokens.append(Token(TK_OTHERS_HOLY, ident_str, line))
                        return True
                    else:
                        errors.append(LexicalError(
                            pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                        lexer.advance()
                        return True

        # IDENTIFIER
        ident_str = "h"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER M
    if lexer.current_char is not None and lexer.current_char == "m":
        ident_str = "m"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # MASSOF
        if lexer.current_char is not None and lexer.current_char == "a":
            ident_str += "a"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "s":
                ident_str += "s"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "s":
                    ident_str += "s"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "o":
                        ident_str += "o"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "f":
                            ident_str += "f"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_OTHERS_MASSOF, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # IDENTIFIER
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER O
    if lexer.current_char is not None and lexer.current_char == "o":
        ident_str = "o"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # ORDAIN
        if lexer.current_char is not None and lexer.current_char == "r":
            ident_str += "r"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "d":
                ident_str += "d"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "a":
                    ident_str += "a"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "i":
                        ident_str += "i"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "n":
                            ident_str += "n"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_OTHERS_ORDAIN, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

        # BACKTRACK FOR ORDER
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # ORDER
        if lexer.current_char is not None and lexer.current_char == "r":
            ident_str += "r"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "d":
                ident_str += "d"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "e":
                    ident_str += "e"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "r":
                        ident_str += "r"
                        lexer.advance()

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_OTHERS_ORDER, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(
                                pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

        # IDENTIFIER
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER P
    if lexer.current_char is not None and lexer.current_char == "p":
        ident_str = "p"
        pos = lexer.pos.copy()
        lexer.advance()

        if lexer.current_char is not None and lexer.current_char == "r":
            ident_str += "r"
            lexer.advance()

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            # PROCEED
            if lexer.current_char is not None and lexer.current_char == "o":
                ident_str += "o"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "e":
                            ident_str += "e"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "d":
                                ident_str += "d"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_CF_PROCEED, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

            # BACKTRACK FOR PROCLAIM
            lexer.pos = save_pos.copy()
            lexer.current_char = save_char
            ident_str = save_str

            if lexer.current_char is not None and lexer.current_char == "o":
                ident_str += "o"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "l":
                        ident_str += "l"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "a":
                            ident_str += "a"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "i":
                                ident_str += "i"
                                lexer.advance()

                                if lexer.current_char is not None and lexer.current_char == "m":
                                    ident_str += "m"
                                    lexer.advance()

                                    if lexer.current_char is None or lexer.current_char in idnt_delim:
                                        tokens.append(Token(TK_IO_PROCLAIM, ident_str, line))
                                        return True
                                    else:
                                        errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                        lexer.advance()
                                        return True

            # BACKTRACK FOR PROCESSION (REAL FIX)
            lexer.pos = save_pos.copy()
            lexer.current_char = save_char
            ident_str = save_str

            if lexer.current_char is not None and lexer.current_char == "o":
                ident_str += "o"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "c":
                    ident_str += "c"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "s":
                            ident_str += "s"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "s":
                                ident_str += "s"
                                lexer.advance()

                                if lexer.current_char is not None and lexer.current_char == "i":
                                    ident_str += "i"
                                    lexer.advance()

                                    if lexer.current_char is not None and lexer.current_char == "o":
                                        ident_str += "o"
                                        lexer.advance()

                                        if lexer.current_char is not None and lexer.current_char == "n":
                                            ident_str += "n"
                                            lexer.advance()

                                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                                tokens.append(Token(TK_CF_PROCESSION, ident_str, line))
                                                return True
                                            else:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                                lexer.advance()
                                                return True

        ident_str = "p"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True


    # LETTER R
    if lexer.current_char is not None and lexer.current_char == "r":
        ident_str = "r"
        pos = lexer.pos.copy()
        lexer.advance()

        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # RECEIVE
        if lexer.current_char is not None and lexer.current_char == "e":
            ident_str += "e"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "c":
                ident_str += "c"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "e":
                    ident_str += "e"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "i":
                        ident_str += "i"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "v":
                            ident_str += "v"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "e":
                                ident_str += "e"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_IO_RECEIVE, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(
                                        pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

        # BACKTRACK FOR RITUAL / RITE
        lexer.pos = save_pos
        lexer.current_char = save_char
        ident_str = save_str

        # RITUAL / RITE
        if lexer.current_char is not None and lexer.current_char == "i":
            ident_str += "i"
            lexer.advance()

            save_pos2 = lexer.pos.copy()
            save_char2 = lexer.current_char
            save_str2 = ident_str

            # RITUAL
            if lexer.current_char is not None and lexer.current_char == "t":
                ident_str += "t"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "u":
                    ident_str += "u"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "a":
                        ident_str += "a"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "l":
                            ident_str += "l"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_CF_RITUAL, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(
                                    pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

            # BACKTRACK FOR RITE
            lexer.pos = save_pos2
            lexer.current_char = save_char2
            ident_str = save_str2

            if lexer.current_char is not None and lexer.current_char == "t":
                ident_str += "t"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "e":
                    ident_str += "e"
                    lexer.advance()

                    if lexer.current_char is None or lexer.current_char in idnt_delim:
                        tokens.append(Token(TK_CF_RITE, ident_str, line))
                        return True
                    else:
                        errors.append(LexicalError(
                            pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                        lexer.advance()
                        return True

        # IDENTIFIER
        ident_str = "r"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER S
    if lexer.current_char is not None and lexer.current_char == "s":
        ident_str = "s"
        pos = lexer.pos.copy()
        lexer.advance()

        # SACRED
        if lexer.current_char is not None and lexer.current_char == "a":
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            ident_str += "a"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "c":
                ident_str += "c"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "r":
                    ident_str += "r"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "d":
                            ident_str += "d"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_CONST, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

        # SCRIPTURE
        if lexer.current_char is not None and lexer.current_char == "c":
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            ident_str += "c"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "r":
                ident_str += "r"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "i":
                    ident_str += "i"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "p":
                        ident_str += "p"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "t":
                            ident_str += "t"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "u":
                                ident_str += "u"
                                lexer.advance()

                                if lexer.current_char is not None and lexer.current_char == "r":
                                    ident_str += "r"
                                    lexer.advance()

                                    if lexer.current_char is not None and lexer.current_char == "e":
                                        ident_str += "e"
                                        lexer.advance()

                                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                                            tokens.append(Token(TK_DTYPE_SCRIPTURE, ident_str, line))
                                            return True
                                        else:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                            lexer.advance()
                                            return True

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

        # SIGIL
        if lexer.current_char is not None and lexer.current_char == "i":
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            ident_str += "i"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "g":
                ident_str += "g"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "i":
                    ident_str += "i"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "l":
                        ident_str += "l"
                        lexer.advance()

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_DTYPE_SIGIL, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

        # IDENTIFIER
        ident_str = "s"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER T
    if lexer.current_char is not None and lexer.current_char == "t":
        ident_str = "t"
        pos = lexer.pos.copy()
        lexer.advance()

        # TALLY
        if lexer.current_char is not None and lexer.current_char == "a":
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            ident_str += "a"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "l":
                ident_str += "l"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "l":
                    ident_str += "l"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "y":
                        ident_str += "y"
                        lexer.advance()

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_DTYPE_TALLY, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

        # IDENTIFIER
        ident_str = "t"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER U
    if lexer.current_char is not None and lexer.current_char == "u":
        ident_str = "u"
        pos = lexer.pos.copy()
        lexer.advance()

        # UNHOLY
        if lexer.current_char is not None and lexer.current_char == "n":
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            ident_str += "n"
            lexer.advance()

            if lexer.current_char is not None and lexer.current_char == "h":
                ident_str += "h"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "o":
                    ident_str += "o"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "l":
                        ident_str += "l"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "y":
                            ident_str += "y"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_OTHERS_UNHOLY, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

        # IDENTIFIER
        ident_str = "u"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True

    # LETTER V
    if lexer.current_char is not None and lexer.current_char == "v":
        ident_str = "v"
        pos = lexer.pos.copy()
        lexer.advance()

        if lexer.current_char is not None and lexer.current_char == "e":
            ident_str += "e"
            lexer.advance()

            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            # VERITY
            if lexer.current_char is not None and lexer.current_char == "r":
                ident_str += "r"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "i":
                    ident_str += "i"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "t":
                        ident_str += "t"
                        lexer.advance()

                        if lexer.current_char is not None and lexer.current_char == "y":
                            ident_str += "y"
                            lexer.advance()

                            if lexer.current_char is None or lexer.current_char in idnt_delim:
                                tokens.append(Token(TK_DTYPE_VERITY, ident_str, line))
                                return True
                            else:
                                errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                lexer.advance()
                                return True

            # BACKTRACK FOR VERSE / VERSEOF
            lexer.pos = save_pos
            lexer.current_char = save_char
            ident_str = save_str

            # VERSE
            if lexer.current_char is not None and lexer.current_char == "r":
                ident_str += "r"
                lexer.advance()

                if lexer.current_char is not None and lexer.current_char == "s":
                    ident_str += "s"
                    lexer.advance()

                    if lexer.current_char is not None and lexer.current_char == "e":
                        ident_str += "e"
                        lexer.advance()

                        # Check VERSEOF
                        if lexer.current_char is not None and lexer.current_char == "o":
                            save_pos2 = lexer.pos.copy()
                            save_char2 = lexer.current_char
                            save_str2 = ident_str

                            ident_str += "o"
                            lexer.advance()

                            if lexer.current_char is not None and lexer.current_char == "f":
                                ident_str += "f"
                                lexer.advance()

                                if lexer.current_char is None or lexer.current_char in idnt_delim:
                                    tokens.append(Token(TK_OTHERS_VERSEOF, ident_str, line))
                                    return True
                                else:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                                    lexer.advance()
                                    return True

                            lexer.pos = save_pos2
                            lexer.current_char = save_char2
                            ident_str = save_str2

                        if lexer.current_char is None or lexer.current_char in idnt_delim:
                            tokens.append(Token(TK_CF_VERSE, ident_str, line))
                            return True
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{lexer.current_char}' after '{ident_str}'"))
                            lexer.advance()
                            return True

        # IDENTIFIER
        ident_str = "v"
        while lexer.current_char is not None and lexer.current_char in ALPHA_DIG + "_":
            ident_str += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_IDENTIFIER, ident_str, line))
        return True