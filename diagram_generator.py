from graphviz import Digraph
from LTS import LTS, Transition


def get_states(lts):
    for transition in lts.transitions:
        yield transition.from_state
        yield transition.to_state


def generate_diagram(lts, filename):
    dot = Digraph()
    for state in set(get_states(lts)):
        dot.node(', '.join(state), style='filled', fillcolor='grey' if state == lts.initial_state else 'white')
    for from_state, token, to_state in lts.transitions:
        dot.edge(', '.join(from_state), ', '.join(to_state), label=token)
    dot.render(filename, directory='result')


def test():
    lts = LTS([
        Transition(('off', 'rel'), 'press', ('low', 'pr')),  #
        Transition(('low', 'pr'), 'hold', ('high', 'pr')),  #
        Transition(('high', 'pr'), 'release', ('high', 'rel')),  #
        Transition(('high', 'rel'), 'press', ('off', 'pr')),  #
        Transition(('low', 'pr'), 'release', ('low', 'rel')),  #
        Transition(('low', 'rel'), 'press', ('off', 'pr')),  #
        Transition(('off', 'pr'), 'release', ('off', 'rel'))  #
    ], ('off', 'rel'))
    generate_diagram(lts)
