#!/usr/bin/env python

import sys
import json
from dateutil import parser
import requests
from retrying import retry

def die_with_message(message):
    sys.stderr.write(f"{message}\n")
    sys.exit(1)


@retry(
    stop_max_attempt_number=3,  # Number of maximum retry attempts
    wait_fixed=1000  # Time (in milliseconds) between retry attempts
)
def query_tax_server(tax_id):
    server = "https://api.ncbi.nlm.nih.gov"
    ext = f"/datasets/v2alpha/taxonomy/taxon/{tax_id}"
     
    r = requests.get(f"{server}/{ext}", headers={ "Content-Type" : "application/json"})
     
    if not r.ok:
        r.raise_for_status()
        sys.exit()
     
    tax_json = r.json()
    return tax_json


def get_taxonomic_lineage(tax_id):
    tax_json = query_tax_server(tax_id)

    taxon_info = tax_json["taxonomy_nodes"][0]["taxonomy"]
    try:
        org_name = taxon_info["organism_name"]
        lineage = taxon_info["lineage"]
        rank = taxon_info["rank"]
    except KeyError:
        print(taxon_info)
        sys.exit(1)

    lineage_list = []
    for desc_tax_id in lineage:
        desc_tax_json = query_tax_server(desc_tax_id)
        desc_tax_info = desc_tax_json["taxonomy_nodes"][0]["taxonomy"]
        desc_org_name = desc_tax_info["organism_name"]

        try:
            desc_rank = desc_tax_info["rank"]
        except KeyError:
            continue

        lineage_list.append([desc_org_name, desc_rank])
    lineage_list.append([org_name, rank])
    return lineage_list

def full_lineage_string(lineage):
    return "; ".join(x[0] for x in lineage)

def short_lineage_string(lineage):
    return "; ".join(x[0] for x in lineage if x[1] in ['KINGDOM', 'PHYLUM', 'CLASS', 'ORDER', 'FAMILY'])



with open(sys.argv[1], 'r') as json_file:
    json_data = json.load(json_file)

report_breakdown = {
    "title"     : "",
    "abstract"  : "",
    "taxonomy"  : "",
    "background": "TBD",
    "seq_report": ""
}

# Fetch basic organism information, incl taxonomic lineage
try:
    organism_name = json_data["organism"]["organismName"]
    tax_id        = json_data["organism"]["taxId"]
    tax_lineage   = get_taxonomic_lineage(tax_id)
    short_lineage = short_lineage_string(tax_lineage)
    report_breakdown['taxonomy'] = full_lineage_string(tax_lineage)
    report_breakdown['title'] = f"# The genome sequence of {organism_name}"
    report_breakdown['abstract'] += f"We present a genome assembly for {organism_name} ({short_lineage})"
except KeyError:
    die_with_message("Cannot find organism information. Fatal.")


# Fetch collection/isolation details
try:
    biosample = json_data["assemblyInfo"]["biosample"]
    for attr in biosample["attributes"]:
        if attr["name"] == "collection_date":
            collection_date = attr["value"]
        elif attr["name"] == "isolation_source":
            isolation_source = attr["value"]
        elif attr["name"] == "geo_loc_name":
            geo_location = attr["value"]
    
    if collection_date or isolation_source or geo_location:
        report_breakdown['abstract'] += ", first isolated"
        if isolation_source:
            report_breakdown['abstract'] += f" from {isolation_source}"
        if geo_location:
            report_breakdown['abstract'] += f" in {geo_location}"
        if collection_date:
            parsed_date = parser.parse(collection_date)
            date_text = parsed_date.strftime("%B %Y")
            report_breakdown['abstract'] += f" in {date_text}"
    report_breakdown['abstract'] += ". "
except KeyError:
    # just end sentence if no further info is available
    report_breakdown['abstract'] += ". "


# Fetch assembly statistics
try:
    assembly_stats = json_data["assemblyStats"]
    seq_len = assembly_stats["totalSequenceLength"]
    seq_len_mbp = float(seq_len)/1000000
    contigs = assembly_stats["numberOfContigs"]
    report_breakdown['abstract'] += f"The genome sequence is {seq_len_mbp:.1f} megabases in span, arranged into {contigs} contigs. "
except KeyError:
    assembly_stats = {}

try:
    assembly_info = json_data["assemblyInfo"]
    # print("\n\n------- Assembly Info --------")
    # pp_json = json.dumps(assembly_info, indent=4)
    # print(pp_json)
except KeyError:
    assembly_info = {}


try:
    annotation_info = json_data["annotationInfo"]
except KeyError:
    annotation_info = {}


report_markdown  = f"{report_breakdown['title']}\n\n"
report_markdown += f"## Abstract\n\n{report_breakdown['abstract']}\n\n"
report_markdown += f"## Species taxonomy\n\n{report_breakdown['taxonomy']}\n\n"
report_markdown += f"## Background\n\n{report_breakdown['background']}\n\n"
report_markdown += f"## Genome Sequence Report\n\n{report_breakdown['seq_report']}\n\n"
print(report_markdown)
