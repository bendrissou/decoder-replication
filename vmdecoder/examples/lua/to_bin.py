#!/usr/bin/python

import sys,getopt

filename = sys.argv[1]
blocksize = 1024

v = []
with open(filename) as f:
    for line in f:
        if len(line.strip()) == 0: continue
        if line[0] == '#': continue
        b = line.strip().split()[1].replace('0x','')
        if len(b) < 2:
            b = '0' + b
        v.append(b)

r = bytearray.fromhex(' '.join(v))

with open(sys.argv[2], 'bw') as f:
    f.write(r)
