# Candidate203 certificate-gated review read ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate203のADR9 r2全9ケース各5件は、Candidate202登録resultとその保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `6df56b9d3f67868f801bfc735ebdd5fda5922e4690c8d06ef4dc8943675dc32c`
- reference result: `0a509a780f0e40ae857ea602f00ff89b`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate202 reference pool: `40e9e885b6c19e9a43680c0cd61b0034abb7de67911530a4d1faef8f0f0fd169`
- Candidate203 pool: `70d1a0d1f55219ada2bf3dd4f32da170bac4ad7ab557b72fe80685264ac7a062`
- dispatch plan SHA-256: `d4e8257089f868a0d44da74997e6a38f38ed6817cb5443894b2eeffdb63ff46c`
- global plan SHA-256: `e1345223231125aa887e14510069cd954fbb317fad95bdcf6ea78772a3c35792`
- comparison generation receipt SHA-256: `0051b416295053565cf75c5f9989aea2fb054ed4b5b32acd3f92191e94bf7826`
- comparison preflight receipt SHA-256: `c7cc8f99a43b6929c17c7bfe9561f5d780307e95a9d8018e8b1d9953ea8aea0e`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate203-certificate-gated-review-read-adr9-r2-n5-20260813-r1`

## 不足slotと互換条件

`seed-pool`はCandidate203の空poolを作成した。`plan-missing --desired-count 5`の結果はADR01〜ADR09のexisting各0、missing各5、合計45件である。各slotは独立sample IDを持ち、global planの設定上の並列上限はM=24である。

Evaluation set identity `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`、全fixture identity、case revision、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はreferenceと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

`prepare-comparison-layer1`、`prepare_atomic_plan`、`preflight-comparison`および`verify-comparison-preflight`はすべて成功した。run直前にも同じreceiptを再検証し、一項目でもdriftした場合はadapter起動前に停止する。

`candidate203_existing_0 / candidate203_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate203_not_evaluated`
