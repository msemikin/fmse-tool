from fmse_tool.AST.Node import Node


class FalseNode(Node):
    def evaluate(self):
        return set()
