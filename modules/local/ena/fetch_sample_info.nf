process FETCH_SAMPLE_INFO {
    tag "${meta.sample_accession}"
    label 'process_low'
    debug true
    
    conda "conda-forge::python=3.10.2"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/python:3.10.2':
        'biocontainers/python:3.10.2' }"
    
    input:
        val meta

    output:
        tuple val(meta), path(sample_json)

    script:
    sample_json = "${meta.sample_accession}.info.json"
    """
    sample_information.py --acc ${meta.sample_accession} --out ${sample_json}
    """
}
