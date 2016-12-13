from itertools import chain
from string import Template

from collections import defaultdict

from fmse_tool.model.LTS import LTS


class CTLLTS(LTS):
    def __init__(self, transitions, initial_state, labellings):
        """
        labellings is a dictionary {state: set[str]}
        """
        super(CTLLTS, self).__init__(transitions, initial_state)
        self.labellings = labellings

    def compose(self, second_lts):
        composed = super(CTLLTS, self).compose(second_lts)
        original_labellings = [self.labellings, second_lts.labellings]
        labellings = defaultdict(set, {
            state: self.get_result_labelling(original_labellings, state)
            for state in composed.get_states()
        })
        return CTLLTS(
            composed.transitions,
            composed.initial_state,
            labellings
        )

    @staticmethod
    def get_result_labelling(original_labellings, state):
        return set(chain.from_iterable(
            labelling[(atom,)]
            for atom in state
            for labelling in original_labellings
            if (atom,) in labelling
        ))

    def __str__(self):
        template = Template("""
            initial_state: $initial_state,
            transitions: $transitions,
            labellings: $labellings,
        """)
        return template.substitute({
            'initial_state': self.initial_state,
            'transitions': self.transitions,
            'labellings': self.labellings,
        })

