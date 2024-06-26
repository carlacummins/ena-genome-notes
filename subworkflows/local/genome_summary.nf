include { BUSCO_PLOT         } from '../../modules/local/busco_plot'
include { CREATE_GENOME_NOTE } from '../../modules/local/create_genome_note'

workflow GENOMESUMMARY {
    take:
        accession
        sample_json
        assembly_json
        busco_dir_ch

    main:
        BUSCO_PLOT(busco_dir_ch)
        | set { busco_plot }

        CREATE_GENOME_NOTE(accession, sample_json, assembly_json, busco_plot)
        | set { genomenote_ch }

    emit:
        genomenote_ch.out
}
