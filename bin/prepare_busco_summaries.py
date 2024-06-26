#!/usr/bin/env python

# Copyright [2023] EMBL-European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse
import glob
import shutil
import re
import json

"""

"""

parser = argparse.ArgumentParser(
    description="""This script finds all short_summary.txt files in BUSCO output directory
    and copies them to a directory in preparation for plotting"""
)
parser.add_argument('-i',
                    '--busco-dir',
                    help="path to BUSCO output directory (input)",
                    required=True)
parser.add_argument('-o',
                    '--summary-dir',
                    help="path to summary directory (output)",
                    required=True)
opts = parser.parse_args(sys.argv[1:])


summary_files = glob.glob(f"{opts.busco_dir}/**/auto_lineage/**/short_summary.json")

for sf in summary_files:
    with open(sf, 'r') as json_file:
        this_busco_summary = json.load(json_file)

    # only include lineages with some complete BUSCOs in plot
    if this_busco_summary['results']['Complete'] > 0:
        sf_txt = re.sub('json', 'txt', sf)
        spl = sf_txt.split('/')
        lineage_full = spl[-2]
        lineage_name = lineage_full.split('_')[1]
        lineage_type = 'generic' if lineage_name in ['archaea', 'bacteria', 'eukaryota'] else 'specific'

        new_sf = f"short_summary.{lineage_type}.{lineage_full}.{lineage_name}.txt"
        print(f"copying {sf_txt} > {opts.summary_dir}/{new_sf}")
        shutil.copyfile(sf_txt, f"{opts.summary_dir}/{new_sf}")