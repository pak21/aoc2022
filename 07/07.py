#!/usr/bin/env python3

import collections
import sys

sizes = collections.defaultdict(int)

with open(sys.argv[1]) as f:
    for l in [x.rstrip() for x in f]:
        if l[0:2] == '$ ':
            if l[2:5] == 'cd ':
                newdir = l[5:]
                match newdir:
                    case '/':
                        path = ['']
                    case '..':
                        path = path[:-1]
                    case _:
                        path.append(path[-1] + '/' + newdir)
        else:
            size, name = l.split()
            if size != 'dir':
                for component in path:
                    sizes[component] += int(size)

print(sum([size for size in sizes.values() if size <= 100000]))

required = sizes[''] - 40000000
print(sorted([size for size in sizes.values() if size >= required])[0])
