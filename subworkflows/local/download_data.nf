include { DOWNLOAD_FASTA } from '../../modules/local/ena/download_fasta'
include { BLOBTOOLKIT    } from '../../modules/local/blobtoolkit'

nextflow.enable.dsl=2

workflow DOWNLOAD_DATA {
    take:
        meta

    main:
        DOWNLOAD_FASTA(meta)
        | set { fasta }
        fasta | view

        BLOBTOOLKIT(meta)
        | set { btk }
        btk.png   | view
        btk.busco | view

    emit:
        fasta
        btk_images = btk.png
        busco_json = btk.busco

}

workflow {
    DOWNLOAD_DATA(params.meta)
}
