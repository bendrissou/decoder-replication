import sys

with open('tokens.py') as f:
    v = "[" + f.read() + "]"
    res= eval(v, {},{})
    d = {}
    for r in res:
        d[str(r)] = r
    print(len(d))

with open('k.py', 'w+') as f:
    print('INSTRUCTIONS= [', file=f)
    for k in d:
        print(k + ",", file=f)
    print(']', file=f)
