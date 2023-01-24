#!/usr/bin/env python3
import random
import subprocess
import os
import sys
from ast import literal_eval
from driver import create_lua_binary
def get_cov():
    cmd = "gcovr -r lua-5.1.5/src --branches -e lua-5.1.5/src/lparser.c -e lua-5.1.5/src/lcode.c -e lua-5.1.5/src/lstrlib.c -e lua-5.1.5/src/luac.c"
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    output = stdout.decode('utf-8')
    ol = stdout.decode().split('\n')
    l = '-1'
    b = ol[-3].split()[3][:-1]
    return l, b

inputs = []

with open("valid_inputs.txt", "r") as valid_inputs_file:
        for line in valid_inputs_file:
            if line.startswith("["):
                line = literal_eval(line.strip())
                inputs.append(line)


total_inputs = len(inputs)
if total_inputs == 0:
    print("inputs file is empty! Please provide inputs.")
    sys.exit()
else:
    print("Number of inputs: " + str(total_inputs))

postfix = random.randint(999, 9999)
with open("coverage.txt", "w") as myfile:
    for input in inputs:
        create_lua_binary(input)
        cmd = "./lua-5.1.5/src/lua compiled.luap >/dev/null"
        excode = os.system(cmd)
        cov = get_cov()
        if True:
            myfile.write(str(cov) + "\n")
    myfile.close()
#os.system("gcovr -r lua-5.1.5/src --branches --html --html-details -o coverage.html")
