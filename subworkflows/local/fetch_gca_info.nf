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
        | set { stats_json }
        stats_json | view

        FETCH_SAMPLE_INFO(assembly_info)
        | set { sample_info }
        sample_info | view

    emit:
        meta = assembly_info
        stats_json
        sample_info
}

workflow {
    FETCH_GCA_INFO(params.accession)
}
