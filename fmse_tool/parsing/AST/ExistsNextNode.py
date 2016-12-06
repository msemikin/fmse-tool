from fmse_tool.parsing.AST.Node import Node


class ExistsNextNode(Node):
    def __init__(self, child):
        self.child = child

    def evaluate(self, lts, states):
        valid_states = self.child.evaluate(lts, states)
        previous_states = {
            transition.from_state
            for state in valid_states
            for transition in lts.get_transitions_to_state(state)
        }
        return previous_states

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.child == other.child
        return False
