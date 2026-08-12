# Candidate190 ADR05・ADR07・ADR09 N=20拡張実行準備監査

> **位置づけ**: M6実行前監査／既存15件再利用／不足45件承認／発行0件

## 結論

Candidate190のM6は、`TC-ADR05`、`TC-ADR07`、`TC-ADR09`の既存各5件を再利用し、累積各20件に必要な不足各15件、合計45件だけを発行できる状態まで準備した。comparison preflightは45 slotを`ready`として承認し、監査時点の発行数は0件である。

最初のpreflightは累積N=20 profileを互換基準へ直接使ったため、保存済み基準のcoverage N=5との不一致で停止した。この試行ではslotを一件も発行していない。正規のatomic N拡張手順に従い、M5の三ケース各5件を固定するreference profileを分離し、N=20は最終selectionのcoverageとして扱った。条件を除外または緩和せず、canonical receiptは`cycle-r3`に固定した。

## 固定identity

- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- reference result: `72b1167d8bd84719b975d227c590aa4e`
- reference result content SHA-256: `2f062f27deb082c7551a75af195e4d577481b5b59f1de32a65c39f7b37bc5117`
- reference profile: `candidate190-current-prior-review-result-admission-adr05-adr07-adr09-reference-n5-medium-m24-cli0146`
- final profile: `candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-medium-m24-cli0146`
- pool key: `11b57d4d2908982935f1d21fef9e541e56313b0b2240764f852ac9a7222d58c1`
- compatibility key: `155587cce22ef1f34d5366bd6612a0a6e69ed8225160c51cd5abc6fada945b15`
- comparison receipt content SHA-256: `e2be696cb49c91bbd34904c40a6dc788983ae883b3d035baf42e28354008f009`
- global plan SHA-256: `c6305eb8767ce8f60e92b2cf3e15df8bd07a6bff2258ff6332b72dbd39feb7bb`
- dispatch plan SHA-256: `ae470c436687ea8f7df6d0767011d0d7603b3d3302735e312e48e4c463e0f7f6`
- max workers: `24`

一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-20260812-r1`に保存した。実行対象は`atomic-plan-r3/global-plan.json`、comparison preflight正本は`cycle-r3/layer1/comparison-preflight.json`である。

## 発行範囲

| case | 既存再利用 | 新規承認 | 累積gate |
| --- | ---: | ---: | ---: |
| `TC-ADR05` | 5 | 15 | 20 |
| `TC-ADR07` | 5 | 15 | 20 |
| `TC-ADR09` | 5 | 15 | 20 |
| 合計 | 15 | 45 | 60 |

`TC-ADR01`〜`TC-ADR04`、`TC-ADR06`、`TC-ADR08`およびTPO系列は追加発行しない。

## 監査結果

1. evaluation set、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件およびLayer 1はM5基準と一致した。
2. `plan-missing --desired-count 20`は既存各5件を数え、不足各15件だけをdispatchへ含めた。
3. 45 capsuleはCandidate190のprompt identityと固定comparison conditionsへbindされた。
4. templateとcapsuleにはprivate oracle、期待terminal、期待review件数、過去Candidateの結果、quality scoreまたはresult kindの正解値を混入していない。
5. M=24を不足件数へ合わせて変更せず、`environment_adjustment=none`、`max_attempts=3`を維持した。
6. preflight失敗履歴は削除せず、未発行の準備診断として保持した。canonical receiptだけを`cycle-r3`へ一意化した。

## 境界

本監査が証明するのは、比較互換性、入力封鎖および発行範囲だけである。Candidate190のquality、mechanism、採用、releaseまたはprojectionは証明しない。次に許可する操作は、固定global planの45 slotを発行することだけである。

## 状態

`execution_preparation_passed / reference_n5_bound / cumulative_n20_final_gate / authorized_45 / issued_0 / private_boundary_passed / ready_for_m6_execution`
