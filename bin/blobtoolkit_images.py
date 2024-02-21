#!/usr/bin/env python

import sys
import argparse

import requests
import json
from urllib.parse import urlparse

import subprocess

parser = argparse.ArgumentParser(description="Generate map from ENA Advanced Search output (TSV format)")
parser.add_argument('--acc', help="accession (wgs_set)")
parser.add_argument('--outdir', help="output directory (default: .)", default='.')
opts = parser.parse_args(sys.argv[1:])

# check xrefs API to find blobtools URL
xref_url = f"https://www.ebi.ac.uk/ena/xref/rest/json/search?source=BlobToolKit&source_accession={opts.acc}"
content = requests.get(xref_url)
try:
    data = json.loads(content.content)
except json.decoder.JSONDecodeError:
    sys.stderr.write(f"Error fetching BlobToolKit information for {opts.acc}")
    sys.exit(0)

parsed = urlparse(data[0]['Source URL'])
btk_host = f"{parsed.scheme}://{parsed.netloc}"

# loop through required plots
# note: blobtools hangs when a plot is not available - implement a timeout here
for itype in ['snail', 'busco', 'cumulative', 'blob']:
    cmd = f"blobtools view --view {itype} --host {btk_host} --out {opts.outdir} {opts.acc}"
    print(cmd)
    try:
        p = subprocess.run(cmd, timeout=60, shell=True)
    except subprocess.TimeoutExpired:
        print(f' ! blobtools timeout reached - no {itype} image found')
