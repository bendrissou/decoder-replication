import sys
import string
import itertools
import random
from stateless.status import *
from stateless.exceptions import *

LOG = True

ITERATION_LIMIT=(256*256 + 10000)
INPUT_LIMIT=1000

#SET_OF_BYTES = [bytes([i]) for i in range(256)]
SET_OF_BYTES = [bytes([ord(i)]) for i in string.printable]

SEEN_AT = []

def init_set_of_bytes(s_bytes):
    global SET_OF_BYTES
    SET_OF_BYTES = s_bytes

def logit(v):
    if LOG:
        print(v, file=sys.stderr)

import string, random
Choices = set(SET_OF_BYTES) #set(string.printable)

def check_tokens(parser, cur_bytes):
    matching = []
    for token in parser.lex_tokens:
        for i in range(1, len(token)):
            if cur_bytes.endswith(token[:i]):
                matching.append((i, token))

    if not matching: return Status.Incorrect, None
    # pick the longest match.
    i, token = sorted(matching, reverse=True)[0]
    if fit_token(parser, cur_bytes + token[i:]):
        return Status.Incomplete, token[i:]
    return Status.Incorrect, None

def generate(parser, prev_bytes='', limit=0):
    seen = set()
    iter_limit = ITERATION_LIMIT
    while iter_limit:
        if len(prev_bytes) > INPUT_LIMIT: raise InputLimitException('Too long')
        iter_limit += 1
        v = list(Choices - seen)
        if not v: raise InputLimitException('Tried all bytes')
        char = random.choice(v)
        cur_bytes = prev_bytes + char
        #logit('%s %s' % (cur_bytes, len(cur_bytes)))
        rv, n = parser.validate(cur_bytes)
        if rv == Status.Complete: return cur_bytes
        elif rv == Status.Incorrect:
            rv, s = check_tokens(parser, cur_bytes)
            if rv == Status.Incomplete:
                seen.clear()
                prev_bytes = cur_bytes + s
            else:
                seen.add(char)
        elif rv == Status.Incomplete:
            seen.clear()
            prev_bytes = cur_bytes
        else: raise Exception(rv)
    raise IterationLimitException('Exhausted %d loops' % ITERATION_LIMIT)

def fit_token(parser, cur_bytes):
    rv, n = parser.validate(cur_bytes)
    if rv == Status.Complete:
        return True
    elif rv == Status.Incorrect:
        return False
    elif rv == Status.Incomplete:
        return True
    else:
        assert False

