import unittest

from fmse_tool.AST.ExistsGloballyNode import ExistsGloballyNode
from fmse_tool.AST.TrueNode import TrueNode
from fmse_tool.model.LTS import LTS

from fmse_tool.model.Transition import Transition


class ASTTest(unittest.TestCase):
    def test_find_strongly_connected_component(self):
        lts = LTS([
            Transition(('a', ), '', ('b', )),
            Transition(('b', ), '', ('c', )),
            Transition(('c', ), '', ('a', )),
            Transition(('b', ), '', ('d', )),
            Transition(('d', ), '', ('e', )),
            Transition(('e', ), '', ('f', )),
            Transition(('f', ), '', ('d', )),
            Transition(('g', ), '', ('f', )),
            Transition(('g', ), '', ('h', )),
            Transition(('h', ), '', ('i', )),
            Transition(('i', ), '', ('j', )),
            Transition(('j', ), '', ('g', )),
            Transition(('j', ), '', ('k', )),
        ], ('a', ))
        node = ExistsGloballyNode(lts, None)
        self.assertEqual(
            {
                frozenset(component)
                for component in
                node.find_strongly_connected_components([
                    ('a', ), ('b', ), ('c', ), ('d', ),
                    ('e', ), ('f', ), ('g', ), ('h', ),
                    ('i', ), ('j', ), ('k', )
                ])
            },
            {
                frozenset([('a', ), ('b', ), ('c', )]),
                frozenset([('k', )]),
                frozenset([('i', ), ('h', ), ('g', ), ('j', )]),
                frozenset([('d', ), ('f', ), ('e', )]),
            }
        )

    def test_check_exists_globally(self):
        lts = LTS([
            Transition(('0', ), '', ('6', )),
            Transition(('0', ), '', ('1', )),
            Transition(('6', ), '', ('2', )),
            Transition(('5', ), '', ('6', )),
            Transition(('1', ), '', ('2', )),
            Transition(('2', ), '', ('3', )),
            Transition(('3', ), '', ('4', )),
            Transition(('4', ), '', ('2', )),
            Transition(('4', ), '', ('5', )),
        ], ('0', ))
        node = ExistsGloballyNode(lts, TrueNode())
        self.assertEqual(
            node.evaluate({
                ('0', ), ('1', ), ('2', ), ('3', ),
                ('4', ), ('5', )
            }),
            {('0', ), ('1', ), ('2', ), ('3', ), ('4', )}
        )


if __name__ == '__main__':
    unittest.main()
