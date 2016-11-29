from fmse_tool.model.LTS import LTS
from fmse_tool.model.Transition import Transition
from fmse_tool.model.CTLLTS import CTLLTS


def parse_lts(filename):
    file = [line for line in open(filename, 'r').read().split('\n') if line]
    initial_state = (file[0],)
    transitions = [
        Transition((from_state,), token, (to_state,))
        for (from_state, token, to_state) in (
            line.split(' ') for line in file[1:]
        )
    ]
    return LTS(transitions, initial_state)


def parse_ctl_lts(filename):
    file = [line for line in open(filename, 'r').read().split('\n')]
    initial_state = (file[0],)
    delimiter = file.index('')
    raw_transitions = file[1:delimiter]
    raw_labellings = file[delimiter + 1:]

    transitions = [
        Transition((from_state,), token, (to_state,))
        for (from_state, token, to_state) in (
            line.split(' ') for line in raw_transitions
        )
    ]

    labellings = {}
    for labelling in raw_labellings:
        (state, atomic_propositions) = labelling.split(': ')
        labellings[(state, )] = atomic_propositions.split(', ')
    return CTLLTS(transitions, initial_state, labellings)
