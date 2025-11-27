class Token:
    def __init__(self, type_, value=None, pos=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def to_dict(self):
        if isinstance(self.pos, int):
            return {
                "type": self.type,
                "value": self.value,
                "pos": {"index": self.pos, "line": None, "col": None}
            }
        elif self.pos:
            return {
                "type": self.type,
                "value": self.value,
                "pos": {"index": self.pos.index, "line": self.pos.ln, "col": self.pos.col}
            }
        else:
            return {
                "type": self.type,
                "value": self.value,
                "pos": None
            }

    def __repr__(self):
        return f"{self.type}:{self.value}"


# I/O TOKENS
TK_IO_RECEIVE   = "TK_IO_RECEIVE"
TK_IO_PROCLAIM  = "TK_IO_PROCLAIM"

# DATA TYPES
TK_DTYPE_SIGIL      = "TK_DTYPE_SIGIL"
TK_DTYPE_TALLY      = "TK_DTYPE_TALLY"
TK_DTYPE_DIVINE     = "TK_DTYPE_DIVINE"
TK_DTYPE_SCRIPTURE  = "TK_DTYPE_SCRIPTURE"
TK_DTYPE_HOLLOW     = "TK_DTYPE_HOLLOW"
TK_DTYPE_VERITY     = "TK_DTYPE_VERITY"

# CONTROL FLOW TOKENS
TK_CF_DECREE        = "TK_CF_DECREE"
TK_CF_ABSOLUTION    = "TK_CF_ABSOLUTION"
TK_CF_EDICT         = "TK_CF_EDICT"
TK_CF_DISCERN       = "TK_CF_DISCERN"
TK_CF_VERSE         = "TK_CF_VERSE"
TK_CF_GRACE         = "TK_CF_GRACE"
TK_CF_ABSOLVE       = "TK_CF_ABSOLVE"
TK_CF_PROCEED       = "TK_CF_PROCEED"
TK_CF_PROCESSION    = "TK_CF_PROCESSION"
TK_CF_ENDURE        = "TK_CF_ENDURE"
TK_CF_RITUAL        = "TK_CF_RITUAL"
TK_CF_RITE          = "TK_CF_RITE"
TK_CF_DISMISS       = "TK_CF_DISMISS"

# QUALIFIERS
TK_CONST            = "TK_CONST"

# MISC KEYWORDS
TK_OTHERS_MAIN      = "TK_OTHERS_MAIN"
TK_OTHERS_HOLY      = "TK_OTHERS_HOLY"
TK_OTHERS_UNHOLY    = "TK_OTHERS_UNHOLY"
TK_OTHERS_ORDER     = "TK_OTHERS_ORDER"
TK_OTHERS_ORDAIN    = "TK_OTHERS_ORDAIN"
TK_OTHERS_MASSOF    = "TK_OTHERS_MASSOF"
TK_OTHERS_VERSEOF   = "TK_OTHERS_VERSEOF"

# OPERATOR TOKENS
TK_OP_PLUS      = "TK_OP_PLUS"
TK_OP_MINUS     = "TK_OP_MINUS"
TK_OP_MUL       = "TK_OP_MUL"
TK_OP_DIV       = "TK_OP_DIV"
TK_OP_MOD       = "TK_OP_MOD"
TK_OP_POW       = "TK_OP_POW"
TK_OP_TILDE     = "TK_OP_TILDE"

TK_OP_ASSIGN    = "TK_OP_ASSIGN"
TK_OP_PLUS_EQ   = "TK_OP_PLUS_EQ"
TK_OP_MINUS_EQ  = "TK_OP_MINUS_EQ"
TK_OP_MUL_EQ    = "TK_OP_MUL_EQ"
TK_OP_DIV_EQ    = "TK_OP_DIV_EQ"
TK_OP_MOD_EQ    = "TK_OP_MOD_EQ"
TK_OP_POW_EQ    = "TK_OP_POW_EQ"

TK_OP_EQ        = "TK_OP_EQ"
TK_OP_NOTEQ     = "TK_OP_NOTEQ"
TK_OP_GT        = "TK_OP_GT"
TK_OP_LT        = "TK_OP_LT"
TK_OP_GTE       = "TK_OP_GTE"
TK_OP_LTE       = "TK_OP_LTE"

TK_OP_AND       = "TK_OP_AND"
TK_OP_OR        = "TK_OP_OR"
TK_OP_NOT       = "TK_OP_NOT"

TK_OP_INC       = "TK_OP_INC"
TK_OP_DEC       = "TK_OP_DEC"

# SYMBOL TOKENS
TK_SYM_SPACE    = "TK_SYM_SPACE"
TK_SYM_COMMA    = "TK_SYM_COMMA"
TK_SYM_SEMICOL  = "TK_SYM_SEMICOL"
TK_SYM_SINGLEQ  = "TK_SYM_SINGLEQ"
TK_SYM_DOUBLEQ  = "TK_SYM_DOUBLEQ"
TK_SYM_OPPAREN  = "TK_SYM_OPPAREN"
TK_SYM_CLSPAREN = "TK_SYM_CLSPAREN"
TK_SYM_BRACK    = "TK_SYM_BRACK"
TK_SYM_OPBRACK  = "TK_SYM_OPBRACK"
TK_SYM_CLSBRACK = "TK_SYM_CLSBRACK"
TK_SYM_BRACE    = "TK_SYM_BRACE"
TK_SYM_OPBRACE  = "TK_SYM_OPBRACE"
TK_SYM_CLSBRACE = "TK_SYM_CLSBRACE"
TK_SYM_COLON    = "TK_SYM_COLON"
TK_SYM_DOT      = "TK_SYM_DOT"
TK_SYM_AMP      = "TK_SYM_AMP"
TK_SYM_NEWLINE  = "TK_SYM_NEWLINE"

# LITERAL TOKENS
TK_LIT_INT      = "TK_LIT_INT"
TK_LIT_DECIMAL  = "TK_LIT_DECIMAL"
TK_LIT_CHAR     = "TK_LIT_CHAR"
TK_LIT_STRING   = "TK_LIT_STRING"
TK_LIT_BOOL     = "TK_LIT_BOOL"

# SPECIAL TOKENS
TK_IDENTIFIER       = "TK_IDENTIFIER"
TK_COMMENT          = "TK_COMMENT"
TK_COMMENT_BLOCK    = "TK_COMMENT_BLOCK"
