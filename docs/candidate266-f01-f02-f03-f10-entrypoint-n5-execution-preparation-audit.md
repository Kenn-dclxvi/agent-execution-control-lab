# Candidate266 F01・F02・F03・F10 entrypoint N=5実行準備監査

> **目的対応の訂正（2026-08-16）**: 比較互換preflightは成立したが、Candidate266は固定すべきCandidate254改善系列の`task_objective`に対応していなかった。比較条件が一致することは、派生operationが利用者目的を直接進めることを証明しない。本来は不足20件を発行せず、同じ目的を満たすCandidate254基盤の設計へ進むべきだった。以下は実際に発行した履歴と手順逸脱を保存する監査であり、現在系列の実行許可根拠には使わない。

> **Candidate267方針（2026-08-16）**: 後続の明示判断では、Candidate267の直接基盤をCandidate264へ固定した。Candidate264の本文とF01・F02・F03の成立効果を保持し、F10のpermission edgeだけを閉じる。上の当時の訂正文と実行履歴は変更せず、Candidate266をCandidate267の親、必須gateまたは成功根拠にはしない。

## 結論

C147の保存済みStandard14 poolから対象四ケース各5件を選び、基準result `29cf98307448409f820a739b2d008f7b`へ固定した。Candidate266とのprompt identity以外の条件は一致し、比較前receiptは`ready`、不足20件だけを許可した。C147の新規runは発行していない。

Candidate266は、Candidate264を置き換える完成案ではなく、exact instruction pathと配下pathの関係だけでpermission edgeを閉じられるかをC147上で単独検証する機序probeである。Candidate254系にある他の有効制御の保持は、この比較の成立範囲に含めない。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate266 bundle SHA-256: `274217c1f7adbaadbbb7bbec31a3443bdd336f53b5794ef99d799f8509dbc4b4`。
- C147基準selection: `ad6913bd8bba4780ab97ffcd6ec1652a`。
- C147基準result: `29cf98307448409f820a739b2d008f7b`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate266 pool: `17d3405266eedf5e4569fea579c34d14dce3b4c8e826d9f1cf3395320dcabcf3`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `65fcfe6476860f95403588e5a641c27b1d4802b88f78e3ea98b5fc227a9eb811`。
- global plan SHA-256: `dec14a67e1b40dabf814baa754e23cea341548abb447a76e6192c60034b30fa0`。
- preflight receipt content SHA-256: `6e0931f6fc5cd1f510bcf758eae8758c76394326cc8730f42ddb53a9111c1b02`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

## 容量guardの手順逸脱

`long_run_storage.py guard`を評価slot発行前に実行すべきだったが、20件のterminal完了直後まで発行していなかった。完了直後の観測はfree `36,379,435,008` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで、停止条件には該当しなかった。

この逸脱はprompt、fixture、TaskSpec、capsule、model-visible inputまたはrun resultを変更していないため比較resultを再実行しない。ただし、正しい時機でguardしたことにはせず、運用監査上の逸脱として保持する。

## 実行後状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0だった。Candidate266 selectionは`0cbcb3a897aa402397d91b43aa49ecac`、analysisは`111fd55bcc0741d3a85c32f307b1a48e`、登録resultは`5ca7e3a68e444ccbad70ecf50a82236a`である。

execution sealと最終圧縮を完了した。execution archive SHA-256は`a30c738de42199bdd313b88f6cf7d82021d56eeeb936605246dd8fbd2d77a4ca`、final evidence archive SHA-256は`734a2d15d3f31f69a65d290fd10334b0f98681fd25effeefa445450540c70560`である。当時の実行状態は`preflight_ready / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed / capacity_guard_timing_deviation_retained`として保持し、現在の位置づけを`objective_mismatch_confirmed / off_target_execution_history / not_reusable_as_current_objective_admission`とする。
