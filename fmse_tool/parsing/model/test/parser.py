from unittest import TestCase

from fmse_tool.model.CTLLTS import CTLLTS
from fmse_tool.model.Transition import Transition
from fmse_tool.parsing.model.parser import parse_ctllts


class ModelParserTest(TestCase):
    def test_works(self):
        definition = """
            OFF (press -> LOW);
            LOW {lightOn} (hold -> HIGH, press -> OFF);
            HIGH {lightOn, highBatteryUse} (press -> OFF);
        """
        result = parse_ctllts(definition)
        expected_result = CTLLTS(
            initial_state=('OFF',),
            transitions=[
                Transition(('OFF',), 'press', ('LOW',)),
                Transition(('LOW',), 'hold', ('HIGH',)),
                Transition(('LOW',), 'press', ('OFF',)),
                Transition(('HIGH',), 'press', ('OFF',))
            ],
            labellings={
                ('LOW',): {'lightOn'},
                ('HIGH',): {'lightOn', 'highBatteryUse'},
                ('OFF',): set()
            }
        )
        print(result, expected_result)
        self.assertEqual(result, expected_result)
