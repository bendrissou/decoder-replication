#!/usr/bin/python

import sys,getopt

filename = sys.argv[1]
blocksize = 1024

offset = 0
i = 0
with open(filename,"rb") as f:
    block = f.read(blocksize)
    str = ""
    for ch in block:
        print(i, hex(ch))
        #str += hex(ch)+" "
        i+=1
    #print(str)

