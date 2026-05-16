# Constants used for lexical analysis and command parsing

IDENTIFIER_REGEX = r'[a-zA-Z][a-zA-Z0-9]*'
FLOAT_REGEX = r'[-]?\d+\.\d+'
INTEGER_REGEX = r'[-]?\d+'

# Valid SNOL operators
OPERATORS = ['+', '-', '*', '/', '%', '=']

# Reserved keywords in the SNOL language
KEYWORDS = ['BEG', 'PRINT', 'EXIT!']
