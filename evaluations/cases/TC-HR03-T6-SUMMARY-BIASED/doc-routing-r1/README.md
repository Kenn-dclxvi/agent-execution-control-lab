# TC-HR03-T6-SUMMARY-BIASED

HR02と同じdiffを、誤ったproducer closure判断を受け取ったrootが扱う自律routing case。

- expected disposition: `completion_ready`
- expected route: `one_information_blocked_independent_quality_reviewer`
- paired case: `TC-HR02-T6-SUMMARY-UNBIASED`

後続見直しで、raw blind responseがないまま`読めた`を`構成されていた`へ強めており、expected dispositionをallowed evidenceから一意に導けないと判定した。r1は`case_design_invalid / quality_not_adjudicable`として履歴保持し、再実行しない。現在解釈は[`candidate166-review4-case-validity-analysis.md`](../../../../docs/candidate166-review4-case-validity-analysis.md)を参照する。
