# Candidate261 A01 / F03 N=5実行準備監査

## 結論

Candidate147の保存済みStandard14 atomic runからA01とF03を各5件選び、新しいrunを発行せず参照result `ea9b4bfba2054405896a886be25fe6b1`へ固定した。Candidate261のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、許可10件、発行0件だった。

## 発行前固定

- 対象: A01 r2、F03 r2、各N=5。
- Candidate261 bundle SHA-256: `e651154c31525acf346ce42f0dd002e79522ecb0b5cc478fb56d272df763b7ad`。
- 参照result: `ea9b4bfba2054405896a886be25fe6b1`。
- 参照元のCandidate147 Standard14 result: `f7baeadc5bd44399ac13cc0e0a8aff48`。
- comparison compatibility key: `740cb6782860f75b91235e9f2c9926554e68bd1838e7749f8f414265d6050c8f`。
- Candidate261 pool: `e8bea7021920079ab87acfaa0971f99d6df676ead9929e5ae9bcf0601e2ec627`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。

保存済み14ケースLayer 1をそのまま2ケースresultへ渡した最初の準備は、coverageが14ケースと2ケースで一致せず停止した。評価slotは0件だった。この失敗実体は`cycle-failed-full-coverage`として保持した。続いて保存Layer 1のsetとfixture bytesを変えずに複製し、公式`bind-coverage`でA01、F03、iteration 1〜5だけを固定した。条件を緩和せず、2ケースの参照result、2ケースcoverageのLayer 1、2ケースprofileを一致させた。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptは10件だけを許可し、Candidate147の新規runは許可していない。

## 実行後状態

許可10件を発行し、10 / 10件がvalid、excluded 0、実行エラー0だった。評価と比較は[Candidate261 A01 / F03 N=5結果](../evaluations/results/candidate261-spec-output-consumer-closure-a01-f03-n5_2026-08-16.md)へ分離して記録する。

`preflight_completed / authorized_10 / issued_10 / valid_10 / reference_rerun_0`
