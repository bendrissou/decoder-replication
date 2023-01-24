#!/usr/bin/env python3
from glob import glob
import json, os
from csv import reader
from rich.console import Console
from rich.table import Table
import statistics

with open("input-eval/config.json", "r") as config_file: CONFIGURATION = json.load(config_file)
aggregated_results_json_name = CONFIGURATION["cdecoder_root_directory"] + "/results/aggregated_results.json"
with open(aggregated_results_json_name, "r") as result_file: aggregated_results = json.load(result_file)


def get_last_two_columns_values(subjname):
    if subjname == "INI": target_subject = aggregated_results[2]
    elif subjname == "CSV": target_subject = aggregated_results[1]
    elif subjname == "JSON": target_subject = aggregated_results[0]
    elif subjname == "TINYC": target_subject = aggregated_results[4]
    elif subjname == "MJS": target_subject = aggregated_results[3]
    else: raise Exception(fr"Statistics for {subjname} is not in the aggregated results!")
    return ("%2.1f" % target_subject["mean_total_number_of_nodes"] + " (%2.1f)" % target_subject["pstdev_total_number_of_nodes"],
         "%2.1f" % target_subject["mean_number_of_unique_nodes"] + " (%2.1f)" % target_subject["pstdev_number_of_unique_nodes"])


def process_rows(subj, subjname):
    results = []
    uniq = 0
    maxcov = 0
    # Unique Valid, Branch%
    for run in subj:
        covs = []
        lengths = []
        for row in run:
            covs.append(float(row[4]))
            lengths.append(float(row[3]))

        uniq = len(lengths)
        maxcov = max(covs)
        results.append([uniq, maxcov])

    last_two_cols = get_last_two_columns_values(subjname)
    if len(results) == 1:
        return (subjname, str(uniq), "%2.1f" % maxcov, *last_two_cols)
    else:
        covs = []
        uniqs = []
        for tup in results:
            uniqs.append(tup[0])
            covs.append(tup[1])

        uniq = statistics.mean(uniqs)
        uniq_stdv = statistics.stdev(uniqs)
        maxcov = statistics.mean(covs)
        cov_stdv = statistics.stdev(covs)
        return (subjname, "%2.1f" % uniq + " (%2.1f)" % uniq_stdv, "%2.1f" % maxcov + " (%2.1f)" % cov_stdv, *last_two_cols)


console = Console()

table  = Table(show_header=True, header_style='bold #2070b2',
          title='[bold]Table [#2070b2]IV: Decoder Evaluation (Programs)[/#2070b2]')
for k in ['', 'Unique Valid', 'Branch%', '#Functions', '#Unique Fun']:
    table.add_column(k)

ini_rows = []
csv_rows = []
json_rows = []
tiny_rows = []
mjs_rows = []
all_rows = []

with open('results/cdecoder_runs.csv') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        subj = row[1]
        run = int(row[0])

        if subj == 'ini':
            if run != len(ini_rows): ini_rows.append(list())
            ini_rows[-1].append(row)

        elif subj == 'csv':
            if run != len(csv_rows): csv_rows.append(list())
            csv_rows[-1].append(row)

        elif subj == 'cjson':
            if run != len(json_rows): json_rows.append(list())
            json_rows[-1].append(row)

        elif subj == 'tiny':
            if run != len(tiny_rows): tiny_rows.append(list())
            tiny_rows[-1].append(row)

        elif subj == 'mjs':
            if run != len(mjs_rows): mjs_rows.append(list())
            mjs_rows[-1].append(row)


all_rows = [ini_rows, csv_rows, json_rows, tiny_rows, mjs_rows]
names = ["INI", "CSV", "JSON", "TINYC", "MJS"]

i = 0
for subj in all_rows:
    table.add_row(*process_rows(subj, names[i]))
    i += 1

console.print(table)
