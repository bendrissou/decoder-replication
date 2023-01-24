#!/usr/bin/env python3
from glob import glob
import json, os
import statistics
from rich.console import Console
from rich.table import Table

with open("input-eval/config.json", "r") as config_file: CONFIGURATION = json.load(config_file)
aggregated_results_json_name = CONFIGURATION["aflc_root_directory"] + "/results/aggregated_results.json"
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
    with open(f, 'rb') as file:
        txt = file.readlines()
        cov = str(txt[-2]).split(':')[1].split('%')[0].strip()
    return cov


def process_rows(subj, subjname):
    results = []
    uniq = 0
    maxcov = 0
    # Unique Valid, Mean Len, Max Len, Branch%
    last_two_cols = get_last_two_columns_values(subjname)
    if len(subj) == 1:
        return (subjname, str(subj[0][0]), "%2.1f" % float(subj[0][3]), *last_two_cols)
    else:
        covs = []
        uniqs = []

        for tup in subj:
            uniqs.append(tup[0])
            covs.append(tup[3])

        uniq = statistics.mean(uniqs)
        uniq_stdv = statistics.stdev(uniqs)
        maxcov = statistics.mean(covs)
        cov_stdv = statistics.stdev(covs)
        return (subjname, "%2.1f" % uniq + " (%2.1f)" % uniq_stdv, "%2.1f" % maxcov + " (%2.1f)" % cov_stdv, *last_two_cols)


console = Console()

table  = Table(show_header=True, header_style='bold #2070b2',
          title='[bold]Table [#2070b2]V: AFL Evaluation (Programs)[/#2070b2]')
for k in ['', 'Unique Valid', 'Branch%', '#Functions', '#Unique Fun']:
    table.add_column(k)

ini_rows = []
csv_rows = []
json_rows = []
tiny_rows = []
mjs_rows = []
all_rows = []

def read_files():
    r = 0
    for dirname in os.listdir("results/afl-c"):
        if dirname == 'results': continue
        r += 1
        uniq, meanlen, maxlen = process_stats_file("results/afl-c/" + dirname + "/ini/stats-dm.txt")
        cov = process_cov_file("results/afl-c/" + dirname + "/ini/eval-dm.txt")
        #print("\nINI stats: " + uniq + " - " + meanlen + " - " + maxlen)
        #print("\nINI cov: " + cov)
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        ini_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-c/" + dirname + "/csv/stats-dm.txt")
        cov = process_cov_file("results/afl-c/" + dirname + "/csv/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        csv_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-c/" + dirname + "/cjson/stats-dm.txt")
        cov = process_cov_file("results/afl-c/" + dirname + "/cjson/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        json_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-c/" + dirname + "/tiny/stats-dm.txt")
        cov = process_cov_file("results/afl-c/" + dirname + "/tiny/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        tiny_rows.append(row)

        uniq, meanlen, maxlen = process_stats_file("results/afl-c/" + dirname + "/mjs/stats-dm.txt")
        cov = process_cov_file("results/afl-c/" + dirname + "/mjs/eval-dm.txt")
        row = [float(uniq), float(meanlen), float(maxlen), float(cov)]
        mjs_rows.append(row)

all_rows = [ini_rows, csv_rows, json_rows, tiny_rows, mjs_rows]
names = ["INI", "CSV", "JSON", "TINYC", "MJS"]

read_files()
i = 0
for subj in all_rows:
    table.add_row(*process_rows(subj, names[i]))
    i += 1

console.print(table)
