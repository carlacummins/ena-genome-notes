process FETCH_SAMPLE_INFO {
    tag "${meta.sample_accession}"
    label 'process_low'

    conda "../../../env.yaml"
    container "carlacummins/ena-genome-notes:latest"

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
