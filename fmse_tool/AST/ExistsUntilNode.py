from fmse_tool.AST.Node import Node
from fmse_tool.AST.common_algorithms import find_states_predecessors


class ExistsUntilNode(Node):
    def __init__(self, lts, condition, until_condition):
        self.lts = lts
        self.condition = condition
        self.until_condition = until_condition

    def evaluate(self, states):
        final_states = self.until_condition.evaluate(states)
        valid_predecessors = self.condition.evaluate(states)
        predecessors = find_states_predecessors(
            self.lts,
            final_states,
            lambda state: state in valid_predecessors
        )
        return predecessors | final_states

