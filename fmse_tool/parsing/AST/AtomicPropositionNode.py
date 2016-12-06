from fmse_tool.parsing.AST.Node import Node


class AtomicPropositionNode(Node):
    def __init__(self, atomic_proposition):
        self.atomic_proposition = atomic_proposition

    def evaluate(self, lts, states):
        return {
            state for state in states
            if (self.atomic_proposition in lts.labellings[state])
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.atomic_proposition == other.atomic_proposition
        return False
