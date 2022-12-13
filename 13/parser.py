#!/usr/bin/env python3

import sys

def append_maybe_int(l, maybe_int):
    return l if maybe_int is None else l + [maybe_int]

def parse_(s, l, maybe_int):
    match s[0]:
        case '[':
            sublist, to_parse = parse_(s[1:], [], None)
            return parse_(to_parse[1:], l + [sublist], None)
        case c if c >= '0' and c <= '9':
            i = ord(c) - 48
            return parse_(s[1:], l, i if maybe_int is None else 10 * maybe_int + i)
        case ',':
            return parse_(s[1:], append_maybe_int(l, maybe_int), None)
        case ']':
            return append_maybe_int(l, maybe_int), s
        case _:
            raise Exception(f'Unexpected character {s[0]}')

def parse(s):
    parsed, _ = parse_(s[1:], [], None)
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
