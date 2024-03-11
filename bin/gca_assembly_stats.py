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

# URL of the XML data
ena_xml_url = 'https://www.ebi.ac.uk/ena/browser/api/xml'
gca_xml = fetch_xml(f"{ena_xml_url}/{opts.acc}")['ASSEMBLY_SET']['ASSEMBLY']

# parse XML and pull out stats of interest
assembly_stats = {}
for stat in gca_xml['ASSEMBLY_ATTRIBUTES']['ASSEMBLY_ATTRIBUTE']:
    assembly_stats[stat['TAG']] = stat['VALUE']

chr_list = gca_xml.get('CHROMOSOMES').get('CHROMOSOME', []) if gca_xml.get('CHROMOSOMES') else []
assembly_stats['chromosome-count'] = len(chr_list)

assembly_stats['assembly-level'] = gca_xml.get('ASSEMBLY_LEVEL')
assembly_stats['genome-representation'] = gca_xml.get('GENOME_REPRESENTATION')

# write stats to JSON file
with open(opts.out, 'w') as outfile:
    json.dump(assembly_stats, outfile, indent=4)
