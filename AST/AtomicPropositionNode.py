from AST.Node import Node


class AtomicPropositionNode(Node):
    def __init__(self, lts, atomic_proposition):
        self.lts = lts
        self.atomic_proposition = atomic_proposition

    def evaluate(self, states):
        return [
            state for state in states
            if (self.atomic_proposition in self.lts.labellings[state])
        ]
