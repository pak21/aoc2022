#!/usr/bin/env python3

import sys

def parse_(s, idx, target):
    int_value = None
    while True:
        match s[idx]:
            case '[':
                l, idx = parse_(s, idx + 1, [])
                target.append(l)
            case c if c >= '0' and c <= '9':
                i = ord(c) - 48
                int_value = i if int_value is None else 10 * int_value + i
            case ',':
                if int_value is not None:
                    target.append(int_value)
                int_value = None
            case ']':
                if int_value is not None:
                    target.append(int_value)
                return target, idx
            case _:
                raise Exception(f'Unexpected character {s[idx]}')
        idx += 1

def parse(s):
    parsed, _ = parse_(s, 1, [])
    return parsed

with open(sys.argv[1]) as f:
    for line in [l.rstrip() for l in f if l != '\n']:
        parsed = parse(line)
        cheat = eval(line)
        if parsed != cheat:
            print(f'Parsing failure for "{line}"')
            print(f'     Got {parsed}')
            print(f'Expected {cheat}')
            print()
