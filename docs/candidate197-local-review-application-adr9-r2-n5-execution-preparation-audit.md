# Candidate197 C147局所review応用ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate197のADR9 r2全9ケース各5件は、Candidate196の登録済み45 atomic runsと保存Layer 1を参照へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、Candidate197の不足45件だけを許可した。監査時点の発行数は0件である。

Candidate196 runはCandidate197 runとして流用していない。Candidate196は互換参照でありprompt親ではない。Candidate197の直接親はCandidate147である。

## 固定identity

- profile: `candidate197-local-review-application-adr9-r2-medium-m24-n5-cli0146`
- profile SHA-256: `3762733c4e920449bfd757d95fd4c5360653c52f54fc0359af74f3604e9e38d2`
- reference result: `76fa5af714b149baa2328516e5722f9f`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate196 reference pool: `1352703cc5b95bdc539ff16a2206423c786f4bb4a8b7144c336baab712b04407`
- Candidate197 pool: `e5bc99b2bbe81149088ee328b80dcf6c927dde49828bd8a89ec362f0675e5d8d`
- plan ID: `9e28f0734ebe46e1b89e3d67fbd44ce6`
- dispatch plan SHA-256: `79f641d77bc28d2fdd7fd8842367b3ed706b6a3ab5a4a390872adad9e9a1d4ba`
- global plan SHA-256: `069f76a303af427ce05f592c27f0e09cfc476261fdeee9c6065cce08d2022fa7`
- comparison generation SHA-256: `09a7402469519c775e94db81d016be59c2a22d609984dc5e37a254c7b091873e`
- comparison preflight SHA-256: `11dbff9e94810378286502bc1b5caf08fcf98a87331b9f107abd2969e53313ad`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate197-local-review-application-adr9-r2-n5-20260812-r1`

## 不足計画と互換性

`seed-pool`は架空runを作らずCandidate197の空poolを作成した。`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件とした。45 capsuleは独立sample IDを持つ。

Evaluation set、9 case revision、fixture identity、TaskSpec、rating、command evidence protocol、model、reasoning、Agent/runtime/CLI、permission、executor、token accounting、target commit/treeおよびM=24はCandidate196登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

準備rootへ残っていたCandidate196の`cycle/layer1`コピーはCandidate197生成票として使わず退避した。さらに、最初の`prepare-comparison-layer1`ではCandidate196の生成票を含む`cycle/layer1`を参照先に指定したため、上書き拒否で停止した。正しい保存Layer 1であるCandidate196の`reference-layer1`へbindし直し、Candidate197のcomparison generationを新規生成した。この間のslot発行、adapter起動およびrunは0件だった。

## 発行境界

comparison receiptは`status=ready`、authorized slots 45、issued slots 0、M=24を固定した。preparation rootに`parallel-run`は存在しない。`ready`は互換条件と発行集合が揃ったことだけを意味し、品質、機構、採用、releaseまたはprojectionを意味しない。

`execution_preparation_passed / reference_candidate196_45_bound / candidate197_existing_0 / candidate197_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate197_not_evaluated`
