from fmse_tool.AST.Node import Node


class NotNode(Node):
    def __init__(self, lts, child):
        self.lts = lts
        self.child = child

    def evaluate(self, states):
        valid_states = self.child.evaluate(states)
        return {
            state
            for state in self.lts.get_states()
            if state not in valid_states
        }
