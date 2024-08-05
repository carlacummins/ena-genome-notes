#!/usr/bin/env python

import requests
import xmltodict
import json
import sys

# define endpoint base URLs
# xml_url_base = 'https://www.ebi.ac.uk/ena/browser/api/sra'
browser_xml_url_base = 'https://www.ebi.ac.uk/ena/browser/api/xml'
taxonomy_url_base = "https://www.ebi.ac.uk/ena/taxonomy/rest"
portal_api_url_base = "https://www.ebi.ac.uk/ena/portal/api/search"

def query_endpoint(url):
    """Use requests.get to send an HTTP GET request to the URL

    Parameters
    ----------
    url : str
        The URL of the endpoint to fetch data from

    Returns
    -------
    str
        the text content of the data returned by the endpoint

    """
    #
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.content
    else:
        sys.stderr.write(f"Failed to fetch data from {url}\n")
        sys.stderr.write(f"Status code: {response.status_code}\n\n")
        sys.exit(1)


def fetch_ena_xml(accession):
    """Fetch the XML for the given accession from the ENA
    browser API. Return parsed structure

    Parameters
    ----------
    accession : str
        INSDC record accession

    Returns
    -------
    dict
        XML content parsed into a Python dict structure

    """
    xml_url = f"{browser_xml_url_base}/{accession}"
    root = xmltodict.parse(query_endpoint(xml_url))
    return root


def query_taxonomy_by_id(taxon_id):
    """Use taxonomy ID to query ENA's taxonomy endpoint

    Parameters
    ----------
    taxon_id : int
        A taxonomy ID

    Returns
    -------
    dict
        JSON content parsed into a Python dict structure

    """
    tax_id_url = f"{taxonomy_url_base}/tax-id/{taxon_id}"
    return json.loads(query_endpoint(tax_id_url).decode())

def query_taxonomy_by_name(scientific_name):
    """Use a scientific name to query ENA's taxonomy endpoint

    Parameters
    ----------
    scientific_name : str
        The scientific name of the node of interest

    Returns
    -------
    dict
        JSON content parsed into a Python dict structure

    """
    sci_name_url = f"{taxonomy_url_base}/scientific-name/{scientific_name}"
    return json.loads(query_endpoint(sci_name_url).decode())



def ena_advanced_search(search_params):
    """Query ENA's Advanced Search API. The search parameters
    are passed in a dictionary structure

    Parameters
    ----------
    search_params : dict
        The search parameters

        Example:
        {
            'result':'assembly',
            'format':'tsv',
            'fields': 'sample_accession,wgs_set,version',
            'limit':'1',
            'query':'assembly_accession=ERS12345'
        }

        For more information about Advanced Search options,
        see: https://www.ebi.ac.uk/ena/browser/advanced-search

    Returns
    -------
    if format is json:
        dict : JSON data parsed into Python dict
    else:
        str: text of TSV/CSV returned from endpoint

    """
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(portal_api_url_base, data=search_params, headers=headers)

    if data.get('format') == 'json':
        results = json.loads(r.content.decode())
    else:
        results = r.text

    return results