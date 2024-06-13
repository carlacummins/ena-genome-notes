#!/usr/bin/env python

import sys, argparse

import requests
import xmltodict
import json
import re

parser = argparse.ArgumentParser(description="Fetch and parse assembly stats for a given accession")
parser.add_argument('--acc', help="assembly accession")
parser.add_argument('--out', help="output file (json format)")
opts = parser.parse_args(sys.argv[1:])

def query_endpoint(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch data from {url}")
        print(f"Status code: {response.status_code}")
        sys.exit(1)

def fetch_ena_xml(acc):
    # xml_url_root = 'https://www.ebi.ac.uk/ena/browser/api/sra'
    xml_url_root = 'https://www.ebi.ac.uk/ena/browser/api/xml'
    xml_url = f"{xml_url_root}/{acc}"
    root = xmltodict.parse(query_endpoint(xml_url))

    return root

def taxonomic_lineage(taxon_id):
    tax_url_base = "https://www.ebi.ac.uk/ena/taxonomy/rest"
    tax_id_url = f"{tax_url_base}/tax-id/{taxon_id}"
    taxon_json = json.loads(query_endpoint(tax_id_url).decode())

    lineage = []
    for sci_name in taxon_json['lineage'].split('; '):
        if not sci_name:
            continue
        sci_name_url = f"{tax_url_base}/scientific-name/{sci_name}"
        print(sci_name_url)
        this_tax_json = json.loads(query_endpoint(sci_name_url).decode())
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
