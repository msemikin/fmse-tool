from fmse_tool.parsing.AST.Node import Node


class NotNode(Node):
    def __init__(self, child):
        self.child = child

    def evaluate(self, lts, states):
        valid_states = self.child.evaluate(lts, states)
        return {
            state
            for state in lts.get_states()
            if state not in valid_states
        }

    def __eq__(self, other):
        return isinstance(other, self.__class__)
