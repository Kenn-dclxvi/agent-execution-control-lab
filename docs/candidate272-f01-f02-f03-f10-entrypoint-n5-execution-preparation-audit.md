# Candidate272 F01・F02・F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate269の保存済み四ケース各N=5を基準result `2398d22125bd4e658fe5b653679167b5`へ固定した。Candidate272のprompt identity以外の比較条件は一致し、比較前receiptは`ready / authorized_20 / issued_0`となった。容量guard通過後にCandidate272の不足20件だけを発行し、Candidate269とCandidate147は再実行していない。

20 / 20件がvalidかつScore `4`だったが、raw rollout基準のF03共同発行は3 / 5で、raw resultをwrapper carrierへ収容するrouteが10 / 10件で残り、F01同理由再取得も1 / 5件で発生した。F01・F02 token中央値がCandidate269比でそれぞれ`+18.04%`、`+32.15%`へ悪化したため、N=20は発行していない。

## 発行前固定

- 対象: F01 r3、F02 r1、F03 r2、F10 entrypoint r1、各N=5。
- Candidate272 bundle SHA-256: `6830ca4b0a48ffa96b6145bcf6f5ac48980cb3b1816878f682a25da2dc79e5f1`。
- 直接比較基準: Candidate269 N=5 result `2398d22125bd4e658fe5b653679167b5`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate269 pool: `97ddb64f950344d48844361e59422eccd55c32d4132ec9820dd52de2ff41a1d5`。
- Candidate272 pool: `998ab18a9b783c2e0383084960bf59c1636c2fe82ee28ca334589a9e152da048`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- profile SHA-256: `ca3ea3d089cbe31f954184052024a1761a3c926cbca7fc060514920e941a2461`。
- global plan SHA-256: `c57fd347914f5e8dae61a4d2010a382be6fdb7a7ec01e311657a12757093c647`。
- preflight receipt file SHA-256: `4457b3347183112c9b831734d00d3d01ed0142ce0d164af61fe887183a553431`。
- 比較前receipt: `ready / authorized_20 / issued_0`。

最初のpreflight commandはreference result IDの入力誤りで、cycle作成およびslot発行より前に停止した。正しいIDへ直した後のreceiptだけを比較根拠に用いた。また、一つのplanを複数plan用campaign runnerへ渡した試行はentrypoint側で即時拒否され、slotは発行されなかった。その後、固定済み単一planを`parallel_runner.py`へ渡して許可済み20件だけを実行した。

容量guardは発行前に実行し、free `32,585,752,576` bytes、2.5 GiB発行後の予測free `29,901,398,016` bytes、dispatch停止 `26,843,545,600` bytes、hard floor `21,474,836,480` bytesで`dispatch_allowed`となった。

## 実行・採点・登録状態

許可済み20件だけを発行し、20 / 20件がvalid、excluded 0、実行エラー0、Score `4`となった。実行時間はrunner全体で105.848秒だった。execution archive SHA-256は`0e6704a76856f8594f42fa8ed90bffca2e81f4f3cc84d33021b19657bc3d8df1`、final evidence archive SHA-256は`6eb80ee80469a10c98b9b896656d5a5f6697299529d4bae74056944b13447ddc`である。

封印前にall-agent command evidenceとowner-producer evidenceを生成し、execution sealでblind rating viewを固定してから同じ20件を採点した。owner-producer collectorはexit `0`だった。20 atomic runをpoolへappend-only登録し、各ケース5件のselectionをCandidate269 resultとcycle receiptへbindしてcomparison result `8048e02d1765434fa93155a256550ce7`を登録した。

現在状態は`preflight_ready / capacity_guard_passed_before_dispatch / authorized_20 / issued_20 / valid_20 / score4_20 / reference_rerun_0 / comparison_registration_completed / f03_mechanism_failed / target_permission_mechanism_failed / major_case_kpi_regression / no_n20_extension / stopped`である。
