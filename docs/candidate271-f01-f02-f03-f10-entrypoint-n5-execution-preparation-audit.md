# Candidate271 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate269の保存済み四ケース各N=5を基準result `2398d22125bd4e658fe5b653679167b5`へ固定した。Candidate271のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。容量guard通過後にCandidate271の不足20件だけを発行し、Candidate269、Candidate270およびCandidate147は再実行していない。

## 発行前固定

- 対象: F01 r3、F02 r1、F03 r2、F10 entrypoint r1、各N=5。
- Candidate271 bundle SHA-256: `368d6e420b08ab1675834a15b828558c7ad4842e7c1d9155a870c1defc72ee89`。
- 直接比較基準: Candidate269 N=5 result `2398d22125bd4e658fe5b653679167b5`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate269 pool: `97ddb64f950344d48844361e59422eccd55c32d4132ec9820dd52de2ff41a1d5`。
- Candidate271 pool: `18ad6641c51adc9f1029f4d448351b2586c6d9bb46dc844f21c15a4fc1e117ea`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `93a67c816c70cd0fe9a6ff3ede0e590e5c43abeeaab5d46ae4f8baaa62dc3487`。
- global plan SHA-256: `17629588944d8725c5e0053f256175e976ab1a30504ebbb393ae938eab36d73b`。
- preflight receipt file SHA-256: `eef89742eadafbe7635a84ccce7b7a09593b0acee6932df98fee4391c089afb2`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

最初の`prepare-comparison-layer1`は、C269 Layer 1に残る旧write-once `comparison-generation.json`を専用cycleへ複製したため、receipt上書き拒否で停止した。評価slotは0件だった。不完全cycleを退避し、C269 Layer 1のclonefile-backed参照コピーから旧`comparison-generation.json`と`comparison-preflight.json`だけを分離して再実行した。set、coverage、fixture identityおよび基準resultは変更していない。

容量guardは発行前に実行し、free `34,702,979,072` bytes、2.5 GiB発行後の予測free `32,018,624,512` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点・登録状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。execution archive SHA-256は`a4423be7ee08bf5891d100795d53e45f3b4ecf913e4ecfa513dc8e953e502ac1`、final evidence archive SHA-256は`1bf66778455c3d185ada2db5e5914c50cccabca7e40a7fbf22512dac13847032`である。

品質監査の最初の適用は、owner-producer evidenceとblind `rating-view`がまだ生成されていなかったため、rating書込み前に停止した。固定collectorでcommand evidenceとowner-producer evidenceを生成し、execution sealでrating viewを固定してから同じ20件へ採点を適用した。owner-producer collectorのexit 1は契約どおり診断だけに保持し、品質scoreを変更していない。

最初のselection登録`3c28d737d2ff475b8119b8bd2a717d93`はreference resultとcycle receiptを付けず比較不能になった。同じselectionを再実行せず、Candidate269 resultとcycleへbindした比較result `baf01e47d8d8432bbe2dc92a961287cb`を別IDで登録した。

現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / score4_20 / reference_rerun_0 / comparison_registration_completed / target_route_not_exercised / token_not_improved / mechanism_failed / no_n20_extension / stopped`である。
