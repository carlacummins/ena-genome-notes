// include { FASTQC } from '../modules/nf-core/fastqc/main'
include { BUSCO } from '../../modules/nf-core/busco/main'

workflow RUN_QCS {
    take:
        genome_ch     // channel: [ meta, fasta ]
        lineage_db    // channel: /path/to/buscoDB

    main:
        BUSCO(genome_ch, 'auto', lineage_db.ifEmpty([]), [])
        batch_summary_ch = BUSCO.out.batch_summary.view()
        short_summary_ch = BUSCO.out.short_summaries_txt.view()
        short_summary_json_ch = BUSCO.out.short_summaries_json.view()
        busco_dir_ch = BUSCO.out.busco_dir.view()

    emit:
        busco_dir_ch
}
