from model.Transition import Transition


class LTS(object):
    def __init__(self, transitions, initial_state):
        self.transitions = transitions
        self.initial_state = initial_state

    def get_states(self):
        for transition in self.transitions:
            yield transition.from_state
            yield transition.to_state

    def get_transitions_from_state(self, state):
        return {
            transition
            for transition in self.transitions
            if transition.from_state == state
        }

    def get_transitions_to_state(self, state):
        return {
            transition
            for transition in self.transitions
            if transition.to_state == state
        }

    def get_state_transitions(self, state):
        return {
            transition
            for transition in self.transitions
            if state in [transition.to_state, transition.from_state]
        }

    def get_alphabet(self):
        return {transition.token for transition in self.transitions}

    def compose(self, second_lts):
        transitions = []
        first_lts_alphabet = self.get_alphabet()
        second_lts_alphabet = second_lts.get_alphabet()

        def iterate(first_state, second_state):
            first_state_transitions = self.get_transitions_from_state(first_state)
            second_state_transitions = second_lts.get_transitions_from_state(second_state)

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
                if transition.token not in mutual_transition_tokens and \
                                transition.token not in second_lts_alphabet and \
                                transition_to_add not in transitions:
                    transitions.append(transition_to_add)
                    iterate(transition.to_state, second_state)

            for transition in second_state_transitions:
                transition_to_add = Transition(
                    first_state + second_state,
                    transition.token,
                    first_state + transition.to_state
                )
                if transition.token not in mutual_transition_tokens and \
                                transition.token not in first_lts_alphabet and \
                                transition_to_add not in transitions:
                    transitions.append(transition_to_add)
                    iterate(first_state, transition.to_state)

        iterate(self.initial_state, second_lts.initial_state)
        return LTS(transitions, transitions[0].from_state)
