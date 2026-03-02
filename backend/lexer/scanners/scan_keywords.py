from backend.tokens import *
from backend.delimiters import *
from backend.errors import LexicalError
from backend.delimiters import format_expected_delims

def scan_keywords_manual(lexer, tokens, errors):
    def restore(saved_pos):
        lexer.pos = saved_pos.copy()
        if 0 <= lexer.pos.index < len(lexer.source_code):
            lexer.current_char = lexer.source_code[lexer.pos.index]
        else:
            lexer.current_char = None

    def is_ident_char(ch):
        return ch is not None and ch in (ALPHA_DIG + "_")

    def accept_keyword(tok_type, ident_str, start_pos, allowed_delims):
        if isinstance(allowed_delims, str):
            allowed_delims = {allowed_delims}

        ch = lexer.current_char
        if ch == "\r":
            ch = "\n"

        expected = format_expected_delims(allowed_delims)

        if ch is not None and (ch.isalnum() or ch == "_"):
            restore(start_pos)
            return False

        if ch is None and None not in allowed_delims:
            errors.append(LexicalError(start_pos, f"Missing delimiter after '{ident_str}'. Expected: {expected}"))
            return True

        if ch is not None and ch in allowed_delims:
            tokens.append(Token(tok_type, ident_str, start_pos))
            return True

        if ch is not None and ch not in allowed_delims:
            errors.append(LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after '{ident_str}'. Expected: {expected}"))
            return True

        tokens.append(Token(tok_type, ident_str, start_pos))
        return True

    start_pos = lexer.pos.copy()
    first = lexer.current_char
    
    # LETTER A
    if first == "a":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # ABSOLUTION
        restore(save_pos)
        ident_str = "a"
        if lexer.current_char == "b":
            ident_str += "b"; lexer.advance()
            if lexer.current_char == "s":
                ident_str += "s"; lexer.advance()
                if lexer.current_char == "o":
                    ident_str += "o"; lexer.advance()
                    if lexer.current_char == "l":
                        ident_str += "l"; lexer.advance()
                        if lexer.current_char == "u":
                            ident_str += "u"; lexer.advance()
                            if lexer.current_char == "t":
                                ident_str += "t"; lexer.advance()
                                if lexer.current_char == "i":
                                    ident_str += "i"; lexer.advance()
                                    if lexer.current_char == "o":
                                        ident_str += "o"; lexer.advance()
                                        if lexer.current_char == "n":
                                            ident_str += "n"; lexer.advance()
                                            return accept_keyword(TK_CF_ABSOLUTION, ident_str, start_pos, els_delim)

        # ABSOLVE
        restore(save_pos)
        ident_str = "a"
        if lexer.current_char == "b":
            ident_str += "b"; lexer.advance()
            if lexer.current_char == "s":
                ident_str += "s"; lexer.advance()
                if lexer.current_char == "o":
                    ident_str += "o"; lexer.advance()
                    if lexer.current_char == "l":
                        ident_str += "l"; lexer.advance()
                        if lexer.current_char == "v":
                            ident_str += "v"; lexer.advance()
                            if lexer.current_char == "e":
                                ident_str += "e"; lexer.advance()
                                return accept_keyword(TK_CF_ABSOLVE, ident_str, start_pos, {semicolon})
        restore(start_pos)
        return False

    # LETTER D
    if first == "d":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # DECREE
        restore(save_pos)
        ident_str = "d"
        if lexer.current_char == "e":
            ident_str += "e"; lexer.advance()
            if lexer.current_char == "c":
                ident_str += "c"; lexer.advance()
                if lexer.current_char == "r":
                    ident_str += "r"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        if lexer.current_char == "e":
                            ident_str += "e"; lexer.advance()
                            return accept_keyword(TK_CF_DECREE, ident_str, start_pos, {op_par, space})

        # (DISCERN / DISMISS / DIVINE)
        restore(save_pos)
        ident_str = "d"
        if lexer.current_char == "i":
            ident_str_di = "di"
            lexer.advance()
            save_pos_di = lexer.pos.copy()

            # DISCERN
            restore(save_pos_di)
            ident_str = ident_str_di
            if lexer.current_char == "s":
                ident_str += "s"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        if lexer.current_char == "r":
                            ident_str += "r"; lexer.advance()
                            if lexer.current_char == "n":
                                ident_str += "n"; lexer.advance()
                                return accept_keyword(TK_CF_DISCERN, ident_str, start_pos, {op_par, space})

            # DISMISS
            restore(save_pos_di)
            ident_str = ident_str_di
            if lexer.current_char == "s":
                ident_str += "s"; lexer.advance()
                if lexer.current_char == "m":
                    ident_str += "m"; lexer.advance()
                    if lexer.current_char == "i":
                        ident_str += "i"; lexer.advance()
                        if lexer.current_char == "s":
                            ident_str += "s"; lexer.advance()
                            if lexer.current_char == "s":
                                ident_str += "s"; lexer.advance()
                                return accept_keyword(TK_CF_DISMISS, ident_str, start_pos, {space})

            # DIVINE
            restore(save_pos_di)
            ident_str = ident_str_di
            if lexer.current_char == "v":
                ident_str += "v"; lexer.advance()
                if lexer.current_char == "i":
                    ident_str += "i"; lexer.advance()
                    if lexer.current_char == "n":
                        ident_str += "n"; lexer.advance()
                        if lexer.current_char == "e":
                            ident_str += "e"; lexer.advance()
                            return accept_keyword(TK_DTYPE_DIVINE, ident_str, start_pos, {space})

        restore(start_pos)
        return False

    # LETTER E
    if first == "e":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # EDICT
        restore(save_pos)
        ident_str = "e"
        if lexer.current_char == "d":
            ident_str += "d"; lexer.advance()
            if lexer.current_char == "i":
                ident_str += "i"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "t":
                        ident_str += "t"; lexer.advance()
                        return accept_keyword(TK_CF_EDICT, ident_str, start_pos, {op_par, space})

        # ENDURE
        restore(save_pos)
        ident_str = "e"
        if lexer.current_char == "n":
            ident_str += "n"; lexer.advance()
            if lexer.current_char == "d":
                ident_str += "d"; lexer.advance()
                if lexer.current_char == "u":
                    ident_str += "u"; lexer.advance()
                    if lexer.current_char == "r":
                        ident_str += "r"; lexer.advance()
                        if lexer.current_char == "e":
                            ident_str += "e"; lexer.advance()
                            return accept_keyword(TK_CF_ENDURE, ident_str, start_pos, {op_par, space})

        restore(start_pos)
        return False
    # LETTER F
    if first == "f":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # FALL
        restore(save_pos)
        ident_str = "f"
        if lexer.current_char == "a":
            ident_str += "a"; lexer.advance()
            if lexer.current_char == "l":
                ident_str += "l"; lexer.advance()
                if lexer.current_char == "l":
                    ident_str += "l"; lexer.advance()
                    return accept_keyword(TK_CF_FALL, ident_str, start_pos, {semicolon})
                
        restore(start_pos)
        return False

    # LETTER G
    if first == "g":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # GENESIS
        restore(save_pos)
        ident_str = "g"
        if lexer.current_char == "e":
            ident_str += "e"; lexer.advance()
            if lexer.current_char == "n":
                ident_str += "n"; lexer.advance()
                if lexer.current_char == "e":
                    ident_str += "e"; lexer.advance()
                    if lexer.current_char == "s":
                        ident_str += "s"; lexer.advance()
                        if lexer.current_char == "i":
                            ident_str += "i"; lexer.advance()
                            if lexer.current_char == "s":
                                ident_str += "s"; lexer.advance()
                                return accept_keyword(TK_OTHERS_GENESIS, ident_str, start_pos, {op_par})

        # GRACE
        restore(save_pos)
        ident_str = "g"
        if lexer.current_char == "r":
            ident_str += "r"; lexer.advance()
            if lexer.current_char == "a":
                ident_str += "a"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        return accept_keyword(TK_CF_GRACE, ident_str, start_pos, {colon})

        restore(start_pos)
        return False
    
    # LETTER H
    if first == "h":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # HOLLOW
        restore(save_pos)
        ident_str = "h"
        if lexer.current_char == "o":
            ident_str += "o"; lexer.advance()
            if lexer.current_char == "l":
                ident_str += "l"; lexer.advance()
                if lexer.current_char == "l":
                    ident_str += "l"; lexer.advance()
                    if lexer.current_char == "o":
                        ident_str += "o"; lexer.advance()
                        if lexer.current_char == "w":
                            ident_str += "w"; lexer.advance()
                            return accept_keyword(TK_DTYPE_HOLLOW, ident_str, start_pos, {space})

        # HOLY
        restore(save_pos)
        ident_str = "h"
        if lexer.current_char == "o":
            ident_str += "o"; lexer.advance()
            if lexer.current_char == "l":
                ident_str += "l"; lexer.advance()
                if lexer.current_char == "y":
                    ident_str += "y"; lexer.advance()
                    return accept_keyword(TK_OTHERS_HOLY, ident_str, start_pos, bool_delim)

        restore(start_pos)
        return False
    
    # LETTER O
    if first == "o":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # ORDAIN
        restore(save_pos)
        ident_str = "o"
        if lexer.current_char == "r":
            ident_str += "r"; lexer.advance()
            if lexer.current_char == "d":
                ident_str += "d"; lexer.advance()
                if lexer.current_char == "a":
                    ident_str += "a"; lexer.advance()
                    if lexer.current_char == "i":
                        ident_str += "i"; lexer.advance()
                        if lexer.current_char == "n":
                            ident_str += "n"; lexer.advance()
                            return accept_keyword(TK_OTHERS_ORDAIN, ident_str, start_pos, {space})

        # ORDER
        restore(save_pos)
        ident_str = "o"
        if lexer.current_char == "r":
            ident_str += "r"; lexer.advance()
            if lexer.current_char == "d":
                ident_str += "d"; lexer.advance()
                if lexer.current_char == "e":
                    ident_str += "e"; lexer.advance()
                    if lexer.current_char == "r":
                        ident_str += "r"; lexer.advance()
                        return accept_keyword(TK_OTHERS_ORDER, ident_str, start_pos, space)

        restore(start_pos)
        return False

    # LETTER P
    if first == "p":
        lexer.advance()
        save_pos = lexer.pos.copy()

        restore(save_pos)
        ident_str = "p"
        if lexer.current_char == "r":
            ident_str_pr = "pr"
            lexer.advance()
            save_pos_pr = lexer.pos.copy()

            # PROCEED
            restore(save_pos_pr)
            ident_str = ident_str_pr
            if lexer.current_char == "o":
                ident_str += "o"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        if lexer.current_char == "e":
                            ident_str += "e"; lexer.advance()
                            if lexer.current_char == "d":
                                ident_str += "d"; lexer.advance()
                                return accept_keyword(TK_CF_PROCEED, ident_str, start_pos, {semicolon})

            # PROCLAIM
            restore(save_pos_pr)
            ident_str = ident_str_pr
            if lexer.current_char == "o":
                ident_str += "o"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "l":
                        ident_str += "l"; lexer.advance()
                        if lexer.current_char == "a":
                            ident_str += "a"; lexer.advance()
                            if lexer.current_char == "i":
                                ident_str += "i"; lexer.advance()
                                if lexer.current_char == "m":
                                    ident_str += "m"; lexer.advance()
                                    return accept_keyword(TK_IO_PROCLAIM, ident_str, start_pos, {op_par})

            # PROCESSION
            restore(save_pos_pr)
            ident_str = ident_str_pr
            if lexer.current_char == "o":
                ident_str += "o"; lexer.advance()
                if lexer.current_char == "c":
                    ident_str += "c"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        if lexer.current_char == "s":
                            ident_str += "s"; lexer.advance()
                            if lexer.current_char == "s":
                                ident_str += "s"; lexer.advance()
                                if lexer.current_char == "i":
                                    ident_str += "i"; lexer.advance()
                                    if lexer.current_char == "o":
                                        ident_str += "o"; lexer.advance()
                                        if lexer.current_char == "n":
                                            ident_str += "n"; lexer.advance()
                                            return accept_keyword(TK_CF_PROCESSION, ident_str, start_pos, {op_par, space})

        restore(start_pos)
        return False

    # LETTER R
    if first == "r":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # RECEIVE
        restore(save_pos)
        ident_str = "r"
        if lexer.current_char == "e":
            ident_str += "e"; lexer.advance()
            if lexer.current_char == "c":
                ident_str += "c"; lexer.advance()
                if lexer.current_char == "e":
                    ident_str += "e"; lexer.advance()
                    if lexer.current_char == "i":
                        ident_str += "i"; lexer.advance()
                        if lexer.current_char == "v":
                            ident_str += "v"; lexer.advance()
                            if lexer.current_char == "e":
                                ident_str += "e"; lexer.advance()
                                return accept_keyword(TK_IO_RECEIVE, ident_str, start_pos, {op_par})

        # RI* group (RITUAL / RITE)
        restore(save_pos)
        ident_str = "r"
        if lexer.current_char == "i":
            ident_str_ri = "ri"
            lexer.advance()
            save_pos_ri = lexer.pos.copy()

            # RITUAL
            restore(save_pos_ri)
            ident_str = ident_str_ri
            if lexer.current_char == "t":
                ident_str += "t"; lexer.advance()
                if lexer.current_char == "u":
                    ident_str += "u"; lexer.advance()
                    if lexer.current_char == "a":
                        ident_str += "a"; lexer.advance()
                        if lexer.current_char == "l":
                            ident_str += "l"; lexer.advance()
                            return accept_keyword(TK_CF_RITUAL, ident_str, start_pos, {space, op_bra})

            # RITE
            restore(save_pos_ri)
            ident_str = ident_str_ri
            if lexer.current_char == "t":
                ident_str += "t"; lexer.advance()
                if lexer.current_char == "e":
                    ident_str += "e"; lexer.advance()
                    return accept_keyword(TK_CF_RITE, ident_str, start_pos, {space})

        restore(start_pos)
        return False

    # LETTER S
    if first == "s":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # SACRED
        restore(save_pos)
        ident_str = "s"
        if lexer.current_char == "a":
            ident_str += "a"; lexer.advance()
            if lexer.current_char == "c":
                ident_str += "c"; lexer.advance()
                if lexer.current_char == "r":
                    ident_str += "r"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()
                        if lexer.current_char == "d":
                            ident_str += "d"; lexer.advance()
                            return accept_keyword(TK_SACRED, ident_str, start_pos, {space})

        # SCRIPTURE
        restore(save_pos)
        ident_str = "s"
        if lexer.current_char == "c":
            ident_str += "c"; lexer.advance()
            if lexer.current_char == "r":
                ident_str += "r"; lexer.advance()
                if lexer.current_char == "i":
                    ident_str += "i"; lexer.advance()
                    if lexer.current_char == "p":
                        ident_str += "p"; lexer.advance()
                        if lexer.current_char == "t":
                            ident_str += "t"; lexer.advance()
                            if lexer.current_char == "u":
                                ident_str += "u"; lexer.advance()
                                if lexer.current_char == "r":
                                    ident_str += "r"; lexer.advance()
                                    if lexer.current_char == "e":
                                        ident_str += "e"; lexer.advance()
                                        return accept_keyword(TK_DTYPE_SCRIPTURE, ident_str, start_pos, {space})

        # SIGIL
        restore(save_pos)
        ident_str = "s"
        if lexer.current_char == "i":
            ident_str += "i"; lexer.advance()
            if lexer.current_char == "g":
                ident_str += "g"; lexer.advance()
                if lexer.current_char == "i":
                    ident_str += "i"; lexer.advance()
                    if lexer.current_char == "l":
                        ident_str += "l"; lexer.advance()
                        return accept_keyword(TK_DTYPE_SIGIL, ident_str, start_pos, {space})

        restore(start_pos)
        return False

    # LETTER T
    if first == "t":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # TALLY
        restore(save_pos)
        ident_str = "t"
        if lexer.current_char == "a":
            ident_str += "a"; lexer.advance()
            if lexer.current_char == "l":
                ident_str += "l"; lexer.advance()
                if lexer.current_char == "l":
                    ident_str += "l"; lexer.advance()
                    if lexer.current_char == "y":
                        ident_str += "y"; lexer.advance()
                        return accept_keyword(TK_DTYPE_TALLY, ident_str, start_pos, {space})

        restore(start_pos)
        return False

    # LETTER U
    if first == "u":
        lexer.advance()
        save_pos = lexer.pos.copy()

        # UNHOLY
        restore(save_pos)
        ident_str = "u"
        if lexer.current_char == "n":
            ident_str += "n"; lexer.advance()
            if lexer.current_char == "h":
                ident_str += "h"; lexer.advance()
                if lexer.current_char == "o":
                    ident_str += "o"; lexer.advance()
                    if lexer.current_char == "l":
                        ident_str += "l"; lexer.advance()
                        if lexer.current_char == "y":
                            ident_str += "y"; lexer.advance()
                            return accept_keyword(TK_OTHERS_UNHOLY, ident_str, start_pos, bool_delim)

        restore(start_pos)
        return False

    # LETTER V
    if first == "v":
        lexer.advance()
        save_pos = lexer.pos.copy()

        restore(save_pos)
        ident_str = "v"
        if lexer.current_char == "e":
            ident_str_ve = "ve"
            lexer.advance()
            save_pos_ve = lexer.pos.copy()

            # VERITY
            restore(save_pos_ve)
            ident_str = ident_str_ve
            if lexer.current_char == "r":
                ident_str += "r"; lexer.advance()
                if lexer.current_char == "i":
                    ident_str += "i"; lexer.advance()
                    if lexer.current_char == "t":
                        ident_str += "t"; lexer.advance()
                        if lexer.current_char == "y":
                            ident_str += "y"; lexer.advance()
                            return accept_keyword(TK_DTYPE_VERITY, ident_str, start_pos, {space})

            # VERSE / VERSEOF
            restore(save_pos_ve)
            ident_str = ident_str_ve
            if lexer.current_char == "r":
                ident_str += "r"; lexer.advance()
                if lexer.current_char == "s":
                    ident_str += "s"; lexer.advance()
                    if lexer.current_char == "e":
                        ident_str += "e"; lexer.advance()

                        # Try VERSEOF
                        if lexer.current_char == "o":
                            save_pos_o = lexer.pos.copy()
                            ident_str_before = ident_str

                            ident_str += "o"; lexer.advance()
                            if lexer.current_char == "f":
                                ident_str += "f"; lexer.advance()
                                return accept_keyword(TK_OTHERS_VERSEOF, ident_str, start_pos, {op_par})

                            restore(save_pos_o)
                            ident_str = ident_str_before

                        return accept_keyword(TK_CF_VERSE, ident_str, start_pos, {space})

        restore(start_pos)  
        return False

    restore(start_pos)
    return False

def scan_keywords(lexer, tokens, errors):
    return scan_keywords_manual(lexer, tokens, errors)
