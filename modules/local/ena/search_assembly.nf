process ENA_SEARCH_ASSEMBLY {
    tag "$accession"
    label 'process_tiny'

    conda "../../../env.yaml"
    container "carlacummins/ena-genome-notes:latest"

    input:
        val accession

    output:
        path(prefix), emit: result

    script:
    prefix = "${accession}.tsv"
    """
    search_assembly.py ${accession} > ${prefix}
    """
}
