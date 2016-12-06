import ply.yacc as yacc
from fmse_tool.parsing.AST.AndNode import AndNode
from fmse_tool.parsing.AST.ExistsGloballyNode import ExistsGloballyNode
from fmse_tool.parsing.AST.ExistsNextNode import ExistsNextNode
from fmse_tool.parsing.AST.ExistsUntilNode import ExistsUntilNode
from fmse_tool.parsing.AST.FalseNode import FalseNode
from fmse_tool.parsing.AST.NotNode import NotNode
from fmse_tool.parsing.AST.OrNode import OrNode
from fmse_tool.parsing.AST.TrueNode import TrueNode

from fmse_tool.parsing.AST.AtomicPropositionNode import AtomicPropositionNode

# don't remove this line
from fmse_tool.parsing.tokenizer import tokens

# FORMULA


def p_formula_ap(p):
    """formula : AP"""
    p[0] = AtomicPropositionNode(p[1])


def p_formula_expression(p):
    """formula : expression"""
    p[0] = p[1]


def p_formula_true(p):
    """formula : TRUE"""
    p[0] = TrueNode()


def p_formula_false(p):
    """formula : FALSE"""
    p[0] = FalseNode()


def p_formula_not(p):
    """formula : not"""
    p[0] = p[1]


def p_formula_or(p):
    """formula : or"""
    p[0] = p[1]


def p_formula_and(p):
    """formula : and"""
    p[0] = p[1]


# other

def p_expression(p):
    """expression : path_quantifier temporal_operator"""
    p[0] = ExistsNextNode(p[2])


def p_path_quantifier(p):
    """path_quantifier : ALWAYS | EXISTS"""


def p_temporal_operator(p):
    """temporal_operator : NEXT | GLOBALLY | FINALLY | until"""


def p_until(p):
    """until : L_BRACKET formula UNTIL formula R_BRACKET"""


def p_eg(p):
    """eg : EG formula"""
    p[0] = ExistsGloballyNode(p[2])


def p_eu(p):
    """eu : EU """
    (_, _, _, condition, _, until_condition, _) = p
    p[0] = ExistsUntilNode(condition, until_condition)


def p_not(p):
    """not : EXCLAMATION formula"""
    p[0] = NotNode(p[2])


def p_and(p):
    """and : formula AND formula"""
    p[0] = AndNode(p[1], p[3])


def p_or(p):
    """or : formula OR formula"""
    p[0] = OrNode(p[1], p[3])


# Error rule for syntax errors
def p_error(p):
    if p is None:
        print("Unexpected end of input")
    else:
        print("Syntax error in input!", p)


parser = yacc.yacc()
