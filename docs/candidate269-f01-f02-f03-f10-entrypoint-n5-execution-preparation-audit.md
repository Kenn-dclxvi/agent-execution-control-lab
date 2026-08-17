# Candidate269 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate268の保存済み四ケース各N=5を基準result `f43e7342001140b38f7f33e5bcb73cac`へ固定した。Candidate269のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。Candidate268は再実行せず、容量guard通過後にCandidate269の不足20件だけを発行する。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate269 bundle SHA-256: `19630df248b648690238757813941f55e97aa82c8b5597659a9e731d0877162f`。
- 直接比較基準: Candidate268。
- 基準result: `f43e7342001140b38f7f33e5bcb73cac`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate268 pool: `c8ab9726010f7c2c2ef87d61e868984e29edfad38ae4db8dde211d4b74676e25`。
- Candidate269 pool: `97ddb64f950344d48844361e59422eccd55c32d4132ec9820dd52de2ff41a1d5`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `815ce16c7612a759b807f4d62c830c2fdfdb64eec4693ff02b47b5d0d0d685fa`。
- global plan SHA-256: `dfc3abb0fadb6c64d017cdc025f23a283d425122d75afefc2dc67c60ad25d260`。
- preflight receipt content SHA-256: `06b41e3ca539e962c737c5c31f59c10e71dc80908709c6e23fd38116b8380817`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

容量guardは発行前に実行し、free `35,458,396,160` bytes、2.5 GiB発行後の予測free `32,774,041,600` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。Candidate269 selectionは`39f9d580b9ed469ead8bee9edf81c01d`、analysisは`1241c8e2414e4b65b75fb377f8eed133`、比較可能な登録resultは`2398d22125bd4e658fe5b653679167b5`である。基準Candidate268のrunは再実行していない。

採点用の事前観測より先にexecution sealを実行したため、最初の監査収集はscore書込み前に停止した。execution archiveを一時領域へ復元して事前観測だけを生成し、run再実行0件で元のsealed batchへ採点を適用した。一時復元領域はシステムのゴミ箱へ移動した。execution archive SHA-256は`edfe9f91c602b3d03bfed010288f6ec3570430212455035b4a4c03042e746d63`、最終evidence archive SHA-256は`8475169bde8bd18461d45381eed5cfef70b5e20328ad4365a294dd21ceeafa0b`である。

機序判定はterminal dependency 9 / 9、F01 5 / 5、F02 5 / 5、F10 5 / 5だったが、F03共同発行が4 / 5となったため停止した。現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed / scoring_order_recovered_without_rerun / quality_passed / terminal_dependency_passed / f03_mechanism_failed / stopped`とする。
