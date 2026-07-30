# Candidate99 Rating v14 Medium F07 canonical N=5

## 結論

Candidate99をF07 canonical r2で5回実行した。5 / 5がvalid・rateable・score `4`で、required command evidence、root-only、許可pathを維持した。

一方、狙った判断証拠境界は成立しなかった。履歴参照を1 / 5、対象外を含む広い検索を4 / 5で観測した。未取得証拠identityとconsumer predicateを先に固定せず追加入力したrunも4 / 5だった。設計の停止条件に従い、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_not_registered / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-decision-evidence-boundary-r1` |
| bundle SHA-256 | `482bdd3e17523f3640dacb5d1adfc68023a790b3890f47ce1748782b3b156bd1` |
| direct parent | Candidate98 |
| case | `TC-F07-CANONICAL-V4-RUNNER/r2` |
| source Evaluation set | `the-caption-standard14-r1/r1` |
| source set identity | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| F07 fixture identity | `bece63e466ad63f5ad0c40f23d2ac98b6a26f2033c1e6d883838e1ed6ab3ca87` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / runtime | `0.146.0` / Python `3.14.5` |
| execution | global queue、設定上の`M=24`、実同時実行5件、`N=5` |
| token accounting | all-agent v1 |
| comparison conditions SHA-256 | `8d3b7cf0ff1151c29acc5b8540b10d4898c880a112766c3d8d99154411a3a2dc` |

C81 Standard14 B20のLayer 1を`clonefile`で再利用した。comparison conditionsはC81 B20と一致する。Candidate99はF07だけを発行したため、14 case全体のC81 primary resultとは同一compatibility keyの正式比較を行わない。

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| required command evidence | 5 / 5 |
| command protocol violation | 0 / 5 |
| 許可外変更 | 0 / 5 |
| root-only | 5 / 5 |

owner-producer evidenceは5 / 5で`failed`だが、Rating v14ではdiagnostic-onlyである。各runはrootだけで成果と必須検証を完了しており、品質scoreを変更しない。

## 判断証拠境界

| iteration | command数 | 履歴参照 | 対象外を含む広い検索 | 不足証拠と利用先を先に固定 | 判定 |
| ---: | ---: | --- | --- | --- | --- |
| 1 | 16 | `git log`あり | あり | なし | mechanism不成立 |
| 2 | 8 | なし | `scripts / tests / src`検索 | なし | mechanism不成立 |
| 3 | 11 | なし | `run.sh / src / tests / scripts`検索 | なし | mechanism不成立 |
| 4 | 8 | なし | なし | 追加入力なし | mechanism成立 |
| 5 | 10 | なし | `run.sh / main_verify / tests`検索 | なし | mechanism不成立 |

集計すると、履歴入力0件は4 / 5、対象外を含む広い検索0件は1 / 5、理由を先にbindしない追加入力0件は1 / 5だった。事前gateはすべて5 / 5を要求するため不通過である。

## token・elapsed診断

| iteration | all-agent token | elapsed | command数 |
| ---: | ---: | ---: | ---: |
| 1 | 132,561 | 64.809秒 | 16 |
| 2 | 135,549 | 64.806秒 | 8 |
| 3 | 134,327 | 77.347秒 | 11 |
| 4 | 110,083 | 65.821秒 | 8 |
| 5 | 129,899 | 65.617秒 | 10 |
| 中央値 | 132,561 | 65.617秒 | 10 |
| 最小〜最大 | 110,083〜135,549 | 64.806〜77.347秒 | 8〜16 |

Candidate99の最大 / 最小比はtoken `+23.13%`、elapsed `+19.35%`だった。参考として、同じfixtureを使ったC81 B20のF07 100件はtoken `103,590〜321,388`、elapsed `57.155〜149.407秒`、中央値はそれぞれ`144,585.5`と`83.286秒`だった。Candidate98の別fixture N=5はtoken `135,619〜250,722`、elapsed `75.625〜132.423秒`だった。

Candidate99の振れ幅は小さいが、N=5とN=100の差があり、正式比較resultでもないため、安定化を確定しない。また、狙った境界が4 / 5で破られているため、KPI差を`EVIDENCE_SCOPE`の成立効果とは判断しない。

## result登録境界

executionとRating v14採点は完了したが、Layer 4 resultは登録していない。固定したLayer 1はStandard14全14 caseを含む一方、Candidate99が発行したのはF07の5 slotだけだった。`record-result`は「固定setの全caseと全iterationを含むこと」を要求し、`prompt set must cover every frozen case and iteration`で停止した。

実行済み5件を後から別setへbindせず、登録のための再実行も行わない。raw executionはSHA-256 `801ad1c203bf39bb796d4942fb6c5c39eabb2980e638593d2f86d45eeaf93b77`のarchiveへseal済みである。この不足を受け、Layer 1 coverageとLayer 4登録条件の機械照合をroot `AGENTS.md`の実行前gateへ追加した。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate99-decision-evidence-boundary-v14-medium-f07-canonical-n5-cli0146-20260730-r1`
- preflight receipt: campaign直下`preflight-receipt.json`
- quality audit: `batch-001/quality-audit.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`

非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。
