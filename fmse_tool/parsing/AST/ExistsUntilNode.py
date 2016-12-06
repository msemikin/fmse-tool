from fmse_tool.parsing.AST.Node import Node
from fmse_tool.parsing.AST.common_algorithms import find_states_predecessors


class ExistsUntilNode(Node):
    def __init__(self, condition, until_condition):
        self.condition = condition
        self.until_condition = until_condition

    def evaluate(self, lts, states):
        valid_predecessors = self.condition(states)
        final_states = self.until_condition(states)
        predecessors = find_states_predecessors(
            lts,
            final_states,
            lambda state: state in valid_predecessors
        )
        return predecessors | final_states

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.condition == other.condition and\
                self.until_condition == other.until_condition
        return False
