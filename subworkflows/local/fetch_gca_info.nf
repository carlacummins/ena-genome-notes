include { ENA_SEARCH_ASSEMBLY } from '../../modules/local/ena/search_assembly'
include { BLOBTOOLKIT         } from '../../modules/local/blobtoolkit.nf'

nextflow.enable.dsl=2

workflow FETCH_GCA_INFO {
    take:
        accession
    // accession = params.accession

    main:
        ENA_SEARCH_ASSEMBLY(accession)
        | splitCsv(header: true, sep:"\t")
        | map { row ->
            meta = row.subMap('accession','sample_accession','wgs_set','version')
            meta
        }
        | set { assembly_info }

        assembly_info | view

        BLOBTOOLKIT(assembly_info)
        | set { btk }
        
        btk.png   | view
        btk.busco | view

    emit:
        btk_images = btk.png
        busco_json = btk.busco
        meta       = assembly_info
}

workflow {
    // def meta = [:]
    // meta.id = params.accession
    FETCH_GCA_INFO(params.accession)
}
