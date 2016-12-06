from fmse_tool.parsing.AST.Node import Node


class TrueNode(Node):
    def evaluate(self, _, states):
        return states

    def __eq__(self, other):
        return isinstance(other, self.__class__)
