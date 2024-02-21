include { ENA_SEARCH_ASSEMBLY } from '../../modules/local/ena/search_assembly'
include { BLOBTOOLKIT         } from '../../modules/local/blobtoolkit.nf'

nextflow.enable.dsl=2

workflow {
    accession = params.accession

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
}
