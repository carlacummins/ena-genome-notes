process BUSCO_PLOT {
    tag "$meta.accession"
    label 'process_tiny'
    debug true

    conda "bioconda::busco=5.4.3"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/busco:5.4.3--pyhdfd78af_0':
        'biocontainers/busco:5.4.3--pyhdfd78af_0' }"

    input:
        // val accession
        tuple val(meta), path(busco_dir)

    output:
        path(busco_plot)

    script:
    summary_dir = 'busco-summaries'
    busco_plot = "busco_figure.png"
    """
    mkdir -p $summary_dir
    prepare_busco_summaries.py --busco-dir $busco_dir --summary-dir $summary_dir
    generate_plot.py -wd $summary_dir
    ln -s $summary_dir/busco_figure.png $busco_plot
    """
}