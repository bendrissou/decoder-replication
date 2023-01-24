#!/usr/bin/env python3
from glob import glob
import json, os
from csv import reader
from rich.console import Console
from rich.table import Table
import statistics

def process_rows(subj, subjname):
    results = []
    uniq = 0
    mean = 0
    maxlen = 0
    maxcov = 0
    # Unique Valid, Mean Len, Max Len, Branch%
    for run in subj:
        covs = []
        lengths = []
        for row in run:
            covs.append(float(row[4]))
            lengths.append(float(row[3]))

        uniq = len(lengths)
        mean = statistics.mean(lengths)
        maxlen = max(lengths)
        maxcov = max(covs)
        results.append([uniq, mean, maxlen, maxcov])

    if len(results) == 1:
        return (subjname, str(uniq), "%2.1f" % maxcov)
    else:
        means = []
        maxes = []
        covs = []
        uniqs = []

        for tup in results:
            uniqs.append(tup[0])
            means.append(tup[1])
            maxes.append(tup[2])
            covs.append(tup[3])

        if len(uniqs) == 0:
            return (subjname, "0", "0")
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
          title='[bold]Table [#2070b2]VIII: Decoder Evaluation (Parser Generators)[/#2070b2]')
for k in ['', 'Unique Valid', 'Branch%']:
    table.add_column(k)

c99_rows = []
ccalc_rows = []
expr_rows = []
lua_rows = []
lemon_rows = []

with open('results/gpdecoder_runs.csv') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        subj = row[1]
        run = int(row[0])

        if subj == 'c99':
            if run != len(c99_rows): c99_rows.append(list())
            c99_rows[-1].append(row)

        elif subj == 'ccalc':
            if run != len(ccalc_rows): ccalc_rows.append(list())
            ccalc_rows[-1].append(row)

        elif subj == 'expr':
            if run != len(expr_rows): expr_rows.append(list())
            expr_rows[-1].append(row)

        elif subj == 'lua':
            if run != len(lua_rows): lua_rows.append(list())
            lua_rows[-1].append(row)

        elif subj == 'lemon':
            if run != len(lemon_rows): lemon_rows.append(list())
            lemon_rows[-1].append(row)

all_rows = [c99_rows, ccalc_rows, expr_rows, lua_rows, lemon_rows]
names = ["c99", "ccalc", "Expr", "Lua", "simplec"]

i = 0
for subj in all_rows:
    table.add_row(*process_rows(subj, names[i]))
    i += 1

console.print(table)
