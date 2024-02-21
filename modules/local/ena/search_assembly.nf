process ENA_SEARCH_ASSEMBLY {
    label 'process_low'
    
    conda "bioconda::coreutils=8.25"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/coreutils:8.25--1' :
        'biocontainers/coreutils:8.25--1' }"
    
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
