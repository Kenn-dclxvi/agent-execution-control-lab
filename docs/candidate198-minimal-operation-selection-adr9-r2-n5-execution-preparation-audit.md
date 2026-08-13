# Candidate198 最小operation選択ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate198のADR9 r2全9ケース各5件は、Candidate197登録resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `8a589cb39bfdc9bf778ccaf4408122c5fe508ee151479bb05276424c42981d06`
- reference result: `01ec5be067fb4c25924130860f622794`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate197 reference pool: `e5bc99b2bbe81149088ee328b80dcf6c927dde49828bd8a89ec362f0675e5d8d`
- Candidate198 pool: `6cbb0e1f0522f46dcec8fc431815c211b1087606bfedaa0184690bcc13f2966d`
- dispatch plan SHA-256: `3885490f4021070e1b54e74019805f91063bff3a64203cda61cc958d36cd9b0d`
- global plan SHA-256: `1fef4b5d38afff97a5e6d9f7d2dc30fef9c2f35f3dca87fc51e3fe00b9881e37`
- comparison generation SHA-256: `e51abbe3c4ccec841241eb9917b31b037711474141335d9b4e8ba491f316342b`
- comparison preflight SHA-256: `f749a5532daeb5bad78ee5035bfdfca0d14bc394de8024907b27cb994b928da4`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate198-minimal-operation-selection-adr9-r2-n5-20260813-r1`

`seed-pool`はCandidate198の空poolを作り、`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件と固定した。45 capsuleは独立sample IDを持つ。

Evaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、token accounting、target commit/treeおよびM=24はCandidate197登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

comparison receiptは`status=ready`、authorized 45、issued 0、M=24を固定した。この状態は互換条件と発行集合だけを表し、品質、機構、採用、releaseまたはprojectionを意味しない。

`candidate198_existing_0 / candidate198_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate198_not_evaluated`
