# Candidate226 A02 N=5実行準備監査

## 結論

Candidate147の保存済みA02 5件を参照result `c08d676a0d97424f88dc2ab1d7fe2961`へ固定し、同じfixture bytesを持つA02 coverageのLayer 1へbindした。Candidate226のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 発行前固定

- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- N: 5
- candidate bundle SHA-256: `5545d75864a396a6eedbc3212c24e6f5cd0322a35313fdaa04f3e29b5f8b25dd`
- reference result: `c08d676a0d97424f88dc2ab1d7fe2961`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- candidate pool: `418d13570507c9637d566a7f417eae173620451dc32df606d66e7299980743c0`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- configured M: 24
- token accounting: all-agent v1

Candidate147の全14ケースresult `f7baeadc5bd44399ac13cc0e0a8aff48`から、保存済みA02 5件だけをatomic selectionとして選び、新規実行せず一ケースの参照resultへ登録した。参照Layer 1は、保存済みStandard14 Layer 1のsetとfixtureをbyte変更せずcloneし、公式`bind-coverage`でA02とiteration 1〜5だけへ固定した。

## 発行前停止の履歴

最初の比較確認は、全14ケースの参照resultに対してA02だけのprofileを照合したためcoverage不一致で停止した。次の確認は、一ケースの参照resultに対して14ケースcoverageのLayer 1を渡したため停止した。いずれもpreflight前で、評価slotは0件のままである。coverage条件を緩めず、一ケースの参照result、一ケースcoverageのLayer 1、一ケースprofileを固定し直した。

最終receiptはprofile SHA-256 `9fece2e7e6af610c68daf6ce9207371b50a32dc3ce028d5739039123f8a0b5b2`、global plan SHA-256 `3a4057e3df868981a1fddff4ad2beca06aa034bdc41d514c223111b518ff6070`、許可5件、発行0件を固定した。

## 発行前状態

`preflight_ready / authorized_5 / issued_0 / a01_not_authorized`

この状態は発行直前のreceiptを記録する。実行後の判定は[`candidate226-human-result-effect-scope-a02-n5_2026-08-14.md`](../evaluations/results/candidate226-human-result-effect-scope-a02-n5_2026-08-14.md)を正本とする。
