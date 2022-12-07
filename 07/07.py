#!/usr/bin/env python3

import collections
import sys

with open(sys.argv[1]) as f:
    path = []
    currentdir = ''
    sizes = collections.defaultdict(int)
    for l in [x.rstrip() for x in f]:
        if l[0:2] == '$ ':
            if l[2:5] == 'cd ':
                newdir = l[5:]
                if newdir == '..':
                    path = path[:-1]
                    currentdir = '/'.join(path)
                else:
                    currentdir = currentdir + '/' + newdir
                    path.append(currentdir)
        else:
            size, name = l.split()
            if size == 'dir':
                pass
            else:
                for component in path:
                    sizes[component] += int(size)

    print(sum([size for size in sizes.values() if size <= 100000]))

    required = sizes['//'] - 40000000
    print(sorted([size for size in sizes.values() if size >= required])[0])
