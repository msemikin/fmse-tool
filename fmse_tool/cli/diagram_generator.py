from graphviz import Digraph


def generate_diagram(lts, filename):
    dot = Digraph()
    for state in set(lts.get_states()):
        dot.node(', '.join(state), style='filled', fillcolor='grey' if state == lts.initial_state else 'white')
    for from_state, token, to_state in lts.transitions:
        dot.edge(', '.join(from_state), ', '.join(to_state), label=token)
    dot.render(filename, directory='result')


def generate_extended_diagram(lts, valid_states, filename=None):
    dot = Digraph()
    for state in set(lts.get_states()):
        dot.node(
            ', '.join(state),
            style='filled',
            fillcolor='darkgreen' if state == lts.initial_state and state in valid_states
                else 'green' if state in valid_states
                else 'grey' if state == lts.initial_state
                else 'white',
            xlabel=', '.join(lts.labellings[state]),
            forcelabels='True'
        )
    for from_state, token, to_state in lts.transitions:
        dot.edge(', '.join(from_state), ', '.join(to_state), label=token)
    if filename is not None:
        dot.render(filename, directory='result')
    else:
        return dot.source
