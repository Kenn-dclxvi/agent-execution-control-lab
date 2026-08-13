# Candidate195 operation ticket型review制御 ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate195のADR9 r2全9ケース各5件は、Candidate194の登録済み45 atomic runsと保存Layer 1を参照側へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、Candidate195の不足45件だけを許可した。監査時点の発行数は0件であり、評価runは開始していない。

Candidate194のrunはCandidate195のrunとして流用していない。Candidate194は互換条件と保存Layer 1の参照であり、Candidate195の親または成功機構ではない。Candidate195の直接親はCandidate147である。

## 固定identity

- profile: `candidate195-operation-ticketed-review-control-adr9-r2-medium-m24-n5-cli0146`
- profile SHA-256: `63ef94aa03d326e6098f0d5a32361ab3f058ca3eeae39163e1fa914f9945ae9c`
- reference result ID: `04c8b680e4884eafa39929e06a935035`
- reference result content SHA-256: `5fa0382075429c0d3707fb25007021427135b888fa69bcaa63e9960dbb2d227e`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate194 reference pool key: `9366b6dfdb17780afb3a5edc46da9ac4ade6530dbae86333a7c99f7af1bc2453`
- Candidate195 pool key: `5643489ca90215addca33c43a4de5bce88a5b6a7d9363784671dba7fd4fe7428`
- Evaluation set identity SHA-256: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- dispatch plan content SHA-256: `da149ffad02616509a189625e6989242c5e4115dacf0a6647d35754fca22641d`
- global plan SHA-256: `9dfb3af6a06d01ccb64cc6615fe5882995e5ef2c0e0a250aecdc6ee30a204fa3`
- comparison generation content SHA-256: `e9a82f9ac296c2e98b6d8f66d63d13734c4ae699ba34170bbbd4de307f0fdb57`
- comparison preflight content SHA-256: `d661292729728001dc8701900d7543a61db2effb2a6070efc018cc17874870a9`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate195-operation-ticketed-review-control-adr9-r2-n5-20260812-r1`

## profile

profileは[評価設計](candidate195-operation-ticketed-review-control-adr9-r2-n5-evaluation-design.md)の固定条件を転記した。

- prompt identityとbundle SHAだけをCandidate195へ変更した。
- Evaluation set、全9ケースrevision、TaskSpec、rating contract、model、reasoning、runtime、permission、token accountingおよびexecutor parameterはCandidate194参照条件と一致する。
- command evidence protocolはADR01、ADR02、ADR07の`git diff --check`だけをrequired commandとして維持する。
- `max_workers=24`を維持し、45件やcase別件数に合わせて変更していない。

profile追加後、`scripts/generate_profile_index.py --write`で索引を410 profileへ再生成し、引数なし実行で`current=true`を確認した。

## 不足計画

Candidate194 reference poolからCandidate195 prompt identityへ空poolをseedした。架空runは登録していない。

`plan-missing --desired-count 5`は次を固定した。

- Candidate195 existing sample count: ADR01からADR09まで各0件
- missing sample count: ADR01からADR09まで各5件
- missing slot count: 合計45件
- plan ID: `3ea909e8cdcd4f04881301c30bfc1e83`
- coverage: ADR01からADR09、各iteration 1から5

45件のcapsuleは一件ごとに独立した`sample_id`を持つ。Candidate194の45件は参照側に保持し、Candidate195の既存件数へ数えていない。

## 互換条件

45 capsuleはCandidate195のprompt name、bundle hash、bundle pathだけをCandidate195へbindした。次はreference resultと一致している。

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

開始identityの判定は各caseのmodel-visible payloadに従う。全9ケースでHEAD系列が不一致なら停止するため、identity一致result受領前のrepository readは許容していない。

## Layer 1準備時の停止と回復

最初の`prepare-comparison-layer1`では、Candidate194の比較cycle内Layer 1をそのままsourceへ指定したため、旧`comparison-generation.json`も複製され、write-once保護が上書きを拒否した。このattemptではcapsule実行、adapter起動およびslot発行は0件である。

未完了cycleを`failed-comparison-attempt-1`へ移して保持し、同じ保存Layer 1から旧comparison receiptだけを除いたread-only projectionを`reference-layer1`として作成した。Evaluation set、fixture、mode、case coverageおよび参照result内容は変更していない。再実行ではcomparison generationが成功し、preflightも同じreference resultへbindされた。

## 発行境界

comparison receiptは次を固定した。

- status: `ready`
- authorized slots: 45
- issued slots: 0
- max workers: 24
- global plan jobs: 45
- `parallel-run`: 不存在

`ready`は互換条件と発行集合が揃ったことだけを意味する。Candidate195の品質、機構、採用、releaseまたはprojectionを意味しない。固定global planを使うrun発行は、利用者の次の明示的な実行判断まで行わない。

`execution_preparation_passed / reference_candidate194_45_bound / candidate195_existing_0 / candidate195_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate195_not_evaluated`
