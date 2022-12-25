#!/usr/bin/env python3

import sys

TO_DECIMAL = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

TO_SNAFU = {
    0: ('0', 0),
    1: ('1', 0),
    2: ('2', 0),
    3: ('=', 1),
    4: ('-', 1),
    5: ('0', 1),
}

with open(sys.argv[1]) as f:
    decimal = sum([TO_DECIMAL[c] * 5**i for l in f for i, c in enumerate(reversed(l.rstrip()))])

snafu = ''
carry = 0
while decimal or carry:
    a = carry + (decimal % 5)
    digit, carry = TO_SNAFU[a]
    snafu = digit + snafu
    decimal //= 5
print(snafu)
