import ply.yacc as yacc

from fmse_tool.model.CTLLTS import CTLLTS
from fmse_tool.model.Transition import Transition

# don't remove this line
from fmse_tool.parsing.exception import UnexpectedEndOfInputError, InputSyntaxError
from fmse_tool.parsing.model.tokenizer import tokens, lexer


# EXPRESSION


def p_expression(p):
    """expression : NAME atomic_propositions transitions SEMICOLON expression
                  | empty"""
    if not p[1]:
        return
    state = (p[1],)
    labellings = {state: p[2]}
    transitions_descriptions = p[3]
    transitions = [Transition(state, action, (to_state,))
                   for (action, to_state) in transitions_descriptions]
    if p[5] is not None:
        (_, next_transitions, next_labellings) = p[5]
        transitions += next_transitions
        labellings.update(next_labellings)
    p[0] = (state, transitions, labellings)


def p_atomic_propositions(p):
    """atomic_propositions : L_CURLY atomic_proposition R_CURLY
                           | empty"""
    p[0] = p[2] if p[1] else set()


def p_atomic_proposition_single(p):
    """atomic_proposition : NAME
                          | empty"""
    p[0] = {p[1]} if p[1] else set()


def p_atomic_proposition_mutliple(p):
    """atomic_proposition : NAME COMMA atomic_proposition"""
    p[0] = {p[1]} | p[3]


def p_transitions(p):
    """transitions : L_PAREN transition R_PAREN
                   | empty"""
    p[0] = p[2] if p[1] else []


def p_transition_single(p):
    """transition : NAME ARROW NAME
                  | empty"""
    p[0] = [(p[1], p[3])] if p[1] else []


def p_transition_multiple(p):
    """transition : NAME ARROW NAME COMMA transition"""
    p[0] = [(p[1], p[3])] + p[5]


def p_empty(p):
    """empty :"""
    pass


# Error rule for syntax errors
def p_error(p):
    if p is None:
        raise UnexpectedEndOfInputError()
    else:
        raise InputSyntaxError(str(p))


parser = yacc.yacc(debug=False, write_tables=False)


def parse_ctllts(source):
    (initial_state, transitions, labellings) = parser.parse(source, lexer=lexer)
    return CTLLTS(initial_state=initial_state, transitions=transitions, labellings=labellings)
