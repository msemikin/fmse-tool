import unittest
from LTS import *


class LTSTest(unittest.TestCase):
    def test_compose_lts(self):
        # prepare
        first_transitions = {
            Transition(('off',), 'press', ('low',)),
            Transition(('low',), 'hold', ('high',)),
            Transition(('high',), 'press', ('off',)),
            Transition(('low',), 'press', ('off',))
        }
        second_transitions = {
            Transition(('rel',), 'press', ('pr',)),
            Transition(('pr',), 'hold', ('pr',)),
            Transition(('pr',), 'release', ('rel',))
        }

        first_lts = LTS(first_transitions, ('off',))
        second_lts = LTS(second_transitions, ('rel',))

        result_transitions = {
            Transition(('off', 'rel'), 'press', ('low', 'pr')),  #
            Transition(('low', 'pr'), 'hold', ('high', 'pr')),  #
            Transition(('high', 'pr'), 'release', ('high', 'rel')),  #
            Transition(('high', 'rel'), 'press', ('off', 'pr')),  #
            Transition(('low', 'pr'), 'release', ('low', 'rel')),  #
            Transition(('low', 'rel'), 'press', ('off', 'pr')),  #
            Transition(('off', 'pr'), 'release', ('off', 'rel'))  #
        }

        # act
        result = compose_lts(first_lts, second_lts)

        # assert
        self.assertEqual(set(result.transitions), set(result_transitions))


if __name__ == '__main__':
    unittest.main()
