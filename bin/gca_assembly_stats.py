#!/usr/bin/env python

import sys, argparse
import json
from ena_utils import *

parser = argparse.ArgumentParser(description="Fetch and parse assembly stats for a given accession")
parser.add_argument('--acc', help="assembly accession")
parser.add_argument('--out', help="output file (json format)")
opts = parser.parse_args(sys.argv[1:])

# moved to ena_utils : def ena_advanced_search(data)

def add_chromosome_lengths(chr_list):
    accessions = [x[2] for x in chr_list]
    search_terms = {
        'result':'sequence', 'format':'json',
        'fields': 'sequence_accession,base_count',
        'query': ' OR '.join([f"sequence_accession=\"{x}\"" for x in accessions])
    }
    seq_lens = ena_advanced_search(search_terms)
    sl_dict = {x['sequence_accession']:x['base_count'] for x in seq_lens}
    for i in range(len(chr_list)):
        chr_list[i].append(sl_dict.get(chr_list[i][2]))
    return chr_list

# fetch assembly XML data
ena_xml = fetch_ena_xml(opts.acc)
gca_xml = ena_xml['ASSEMBLY_SET']['ASSEMBLY']
print(gca_xml)

# parse XML and pull out stats of interest
assembly_stats = {'accession':opts.acc}
for stat in gca_xml['ASSEMBLY_ATTRIBUTES']['ASSEMBLY_ATTRIBUTE']:
    assembly_stats[stat['TAG']] = stat['VALUE']

chr_list = gca_xml.get('CHROMOSOMES').get('CHROMOSOME', []) if gca_xml.get('CHROMOSOMES') else []
if type(chr_list) is not list:
    chr_list = [chr_list]

assembly_stats['chromosome-count'] = len(chr_list)
print(chr_list)
print(f"chr count: {len(chr_list)}")
assembly_stats['chromosomes'] = [[x.get('NAME'), x.get('TYPE'), x.get('@accession')] for x in chr_list]
assembly_stats['chromosomes'] = add_chromosome_lengths(assembly_stats['chromosomes'])

assembly_stats['assembly-level'] = gca_xml.get('ASSEMBLY_LEVEL')
assembly_stats['genome-representation'] = gca_xml.get('GENOME_REPRESENTATION')

# write stats to JSON file
with open(opts.out, 'w') as outfile:
    json.dump(assembly_stats, outfile, indent=4)
