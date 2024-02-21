import requests, sys, json

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
    return ";".join(x[0] for x in lineage)

def short_lineage_string(lineage):
    return ";".join(x[0] for x in lineage if x[1] in ['KINGDOM', 'PHYLUM', 'CLASS', 'ORDER', 'FAMILY'])



lineage = get_taxonomic_lineage(sys.argv[1])
print(lineage)
print(full_lineage_string(lineage))
print(short_lineage_string(lineage))
