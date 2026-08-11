# Candidate187 TPO04 N=20拡張実行準備監査

> **結果**: `execution_preparation_passed / fifteen_missing_slots_authorized / zero_slots_issued`

## 結論

Candidate187の`TC-TPO04`を累積N=20へ拡張する準備は完了した。初回Targeted試験の適格なatomic run 5件を再利用し、不足する15件だけを新規発行対象へ固定した。比較前ゲートは`ready`で、15 slotが承認され、発行数は0件である。

一次監査票は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate187-review-admission-proof-obligation-tpo04-n20-20260812-r1/execution-preparation-audit-r2.json`に保存した。

## 基準と不足分

- reference selection ID: `8950d821a2fd4c599cfea615754b0cb4`
- reference result ID: `3b7d157cb3844bfc866374c2e0b15ad0`
- atomic pool key: `9b1d45d124c63e1c705b25ae1f7c351c92ca10275f7a015bb363eafc740fa668`
- 既存run: `TC-TPO04` 5件
- 要求件数: 20件
- 新規発行対象: `TC-TPO04` 15件

`N`とiteration集合はatomic poolのmember identityへ含めず、既存run集合と不足dispatchを分離した。既存5件は再実行しない。

## 固定内容

- frozen set SHA-256: `e8da310d71c5b5c2a478dc39172898137f75a437276d27101b8dadeb5aa91e26`
- evaluation set identity SHA-256: `736421076b89577846e5618102a1bad30fdd9b495548ff1ba9e30b923109b438`
- `TC-TPO04` fixture SHA-256: `1ec8006dc50cdb5712ab31ebfb919e2d85b7ce2a228ac4a9f8bc183e7906254d`
- dispatch plan content SHA-256: `6e5c8adf1c79e7714f187b7b59ad349a2299614dacc49f5350b9cf019b069591`
- global plan SHA-256: `d764148adbb2c62b5fbfe3a46a3e52e0ccb7ce74a3120b4abd7e3dcd82dc3b21`
- comparison preflight file SHA-256: `ab01b757194d953ecb6d2ff8ed6f575f81900cb1a3a2fc671d9cd5a3e3bdc65b`

15 capsuleはすべて`the-caption-prompt.execution-capsule/v3`で、`TC-TPO04`だけを対象とし、相異なる`sample_id`へ固定されている。固定setとcapsuleにprivate oracle、期待score、期待review件数、過去Candidate結果は混入していない。

## 初回準備失敗の扱い

初回の`cycle`と`plan`は履歴として保存した。初回は6ケースcoverageのLayer 1を単一ケースのreference resultへ結び付けようとして拒否され、比較前ゲートを通過していない。試験slotも発行していない。

再準備では別経路`reference-cycle-tpo04-n5`、`cycle-r2`、`plan-r2`を使用した。基準coverageを既存5件へ固定し、不足15件をatomic dispatch側で承認したため、保存済み5件と新規15件の役割が混ざっていない。

## 境界

本監査が確認したのは互換性、入力固定、不足件数および発行可能性である。quality、mechanism、採用、releaseまたはprojectionは未判定である。次に許可される操作は、`plan-r2/global-plan.json`で承認済みの15 slotを発行することだけである。

## 状態

`execution_preparation_passed / reference_five_reused / missing_fifteen_only / authorized_fifteen / issued_zero / private_boundary_passed / ready_for_execution`

## 後続実行

本監査で固定した`plan-r2`は変更せず後続で発行され、新規15 / 15 valid、除外0件、外部エラー0件で完了した。既存5件との累積結果は20 / 20 Score 4、機構成立20 / 20だった。本節は実行前監査の当時状態を上書きせず、実行後の導線だけを追加する。結果と現在判断は[`Candidate187 TC-TPO04 N=20`](../evaluations/results/candidate187-review-admission-proof-obligation-tpo04-n20_2026-08-12.md)を正本とする。
