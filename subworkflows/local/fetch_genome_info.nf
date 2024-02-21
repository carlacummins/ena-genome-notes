include { GENOMEDOWNLOADER        } from '../../modules/local/ncbidatasets/genomedownloader'
include { UNZIP                   } from '../../modules/nf-core/unzip/main'
include { FINDFILES as FF_GENOME  } from '../../modules/local/findfiles'
include { FINDFILES as FF_SUMMARY } from '../../modules/local/findfiles'

nextflow.enable.dsl=2

workflow FETCH_GENOME_INFO {
    take:
        meta
        accession
        outdir

    main:
        // download genome and stats summary from NCBI
        GENOMEDOWNLOADER([meta, accession])
        versions_ch = GENOMEDOWNLOADER.out.versions

        // unzip the contents
        zipfile = GENOMEDOWNLOADER.out.genomedata
        zipfile | view { "Downloaded file: ${it}" }

        unzipped_ch = UNZIP(zipfile).unzipped_archive
        unzipped_ch | view { "Unzipped dir: ${it}" }

        // find files of interest
        genome_ch = FF_GENOME( unzipped_ch, '*.fna', 'genome.fna' )
        genome_ch | view { "Genome file: ${it}" }
        summary_ch = FF_SUMMARY( unzipped_ch, 'assembly_data_report.*', 'summary.json' )
        summary_ch | view {"Summary file: ${it}"}

    emit:
        // unzipped_ch
        genome_ch
        summary_ch
        versions_ch
}

workflow {
    def meta = [:]
    meta.id = params.accession
    FETCH_GENOME_INFO(meta, params.accession, params.outdir)
}
