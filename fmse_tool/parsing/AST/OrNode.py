from fmse_tool.parsing.AST.Node import Node


class OrNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, lts, states):
        return self.left.evaluate(lts, states) - self.right.evaluate(lts, states)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.left == other.left and self.right == other.right
        return False
