# Candidate267 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate264の保存済み四ケース各N=5を基準result `1a64c1b2429c4e89aff3aedd6836944e`へ固定した。Candidate267のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。発行前に容量guardを通過してからCandidate267の不足20件だけを発行し、Candidate264は再実行していない。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate267 bundle SHA-256: `f76cd120292ba1ca6e8752e3bd15ca3376571fe176db722b1650353400216684`。
- 直接比較基準: Candidate264。
- 基準result: `1a64c1b2429c4e89aff3aedd6836944e`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate264 pool: `2492f6513ec56a00e80104de1ff63f1252448b273cede8d6d2d1c56e04c18d8c`。
- Candidate267 pool: `ed1c860b9ba7bee816e59b2c6e20990f978f36782d0cf39d46a4408461de1864`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `3a48f9815dd86afcc1732577af853b878d06844d08e613b4bbbb086e55c0ba44`。
- global plan SHA-256: `e09d6729f70e9f309a994e44150426467ea1222bac84b46e40be068830954b83`。
- preflight receipt content SHA-256: `810f8387ba0d3e9706030bc7c565922e160fce032ef6ea86acf290a9d361119e`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

容量guardは発行前に実行し、free `34,098,925,568` bytes、2.5 GiB発行後の予測free `31,414,571,008` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。Candidate267 selectionは`3f1973df77be40f8ae7eb7e9a9cce825`、analysisは`848088e5d58c4aad84f07e12f1cf9da8`、登録resultは`e4dee1e302a2468ba055500a0c3610d7`である。

採点用command evidence収集前にexecution sealを先行したため、collectorはworkspace不足でscore記録前に停止した。検証済みexecution archiveから20 workspaceだけを復元し、runを再実行せずcommand evidence収集、owner-producer診断および採点を完了した。復元workspaceはseal receiptのexact path 20件へ限定して再度除去した。この回復はmodel-visible input、run result、rating viewまたは比較条件を変更していない。

execution archive SHA-256は`4c19b5fe3491641a04c0305c6ad71d0dc5e8908f4227417d6041433b47037c2f`、final evidence archive SHA-256は`683abd1269b95fa61485af5cf297e132a01dc6164cb79ef049daa6ab4aa01fe5`である。評価後の判断は[`Candidate267 F01・F02・F03・F10 entrypoint N=5`](../evaluations/results/candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)へ分離する。

現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed / scoring_order_recovered_without_rerun`とする。
