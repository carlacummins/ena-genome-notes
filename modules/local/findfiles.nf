process FINDFILES {
    tag "find_$meta.id"
    label 'process_low'
    
    conda "bioconda::coreutils=8.25"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/coreutils:8.25--1' :
        'biocontainers/coreutils:8.25--1' }"
    
    input:
        tuple val(meta), path(searchpath)
        val filepattern
        val outputfile
    
    output:
        tuple val(meta), path(prefix)

    script:
    prefix = task.ext.prefix ?: ( outputfile ? "${outputfile}" : "${meta.id}.out")
    """
    find ${searchpath}/ -type f -name ${filepattern} -exec cp '{}' ${prefix} \\;
    """
}
