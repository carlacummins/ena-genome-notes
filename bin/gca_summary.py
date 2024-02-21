#!/usr/bin/env python

import sys

import requests
import xmltodict

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
gca_xml = fetch_xml(f"{ena_xml_url}/{sys.argv[1]}")['ASSEMBLY_SET']['ASSEMBLY']

assembly_stats = {}
assembly_stats['num-chr'] = len(gca_xml['CHROMOSOMES']['CHROMOSOME'])
for stat in gca_xml['ASSEMBLY_ATTRIBUTES']['ASSEMBLY_ATTRIBUTE']:
    assembly_stats[stat['TAG']] = stat['VALUE']

print(assembly_stats)
