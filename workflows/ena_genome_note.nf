include { FETCH_GCA_INFO } from '../subworkflows/local/fetch_gca_info'
include { DOWNLOAD_DATA  } from '../subworkflows/local/download_data'
include { RUN_QCS        } from '../subworkflows/local/run_qcs'
include { GENOMESUMMARY  } from '../subworkflows/local/genome_summary'

// Check optional parameters
// if (params.lineage_db) { ch_busco = Channel.fromPath(params.lineage_db) } else { ch_busco = Channel.empty() }

workflow GENOMENOTE {
    take:
        accession
        outdir

    main:
        FETCH_GCA_INFO(accession)
        | set { gca_info }
        meta = gca_info.meta

        DOWNLOAD_DATA(meta)
        | set { downloads }
        genome_ch = downloads.fasta

        RUN_QCS(genome_ch)
        | set { qc_ch }
        qc_ch.busco_dir | view { "GENOMENOTE::qc_ch.busco_dir = $it" }
        qc_ch.busco_short_summaries_json | view { "GENOMENOTE::qc_ch.busco_short_summaries_json = $it" }

        GENOMESUMMARY(accession, gca_info.sample_json, gca_info.assembly_json, qc_ch.busco_dir, qc_ch.busco_short_summaries_json)
        | set { genomenote_ch }
}

// workflow {
//     main:
//         GENOMENOTE(params.accession)
// }
