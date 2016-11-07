from collections import namedtuple

Transition = namedtuple('Transition', 'from_state, token, to_state')
LTS = namedtuple('LTS', 'transitions, initial_state')


def get_transitions_from_state(transitions, state):
    return {
        transition
        for transition in transitions
        if transition.from_state == state
    }


def get_alphabet(lts):
    return {transition.token for transition in lts.transitions}


def compose_lts(first_lts, second_lts):
    transitions = []
    first_lts_alphabet = get_alphabet(first_lts)
    second_lts_alphabet = get_alphabet(second_lts)

    def iterate(first_state, second_state):
        first_state_transitions = get_transitions_from_state(first_lts.transitions, first_state)
        second_state_transitions = get_transitions_from_state(second_lts.transitions, second_state)

        corresponding_transitions = [
            (first_state_transition, second_state_transition)
            for first_state_transition in first_state_transitions
            for second_state_transition in second_state_transitions
            if first_state_transition.token == second_state_transition.token
        ]

        mutual_transition_tokens = [transition.token for transition, _ in corresponding_transitions]

        for first_state_transition, second_state_transition in corresponding_transitions:
            transition_to_add = Transition(
                first_state + second_state,
                first_state_transition.token,
                first_state_transition.to_state + second_state_transition.to_state
            )
            if transition_to_add not in transitions:
                transitions.append(transition_to_add)
                iterate(
                    first_state_transition.to_state,
                    second_state_transition.to_state
                )

        for transition in first_state_transitions:
            transition_to_add = Transition(
                first_state + second_state,
                transition.token,
                transition.to_state + second_state
            )
            if transition.token not in mutual_transition_tokens and\
                    transition.token not in second_lts_alphabet and\
                    transition_to_add not in transitions:
                transitions.append(transition_to_add)
                iterate(transition.to_state, second_state)

        for transition in second_state_transitions:
            transition_to_add = Transition(
                first_state + second_state,
                transition.token,
                first_state + transition.to_state
            )
            if transition.token not in mutual_transition_tokens and\
                    transition.token not in first_lts_alphabet and\
                    transition_to_add not in transitions:
                transitions.append(transition_to_add)
                iterate(first_state, transition.to_state)

    iterate(first_lts.initial_state, second_lts.initial_state)
    return LTS(transitions, transitions[0].from_state)
