# CONSTANTS
ZERO = '0'
DIGITS = '0123456789'
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_DIG = ALPHABET + DIGITS

# BASIC DELIMITERS (single chars)
space      = ' '
newline    = '\n'
tab        = '\t'

comma      = ','
semicolon  = ';'
colon      = ':'
period     = '.'
underscore = '_'

op_par     = '('
cl_par     = ')'
op_brc     = '['
cl_brc     = ']'
op_bra     = '{'
cl_bra     = '}'

id_sym      = set("_" + ALPHA_DIG)

op_delim    = {'+', '-', '*', '/', '%', '!', '&', '|', '=', '>', '<'}
els_delim   = {space, newline, op_bra}
bool_delim = {space, cl_par, cl_brc, semicolon, comma, colon, cl_bra} | op_delim

int_decdelim = {space, semicolon, newline, colon, comma, cl_bra, cl_par, cl_brc} | op_delim
chr_delim    = {space, semicolon, newline, comma, colon, cl_bra, cl_par, '&'}
str_delim    = {comma, semicolon, newline, space, colon, cl_par, cl_bra, '&'}

idnt_delim = {
    space, semicolon, colon, comma, period,
    op_par, cl_par,
    op_brc, cl_brc,
    op_bra, cl_bra,
} | op_delim

delim1  = set(ALPHA_DIG) | {space, '"', op_par}
delim2 = {semicolon, comma, colon, cl_par, cl_brc, cl_bra, space, newline, tab, None} | op_delim | set(ALPHA_DIG)
delim3 = {space, '~', op_par, '!', '+', '-', '"', "'"} | set(ALPHA_DIG)
delim4 = {'"', '~', "'", op_par, '!', '+', '-'} | set(ALPHA_DIG) | {space, newline, op_bra}
delim5  = {space, '~', '"', "'", "!", op_par} | set(ALPHA_DIG)
delim6  = {op_par, cl_par, '!', "'", '"', space} | set(ALPHA_DIG)
delim7  = {semicolon, op_bra, cl_par, '<', '>', '=', '|', '&', '+', '-', '/', '*', '%', space, newline, colon, comma}
delim8  = {cl_brc, op_par, space} | set(ALPHA_DIG)
delim9  = {'=', semicolon, op_brc, cl_par, space, newline}
delim10 = {"'", '"', '~', op_bra, space, newline} | set(ALPHA_DIG)
delim11 = {op_bra, semicolon, cl_bra, comma, space, newline} | set(ALPHABET)
delim12 = {space, "'", '"', op_par} | set(ALPHA_DIG)

asciichr = {chr(i) for i in range(32, 127) if chr(i) != "'"}
asciistr = {chr(i) for i in range(32, 127) if chr(i) != '"'}

_DOCU_PREFIX = [space, newline, tab]

_DOCU_SYMBOLS = [
    comma, semicolon, colon, period,
    op_par, cl_par,
    op_brc, cl_brc,
    op_bra, cl_bra,
]

_DOCU_OPS = ['+', '-', '*', '/', '%', '!', '&', '|', '=', '>', '<']

_DOCU_EOF = [None]

DOCU_DELIM_ORDER = _DOCU_PREFIX + _DOCU_SYMBOLS + _DOCU_OPS + _DOCU_EOF

def format_expected_delims(allowed):
    if not allowed:
        return "(none)"

    remaining = set(allowed)
    parts = []

    DIGIT_SET = set(DIGITS)
    ALPHA_SET = set(ALPHABET)
    ALPHA_DIG_SET = set(ALPHA_DIG)

    if space in remaining:
        parts.append("space")
        remaining.remove(space)

    if comma in remaining:
        parts.append("comma")
        remaining.remove(comma)

    if semicolon in remaining:
        parts.append("semicolon")
        remaining.remove(semicolon)

    if colon in remaining:
        parts.append("colon")
        remaining.remove(colon)

    if period in remaining:
        parts.append("period")
        remaining.remove(period)

    if newline in remaining:
        parts.append("newline")
        remaining.remove(newline)

    if tab in remaining:
        parts.append("tab")
        remaining.remove(tab)

    if None in remaining:
        parts.append("EOF")
        remaining.remove(None)

    for d in DOCU_DELIM_ORDER:
        if d in (space, newline, tab, None):
            continue
        if d in remaining:
            parts.append(repr(d))
            remaining.remove(d)

    if ALPHA_DIG_SET.issubset(remaining):
        parts.append("alphanumeric")
        remaining -= ALPHA_DIG_SET
    else:
        if ALPHA_SET.issubset(remaining):
            parts.append("alphabet")
            remaining -= ALPHA_SET
        if DIGIT_SET.issubset(remaining):
            parts.append("digits")
            remaining -= DIGIT_SET

    for x in sorted(remaining, key=lambda c: str(c)):
        if x in (space, newline, tab, None):
            continue
        parts.append(repr(x))

    return ", ".join(parts) if parts else "(none)"
