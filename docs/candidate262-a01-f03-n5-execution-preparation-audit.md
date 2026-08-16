# Candidate262 A01 / F03 N=5実行準備監査

## 結論

Candidate147の保存済みA01 / F03各5件を参照result `ea9b4bfba2054405896a886be25fe6b1`へ固定した。Candidate262のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、Candidate262の不足10件だけを許可した。Candidate147の新しいrunは発行していない。

## 発行前固定

- 対象: A01 r2、F03 r2、各N=5。
- Candidate262 bundle SHA-256: `61c0735fc0cadcb0d45d2132346d01540d8366040ce886bb3f4332279915ba33`。
- 参照result: `ea9b4bfba2054405896a886be25fe6b1`。
- comparison compatibility key: `740cb6782860f75b91235e9f2c9926554e68bd1838e7749f8f414265d6050c8f`。
- Candidate147 pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`。
- Candidate262 pool: `61ba30c07aec4a14de5ad4ccba114569439867552a0cab27cbb22a88bca3f39f`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。

Candidate261評価時に作成した2ケースの保存Layer 1を再利用し、set、fixture bytes、TaskSpec、case / iteration coverageを変更していない。`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptはCandidate262の10件だけを許可した。

## 実行後状態

許可10件を発行し、10 / 10件がvalid、excluded 0、実行エラー0だった。controllerの実測経過時間は76.800秒だった。

採点登録の最初の試行は、all-agent command evidenceとowner-producer evidenceが未生成だったため、scoreを書き込む前に10件すべて停止した。既存の`standard14_quality_audit.py collect`、`owner_producer_evidence.py`、`standard14_quality_audit.py apply`の順で診断用証拠を生成し、同じ10件を採点した。評価slotの再実行はない。owner-producer evidenceはF03の5件で`failed`だが、現行rating contractでは診断だけに使い品質点を変更しない。

評価と比較は[Candidate262 A01 / F03 N=5結果](../evaluations/results/candidate262-spec-false-start-state-consumer-permission-a01-f03-n5_2026-08-16.md)へ分離して記録する。

`preflight_completed / authorized_10 / issued_10 / valid_10 / reference_rerun_0 / rating_preparation_failure_preserved / rerun_0`
