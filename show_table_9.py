#!/usr/bin/env python3
from glob import glob
import json, os
import statistics
from rich.console import Console
from rich.table import Table
from ast import literal_eval as make_tuple

def process_stats_file(f):
    # LTime, Seed Len, Sigma, Checks
    with open(f) as file:
        txt = file.readlines()
        uniq = [t for t in txt if t.startswith('Number of unique valid inputs')][0].split(':')[1].strip()
        maxlen = [t for t in txt if t.startswith('Maximum length of inputs')][0].split(':')[1].strip()
        meanlen = [t for t in txt if t.startswith('Average length of inputs')][0].split(':')[1].strip()
    return uniq, meanlen, maxlen
    #return ("%2.0f" % float(uniq), "%2.2f" % meanlen, "%2.0f" % maxlen)
    #return "%s|%2.2f|%2.2f|%2.2f|%s" % (fname, "%2.2f" % float(ltime), "%2.2f" % avg, "%2.2f" % stddev, c)

def process_cov_file(f):
    # LTime, Seed Len, Sigma, Checks
    with open(f, 'r') as file:
        txt = file.readlines()
        if len(txt) < 1: cov = '0'
        else:
            covtup = make_tuple(txt[0].strip())
            cov = str(covtup[1])
    #cov = str(txt[-2]).split(':')[1].split('%')[0].strip()
    return cov


def process_rows(subj, subjname):
    results = []
    uniq = 0
    mean = 0
    maxlen = 0
    maxcov = 0
    # Unique Valid, Mean Len, Max Len, Branch%
    if len(subj) == 1:
        return (subjname, str(subj[0][0]), "%2.1f" % float(subj[0][3]))
    else:
        means = []
        maxes = []
        covs = []
        uniqs = []

        for tup in subj:
            uniqs.append(tup[0])
            means.append(tup[1])
            maxes.append(tup[2])
            covs.append(tup[3])

        uniq = statistics.mean(uniqs)
        uniq_stdv = statistics.stdev(uniqs)
        mean = statistics.mean(means)
        mean_stdv = statistics.stdev(means)
        maxlen = statistics.mean(maxes)
        max_stdv = statistics.stdev(maxes)
        maxcov = statistics.mean(covs)
        cov_stdv = statistics.stdev(covs)
        return (subjname, "%2.1f" % uniq + " (%2.1f)" % uniq_stdv, "%2.1f" % maxcov + " (%2.1f)" % cov_stdv)


console = Console()

table  = Table(show_header=True, header_style='bold #2070b2',
          title='[bold]Table [#2070b2]IX: AFL Evaluation (Parser Generators)[/#2070b2]')
for k in ['', 'Unique Valid', 'Branch%']:
    table.add_column(k)

c99_rows = []
expr_rows = []
lua_rows = []
ccalc_rows = []
simple_c_rows = []
all_rows = []

def read_files():
    r = 0
    for dirname in os.listdir("results/afl-gp"):
        r += 1

        uniq, meanlen, maxlen = process_stats_file("results/afl-gp/" + dirname + "/c99/stats-dm.txt")
        cov = process_cov_file("results/afl-gp/" + dirname + "/c99/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        c99_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-gp/" + dirname + "/expr/stats-dm.txt")
        cov = process_cov_file("results/afl-gp/" + dirname + "/expr/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        expr_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-gp/" + dirname + "/lua/stats-dm.txt")
        cov = process_cov_file("results/afl-gp/" + dirname + "/lua/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        lua_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-gp/" + dirname + "/ccalc/stats-dm.txt")
        cov = process_cov_file("results/afl-gp/" + dirname + "/ccalc/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        ccalc_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-gp/" + dirname + "/simple_c/stats-dm.txt")
        cov = process_cov_file("results/afl-gp/" + dirname + "/simple_c/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        simple_c_rows.append(row)

all_rows = [c99_rows, ccalc_rows, expr_rows, lua_rows, simple_c_rows]
names = ["c99", "ccalc", "Expr", "Lua", "simplec"]

read_files()
i = 0
for subj in all_rows:
    table.add_row(*process_rows(subj, names[i]))
    i += 1

console.print(table)
