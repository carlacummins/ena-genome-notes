#!/usr/bin/env python

import sys, argparse

import requests
import xmltodict
import json

parser = argparse.ArgumentParser(description="Fetch and parse assembly stats for a given accession")
parser.add_argument('--acc', help="assembly accession")
parser.add_argument('--out', help="output file (json format)")
opts = parser.parse_args(sys.argv[1:])

def fetch_xml(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the XML content
        root = xmltodict.parse(response.content)
    else:
        print("Failed to fetch data. Status code:", response.status_code)

    return root

def ena_advanced_search(data):
    url = "https://www.ebi.ac.uk/ena/portal/api/search"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(url, data=data, headers=headers)

    if data.get('format') == 'json':
        results = json.loads(r.content.decode())
    else:
        results = r.text

    return results

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

# URL of the XML data
ena_xml_url = 'https://www.ebi.ac.uk/ena/browser/api/xml'
gca_xml = fetch_xml(f"{ena_xml_url}/{opts.acc}")['ASSEMBLY_SET']['ASSEMBLY']
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
