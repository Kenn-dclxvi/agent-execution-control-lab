# Candidate199 構造化変更前review ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate199のADR9 r2全9ケース各5件は、Candidate198 corrected resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `97f063e242bef512b6d2d87d37c2aa0238fac27cec6350bf59621efa064f692d`
- reference result: `981c0c346cdb4491ab15b789b0946a43`
- reference result content SHA-256: `8a18d4600cc9f22478450d5b834510abb169dfede8695adbf4e8255a065d84ed`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate198 reference pool: `6cbb0e1f0522f46dcec8fc431815c211b1087606bfedaa0184690bcc13f2966d`
- Candidate199 pool: `c7a7e594226c484bf56c459de6510bb81637bad5c46ed0e7996bd85a1f28f0a6`
- dispatch plan content SHA-256: `3efc25a0cd0bcecf7904917cc28733d7ff63eaf743462935de6388681e241907`
- global plan SHA-256: `0288fdb6fa863eb8c02ce91159d0b0183ef185adb92307929ea187949593fb59`
- comparison generation receipt SHA-256: `f3fa9125d1c77dcef6d70b633678f8ad13261394edb886fc1a992757c2f1cbee`
- comparison preflight receipt SHA-256: `e5437722826b0483acb5c5f84dd44a050b6b8b54956f2999ffa09c5f9f5b12df`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate199-structured-prechange-review-adr9-r2-n5-20260813-r1`

`seed-pool`はCandidate199の空poolを作り、`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件と固定した。45 capsuleは独立sample IDを持つ。

Evaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はCandidate198 corrected resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

comparison receiptは`status=ready`、authorized 45、issued 0、M=24を固定した。この状態は互換条件と発行集合だけを表し、品質、機構、採用、releaseまたはprojectionを意味しない。

`candidate199_existing_0 / candidate199_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate199_not_evaluated`
