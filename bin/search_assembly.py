#!/usr/bin/env python

import sys
import requests

def ena_advanced_search(data):
    url = "https://www.ebi.ac.uk/ena/portal/api/search"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(url, data=data, headers=headers)
    results = r.text
    return results

accession = sys.argv[1]
search_terms = {
    'result':'assembly', 'format':'tsv',
    'fields': 'sample_accession,wgs_set,version',
    'limit':'1'
}
# check if accession has a version
try:
    spl = accession.split('.')
    search_terms['query'] = f'assembly_accession={spl[0]} AND version={spl[1]}'
except IndexError:
    search_terms['query'] = f'assembly_accession={spl[0]}'

assembly_result = ena_advanced_search(search_terms)
print(assembly_result)
