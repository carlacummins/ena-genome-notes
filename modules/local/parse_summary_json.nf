process PARSESUMMARY {
    tag "$meta.id"
    label 'process_low'
    
    conda "conda-forge::python=3.10.2"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/python:3.10.2':
        'biocontainers/python:3.10.2' }"
    
    input:
        tuple val(meta), path(summary_json)

    output:
        path summary_out

    script:
    summary_out = "${summary_json}.pp.json"
    """
    summary_report.py ${summary_json} | tee ${summary_out}
    """
}
