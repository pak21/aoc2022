class Interpreter:
    def __init__(self, pretick, posttick):
        self._pretick = pretick
        self._posttick = posttick

    def _clocktick(self, old_state):
        new_state = self._pretick(old_state)
        return self._posttick({**new_state, 't': new_state['t'] + 1})

    def _addx(self, old_state, arg):
        new_state = self._clocktick(self._clocktick(old_state))
        return {**new_state, 'x': new_state['x'] + arg}

    def parse(self, filename):
        with open(filename) as f:
            self._program = [self._parsewords(l.rstrip().split()) for l in f]

    def _parsewords(self, words):
        match words[0]:
            case 'noop':
                return lambda self, state: self._clocktick(state)
            case 'addx':
                return lambda self, state: self._addx(state, int(words[1]))
            case _:
                raise Exception(f'Unknown opcode {words[0]}')

    def run(self, initial_state):
        state = initial_state
        for instruction in self._program:
            state = instruction(self, state)
        return state
