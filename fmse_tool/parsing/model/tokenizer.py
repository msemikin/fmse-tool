"""

grammar and parsing for the CTL and LTS models

"""

import ply.lex as lex

tokens = (
    'NAME',
    'ARROW',
    'L_CURLY',
    'R_CURLY',
    'COMMA',
    'L_PAREN',
    'R_PAREN',
    'SEMICOLON'
)


t_NAME = r"[a-zA-Z_]+"
t_ARROW = r'->'
t_L_CURLY = r'\{'
t_R_CURLY = r'\}'
t_COMMA = r'\,'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_SEMICOLON = r';'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()
