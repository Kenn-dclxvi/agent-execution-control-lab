# Candidate205 portable issuance frontier F01 / F02 / F03 N=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / fifteen_slots_authorized / issued_zero`

## 結論

Candidate205のF01 r3、F02 r1、F03 r2各5件、合計15 slotを、Candidate147の保存済み3ケースselection resultと、そのfixtureを生成した保存Layer 1へbindした。prompt identity以外の互換条件は完全一致し、comparison preflightは`ready`である。

Candidate205 poolは空で、各ケース5件、合計15件だけが不足している。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `3e4661c65f1d32b64472a59d5cbfa0bd9f86958c3c635461897a765f84d9937a`
- reference result: `a205f69159464c0da704d8e3a362d0c3`
- reference result content SHA-256: `7ff4a326b5d59c3e405d99b349ec7c7e0966cba0d6119c2d4f45c89d9749e0b6`
- compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- Candidate147 reference pool: `ac1eeac565d603e1f7b3662bf3316e59c28ca4346a3eee522b37c0be506cefbd`
- Candidate205 pool: `986d40563835367740043adec4be7f10ff09bd807a0272e8ae7d41731f03dd17`
- Candidate205 pool content SHA-256: `a40319e9b9d046afe27fadea8b5785c20260d3439bcf5ab7254b8dee3a11a441`
- dispatch plan content SHA-256: `b8cb3eea6bdde5ee0747d4765881db1e61f40677e34ba3e0f8fd58fd15ae8300`
- dispatch plan file SHA-256: `1f13c533e1bc3bddda9857fb231b0d81a511181ec60173be136f62337a343f0c`
- global plan SHA-256: `722e30d3fbc8d1281ef6b460e1bafa1d2c51dd838b15db93c1011a4d839adabe`
- comparison generation receipt SHA-256: `8a8747cf397c5814298067a700d46a8f0978858bfb5afa6163fafb908b1b9b68`
- comparison preflight receipt SHA-256: `41c71e06c5662167a6580415747d73151c03471aecd41b7465c2e5e025aaf98e`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate205-portable-issuance-frontier-f01-f02-f03-n5-20260813-r1`
- active cycle: `cycle`

## 不足slot

`seed-pool`はCandidate205の3ケースについてrun 0件のpoolを作成した。`plan-missing --desired-count 5`は各ケース`existing=0 / missing=5`、合計15件だけを返した。各slotは独立sample IDを持ち、設定上の並列上限はM=24である。

## 互換条件

F01〜F03のcase revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はreferenceと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

`prepare-comparison-layer1`、atomic plan生成、`preflight-comparison`および`verify-comparison-preflight`はすべて成功した。実行直前にも同じreceiptを再検証し、一項目でもdriftした場合はadapter起動前に停止する。

`candidate205_existing_0 / candidate205_missing_15 / authorized_15 / issued_0 / comparison_preflight_ready / candidate205_not_evaluated / Standard14_not_started`
