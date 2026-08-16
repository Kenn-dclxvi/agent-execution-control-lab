# Candidate263 F03・F10 entrypoint N=5実行準備監査

## 結論

Candidate254の保存済みStandard14 N=5からF03とF10 entrypointを各5件選び、基準result `c9023c2303bd45cebb61bd67736f34e4`へ固定した。Candidate263のprompt identity以外の比較条件は一致し、最終の比較前receiptは`ready`、Candidate263の不足10件だけを許可した。Candidate254、Candidate147、Candidate261、Candidate262の新しいrunは発行していない。

## 発行前固定

- 対象: `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate263 bundle SHA-256: `4fd4bb75be18f7882df98368898d38759a9a37336269e61f4f0eef6d77f4841e`。
- 直接比較基準: Candidate254。
- 基準result: `c9023c2303bd45cebb61bd67736f34e4`。
- compatibility key: `f02b8f95c958a564b607d0aaf73f8402baa90fc54a1bc703375d3ec8796adc32`。
- Candidate254 pool: `e71ba5db8f3766df39c9c9af10970888e820ff04761b4f709cd543faa01e8b38`。
- Candidate263 pool: `d19411543307e3b15daea409464d3b34eca25fe870be0b35dac7ba4bd9518a93`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。

## 事前停止の保持

一回目の基準result登録は、二ケースのprofileからA01用の診断条件を削ったため、保存済みrunの比較条件と一致せず停止した。A01は発行対象ではないが、全体のrating条件を基準どおり戻した。

二回目は、二ケースの基準resultに対して14ケースのLayer 1を直接指定したためcoverage不一致で停止した。Candidate254 Standard14 N=5の保存Layer 1からsetとfixtureを同一modeのまま複製し、二ケース各5件だけを`bind-coverage`で固定した。

通常の`cp -R`ではsymlink modeが`0700`から`0755`へ変わり、fixture identityが一致しなかった。このコピーは基準に使わず、modeを保持するコピーからLayer 1を作り直した。最終の`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。これらの停止中に評価slotは一件も発行していない。

## 実行後状態

許可済み10件だけを発行し、10 / 10件がvalid、excluded 0、実行エラー0だった。採点時はrating viewの未生成を点数書込み前に検出し、同じ保存runから10件のviewを作成した。評価slotの再実行は0件である。

現在状態は`preflight_ready / authorized_10 / issued_10 / valid_10 / excluded_0 / execution_errors_0 / reference_rerun_0 / rating_view_recovery_without_slot_rerun / rerun_0`とする。
