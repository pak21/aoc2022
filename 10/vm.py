class Interpreter:
    def __init__(self, pretick, posttick):
        self._pretick = pretick
        self._posttick = posttick

    def _clocktick(self, vm0, puzzle0):
        puzzle1 = self._pretick(vm0, puzzle0)
        vm1 = {**vm0, 't': vm0['t'] + 1}
        puzzle2 = self._posttick(vm1, puzzle1)
        return vm1, puzzle2

    def _addx(self, vm0, puzzle0, arg):
        vm1, puzzle1 = self._clocktick(*self._clocktick(vm0, puzzle0))
        return {**vm1, 'x': vm1['x'] + arg}, puzzle1

    def parse(self, filename):
        with open(filename) as f:
            self._program = [self._parsewords(l.rstrip().split()) for l in f]

    def _parsewords(self, words):
        match words[0]:
            case 'noop':
                return lambda self, vm0, puzzle0: self._clocktick(vm0, puzzle0)
            case 'addx':
                return lambda self, vm0, puzzle0: self._addx(vm0, puzzle0, int(words[1]))
            case _:
                raise Exception(f'Unknown opcode {words[0]}')

    def run(self, vm_state, puzzle_state):
        for instruction in self._program:
            vm_state, puzzle_state = instruction(self, vm_state, puzzle_state)
        return vm_state, puzzle_state
