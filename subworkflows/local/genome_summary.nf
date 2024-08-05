include { BUSCO_SUMMARY      } from '../../modules/local/busco_summary'
include { CREATE_GENOME_NOTE } from '../../modules/local/create_genome_note'

workflow GENOMESUMMARY {
    take:
        accession
        sample_json
        assembly_json
        busco_dir_ch
        busco_short_summaries_json

    main:
        BUSCO_SUMMARY(busco_dir_ch, busco_short_summaries_json)
        | set { busco_plot }

        CREATE_GENOME_NOTE(accession, sample_json, assembly_json, busco_plot)
        | set { genomenote_ch }

    emit:
        genomenote_ch.out
}
