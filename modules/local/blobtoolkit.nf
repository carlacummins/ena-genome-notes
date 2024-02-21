process BLOBTOOLKIT {
    tag "$meta.wgs_set"
    label 'process_low'
    
    // conda "bioconda::blobtools=1.1.1"
    if (workflow.profile.tokenize(',').intersect(['conda', 'mamba']).size() >= 1) {
        exit 1, "BLOBTOOLKIT module does not support Conda. Please use Docker / Singularity / Podman instead."
    }
    container "docker.io/genomehubs/blobtoolkit:4.3.3"
    
    input:
        val meta

    output:
        tuple val(meta), path("*.png") , emit: png
        tuple val(meta), path("*.json"), emit: busco
        path "versions.yml"            , emit: versions

    script:
    """
    blobtoolkit_images.py --acc ${meta.wgs_set}
    
    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        blobtools: \$( blobtools --version | sed -e "s/blobtoolkit v//g" )
    END_VERSIONS
    """
}
