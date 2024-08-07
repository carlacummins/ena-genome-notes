#!/usr/bin/env python

import sys, argparse

import requests
import xmltodict
import json
import re
from ena_utils import *

parser = argparse.ArgumentParser(description="Fetch and parse assembly stats for a given accession")
parser.add_argument('--acc', help="assembly accession")
parser.add_argument('--out', help="output file (json format)")
opts = parser.parse_args(sys.argv[1:])

# moved to ena_utils : def query_endpoint(url)
# moved to ena_utils : def fetch_ena_xml(acc)

def taxonomic_lineage(taxon_id):
    taxon_json = query_taxonomy_by_id(taxon_id)

    lineage = []
    for sci_name in taxon_json['lineage'].split('; '):
        if not sci_name:
            continue

        this_tax_json = query_taxonomy_by_name(sci_name)
        print(this_tax_json)
        lineage.append({'name':sci_name, 'rank':this_tax_json[0]['rank']})

    return lineage

# URL of the XML data
sample_xml = fetch_ena_xml(opts.acc)['SAMPLE_SET']['SAMPLE']
print(sample_xml)

# parse XML and pull out information of interest
sample_info = {}
sample_info['accession'] = sample_xml['@accession']
sample_info['center-name'] = sample_xml['@center_name']
sample_info['broker-name'] = sample_xml.get('@broker_name')
sample_info['title'] = sample_xml['TITLE']
sample_info['scientific-name'] = sample_xml['SAMPLE_NAME']['SCIENTIFIC_NAME']
sample_info['taxon-id'] = sample_xml['SAMPLE_NAME']['TAXON_ID']
sample_info['taxon-lineage'] = taxonomic_lineage(sample_info['taxon-id'])

# first created
for attr in sample_xml['SAMPLE_ATTRIBUTES']['SAMPLE_ATTRIBUTE']:
    # if attr['TAG'] in ['strain', 'ENA-FIRST-PUBLIC']:
    tag = attr['TAG'].lower()
    tag = re.sub('[\s_]+', '-', tag)
    sample_info[tag] = attr['VALUE']

# ena fastqs
for link in sample_xml['SAMPLE_LINKS']['SAMPLE_LINK']:
    if link['XREF_LINK']['DB'] == 'ENA-FASTQ-FILES':
        sample_info['fastq-files'] = link['XREF_LINK']['ID']

# write stats to JSON file
with open(opts.out, 'w') as outfile:
    json.dump(sample_info, outfile, indent=4)
