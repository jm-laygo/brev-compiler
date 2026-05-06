class Token:
    def __init__(self, tokenType, tokenValue=None, tokenPosition=None):
        if isinstance(tokenType, str):
            self.type = tokenType.strip()
        else:
            self.type = tokenType

        self.value = tokenValue
        self.position = tokenPosition

    def displayName(self):
        return TOKEN_DISPLAY_NAMES.get(self.type, self.type)

    def toDictionary(self):
        positionDictionary = None

        # int position
        if isinstance(self.position, int):
            positionDictionary = {
                "index": self.position,
                "line": None,
                "column": None
            }

        # normal position
        elif self.position:
            positionDictionary = {
                "index": self.position.characterIndex,
                "line": self.position.lineNumber,
                "column": self.position.columnNumber
            }

        return {
            "value": self.value,
            "token": self.displayName(),
            "type": self.type,
            "position": positionDictionary,
            "hidden": self.type == TK_EOF,
        }

    def __repr__(self):
        return f"{self.type}:{self.value}"


# token type

# i/o tokens
TK_IO_RECEIVE = "TK_IO_RECEIVE"
TK_IO_PROCLAIM = "TK_IO_PROCLAIM"

# data types
TK_DTYPE_SIGIL = "TK_DTYPE_SIGIL"
TK_DTYPE_TALLY = "TK_DTYPE_TALLY"
TK_DTYPE_DIVINE = "TK_DTYPE_DIVINE"
TK_DTYPE_SCRIPTURE = "TK_DTYPE_SCRIPTURE"
TK_DTYPE_HOLLOW = "TK_DTYPE_HOLLOW"
TK_DTYPE_VERITY = "TK_DTYPE_VERITY"

# control flow
TK_CF_DECREE = "TK_CF_DECREE"
TK_CF_ABSOLUTION = "TK_CF_ABSOLUTION"
TK_CF_EDICT = "TK_CF_EDICT"
TK_CF_DISCERN = "TK_CF_DISCERN"
TK_CF_VERSE = "TK_CF_VERSE"
TK_CF_GRACE = "TK_CF_GRACE"
TK_CF_ABSOLVE = "TK_CF_ABSOLVE"
TK_CF_FALL = "TK_CF_FALL"
TK_CF_PROCEED = "TK_CF_PROCEED"
TK_CF_PROCESSION = "TK_CF_PROCESSION"
TK_CF_ENDURE = "TK_CF_ENDURE"
TK_CF_RITUAL = "TK_CF_RITUAL"
TK_CF_RITE = "TK_CF_RITE"
TK_CF_DISMISS = "TK_CF_DISMISS"

# qualifiers
TK_SACRED = "TK_SACRED"

# miscel keywords
TK_OTHERS_GENESIS = "TK_OTHERS_GENESIS"
# TK_OTHERS_HOLY = "TK_OTHERS_HOLY"
# TK_OTHERS_UNHOLY = "TK_OTHERS_UNHOLY"
TK_OTHERS_ORDER = "TK_OTHERS_ORDER"
TK_OTHERS_ORDAIN = "TK_OTHERS_ORDAIN"
TK_OTHERS_VERSEOF = "TK_OTHERS_VERSEOF"

# operators
TK_OP_PLUS = "TK_OP_PLUS"
TK_OP_MINUS = "TK_OP_MINUS"
TK_OP_MUL = "TK_OP_MUL"
TK_OP_DIV = "TK_OP_DIV"
TK_OP_MOD = "TK_OP_MOD"
TK_OP_POW = "TK_OP_POW"

TK_OP_ASSIGN = "TK_OP_ASSIGN"
TK_OP_PLUS_EQ = "TK_OP_PLUS_EQ"
TK_OP_MINUS_EQ = "TK_OP_MINUS_EQ"
TK_OP_MUL_EQ = "TK_OP_MUL_EQ"
TK_OP_DIV_EQ = "TK_OP_DIV_EQ"
TK_OP_MOD_EQ = "TK_OP_MOD_EQ"
TK_OP_POW_EQ = "TK_OP_POW_EQ"

TK_OP_EQ = "TK_OP_EQ"
TK_OP_NOT_EQ = "TK_OP_NOT_EQ"
TK_OP_GT = "TK_OP_GT"
TK_OP_LT = "TK_OP_LT"
TK_OP_GTE = "TK_OP_GTE"
TK_OP_LTE = "TK_OP_LTE"

TK_OP_AND = "TK_OP_AND"
TK_OP_OR = "TK_OP_OR"
TK_OP_NOT = "TK_OP_NOT"

TK_OP_INC = "TK_OP_INC"
TK_OP_DEC = "TK_OP_DEC"
TK_OP_CONCAT = "TK_OP_CONCAT"

# symbols
TK_SYM_SPACE = "TK_SYM_SPACE"
TK_SYM_NEWLINE = "TK_SYM_NEWLINE"
TK_SYM_TAB = "TK_SYM_TAB"

TK_SYM_COMMA = "TK_SYM_COMMA"
TK_SYM_SEMICOL = "TK_SYM_SEMICOL"
TK_SYM_COLON = "TK_SYM_COLON"
TK_SYM_DOT = "TK_SYM_DOT"

TK_SYM_OPPAREN = "TK_SYM_OPPAREN"
TK_SYM_CLSPAREN = "TK_SYM_CLSPAREN"

TK_SYM_OPBRACK = "TK_SYM_OPBRACK"
TK_SYM_CLSBRACK = "TK_SYM_CLSBRACK"

TK_SYM_OPBRACE = "TK_SYM_OPBRACE"
TK_SYM_CLSBRACE = "TK_SYM_CLSBRACE"

# literals
TK_LIT_INT = "TK_LIT_INT"
TK_LIT_DECIMAL = "TK_LIT_DECIMAL"
TK_LIT_CHAR = "TK_LIT_CHAR"
TK_LIT_STRING = "TK_LIT_STRING"
TK_LIT_BOOL = "TK_LIT_BOOL"

# special
TK_IDENTIFIER = "TK_IDENTIFIER"
TK_COMMENT = "TK_COMMENT"
TK_COMMENT_BLOCK = "TK_COMMENT_BLOCK"
TK_EOF = "TK_EOF"


KEYWORD_MAP = {
    # i/o
    "receive": TK_IO_RECEIVE,
    "proclaim": TK_IO_PROCLAIM,

    # data types
    "sigil": TK_DTYPE_SIGIL,
    "tally": TK_DTYPE_TALLY,
    "divine": TK_DTYPE_DIVINE,
    "scripture": TK_DTYPE_SCRIPTURE,
    "hollow": TK_DTYPE_HOLLOW,
    "verity": TK_DTYPE_VERITY,

    # control flow
    "decree": TK_CF_DECREE,
    "absolution": TK_CF_ABSOLUTION,
    "edict": TK_CF_EDICT,
    "discern": TK_CF_DISCERN,
    "verse": TK_CF_VERSE,
    "grace": TK_CF_GRACE,
    "absolve": TK_CF_ABSOLVE,
    "proceed": TK_CF_PROCEED,
    "fall": TK_CF_FALL,
    "procession": TK_CF_PROCESSION,
    "endure": TK_CF_ENDURE,
    "ritual": TK_CF_RITUAL,
    "rite": TK_CF_RITE,
    "dismiss": TK_CF_DISMISS,

    # qualifier
    "sacred": TK_SACRED,
    

    # misc
    "genesis": TK_OTHERS_GENESIS,
    # "holy": TK_OTHERS_HOLY,
    # "unholy": TK_OTHERS_UNHOLY,
    "order": TK_OTHERS_ORDER,
    "ordain": TK_OTHERS_ORDAIN,
    "verseof": TK_OTHERS_VERSEOF,
}


# display names
TOKEN_DISPLAY_NAMES = {
    TK_IDENTIFIER: "identifier",

    TK_LIT_INT: "integer literal",
    TK_LIT_DECIMAL: "decimal literal",
    TK_LIT_CHAR: "char literal",
    TK_LIT_STRING: "string literal",
    TK_LIT_BOOL: "boolean literal",

    TK_IO_RECEIVE: "receive",
    TK_IO_PROCLAIM: "proclaim",

    TK_DTYPE_SIGIL: "sigil",
    TK_DTYPE_TALLY: "tally",
    TK_DTYPE_DIVINE: "divine",
    TK_DTYPE_SCRIPTURE: "scripture",
    TK_DTYPE_HOLLOW: "hollow",
    TK_DTYPE_VERITY: "verity",

    TK_CF_DECREE: "decree",
    TK_CF_ABSOLUTION: "absolution",
    TK_CF_EDICT: "edict",
    TK_CF_DISCERN: "discern",
    TK_CF_VERSE: "verse",
    TK_CF_GRACE: "grace",
    TK_CF_ABSOLVE: "absolve",
    TK_CF_PROCEED: "proceed",
    TK_CF_FALL: "fall",
    TK_CF_PROCESSION: "procession",
    TK_CF_ENDURE: "endure",
    TK_CF_RITUAL: "ritual",
    TK_CF_RITE: "rite",
    TK_CF_DISMISS: "dismiss",

    TK_SACRED: "sacred",

    TK_OTHERS_GENESIS: "genesis",
    # TK_OTHERS_HOLY: "holy",
    # TK_OTHERS_UNHOLY: "unholy",
    TK_OTHERS_ORDER: "order",
    TK_OTHERS_ORDAIN: "ordain",
    TK_OTHERS_VERSEOF: "verseof",

    TK_OP_PLUS: "+",
    TK_OP_MINUS: "-",
    TK_OP_MUL: "*",
    TK_OP_DIV: "/",
    TK_OP_MOD: "%",
    TK_OP_POW: "**",
    TK_OP_ASSIGN: "=",

    TK_OP_EQ: "==",
    TK_OP_NOT_EQ: "!=",
    TK_OP_GT: ">",
    TK_OP_LT: "<",
    TK_OP_GTE: ">=",
    TK_OP_LTE: "<=",
    TK_OP_PLUS_EQ: "+=",
    TK_OP_MINUS_EQ: "-=",
    TK_OP_MUL_EQ: "*=",
    TK_OP_DIV_EQ: "/=",
    TK_OP_MOD_EQ: "%=",
    TK_OP_POW_EQ: "**=",

    TK_OP_AND: "&&",
    TK_OP_OR: "||",
    TK_OP_NOT: "!!",

    TK_OP_INC: "++",
    TK_OP_DEC: "--",
    TK_OP_CONCAT: "&",

    TK_SYM_SPACE: "space",
    TK_SYM_NEWLINE: "newline",
    TK_SYM_TAB: "tab",

    TK_SYM_COMMA: ",",
    TK_SYM_SEMICOL: ";",
    TK_SYM_COLON: ":",
    TK_SYM_DOT: ".",

    TK_SYM_OPPAREN: "(",
    TK_SYM_CLSPAREN: ")",
    TK_SYM_OPBRACK: "[",
    TK_SYM_CLSBRACK: "]",
    TK_SYM_OPBRACE: "{",
    TK_SYM_CLSBRACE: "}",

    TK_COMMENT: "comment",
    TK_COMMENT_BLOCK: "block comment",

    TK_EOF: "End of File",
}