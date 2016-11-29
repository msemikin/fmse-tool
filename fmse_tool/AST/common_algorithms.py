from itertools import chain


def find_states_predecessors(lts, states, predicate):
    def traverse_predecessors(state, visited=()):
        for transition in lts.get_transitions_to_state(state):
            if transition.from_state not in visited and predicate(transition.from_state):
                return traverse_predecessors(
                    transition.from_state,
                    visited + (transition.from_state,)
                )
        return visited

    return set(chain.from_iterable(
        traverse_predecessors(state)
        for state in states
    ))
