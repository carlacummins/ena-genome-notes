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

    emit:
        busco_batch_summary = busco.batch_summary
        busco_short_summaries_txt  = busco.short_summaries_txt
        busco_short_summaries_json = busco.short_summaries_json
        busco_dir = busco.busco_dir
}
