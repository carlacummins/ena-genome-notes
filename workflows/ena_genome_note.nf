// include { FETCH_GENOME_INFO } from '../subworkflows/local/fetch_genome_info'
// include { GENOMESUMMARY     } from '../subworkflows/local/genome_summary'
// include { RUN_QCS           } from '../subworkflows/local/run_qcs'

include { FETCH_GCA_INFO } from '../subworkflows/local/fetch_gca_info'
include { DOWNLOAD_DATA  } from '../subworkflows/local/download_data'
include { RUN_QCS        } from '../subworkflows/local/run_qcs'

// Check optional parameters
// if (params.lineage_db) { ch_busco = Channel.fromPath(params.lineage_db) } else { ch_busco = Channel.empty() }

workflow GENOMENOTE {
    take:
        accession
        outdir

    main:
        // def meta = [:]
        // meta.id = accession
        // FETCH_GENOME_INFO(meta, accession, outdir)
        // | set { genome_info }
        //
        // GENOMESUMMARY(genome_info.summary_ch)
        // RUN_QCS(genome_info.genome_ch, ch_busco)

        FETCH_GCA_INFO(accession)
        | set { gca_info }
        meta = gca_info.meta

        DOWNLOAD_DATA(meta)
        | set { downloads }
        genome_ch = downloads.fasta

        RUN_QCS(genome_ch)
}

// workflow {
//     main:
//         GENOMENOTE(params.accession)
// }
