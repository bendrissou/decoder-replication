#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
import json


with open("input-eval/config.json", "r") as config_file: CONFIGURATION = json.load(config_file)
aggregated_results_json_name = CONFIGURATION["aflc_root_directory"] + "/results/aggregated_results.json"


if __name__ == "__main__":
    console = Console()

    table  = Table(show_header=True, header_style='bold #2070b2',
            title='[bold]Table [#2070b2]VII[/#2070b2]')
    for k in ['', 'Max Depth', 'Unique 2-paths', 'Unique 3-paths']:
        table.add_column(k)

    with open(aggregated_results_json_name, "r") as result_file:
        data = json.load(result_file)

    for subj in data:
        table.add_row(
            *(subj["name"]
             , "%2.1f" % subj["mean_max_depth"] + " (%2.1f)" % subj["pstdev_max_depth"]
             , "%2.1f" % subj["mean_number_of_unique_2_paths"] + " (%2.1f)" % subj["pstdev_number_of_unique_2_paths"]
             , "%2.1f" % subj["mean_number_of_unique_3_paths"] + " (%2.1f)" % subj["pstdev_number_of_unique_3_paths"])
        )
        
    console.print(table)
