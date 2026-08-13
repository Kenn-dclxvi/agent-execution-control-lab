# Candidate202 review admission routing receipt ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate202のADR9 r2全9ケース各5件は、Candidate201登録resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `dd631e0aee4d697bd8a6daa9f5a9a394c10fbd47bac594fe0a56227885a3dbbf`
- reference result: `ba6c59a08d8744c08600207791c3b34f`
- reference result content SHA-256: `141e34fd20f0b1c5f1d068deb99857ce0dac054db288bc33eb76a1cf9a416a66`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate201 reference pool: `a8133a2c521465e5ec3a530b8310f361e103eb21f81d4183ca7e1a50d36d87c9`
- Candidate202 pool: `40e9e885b6c19e9a43680c0cd61b0034abb7de67911530a4d1faef8f0f0fd169`
- dispatch plan content SHA-256: `4f7c8bcce8810f23070747307ca81bce4e3a51f52da51e409287fc49b27681f5`
- global plan SHA-256: `51bfea1d87e1620e3144babb284a07b958fbe0801d1d5ba5024168823d311dd6`
- comparison generation receipt SHA-256: `b5605d2e9a5efa285b816fc4c3d975553a470dddb09dd92f701ab57d84fd344a`
- comparison preflight receipt SHA-256: `3e047d732a0d9d09d6e83045e575d6e665fe604a84ef5b6f2e314d59677aca52`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate202-review-admission-routing-receipt-adr9-r2-n5-20260813-r1`

## 不足slot

`seed-pool`はCandidate202の空poolを作成した。`plan-missing --desired-count 5`の結果はADR01〜ADR09のexisting各0、missing各5、合計45件である。各slotは独立sample IDを持ち、global planの設定上の並列上限はM=24である。

## 互換条件

Evaluation set identity `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`、全fixture identity、case revision、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はreferenceと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

`prepare-comparison-layer1`、`preflight-comparison`および`verify-comparison-preflight`はすべて成功した。一項目でもdriftした場合はrun直前の再検証で停止する。

`candidate202_existing_0 / candidate202_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate202_not_evaluated`
