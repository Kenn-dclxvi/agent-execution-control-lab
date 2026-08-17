# Candidate268 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate254の保存済み四ケース各N=5を基準result `4208b6ca016d485684f8df9fadc5b38e`へ固定した。Candidate268のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。Candidate254は再実行せず、容量guard通過後にCandidate268の不足20件だけを発行する。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate268 bundle SHA-256: `c09072b2ec153fec63a4e07b2767e7e68499ffcdeef9375bed46f2d03215b9a5`。
- 直接比較基準: Candidate254。
- 基準result: `4208b6ca016d485684f8df9fadc5b38e`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate254 pool: `e71ba5db8f3766df39c9c9af10970888e820ff04761b4f709cd543faa01e8b38`。
- Candidate268 pool: `c8ab9726010f7c2c2ef87d61e868984e29edfad38ae4db8dde211d4b74676e25`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `f66025038b6d2b11458b84d1847fef759e97b9ae6b37db867ee4653af01e5822`。
- global plan SHA-256: `64f0d140b4dac04863fde4134d38dbe2a1566c9ca8612fd99b73b63b3b817ab9`。
- preflight receipt content SHA-256: `4feb9b5c1084426f0d7193ea2fedad79546e29b42d130d6551bcab83b6a59d83`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

容量guardは発行前に実行し、free `34,302,091,264` bytes、2.5 GiB発行後の予測free `31,617,736,704` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。Candidate268 selectionは`4eb73116df5d4aada04d2348f5eab192`、analysisは`33ddc7af1dfb4b6bb3c351c207943a5c`、比較可能な登録resultは`f43e7342001140b38f7f33e5bcb73cac`である。

command evidenceをworkspace削除前に収集した後、execution sealでrating viewを生成して採点した。最初の採点試行はrating view未生成を検出し、score書込み前に停止した。runの再実行はない。execution archive SHA-256は`dc0d99a4cecc34812cb001336acae281b9b4324d1a38a289ee5e53465271c11c`、final evidence archive SHA-256は`a076c04ef9d889b4aae9e0174ba815469e2e514c06cc5d79b1e72e370d631dc6`である。

最初のselection result登録では`--reference-result-id`と`--cycle`を省略し、四ケースfixtureだけを持つ非互換result `7e238bcbaf93457aa2e153d64ec69fd9`をappend-only registryへ作成した。このresultは比較と判断に使用していない。Candidate254の完全なcompatibilityを継承した`f43e7342001140b38f7f33e5bcb73cac`だけを登録resultとして扱う。

現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed / quality_passed / mechanism_failed / stopped`とする。
