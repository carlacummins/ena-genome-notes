process GCA_ASSEMBLY_STATS {
    tag "${meta.accession}"
    label 'process_low'

    conda "../../../env.yaml"
    container "carlacummins/ena-genome-notes:latest"

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
