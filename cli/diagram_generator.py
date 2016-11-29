from graphviz import Digraph

from model.LTS import LTS, Transition, get_states


def generate_diagram(lts, filename):
    dot = Digraph()
    for state in set(get_states(lts)):
        dot.node(', '.join(state), style='filled', fillcolor='grey' if state == lts.initial_state else 'white')
    for from_state, token, to_state in lts.transitions:
        dot.edge(', '.join(from_state), ', '.join(to_state), label=token)
    dot.render(filename, directory='result')

