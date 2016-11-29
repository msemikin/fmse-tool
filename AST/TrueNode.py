from AST.Node import Node


class TrueNode(Node):
    def evaluate(self, states):
        return states

