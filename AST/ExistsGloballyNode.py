from itertools import chain
from AST.Node import Node
from AST.common_algorithms import find_states_predecessors


class ExistsGloballyNode(Node):
    def __init__(self, lts, child):
        self.lts = lts
        self.child = child

    def find_strongly_connected_components(self, states):

        def bfs_traverse():
            visited = []
            result = []

            def visit(state):
                if state not in visited:
                    visited.append(state)
                    out_neighbours = [
                        transition.to_state
                        for transition in
                        self.lts.get_transitions_from_state(state)
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
                        self.lts.get_transitions_to_state(state)
                        if transition.from_state in states
                        ]
                    for neighbor in in_neighbours:
                        assign(neighbor, root)
                return components

            for v in bfs_ordered_vertices:
                assign(v, v)
            return components.values()

        return get_components(bfs_traverse())

    def component_has_enough_transitions(self, component):
        for state in component:
            if len(self.lts.get_state_transitions(state)) > 0:
                return True
        return False

    def evaluate(self, states):
        valid_states = self.child.evaluate(states)
        components = self.find_strongly_connected_components(valid_states)
        maximum_component = max(components, key=len)
        maximally_connected_components = [
            component
            for component in components
            if len(component) == len(maximum_component) and
            self.component_has_enough_transitions(component)
        ]

        predecessors = find_states_predecessors(
            self.lts,
            set(chain.from_iterable(maximally_connected_components)),
            lambda from_state: from_state in valid_states
        )
        return predecessors | set(chain.from_iterable(maximally_connected_components))
