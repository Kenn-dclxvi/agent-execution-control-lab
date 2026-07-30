# Candidate105 Rating v14 Medium F03 N=5

## 結論

Candidate105はF03 r2の5 / 5でvalid・rateable・score `4`だった。意図的なnonterminal yieldとvalidation中の進捗messageは0 / 5になった。一方、1件が実行票内の許可path判定を誤ってterminal failureを返し、第2wrapperでrequired validationを完了した。検証実行票一回と実行票後toolなしは4 / 5である。

設計時の停止条件に従った時点の状態は`targeted_f03_evaluated / quality_gate_passed / terminal_return_gate_passed / single_wrapper_gate_failed / result_registered / stopped`だった。その後、ユーザーがStandard14評価だけを明示的に再開した。後続結果は[`Candidate104 / Candidate105 Standard14 N=5`](candidate104-candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146_2026-07-30.md)へ分離し、このtargeted停止履歴は上書きしない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-validation-terminal-return-r1` |
| bundle SHA-256 | `6eaf12cd58e26244d514a34f4a9238d217058a3b178f138ea3551e930a496aa5` |
| direct parent | Candidate104 |
| case | `TC-F03-ATOMIC-CONTEXT-CLEANUP/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| source set identity | `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33` |
| registered coverage | F03、iteration 1〜5 |
| F03 fixture identity | `5fbbf3e5de7bdb51b8d9586707a63ce6e88b3fad3286f5b00fa984cf080aa52e` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行5件、`N=5` |
| token accounting | all-agent v1 |
| result ID | `f3dd3291c918481299ea6966505b9285` |
| compatibility key | `1c49658de3696219b6bfefb620df32976cc9fde6a1f4460cabea327b1ad33477` |

Candidate104の保存済みLayer 1をclonefileでmaterializeした。複製先に含まれた全70件用`coverage.json`とcomparison receiptは、sourceを変更せず複製先だけから除き、F03 iteration 1〜5をwrite-once coverageへbindした。

最初のpreparation r1は、全70件用coverageを残したままF03 coverageをbindしようとしてslot発行前に停止した。r1は失敗receiptとして保持し、r2で上記境界を明示して準備し直した。model slotの重複発行はない。

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| required command evidence | 5 / 5 |
| command protocol violation | 0 / 5 |
| excluded attempt | 0 |
| root-only | 5 / 5 |

owner-producer evidenceは5 / 5で`failed`だが、Rating v14ではdiagnostic-onlyである。全runはrootだけで成果と必須検証を完了しており、品質scoreを変更しない。

## mechanism gate

| iteration | run ID | validation wrapper | 意図的なnonterminal yield | validation中進捗message | 実行票後tool | 判定 |
| ---: | --- | ---: | --- | --- | --- | --- |
| 1 | `4c30cec3995948fc9638e5829728f310` | 1 | なし | なし | なし | 成立 |
| 2 | `549f486325a446b0aeef08ae1e4c1528` | 1 | なし | なし | なし | 成立 |
| 3 | `3a98e511ea8a4e27b5b52967b46d3fa5` | 2 | なし | なし | あり | 不成立 |
| 4 | `51464c573712444782144c82e5660594` | 1 | なし | なし | なし | 成立 |
| 5 | `22c4d80b2d3d4b0888f6b1746c5642b3` | 1 | なし | なし | なし | 成立 |

全5件は外側custom execのyieldを30秒または120秒へ設定し、1秒の短時間yieldを使用しなかった。validation開始後にfocusedまたはfullの進捗messageを返したrunもない。このため、Candidate105が直接狙ったterminal前のprogress返却は5 / 5で閉じた。

iteration 3では、最初の実行票が`git status --short`の` M src/infra/context_repository.py`を許可path外と誤判定し、required validation発行前に`validation_state=failed`でterminalになった。その後、同じrootがpath判定を修正した第2wrapperを発行し、focused / full validationを成功させた。これはnonterminal progress返却ではないが、検証実行票一回と実行票後toolなしの事前gateを満たさない。

## token・elapsed診断

| iteration | all-agent token | elapsed | model step |
| ---: | ---: | ---: | ---: |
| 1 | 130,193 | 75.545秒 | 5 |
| 2 | 125,317 | 92.407秒 | 5 |
| 3 | 148,020 | 96.748秒 | 6 |
| 4 | 133,239 | 87.920秒 | 5 |
| 5 | 110,983 | 76.689秒 | 4 |
| 中央値 | 130,193 | 87.920秒 | 5 |
| 最小〜最大 | 110,983〜148,020 | 75.545〜96.748秒 | 4〜6 |

参考として、Candidate104 Standard14 N=5のF03 subsetはtoken中央値`149,536`、elapsed中央値`85.649秒`、model step `5〜7`だった。Candidate105との差はtoken`-19,343`（`-12.93%`）、elapsed`+2.272秒`（`+2.65%`）である。ただしCandidate104 resultはStandard14全70件coverage、Candidate105 resultはF03 5件coverageでcompatibility keyが異なるため、この差は正式なLayer 4 KPI比較ではなくroute診断に限定する。

mechanism gateが4 / 5なので、token差をCandidate105の安定した効果として一般化しない。

## 保存場所

- successful campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate105-validation-terminal-return-v14-medium-f03-n5-cli0146-20260730-r2`
- stopped preparation: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate105-validation-terminal-return-v14-medium-f03-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/f3dd3291c918481299ea6966505b9285.json`
- execution archive SHA-256: `cfdec330ec6e06cc445ffd774695920feecb2dc13d209319a05bb6b7376d366e`

非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
