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
          title='[bold]Table [#2070b2]X: Decoder Evaluation (Other Parsers in Python)[/#2070b2]')
for k in ['', 'Unique Valid', 'Branch%']:
    table.add_column(k)

url_rows = []
ssn_rows = []
ip_rows = []
expr_rows = []
pyc_rows = []
pcalc_rows = []
pjson_rows = []

with open('results/pydecoder_runs.csv') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        subj = row[1]
        run = int(row[0])

        if subj == 'url':
            if run != len(url_rows): url_rows.append(list())
            url_rows[-1].append(row)

        elif subj == 'fourfn':
            if run != len(expr_rows): expr_rows.append(list())
            expr_rows[-1].append(row)

        elif subj == 'ip':
            if run != len(ip_rows): ip_rows.append(list())
            ip_rows[-1].append(row)

        elif subj == 'ssn':
            if run != len(ssn_rows): ssn_rows.append(list())
            ssn_rows[-1].append(row)

        elif subj == 'pyc':
            if run != len(pyc_rows): pyc_rows.append(list())
            pyc_rows[-1].append(row)

        elif subj == 'pcalc':
            if run != len(pcalc_rows): pcalc_rows.append(list())
            pcalc_rows[-1].append(row)

        elif subj == 'pjson':
            if run != len(pjson_rows): pjson_rows.append(list())
            pjson_rows[-1].append(row)

all_rows = [pyc_rows, pcalc_rows, pjson_rows, url_rows, ssn_rows, ip_rows, expr_rows]
names = ["pycparser", "calc", "json", "URL", "SSN", "IP-Address", "Expression"]

i = 0
for subj in all_rows:
    table.add_row(*process_rows(subj, names[i]))
    i += 1

console.print(table)
