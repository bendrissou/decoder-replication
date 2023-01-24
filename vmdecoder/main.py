import os
import stateless.generate as G
from stateless.exceptions import *
from stateless.utils import *
import random
import time
import json
import sys
import string
import math
import subprocess

# NOTE: this contains the byte zero. This can cause trouble
# for textual inputs.
#G.init_set_of_bytes([bytes([i]) for i in range(256)])
G.init_set_of_bytes([bytes([ord(i)]) for i in string.printable])
G.INPUT_LIMIT = 1000
#G.LOG = True

def valid_input(validator):
    parray = b''
    cb_arr = []
    while True:
        created_bits = None
        try:
            created_bits = G.generate(validator, parray, 0)
            cb_arr.append(created_bits)
            if randrange(len(created_bits)) == 0:
                parray = created_bits
                #print('+>', repr(created_bits), file=sys.stderr)
                continue
        except (InputLimitException,IterationLimitException,BacktrackLimitException,subprocess.TimeoutExpired,FileNotFoundError) as e:
            print("E:", str(e))
        finally:
            G.SEEN_AT.clear()
        #print(">", repr(created_bits), len(cb_arr), file=sys.stderr)
        return cb_arr[-1] if cb_arr else None

def run_for(validator, name, secs=None):
    start = time.time()
    if secs is None:
        secs = 10
    lst_generated = []
    name = name[:-3]
    if name == 'tinyc': name = 'tiny'
    elif name == 'csvparser': name = 'csv'
    open('examples/%s/inputs.txt' % name, 'w').close()   # erase file content
    open('examples/%s/times.txt' % name, 'w').close()   # erase file content
    with open('examples/%s/inputs.json' % name, 'w') as f:
        while (time.time() - start) < secs:
            i = valid_input(validator)
            if i is None: continue
            tm = str(round((time.time() - start), 2)) + "\n"
            var = repr(i.decode("ascii")) + "\n"
            t = open('examples/%s/times.txt' % name, "a")
            t.write(tm)
            t.close()
            b = open('examples/%s/inputs.txt' % name, "a")
            b.write(var)
            b.close()
            c = (-1, -1)
            lst_generated.append((i,c, (time.time() - start)))
            print(json.dumps({'output':[j for j in i],
                              'cumcoverage': c,
                              'time': (time.time() - start)}),
                  file=f, flush=True)
    et = open('examples/%s/execution_time' % name, 'w')
    et.write(str(secs))
    et.close()
    return lst_generated

#time_to_run = 3600
if __name__ == "__main__":
    import importlib.util
    import sys
    my_module = sys.argv[1]
    time_to_run = float(sys.argv[2])*3600
    name = os.path.basename(my_module)
    spec = importlib.util.spec_from_file_location("decoder", my_module)
    my_decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_decoder)
    lst = run_for(my_decoder.validator, name, time_to_run)
