# PRR-C01 r3 held-out

- case identity: `PRR-C01 / r3`
- 上位仕様: [`pr-review-function-r1`](../../../specifications/pr-review-function-r1.md)
- model-visible: [`input.json`](input.json)
- model-invisible: [`oracle.json`](oracle.json)
- review contract: [`pr-review-contract-r2`](../../../rating-contracts/review-contract-r2.md)
- quality rating contract候補: [`pr-review-finding-quality-v3`](../../../rating-contracts/pr-review-finding-quality-v3.json)
- 状態: `heldout_fixture_frozen / independent_audit_satisfied / not_executed / baseline_not_qualified`

観測対象はr2と同じ`prompt_evaluation_separation`だが、PR説明、changed path、変更本文、base / head identityを新しく固定した。違反は2つのchanged pathの関係で成立し、どちらか一方をanchor、他方を`related_paths`として扱う。

このrevisionはreviewer runを一件も発行する前に固定したheld-out fixture候補である。独立case設計監査は[`prr-c01-r3-case-design-audit-r1`](../../../contracts/prr-c01-r3-case-design-audit-r1.json)で満たした。`PRR-C01/r2`、既存r1 result、過去のreviewer出力をqualification evidenceへ使わない。監査receiptはBaselineをqualifyせず、実行を許可せず、quality claimを作らない。正式Evaluation setへ入れるには、別途固定するBaseline機能qualification profileと残りのadmission gateが必要である。
