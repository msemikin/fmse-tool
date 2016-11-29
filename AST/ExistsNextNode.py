from AST.Node import Node


class ExistsNextNode(Node):
    def __init__(self, lts, child):
        self.lts = lts
        self.child = child

    def evaluate(self, states):
        valid_states = self.child.evaluate(states)
        previous_states = {
            transition.from_state
            for state in valid_states
            for transition in self.lts.get_transitions_to_state(state)
        }
        return previous_states
