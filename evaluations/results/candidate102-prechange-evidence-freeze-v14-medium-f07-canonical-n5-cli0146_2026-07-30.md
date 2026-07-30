# Candidate102 Rating v14 Medium F07 canonical N=5

## 結論

Candidate102はF07 canonical r2の5 / 5でvalid・rateable・score `4`だった。履歴参照は0 / 5だったが、対象外を含む広い検索は3 / 5で、変更前証拠集合の固定は2 / 5でしか成立しなかった。

設計の停止条件に従い、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

Candidate102の直接親はCandidate98である。Candidate99からCandidate101まではprompt lineageへ含めず、誤経路の観測証拠としてだけ参照した。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-prechange-evidence-freeze-r1` |
| bundle SHA-256 | `bea40b133f2a97a1f0972aa30d858edadb8c5338be050dbb4e85771ec497634f` |
| direct parent | Candidate98 |
| case | `TC-F07-CANONICAL-V4-RUNNER/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| registered coverage | F07、iteration 1〜5 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行5件、`N=5` |
| result ID | `b9f57a98c55548c6b8efff351f89c099` |
| compatibility key | `06b6c76f2ed5a00bea385adcd7c7f3f7d5619da55d2847e22c17501e0fb8d72f` |

TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterはCandidate101から変更していない。model slot発行前にF07 iteration 1〜5をcoverageへbindし、Layer 4 resultを登録した。

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| required command evidence | 5 / 5 |
| command protocol violation | 0 / 5 |
| excluded attempt | 0 |
| root-only | 5 / 5 |

## 変更前証拠集合

| iteration | command数 | 履歴参照 | 対象外を含む広い検索 | 判定 |
| ---: | ---: | --- | --- | --- |
| 1 | 11 | なし | なし | mechanism成立 |
| 2 | 11 | なし | repository全体、`AGENTS.md`、正規moduleを検索 | mechanism不成立 |
| 3 | 10 | なし | `scripts / tests / fixture / seed`を検索 | mechanism不成立 |
| 4 | 13 | なし | `AGENTS.md`、start identity、`.agents / .codex`を検索 | mechanism不成立 |
| 5 | 11 | なし | なし | mechanism成立 |

成功したiteration 1と5は、開始identity、clean status、`run.sh`だけで変更へ進んだ。失敗した3件は「TaskSpecを固定した」と宣言した後に、正規entrypoint、repository authority、fixture、start identityの追加根拠を検索した。

したがって、`spec_ready=true`時の内部的なevidence固定だけでは、固定内容をcommand発行前に検証できない。executorは検索後に、その入力をrequired authorityまたは未解決predicateだったと説明できる。次の設計候補は、最初のcommand前にpre-change invocationとconsumer predicateをmodel-visibleな受領票として生成し、後続resultによる失効なしには追加できない形に限定する。

## token・elapsed診断

| iteration | all-agent token | elapsed |
| ---: | ---: | ---: |
| 1 | 159,340 | 85.546秒 |
| 2 | 183,832 | 91.283秒 |
| 3 | 154,014 | 70.645秒 |
| 4 | 139,220 | 93.398秒 |
| 5 | 97,465 | 70.063秒 |
| 中央値 | 154,014 | 85.546秒 |
| 最小〜最大 | 97,465〜183,832 | 70.063〜93.398秒 |

最大 / 最小比はtoken `+88.61%`、elapsed `+33.31%`である。互換なCandidate101比でtoken中央値は`+12.62%`、elapsed中央値は`+17.41%`だった。品質は維持したがmechanism gateが2 / 5なので、この差を証拠固定の効果へ帰属しない。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate102-prechange-evidence-freeze-v14-medium-f07-canonical-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/b9f57a98c55548c6b8efff351f89c099.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`

execution archiveはSHA-256 `f799fbcf07b8bdf8968898c9955fc8cb70f7d9be8fb24eb8d9b225cbc403552f`でseal済みである。非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
