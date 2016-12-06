"""

grammar and parsing for the CTL formula DSL

"""

import ply.lex as lex

tokens = (
    'AP',
    'ALWAYS',
    'EXISTS',
    'NEXT',
    'GLOBALLY',
    'FINALLY',
    'UNTIL',
    'AND',
    'OR',
    'TRUE',
    'FALSE',
    'L_BRACKET',
    'R_BRACKET',
    'EXCLAMATION'
)


def t_AP(t):
    r"'[a-zA-Z ]+'"
    # cut the parentheses
    t.value = t.value[1:-1]
    return t


t_ALWAYS = r'A'
t_EXISTS = r'E'
t_NEXT = r'X'
t_GLOBALLY = r'G'
t_FINALLY = r'F'
t_UNTIL = r'U'
t_AND = r'and'
t_OR = r'or'
t_TRUE = r'true'
t_FALSE = r'false'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_EXCLAMATION = r'\!'

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


# Test it output
def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
