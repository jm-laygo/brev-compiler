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
str_delim    = {comma, semicolon, newline, space, colon, cl_par, cl_brc, cl_bra, '&'}

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

def formatExpectedDelimiters(allowedDelimiters):
    # no delimiter
    if not allowedDelimiters:
        return "(none)"

    remainingDelimiters = set(allowedDelimiters)
    delimiterParts = []

    digitSet = set(DIGITS)
    alphabetSet = set(ALPHABET)
    alphaDigitSet = set(ALPHA_DIG)

    # common names first
    if space in remainingDelimiters:
        delimiterParts.append("space")
        remainingDelimiters.remove(space)

    if comma in remainingDelimiters:
        delimiterParts.append("comma")
        remainingDelimiters.remove(comma)

    if semicolon in remainingDelimiters:
        delimiterParts.append("semicolon")
        remainingDelimiters.remove(semicolon)

    if colon in remainingDelimiters:
        delimiterParts.append("colon")
        remainingDelimiters.remove(colon)

    if period in remainingDelimiters:
        delimiterParts.append("period")
        remainingDelimiters.remove(period)

    if newline in remainingDelimiters:
        delimiterParts.append("newline")
        remainingDelimiters.remove(newline)

    if tab in remainingDelimiters:
        delimiterParts.append("tab")
        remainingDelimiters.remove(tab)

    if None in remainingDelimiters:
        delimiterParts.append("EOF")
        remainingDelimiters.remove(None)

    # symbols and operators
    for delimiter in DOCU_DELIM_ORDER:
        if delimiter in (space, newline, tab, None):
            continue

        if delimiter in remainingDelimiters:
            delimiterParts.append(repr(delimiter))
            remainingDelimiters.remove(delimiter)

    # grouped characters
    if alphaDigitSet.issubset(remainingDelimiters):
        delimiterParts.append("alphanumeric")
        remainingDelimiters = remainingDelimiters - alphaDigitSet

    else:
        if alphabetSet.issubset(remainingDelimiters):
            delimiterParts.append("alphabet")
            remainingDelimiters = remainingDelimiters - alphabetSet

        if digitSet.issubset(remainingDelimiters):
            delimiterParts.append("digits")
            remainingDelimiters = remainingDelimiters - digitSet

    # remaining chars
    for delimiter in sorted(remainingDelimiters, key=lambda character: str(character)):
        if delimiter in (space, newline, tab, None):
            continue

        delimiterParts.append(repr(delimiter))

    if delimiterParts:
        return ", ".join(delimiterParts)

    return "(none)"

def format_expected_delims(allowedDelimiters):
    return formatExpectedDelimiters(allowedDelimiters)
