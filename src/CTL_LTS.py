from collections import namedtuple
from itertools import chain

from src.LTS import compose_lts, get_states

"""
transitions is a set of Transition objects
initial_state is a tuple of strings
labellings is a dictionary {state: set[str]}
"""
CTL_LTS = namedtuple('CTL_LTS', 'transitions, initial_state, labellings')


def get_result_labelling(original_labellings, state):
    return set(chain.from_iterable(
        labelling[atom] for atom in state for labelling in original_labellings)
    )


def compose_ctl_lts(structure1, structure2):
    composed = compose_lts(structure1, structure2)
    original_labellings = [structure1.labellings, structure2.labellings]
    labellings = {state: get_result_labelling(state, original_labellings) for state in get_states(composed)}
    return CTL_LTS(composed.transitions, composed.initial_state, labellings)


