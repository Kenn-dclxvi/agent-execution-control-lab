# PRR-C01 r4 qualification fixture

- case identity: `PRR-C01 / r4`
- 上位仕様: [`pr-review-function-r1`](../../../specifications/pr-review-function-r1.md)
- model-visible: [`input.json`](input.json)
- model-invisible: [`oracle.json`](oracle.json)
- review contract: [`pr-review-contract-r2`](../../../rating-contracts/review-contract-r2.md)
- quality rating contract候補: [`pr-review-finding-quality-v4`](../../../rating-contracts/pr-review-finding-quality-v4.json)
- 状態: `qualification_fixture_frozen / independent_audit_unobserved / not_executed / baseline_not_qualified`

r3の実行で観測した入力不整合を修正するための新revisionである。`rules`が返すmodel-visible入力に規則本文と`rule_id`を同時に含める。二つのchanged pathはいずれも新規ファイルとして表し、patchと変更後本文の状態を一致させた。

このrevisionはr3の結果確認後に作成したため、held-out evidenceとして扱わない。Core Baselineの機能qualification専用候補であり、case設計の独立監査、profile、preflight、外部実行は未完了である。
