# Candidate206 admitted evidence current ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate206のADR9 r2全9ケース各5件は、Candidate175の登録resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可し、発行数は0件である。

## 固定identity

- profile SHA-256: `8994264cd2f92ccc7a8adf846704a2212a3f1ba21581f89a2ed998475ac7a279`
- reference result: `eba0a4bc1d0e4391afa631462b8daccb`
- reference result content SHA-256: `2259531513f1570ef0b2f30f5d28ea28991690781d64d4eaceba7dc49b9854f6`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate175 reference pool: `7d74359509c49cb3cc273a50712d8e7ad0bd74204404ba690b6bdfb6248288af`
- Candidate206 pool: `bff5449e6489cff8c22e4627252bc06a570e1520ddf70b9f2b103c05f90a3483`
- dispatch plan SHA-256: `c57178779d7f7aff2dd52cced8b1be493838ee04f63727120b8b65f75a23314b`
- global plan SHA-256: `f6a09280820bd6f070829267e1bca7b06cd0c96bd86fa0a3f964b85b318e55bd`
- comparison generation receipt content SHA-256: `86676c74c4c7495473ceeaa028ac77cdc588d43be2ef0b13e3e54716f2323bfb`
- comparison preflight receipt content SHA-256: `e5fd869a81299afa444a7a2b2e6502c951df4fcf00bc9a8ed487a9ddf4737bad`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate206-admitted-evidence-current-adr9-r2-n5-20260813-r1`
- authoritative cycle: `cycle-r2`

初回の`cycle`生成は、基準の`cycle/layer1`を指定したため過去のwrite-once comparison receiptまで複製し、新receiptと衝突して停止した。slotは発行されていない。基準resultが使用した`reference-layer1`へ入力を訂正し、新しい`cycle-r2`で生成とpreflightを完了した。失敗した`cycle`は診断記録として残し、評価には使用しない。

`seed-pool`はCandidate206の空poolを作り、`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件と固定した。45 capsuleは独立sample IDを持つ。

Evaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はCandidate175登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

`candidate206_existing_0 / candidate206_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate206_not_evaluated`
