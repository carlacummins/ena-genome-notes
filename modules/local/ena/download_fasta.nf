process DOWNLOAD_FASTA {
    tag "$meta.accession"
    label 'process_tiny'

    conda "bioconda::curl"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/curl:7.80.0' :
        'curlimages/curl:8.6.0' }"

    input:
        val meta

    output:
        tuple val(meta), path(final_fasta)

    script:
        inter_fasta = "${meta.accession}.raw.fa"
        final_fasta = "${meta.accession}.fa"
        """
        curl https://www.ebi.ac.uk/ena/browser/api/fasta/${meta.accession} > ${inter_fasta}
        check_fasta.py --fa ${inter_fasta} --out ${final_fasta}
        """
}
