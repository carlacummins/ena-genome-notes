// include { FASTQC } from '../modules/nf-core/fastqc/main'
include { BUSCO } from '../../modules/nf-core/busco/main'

workflow RUN_QCS {
    take:
        genome_ch     // channel: [ meta, fasta ]
        // lineage_db    // channel: /path/to/buscoDB

    main:
        lineage_db = []
        BUSCO(genome_ch, 'auto', lineage_db, [])
        | set { busco }

        busco.batch_summary | view
        busco.short_summaries_txt | view
        busco.short_summaries_json | view
        busco.busco_dir | view

    emit:
        batch_summary        = busco.batch_summary
        short_summaries_txt  = busco.short_summaries_txt
        short_summaries_json = busco.short_summaries_json
        busco_dir            = busco.busco_dir

}
