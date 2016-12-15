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
    (operator_name, value) = p[2]
    expression_name = p[1] + operator_name
    ExistsFinallyNode = lambda val: ExistsUntilNode(TrueNode(), val)

    if expression_name == 'EU':
        (condition, until_condition) = value
        p[0] = ExistsUntilNode(condition, until_condition)
    elif expression_name == 'AU':
        (condition, until_condition) = value
        p[0] = AndNode(
            NotNode(
                ExistsUntilNode(
                    NotNode(until_condition),
                    AndNode(NotNode(condition), NotNode(until_condition))
                )
            ),
            NotNode(
                ExistsGloballyNode(
                    NotNode(until_condition)
                )
            )
        )
    elif expression_name == 'EG':
        p[0] = ExistsGloballyNode(value)
    elif expression_name == 'AG':
        p[0] = NotNode(ExistsFinallyNode(NotNode(value)))

    elif expression_name == 'EX':
        p[0] = ExistsNextNode(value)
    elif expression_name == 'AX':
        p[0] = NotNode(ExistsNextNode(NotNode(value)))

    elif expression_name == 'EF':
        p[0] = ExistsFinallyNode(value)
    elif expression_name == 'AF':
        p[0] = NotNode(ExistsGloballyNode(NotNode(value)))


def p_path_quantifier(p):
    """path_quantifier : ALWAYS
                       | EXISTS"""
    p[0] = p[1]


def p_temporal_operator(p):
    """temporal_operator : next
                         | globally
                         | finally
                         | until"""
    p[0] = p[1]


def p_next(p):
    """next : NEXT formula"""
    p[0] = ('X', p[2])


def p_globally(p):
    """globally : GLOBALLY formula"""
    p[0] = ('G', p[2])


def p_finally(p):
    """finally : FINALLY formula"""
    p[0] = ('F', p[2])


def p_until(p):
    """until : L_BRACKET formula UNTIL formula R_BRACKET"""
    (_, _, condition, _, until_condition, _) = p
    p[0] = ('U', (condition, until_condition))


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


parser = yacc.yacc(debug=False, write_tables=False)

