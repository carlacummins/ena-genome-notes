process GENOMEDOWNLOADER {
    tag "$meta.id"
    label 'process_single'

    conda "conda-forge::ncbi-datasets-cli=14.2.2"
    // container "docker.io/biocontainers/ncbi-datasets-cli:14.2.2_cv2"
    container "docker.io/biocontainers/ncbi-datasets-cli:15.12.0_cv23.1.0-4"

    input:
        tuple val(meta), val(accession)

    output:
        tuple val(meta), path("*.zip"), emit: genomedata
        path "versions.yml"           , emit: versions

    // when:
    //     ask.ext.when == null || task.ext.when

    script:
        // def args = task.ext.args ?: ''
        """
        datasets download genome accession ${accession} --filename ${meta.id}.zip

        cat <<-END_VERSIONS > versions.yml
        "${task.process}":
            ncbi-datasets-cli: \$(datasets --version | sed 's/^.*datasets version: //')
        END_VERSIONS
        """
}
