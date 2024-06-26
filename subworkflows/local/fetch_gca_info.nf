include { ENA_SEARCH_ASSEMBLY } from '../../modules/local/ena/search_assembly'
include { GCA_ASSEMBLY_STATS  } from '../../modules/local/ena/gca_assembly_stats'
include { FETCH_SAMPLE_INFO   } from '../../modules/local/ena/fetch_sample_info'

nextflow.enable.dsl=2

workflow FETCH_GCA_INFO {
    take:
        accession

    main:
        ENA_SEARCH_ASSEMBLY(accession)
        | splitCsv(header: true, sep:"\t")
        | map { row ->
            meta = row.subMap('accession','sample_accession','wgs_set','version')
            meta['id'] = meta.accession
            meta
        }
        | set { assembly_info }

        assembly_info | view

        GCA_ASSEMBLY_STATS(assembly_info)
        | set { assembly_json }
        assembly_json | view

        FETCH_SAMPLE_INFO(assembly_info)
        | set { sample_json }
        sample_json | view

    emit:
        meta = assembly_info
        assembly_json
        sample_json
}

workflow {
    FETCH_GCA_INFO(params.accession)
}
