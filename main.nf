// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

nextflow.enable.dsl=2

// Check the inputs
assert params.accession, "Parameter 'accession' is not specified"

// Run the workflow
include { GENOMENOTE } from './workflows/ena_genome_note'
workflow ENA_GENOMENOTE {
    main:
        GENOMENOTE(params.accession, params.outdir)
}

workflow {
    main:
        ENA_GENOMENOTE()
}
