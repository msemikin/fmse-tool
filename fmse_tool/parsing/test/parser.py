import unittest

from fmse_tool.parsing.AST.AndNode import AndNode
from fmse_tool.parsing.AST.AtomicPropositionNode import AtomicPropositionNode
from fmse_tool.parsing.AST.ExistsGloballyNode import ExistsGloballyNode
from fmse_tool.parsing.AST.ExistsNextNode import ExistsNextNode
from fmse_tool.parsing.AST.ExistsUntilNode import ExistsUntilNode
from fmse_tool.parsing.AST.NotNode import NotNode
from fmse_tool.parsing.AST.OrNode import OrNode
from fmse_tool.parsing.AST.TrueNode import TrueNode
from fmse_tool.parsing.parser import parser


class ParserTest(unittest.TestCase):
    def test_eg(self):
        formula = "EG 'foo bar'"
        result = parser.parse(formula)
        expected_result = ExistsGloballyNode(
            AtomicPropositionNode('foo bar')
        )

        self.assertEqual(result, expected_result)

    def test_eu(self):
        formula = "E ['q' U 'foo bar']"
        result = parser.parse(formula)
        expected_result = ExistsUntilNode(
            AtomicPropositionNode('q'),
            AtomicPropositionNode('foo bar')
        )

        self.assertEqual(result, expected_result)

    def test_nested(self):
        formula = "E ['q' U !EG 'foo bar']"
        result = parser.parse(formula)
        expected_result = ExistsUntilNode(
            AtomicPropositionNode('q'),
            NotNode(
                ExistsGloballyNode(
                    AtomicPropositionNode('foo bar')
                )
            )
        )

        self.assertEqual(result, expected_result)

    def test_with_booleans(self):
        formula = "E ['q' U !EG E[true U 'foo bar']]"
        result = parser.parse(formula)
        expected_result = ExistsUntilNode(
            AtomicPropositionNode('q'),
            NotNode(
                ExistsGloballyNode(
                    ExistsUntilNode(
                        TrueNode(),
                        AtomicPropositionNode('foo bar')
                    )
                )
            )
        )

        self.assertEqual(result, expected_result)

    def test_and(self):
        formula = "EX 'q' and 'p'"
        result = parser.parse(formula)
        expected_result = ExistsNextNode(
            AndNode(
                AtomicPropositionNode('q'),
                AtomicPropositionNode('p')
            )
        )

        self.assertEqual(result, expected_result)

    def test_or(self):
        formula = "EX 'q' or 'p'"
        result = parser.parse(formula)
        expected_result = ExistsNextNode(
            OrNode(
                AtomicPropositionNode('q'),
                AtomicPropositionNode('p')
            )
        )

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
