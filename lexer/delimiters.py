# CONSTANTS

ZERO = '0'
DIGIT = '0123456789'
ZERODIGIT = ZERO + DIGIT

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_DIG = ALPHABET + DIGIT

# BASIC DELIMITERS

space      = ' '
colon      = ':'
semicolon  = ';'
underscore = '_'
op_par     = '{'
op_brc     = '['
comma      = ','
newline    = '\n'

# DELIMITER SETS

id_sym = set(ALPHA_DIG + "_")

els_delim     = {space, newline, '{'}
bool_delim    = {space, ')', semicolon, comma}
op_delim      = {'+', '-', '*', '/', '%', '!', '&', '|', '='}

int_decdelim  = (
    {space, semicolon, colon, comma, '}', ')', ']'} |
    op_delim
)

chr_delim  = {space, semicolon, comma, colon, '}', ')', '&'}
str_delim  = {comma, semicolon, space, colon, ')', '}', '&'}

idnt_delim = (
    {space, semicolon, comma, '.', '(', ')', '}', '[', ']'} |
    op_delim
)

# DELIMITERS SA PDF

delim1  = set(ALPHA_DIG) | {space, '"', '('}
delim2  = {semicolon} | set(ALPHA_DIG) | {')'}
delim3  = {space, '~'} | set(ALPHA_DIG) | {'('}
delim4  = {'"', '~', "'", '('} | set(ALPHABET) | {space, '{'}
delim5  = {space} | set(ALPHA_DIG) | {'~', '"', "'", '('}
delim6  = {'(', ')', '!', "'", '"', space} | set(ALPHA_DIG)
delim7  = {';', '{', ')', '<', '>', '=', '|', '&', '+', '-', '/', '*', '%',
           space, newline, ':', ','}
delim8  = {']', '(', space} | set(ALPHA_DIG)
delim9  = {'=', ';', '[', ')', space, newline}
delim10 = {"'", '"', '~', '{', space, newline} | set(ALPHA_DIG)
delim11 = {'{', ';', '}', ',', space, newline} | set(ALPHABET)
delim12 = {space, "'", '"'} | set(ALPHA_DIG)

# ASCII CHARACTER SETS FOR STRING

asciichr = {chr(i) for i in range(32, 127) if chr(i) != "'"}
asciistr = {chr(i) for i in range(32, 127) if chr(i) != '"'}
