process ENA_SEARCH_ASSEMBLY {
    tag "$accession"
    label 'process_tiny'
    
    conda "bioconda::curl"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/curl:7.80.0' :
        'curlimages/curl:8.6.0' }"
    
    input:
        val accession

    output:
        path(prefix), emit: result

    script:
        prefix = "${accession}.tsv"
        """
        curl -s -X POST -H \"Content-Type: application/x-www-form-urlencoded\" -d 'result=assembly&query=accession%3D%22${accession}%22&fields=sample_accession%2Cwgs_set%2Cversion&format=tsv' \"https://www.ebi.ac.uk/ena/portal/api/search\" > ${prefix}
        """
}
