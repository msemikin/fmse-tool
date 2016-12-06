from fmse_tool.parsing.AST.Node import Node


class FalseNode(Node):
    def evaluate(self):
        return set()

    def __eq__(self, other):
        return isinstance(other, self.__class__)
