# Candidate194 C147直接review制御再構成 ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate194のADR9 r2全9ケース各5件は、Candidate191の登録済み45 atomic runと対応する保存Layer 1を参照側へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、Candidate194の不足45件だけを許可した。監査時点の発行数は0件であり、評価runは開始していない。

Candidate191のrunはCandidate194のrunとして流用していない。Candidate191は評価条件と保存Layer 1の互換参照であり、Candidate194の親、採用済み機構または成功結論ではない。Candidate194の直接親は引き続きCandidate147である。

## 固定identity

- reference result ID: `e599690689294c658b52a6a9e301697f`
- reference result content SHA-256: `2f969876645f5e2f3bfc37acaafab85b68a004dba474e21ec6b1055359d8edac`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate191 reference pool key: `df4cef435915f62453ce6e8b7053dff32f4d94e585cd20d08fbca27519717d51`
- Candidate194 pool key: `9366b6dfdb17780afb3a5edc46da9ac4ade6530dbae86333a7c99f7af1bc2453`
- Evaluation set identity SHA-256: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- profile SHA-256: `8c05ac84ea191f4e02619dba11fe83c3baf9fa4b8c7eeb9fc56ac5cc16cd2795`
- dispatch plan content SHA-256: `871248a6e697bc5bd49b4f9fa91fcd74c0502800d785de97ed88950bc7de6b66`
- global plan SHA-256: `fd7ea69480a6b64553cfc18e46da5a3a8e965f73125fb44e8250f59db7b40c1b`
- comparison generation content SHA-256: `e8f6f446ffeb40cd94de51a59c561100c171a710aa4b75a456fcda19f2fca8eb`
- comparison preflight content SHA-256: `67d98853e0c11c09cc61f39355c94cca6b6325970463b0dfa914002728581bff`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-20260812-r1`

## 不足計画

Candidate194の空poolは、Candidate191 reference poolのcase別実効条件とcomparison keyをCandidate194 prompt identityへbindして作成した。架空のrunは登録していない。

`plan-missing --desired-count 5`は次を固定した。

- Candidate194 existing sample count: ADR01からADR09まで各0件
- missing sample count: 各case 5件
- missing slot count: 合計45件
- coverage: ADR01からADR09、各iteration 1から5

Candidate191の45件は参照側に保持し、Candidate194の既存件数へ数えていない。既存runの再実行も計画していない。

## 互換条件

45 capsuleは、Candidate194のprompt name、bundle hash、bundle pathだけをCandidate194へbindした。次は参照resultと一致している。

- Evaluation setと9ケースrevision
- 9 fixture identity
- model-visible TaskSpec source
- rating contractとcommand evidence protocol
- modelとreasoning effort
- Agent/runtime/CLIとtoken accounting
- permission
- executor parameters
- resource class
- target commitとtree
- 設定上のM=24

開始identityの判定は各caseのmodel-visible payloadに従う。全9ケースでHEAD系列が不一致なら停止するため、開始identityと後続repository readを共同発行する経路は許容していない。

## 発行境界

comparison receiptは`authorized_slots=45`、`issued_slots=0`、`max_workers=24`、`status=ready`を固定した。preparation rootに`parallel-run`は存在せず、Layer 2のadapter実行は始まっていない。

`ready`は実行条件が揃ったことだけを意味する。Candidate194の品質、機構、採用、releaseまたはprojectionを意味しない。固定global planを使うrun発行は、利用者の次の明示的な継続判断まで行わない。

`execution_preparation_passed / reference_45_bound / candidate194_existing_0 / candidate194_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate194_not_evaluated`

固定global planは後続の明示指示で発行され、45 / 45 valid、除外0件、runner error 0件で完了した。本監査の発行前状態は上書きせず、現在判断は[Candidate194 ADR9 r2全9ケースN=5結果](../evaluations/results/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5_2026-08-12.md)を正本とする。
