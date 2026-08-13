# Candidate200 投影済みreview read閉包 ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate200のADR9 r2全9ケース各5件は、Candidate199登録resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `6eabb610a41173e416c48d94e50049688c704fb58376e95429f42d723641a2da`
- reference result: `7751ae31151d48dd87a75b2a71a8a527`
- reference result content SHA-256: `53e4b60bd54777bd22289ac08983687e2ba8d1534721e564855cb99a1c3d7d5c`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate199 reference pool: `c7a7e594226c484bf56c459de6510bb81637bad5c46ed0e7996bd85a1f28f0a6`
- Candidate200 pool: `e352b6f4ee72d434818ac1dcdf52b4b83f3d767d809280486860c782fa4f4ac0`
- dispatch plan content SHA-256: `2a5cabe9fae7723314176a520b565dc7b63030980c30baa2fbfca77d5c082e59`
- global plan SHA-256: `c96d3ac2dfda18d9a2865780db45d2cffebb48bc1d72b722dead76edff5c449e`
- comparison generation receipt content SHA-256: `176fc1f689b3593f8cdabc37c7ab7492d9c844d42973ae5c42844abb017ba46a`
- comparison preflight receipt content SHA-256: `cdeaa6ce3eb13ff30c9d6611284c27203362094c352e123b36e23f360af06ee3`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate200-projected-review-read-closure-adr9-r2-n5-20260813-r1`

`seed-pool`はCandidate200の空poolを作り、`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件と固定した。45 capsuleは独立sample IDを持つ。

Evaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はCandidate199登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

comparison receiptは`status=ready`、authorized 45、issued 0、M=24を固定した。この状態は互換条件と発行集合だけを表し、品質、機構、採用、releaseまたはprojectionを意味しない。

`candidate200_existing_0 / candidate200_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate200_not_evaluated`
