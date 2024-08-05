#!/usr/bin/env python

import sys, argparse
import json
from dateutil import parser
from prettytable import PrettyTable, MARKDOWN

argparser = argparse.ArgumentParser(description="Combine multiple sources into single genome note summary report")
argparser.add_argument('--sample-json'  , help="JSON file containing sample information")
argparser.add_argument('--assembly-json', help="JSON file containing assembly stats")
argparser.add_argument('--busco'        , help="path to BUSCO plot")
argparser.add_argument('--out'          , help="output file (markdown format)")
opts = argparser.parse_args(sys.argv[1:])

def die_with_message(message):
    sys.stderr.write(f"{message}\n")
    sys.exit(1)

def full_lineage_string(lineage):
    return "; ".join(x['name'] for x in lineage)

def short_lineage_string(lineage):
    return "; ".join(x['name'] for x in lineage if x['rank'] in ['kingdom', 'phylum', 'class', 'order', 'family'])

def create_chromosome_table(chr_list):
    # some 'chromosome' lists have names and some don't
    # also, format numbers for readability
    if chr_list[0][0]:
        heading = ['Name', 'Type', 'Accession', 'Length']
        rows = [[c[0], c[1], c[2], f"{int(c[3]):,}"] for c in chr_list]
    else:
        heading = ['Type', 'Accession', 'Length']
        rows = [[c[1], c[2], f"{int(c[3]):,}"] for c in chr_list]

    table = PrettyTable(heading)
    table.add_rows(rows)
    table.set_style(MARKDOWN)
    return table.get_string()

def author_list(sample_info):
    a_list = [x for x in [
        sample_info.get('collected-by'),
        sample_info.get('identified-by'),
        sample_info.get('center-name')
    ] if x is not None]

    if a_list:
        return '; '.join(a_list)
    else:
        return ''

"""
    Load input JSONs
"""
with open(opts.sample_json, 'r') as s_json_file:
    sample_data = json.load(s_json_file)
with open(opts.assembly_json, 'r') as a_json_file:
    assembly_info = json.load(a_json_file)

# create template and part-populate
report_breakdown = {
    "title"     : "",
    "authors"   : author_list(sample_data),
    "abstract"  : "",
    "taxonomy"  : "",
    "background": "TBD",
    "seq_report": ""
}

"""
    Fetch basic organism information, incl taxonomic lineage
"""
try:
    organism_name = sample_data['scientific-name']
    tax_id        = sample_data['taxon-id']
    tax_lineage   = sample_data['taxon-lineage']
    short_lineage = short_lineage_string(tax_lineage)
    report_breakdown['taxonomy'] = full_lineage_string(tax_lineage)
    report_breakdown['title'] = f"# The genome sequence of {organism_name}"
    report_breakdown['abstract'] += f"We present a genome assembly for {organism_name} ({short_lineage})"
except KeyError as ke:
    die_with_message(f"Missing essential organism information ({ke}). Fatal.")


"""
    Fetch collection/isolation details
"""
collection_date = sample_data.get('collection-date')
isolation_source = sample_data.get('isolation-source')
geo_location = sample_data.get('country') or sample_data.get('geo-loc-name')
# TODO : handle all versions of geographic location

if collection_date or isolation_source or geo_location:
    report_breakdown['abstract'] += ", first isolated"
    if isolation_source:
        report_breakdown['abstract'] += f" from {isolation_source}"
    if geo_location:
        report_breakdown['abstract'] += f" in {geo_location}"
    if collection_date:
        parsed_date = parser.parse(collection_date)
        date_text = parsed_date.strftime("%B %Y")
        report_breakdown['abstract'] += f" in {date_text}"
report_breakdown['abstract'] += ". "

"""
    Fetch assembly statistics
"""
seq_len = assembly_info.get("total-length")
seq_len_mbp = float(seq_len)/1000000

count_breakdown = []
for level in ('chromosome', 'scaffold', 'contig'):
    level_count = assembly_info.get(f'{level}-count')
    if level_count:
        count_breakdown.append(f"{level_count} {level}(s)")
count_breakdown_str = ', '.join(count_breakdown)

report_breakdown['abstract'] += f"The genome sequence is {seq_len_mbp:.2f} megabases in span"
if assembly_info.get('assembly-level'):
    report_breakdown['abstract'] += f", assembled to the {assembly_info.get('assembly-level')} level"
if assembly_info.get('genome-representation'):
    report_breakdown['abstract'] += f", representing a {assembly_info.get('genome-representation')} genome"

report_breakdown['abstract'] += f". It is arranged into {count_breakdown_str}. "

"""
    Genome Sequence Report
"""
if assembly_info.get('chromosomes'):
    report_breakdown['seq_report'] += f"#### Chromosomes\n\n{create_chromosome_table(assembly_info.get('chromosomes'))}\n"
report_breakdown['seq_report'] += f"\n#### BUSCO Summary\n\n![BUSCO plot]({opts.busco})"


"""
    Collate information into markdown formatted output
"""
report_markdown  = f"{report_breakdown['title']}\n\n"
report_markdown += f"### Authors\n\n{report_breakdown['authors']}\n\n"
report_markdown += f"### Abstract\n\n{report_breakdown['abstract']}\n\n"
report_markdown += f"### Species taxonomy\n\n{report_breakdown['taxonomy']}\n\n"
report_markdown += f"----------------------\n----------------------\n\n"
report_markdown += f"## Background\n\n{report_breakdown['background']}\n\n"
report_markdown += f"## Genome Sequence Report\n\n{report_breakdown['seq_report']}\n\n"

with open(opts.out, 'w') as md:
    md.write(report_markdown)