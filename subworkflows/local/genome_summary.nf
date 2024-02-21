include { PARSESUMMARY } from '../../modules/local/parse_summary_json'

workflow GENOMESUMMARY {
    take:
        summary_ch

    main:
        summary_out_ch = PARSESUMMARY(summary_ch)
        summary_out_ch | view { "Parsed summary : ${it}" }

    emit:
        // genomenote_ch
        summary_out_ch
}
