# Candidate100 Rating v14 Medium F07 canonical N=5

## 結論

Candidate100はF07 canonical r2の5 / 5でvalid・rateable・score `4`だった。一方、対象外を含む広い検索を4 / 5で観測し、狙った変更前調査の終了条件は1 / 5でしか成立しなかった。設計の停止条件に従い、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

Candidate100の直接親はCandidate98である。Candidate99はprompt lineageへ含めず、誤経路を確認した観測証拠としてだけ参照した。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-outcome-source-closure-r1` |
| bundle SHA-256 | `b4c260e5c18c8b5fdc3d005fe931f531c4328a222111f0522d33f0ba71683df3` |
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
| result ID | `45b6974039ee4a10892f63a36c7f94b5` |
| compatibility key | `06b6c76f2ed5a00bea385adcd7c7f3f7d5619da55d2847e22c17501e0fb8d72f` |

Layer 1の固定後、model slot発行前にF07 iteration 1〜5をwrite-once coverageとしてbindした。Layer 2はcoverage外runを拒否し、Layer 4はbind済み5 slotが揃ったことを確認してresultを登録した。TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterは変更していない。

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

## 変更前調査の経路

| iteration | command数 | 履歴参照 | 対象外を含む広い検索 | TaskSpecと対象artifactだけで変更を確定 | 判定 |
| ---: | ---: | --- | --- | --- | --- |
| 1 | 14 | なし | identity、gate、`AGENTS.md`をrepository全体で検索 | いいえ | mechanism不成立 |
| 2 | 8 | なし | `scripts / tests / .agents / .codex`を検索 | いいえ | mechanism不成立 |
| 3 | 11 | なし | repository全体の`AGENTS.md`列挙 | いいえ | mechanism不成立 |
| 4 | 8 | なし | なし | はい | mechanism成立 |
| 5 | 10 | なし | `run.sh / scripts / tests / .agents / .codex`を検索 | いいえ | mechanism不成立 |

履歴参照なしは5 / 5へ改善したが、広い検索なしは1 / 5のままだった。成功したiteration 4だけが、TaskSpecの指定値と`run.sh`の現在状態を読んだ後に修正へ進んだ。他の4件は、runner gate、seed fixture、検証script、局所authorityなどを別の確認対象として追加した。

したがって、`OUTCOME_SOURCE`は「成果値をrepository authorityで再確認しない」という分岐を狭めても、変更前に別のgateや周辺経路を確かめる分岐を閉じていない。残った差は成果値の情報源ではなく、変更開始に十分な現在状態をどこまで確認するかという判断である。

## token・elapsed診断

| iteration | all-agent token | elapsed | command数 |
| ---: | ---: | ---: | ---: |
| 1 | 136,809 | 86.432秒 | 14 |
| 2 | 172,884 | 72.217秒 | 8 |
| 3 | 111,187 | 72.211秒 | 11 |
| 4 | 109,688 | 58.392秒 | 8 |
| 5 | 145,606 | 86.199秒 | 10 |
| 中央値 | 136,809 | 72.217秒 | 10 |
| 最小〜最大 | 109,688〜172,884 | 58.392〜86.432秒 | 8〜14 |

最大 / 最小比はtoken `+57.61%`、elapsed `+48.02%`である。Candidate99 N=5の中央値に対してtokenは`+3.20%`、elapsedは`+10.06%`で、振れ幅もCandidate99のtoken `+23.13%`、elapsed `+19.35%`より大きい。ただしCandidate99 resultはLayer 4未登録で、両者は正式な互換比較resultではない。ここでは同じ固定条件の経路診断としてだけ扱う。

参考として、保存済みC81 Standard14 B20のF07 100件はtoken `103,590〜321,388`、elapsed `57.155〜149.407秒`、中央値は`144,585.5`と`83.286秒`だった。Candidate100 N=5はこの分布内にあるため、5件のKPIだけから新しい安定化効果は認めない。mechanism gateが1 / 5なので、KPI差を`OUTCOME_SOURCE`の効果へ帰属しない。

## 実行・登録上の補足

5件のmodel run完了後、Candidate99から複製したcampaign controllerがStandard14 70 run用auditを参照していたため、採点前確認が件数不一致で停止した。これはprompt品質失敗ではない。F07用auditへ修正し、既存5件だけを採点・登録した。model runの再発行は行っていない。

execution archiveはSHA-256 `d6b26a34861c47eca505bc786b2e3a60982e7edf140e520c91ff1edb4e188b81`でseal済みである。非公開raw traceはverification checkoutに保持し、このrepositoryへcommitしない。

## 保存場所

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate100-outcome-source-closure-v14-medium-f07-canonical-n5-cli0146-20260730-r1`
- registered result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/45b6974039ee4a10892f63a36c7f94b5.json`
- preflight receipt: campaign直下`preflight-receipt.json`
- quality audit: `batch-001/quality-audit.json`
- execution archive: `batch-001/compact/execution-evidence.tar.zst`
