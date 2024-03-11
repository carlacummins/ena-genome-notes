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

import os
import sys
import argparse
import glob

"""

"""

parser = argparse.ArgumentParser(
    description="""This script finds all short_summary.txt files in BUSCO output directory
    and copies them to a directory in preparation for plotting"""
)
parser.add_argument('-i',
                    '--busco_dir', 
                    help="path to BUSCO output directory (input)"
                    required=True)
parser.add_argument('-o',
                    '--summary_dir', 
                    help="path to summary directory (output)"
                    required=True)
opts = parser.parse_args(sys.argv[1:])


summary_files = glob.glob(f"{opts.busco_dir}/**/short_summary.txt")
print(summary_files)
