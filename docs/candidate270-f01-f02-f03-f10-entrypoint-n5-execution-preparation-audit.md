# Candidate270 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate269の保存済み四ケース各N=5を基準result `2398d22125bd4e658fe5b653679167b5`へ固定した。Candidate270のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。Candidate269は再実行せず、容量guard通過後にCandidate270の不足20件だけを発行する。

Candidate269 N=20登録result `544afbe7e2444037932c7313da4489b6`は初期N=5のLayer 1生成基準に使わず、追加Nへ進んだ場合のKPI比較に使う。N=20 resultへN=5 Layer 1を誤って結びつけた準備試行はcoverage不一致で停止し、評価slotは一件も発行していない。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate270 bundle SHA-256: `481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439`。
- 直接比較基準: Candidate269 N=5。
- 基準result: `2398d22125bd4e658fe5b653679167b5`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate269 pool: `97ddb64f950344d48844361e59422eccd55c32d4132ec9820dd52de2ff41a1d5`。
- Candidate270 pool: `331cef1ce4e99059530788357b1b19cfac27b98bd53620b52dc78f0d4a2b2b3f`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `e719232bdf40b7fdf9964aba7bc2c3cb2f4dc683255639e61637c2f92802e6fe`。
- global plan SHA-256: `c1d6692e991f0d0a9f0474c36b1d1a6d457eb7ba74fb4bd50aec26eda2d7fcc8`。
- preflight receipt file SHA-256: `baa932ecb4f316505810866e643423a244cda893f329e95842097aebd44aa234`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

C269の保存Layer 1には同cycleのwrite-once `comparison-generation.json`と`comparison-preflight.json`も含まれていた。正本を変更せずclonefileで今回専用の参照コピーを作り、そのコピーから旧cycleの二receiptだけを除外した。`prepare-comparison-layer1`はset、coverage、全fixture identityを基準resultへ再照合し、新しいcycleのreceiptを生成した。prompt、case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executorおよびtoken accountingは変更していない。

容量guardは発行前に実行し、free `34,756,096,000` bytes、2.5 GiB発行後の予測free `32,071,741,440` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点・機序状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。比較可能な登録resultは`e34f3b5820d745f5912e5af82fede6aa`であり、Candidate269とC147のrunは再実行していない。execution archive SHA-256は`41c2019074f82eb18dd743eebe1b737df70e15dc8447e5be3c7af0cf748111ed`、final evidence archive SHA-256は`acaa9126785a8264c12901881cdc9517fa7cb5093414c36ee2ced8ddf68c3895`である。

四ケース合算中央値はCandidate269比でtoken `-36,301`（`-6.38%`）、経過時間`-82.007`秒（`-22.27%`）となった。一方、F01・F02の10 / 10件が外側validation wrapperを使わず、required validationと後続diff / statusを個別tool resultへ分割した。対象だったpredicate-bound resultは保持wrapper内で0 / 10件、F03共同発行も0 / 5件だった。KPI低下は対象機序ではなくwrapper迂回によるため、N=20へ進めない。

現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed / quality_passed / kpi_decreased_by_bypass_route / target_mechanism_not_exercised / f03_regressed / mechanism_failed / no_n20_extension / stopped`である。
