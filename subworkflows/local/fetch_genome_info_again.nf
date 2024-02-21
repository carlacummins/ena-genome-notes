nextflow.enable.dsl=2

include { GENOMEDOWNLOADER        } from '../../modules/local/ncbidatasets/genomedownloader'
include { UNZIP                   } from '../../modules/nf-core/unzip/main'
// include { FINDFILES as FF_GENOME  } from '../../modules/local/findfiles'
// include { FINDFILES as FF_SUMMARY } from '../../modules/local/findfiles'


workflow FETCH_GENOME_INFO {
    take:
        meta
        accession
        // outdir

    main:
        // versions_ch = Channel.empty()
    
        // download genome and stats summary from NCBI
        GENOMEDOWNLOADER([meta, accession])
        // versions_ch = versions_ch.mix ( GENOMEDOWNLOADER.out.versions.first() )

        // unzip the contents
        zipfile = GENOMEDOWNLOADER.out.genomedata
        unzipped_ch = UNZIP(zipfile).unzipped_archive

        // versions_ch = versions_ch.mix ( UNZIP.out.versions.first() )

        // // find files of interest
        // Channel.fromPath("${outdir}/genome_info/**/*.fna", followLinks: true)
        // | map { row -> [meta, row] }
        // // | set { genome_ch }
        // | view { "Genome file: ${it}" }
        // 
        // Channel.fromPath("${outdir}/genome_info/**/assembly_data_report.*", followLinks: true)
        // | map { row -> [meta, row] }
        // // | set { summary_ch }
        // | view { "Summary file: ${it}" }

    emit:
        unzipped_ch
    //     genome_ch
    //     summary_ch
    //     versions_ch
}

workflow {
    def meta = [:]
    meta.id = params.accession
    // outdir_ch = Channel.fromPath(params.outdir)
    // FETCH_GENOME_INFO(meta, params.accession, outdir_ch)
    FETCH_GENOME_INFO(meta, params.accession)
}
