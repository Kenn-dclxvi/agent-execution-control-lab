# Candidate101 Rating v14 Medium F07 canonical N=5

## 結論

Candidate101はF07 canonical r2の5 / 5でvalid・rateable・score `4`だった。一方、5 / 5すべてで対象外を含む広い検索を行い、1 / 5でGit履歴も参照した。狙った「具体的な矛盾を観測するまでは追加調査を開始しない」経路は0 / 5だった。

設計の停止条件に従い、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

Candidate101の直接親はCandidate98である。Candidate99とCandidate100はprompt lineageへ含めず、誤経路の観測証拠としてだけ参照した。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-additional-investigation-trigger-r1` |
| bundle SHA-256 | `b31f2156e599319bd243ad5487453b83297d149654f15e58c6a0b5c84d3056e9` |
| direct parent | Candidate98 |
| case | `TC-F07-CANONICAL-V4-RUNNER/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| source set identity | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| registered coverage | F07、iteration 1〜5 |
| F07 fixture identity | `bece63e466ad63f5ad0c40f23d2ac98b6a26f2033c1e6d883838e1ed6ab3ca87` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行5件、`N=5` |
| token accounting | all-agent v1 |
| result ID | `36118d9917f44180ab98b4afed0aa4ed` |
| compatibility key | `06b6c76f2ed5a00bea385adcd7c7f3f7d5619da55d2847e22c17501e0fb8d72f` |

Layer 1固定後、model slot発行前にF07 iteration 1〜5をwrite-once coverageとしてbindした。Layer 2はcoverage外runを拒否し、Layer 4はbind済み5 slotが揃ったことを確認してresultを登録した。TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterはCandidate100から変更していない。

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| required command evidence | 5 / 5 |
| command protocol violation | 0 / 5 |
| excluded attempt | 0 |
| root-only | 5 / 5 |

owner-producer evidenceは5 / 5で`failed`だが、Rating v14ではdiagnostic-onlyである。各runはrootだけで成果と必須検証を完了しており、品質scoreを変更しない。

## 追加調査の経路

| iteration | command数 | 履歴参照 | 対象外を含む広い検索 | 主な追加確認 | 判定 |
| ---: | ---: | --- | --- | --- | --- |
| 1 | 9 | `git log`あり | あり | start identity、fixture、`AGENTS.md`、seed差分 | mechanism不成立 |
| 2 | 11 | なし | あり | `scripts / tests / src / .agents / .codex` | mechanism不成立 |
| 3 | 11 | なし | あり | repository全体のstart identity文字列、entrypoint実在 | mechanism不成立 |
| 4 | 9 | なし | あり | `src / tests / scripts / .agents / .codex` | mechanism不成立 |
| 5 | 14 | なし | あり | `AGENTS.md`、identity、fixture、`.agents / .codex` | mechanism不成立 |

全runがTaskSpecと`run.sh`だけで変更箇所を一意にできたが、変更前に別の根拠を探した。iteration 1はGit履歴とseed差分まで確認した。iteration 2と4はentrypointの存在と公開対象、iteration 3はrunner identity、iteration 5は適用規則とfixtureの所在を追加確認した。

したがって、`METHOD`へ追加した四つの発火条件は検索を閉じなかった。むしろ「start gate」「適用repository authority」「曖昧さを観測したか」という新しい確認責務を作り、executorがその成立確認のために広い検索を先行させた。独立サブエージェントの事後説明で得た判断規則は、正式評価executorへそのまま移植できなかった。

## token・elapsed診断

| iteration | all-agent token | elapsed | command数 |
| ---: | ---: | ---: | ---: |
| 1 | 137,930 | 77.354秒 | 9 |
| 2 | 136,762 | 64.668秒 | 11 |
| 3 | 121,223 | 73.665秒 | 11 |
| 4 | 143,700 | 64.663秒 | 9 |
| 5 | 133,067 | 72.859秒 | 14 |
| 中央値 | 136,762 | 72.859秒 | 11 |
| 最小〜最大 | 121,223〜143,700 | 64.663〜77.354秒 | 9〜14 |

最大 / 最小比はtoken `+18.54%`、elapsed `+19.63%`である。互換なCandidate100登録resultに対してtoken中央値は`-47`（`-0.03%`）、elapsed中央値は`+0.643秒`（`+0.89%`）で、実質的に同じ中心値だった。振れ幅はCandidate100のtoken `+57.61%`、elapsed `+48.02%`より小さいが、N=5であり狙った経路も0 / 5なので、安定化効果とは判断しない。

参考として、保存済みC81 Standard14 B20のF07 100件はtoken `103,590〜321,388`、elapsed `57.155〜149.407秒`、中央値は`144,585.5`と`83.286秒`だった。Candidate101 N=5はこの分布内にある。KPI差を`METHOD`置換の効果へ帰属しない。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate101-additional-investigation-trigger-v14-medium-f07-canonical-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/36118d9917f44180ab98b4afed0aa4ed.json`
- preflight receipt: campaign直下`preflight-receipt.json`
- quality audit: `batch-001/quality-audit.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`

execution archiveはSHA-256 `a65779a307e5d3a9e343c322f319e211470fb5f413dcb399ece3dac5a7cc8ca7`でseal済みである。非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
