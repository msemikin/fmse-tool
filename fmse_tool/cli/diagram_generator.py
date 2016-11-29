from graphviz import Digraph


def generate_diagram(lts, filename):
    dot = Digraph()
    for state in set(lts.get_states()):
        dot.node(', '.join(state), style='filled', fillcolor='grey' if state == lts.initial_state else 'white')
    for from_state, token, to_state in lts.transitions:
        dot.edge(', '.join(from_state), ', '.join(to_state), label=token)
    dot.render(filename, directory='result')

