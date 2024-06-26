process CREATE_GENOME_NOTE {
    tag "$accession"
    label 'process_tiny'
    debug true

    conda "../../../env.yaml"
    container "carlacummins/ena-genome-notes:latest"

    input:
        val accession
        // path sample_json
        // path assembly_json
        tuple val(s_meta), path(sample_json)
        tuple val(a_meta), path(assembly_json)
        path busco_plot

    output:
        path(markdown), emit: out

    script:
    markdown = "${accession}.genome_note.md"
    """
    summary_report.py --sample-json ${sample_json} --assembly-json ${assembly_json} --busco ${busco_plot} --out ${markdown}
    """
}