from backend.lexer.tokens import (
    # I/O
    TK_IO_RECEIVE, TK_IO_PROCLAIM,

    # DATA TYPES
    TK_DTYPE_SIGIL, TK_DTYPE_TALLY, TK_DTYPE_DIVINE,
    TK_DTYPE_SCRIPTURE, TK_DTYPE_HOLLOW, TK_DTYPE_VERITY,

    # Control Flow
    TK_CF_DECREE, TK_CF_ABSOLUTION, TK_CF_EDICT, TK_CF_DISCERN,
    TK_CF_VERSE, TK_CF_GRACE, TK_CF_ABSOLVE, TK_CF_PROCEED,
    TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITE, TK_CF_RITUAL,
    TK_CF_DISMISS,

    # QUALIFIERS
    TK_CONST,

    # OTHERS
    TK_OTHERS_MAIN, TK_OTHERS_HOLY, TK_OTHERS_UNHOLY,
    TK_OTHERS_ORDER, TK_OTHERS_ORDAIN, TK_OTHERS_MASSOF,
    TK_OTHERS_VERSEOF
)

RESERVED_WORDS = {
    # I/O
    "receive":      TK_IO_RECEIVE,
    "proclaim":     TK_IO_PROCLAIM,

    # DATA TYPES
    "sigil":        TK_DTYPE_SIGIL,
    "tally":        TK_DTYPE_TALLY,
    "divine":       TK_DTYPE_DIVINE,
    "scripture":    TK_DTYPE_SCRIPTURE,
    "hollow":       TK_DTYPE_HOLLOW,
    "verity":       TK_DTYPE_VERITY,

    # CONTROL FLOW
    "decree":       TK_CF_DECREE,
    "absolution":   TK_CF_ABSOLUTION,
    "edict":        TK_CF_EDICT,
    "discern":      TK_CF_DISCERN,
    "verse":        TK_CF_VERSE,
    "grace":        TK_CF_GRACE,
    "absolve":      TK_CF_ABSOLVE,
    "proceed":      TK_CF_PROCEED,
    "procession":   TK_CF_PROCESSION,
    "endure":       TK_CF_ENDURE,
    "rite":         TK_CF_RITE,
    "ritual":       TK_CF_RITUAL,
    "dismiss":      TK_CF_DISMISS,

    # Qualifier
    "sacred":       TK_CONST,

    # Misc language keywords
    "genesis":      TK_OTHERS_MAIN,
    "holy":         TK_OTHERS_HOLY,
    "unholy":       TK_OTHERS_UNHOLY,
    "order":        TK_OTHERS_ORDER,
    "ordain":       TK_OTHERS_ORDAIN,
    "massof":       TK_OTHERS_MASSOF,
    "verseof":      TK_OTHERS_VERSEOF,
}