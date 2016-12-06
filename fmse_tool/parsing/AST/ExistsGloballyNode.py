from itertools import chain

from fmse_tool.parsing.AST.Node import Node

from fmse_tool.parsing.AST.common_algorithms import find_states_predecessors


def find_strongly_connected_components(lts, states):
    def bfs_traverse():
        visited = []
        result = []

        def visit(state):
            if state not in visited:
                visited.append(state)
                out_neighbours = [
                    transition.to_state
                    for transition in
                    lts.get_transitions_from_state(state)
                    if transition.to_state in states
                ]
                for neighbour in out_neighbours:
                    visit(neighbour)
                result.insert(0, state)

        for v in states:
            visit(v)
        return result

    def get_components(bfs_ordered_vertices):
        components = {}
        assigned = []

        def assign(state, root):
            if state not in assigned:
                assigned.append(state)
                if root not in components:
                    components[root] = {state}
                else:
                    components[root].add(state)
                in_neighbours = [
                    transition.from_state
                    for transition in
                    lts.get_transitions_to_state(state)
                    if transition.from_state in states
                ]
                for neighbor in in_neighbours:
                    assign(neighbor, root)
            return components

        for v in bfs_ordered_vertices:
            assign(v, v)
        return components.values()

    return get_components(bfs_traverse())


def component_has_enough_transitions(lts, component):
    for state in component:
        if len(lts.get_state_transitions(state)) > 0:
            return True
    return False


class ExistsGloballyNode(Node):
    def __init__(self, child):
        self.child = child

    def evaluate(self, lts, states):
        valid_states = self.child.evaluate(lts, states)
        components = find_strongly_connected_components(lts, valid_states)
        maximum_component = max(components, key=len)
        maximally_connected_components = [
            component
            for component in components
            if len(component) == len(maximum_component) and
            component_has_enough_transitions(lts, component)
        ]

        predecessors = find_states_predecessors(
            lts,
            set(chain.from_iterable(maximally_connected_components)),
            lambda from_state: from_state in valid_states
        )
        return predecessors | set(chain.from_iterable(maximally_connected_components))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.child == other.child
        return False


