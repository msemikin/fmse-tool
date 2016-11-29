from fmse_tool.model.LTS import LTS, Transition


def parse_lts(filename):
    file = [line for line in open(filename, 'r').read().split('\n') if line]
    initial_state = (file[0],)
    transitions = [
        Transition((from_state,), token, (to_state,))
        for (from_state, token, to_state) in (
            line.split(' ') for line in file[1:]
        )
    ]
    return LTS(transitions, initial_state)
