#!/usr/bin/env python3

import collections
import sys

import numpy as np

with open(sys.argv[1]) as f:
    file = []
    for l in [x.rstrip() for x in f]:
        file.append([int(l), None])

def make_linked_list(l):
    head = None
    prev = None
    zero = None
    for i in range(len(l)):
        value = l[i][0]
        node = [value, prev, None]
        l[i][1] = node
        if prev:
            prev[2] = node
        else:
            head = node
        prev = node

        if value == 0:
            zero = node

    head[1] = node
    node[2] = head

    return head, zero

def dump(ll):
    head = ll
    p = head
    s = ''
    while True:
        s += f'{p[0]} '
        p = p[2]
        if p == head:
            break
    print(s)

ll, zero = make_linked_list(file)

for value, ptr in file:
    value = value % (len(file) - 1)
    if value > 0:
         orig_prev = ptr[1]
         orig_next = ptr[2]

         orig_prev[2] = orig_next
         orig_next[1] = orig_prev

         before = ptr
         after = ptr[2]
         for _ in range(value):
            before = before[2]
            after = after[2]

         before[2] = ptr
         ptr[1] = before

         ptr[2] = after
         after[1] = ptr
    elif value < 0:
        orig_prev = ptr[1]
        orig_next = ptr[2]

        orig_prev[2] = orig_next
        orig_next[1] = orig_prev

        before = ptr[1]
        after = ptr
        for _ in range(-value):
            before = before[1]
            after = after[1]

        before[2] = ptr
        ptr[1] = before

        ptr[2] = after
        after[1] = ptr

ptr = zero
result = 0
for _ in range(3):
    for _ in range(1000):
        ptr = ptr[2]
    result += ptr[0]

print(result)
