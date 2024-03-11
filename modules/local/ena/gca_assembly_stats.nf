process GCA_ASSEMBLY_STATS {
    tag "${meta.accession}"
    label 'process_low'
    debug true
    
    conda "conda-forge::python=3.10.2"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/python:3.10.2':
        'biocontainers/python:3.10.2' }"
    
    input:
        val meta

    output:
        tuple val(meta), path(stats_json)
        // path stats_json

    script:
    full_acc   = "${meta.accession}.${meta.version}"
    stats_json = "${full_acc}.stats.json"
    """
    gca_assembly_stats.py --acc ${full_acc} --out ${stats_json}
    """
}
