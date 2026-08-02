# Candidate146 Rating v14 Medium F01 / F02 / F03 atomic N=5

## 結論

Candidate146はF01 / F02 / F03各N=5の15 / 15件でscore `4`を維持した。3 case集約の中央値はCandidate145比でtoken `-23,453`（`-4.50%`）、elapsed `-17.260秒`（`-5.61%`）だった。

ただし、Candidate146が狙ったsource / testの共同発行はCandidate145でも15 / 15件ですでに成立していた。Candidate146も15 / 15件で成立しており、増分mechanismは観測されていない。

Candidate146は変更前model stepをC145より減らさなかった。中央値はF01 `2 → 3`、F02 `2 → 3`、F03 `2 → 2`だった。したがってKPI低下をconsumer closureへ帰属できない。

さらにF01の1件は、Candidate146自身が分離すると定義した開始identityとcontentを同じmodel stepから発行した。評価TaskSpecには反しないためscore `4`は正しいが、Candidate146の設計gateには反する。停止条件に従いCandidate146は停止し、F04 / F07、Standard14、N>5へ進めない。

## Identityと実行

- candidate: `the-caption-3ce91a4-consumer-closure-evidence-operation-r1`
- direct parent: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`（Candidate145）
- bundle SHA-256: `c52dfaf8297281dcb25c618be5f60b62d00e85e031c1a42b035bed5b12ff5d5b`
- evaluation set / cases: `the-caption-standard14-r1 / F01, F02, F03`
- N / configured M: `5 / 24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- formal reference: Candidate145 F01 / F02 / F03 N=5 result `03a862cf469a4b0fbaf0cd1bc1386563`
- Candidate146 pool: `e033ef6a8840a408e91214cb820c8abaa1c767b1e45110d979b540a0aef198e2`
- issued / valid / excluded: `15 / 15 / 0`
- selection / analysis: `184b99c7c9cc47b99043f6fb6b127f85 / 2c558de25c9f400c95b053024d97d616`
- registered result: `81aaff97f669450a84911f9771de5b06`
- compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- comparison key: `eff03fb5215d7742c58d2550c3c3125005b68fddf9e3703f0f5fc9115aa54d85`

最初のcycleはCandidate145の14 case resultへ3 case profileを照合したため、coverage不一致でpreflight停止した。評価slotは0件だった。その後、保存済みCandidate145 runからF01 / F02 / F03各5件の正式subset resultを登録し、新しいwrite-once cycleで全互換条件を機械照合して15 slotを発行した。

## 品質

15件はすべてscore `4`だった。required outcome、focused validation、full validation、許可変更path、終了条件を満たした。score `3`以下、controller error、excluded attempt、command protocol violationはいずれも0件だった。

これは成果品質の初段合格を示す。低頻度の品質退行を否定するstability証拠ではない。

## model step境界の再監査

当初は`command_execution`件数をmodel往復数として扱い、一つのshell commandへ結合したrunだけをclosure成立と判定した。この判定は誤りである。

複数command間に`agent_message`がなければ、それらは同じmodel stepから発行されたtool call群である。この単位で再集計した結果は次のとおりである。

| case | C145変更前model step中央値 | C146変更前model step中央値 | C145 source / test共同発行 | C146 source / test共同発行 |
| --- | ---: | ---: | ---: | ---: |
| F01 | 2 | 3 | 5 / 5 | 5 / 5 |
| F02 | 2 | 3 | 5 / 5 | 5 / 5 |
| F03 | 2 | 2 | 5 / 5 | 5 / 5 |

C145の4 fileを4 commandへ分けたF02 runも、4 commandは同じmodel stepから発行されていた。C146の共同result記述が新しく閉じた経路ではない。

初回content result後の追加stepは、C145ではF02 2 / 5件だった。C146ではF01 2 / 5件、F02 5 / 5件だった。F01の別1件は適用中instructionを次stepで取得した。C146のmodel step数は減っていない。

## 開始identity境界

| 挙動 | C125 | C145 | C146 |
| --- | ---: | ---: | ---: |
| identityとcontentを同じmodel step | 13 / 15 | 0 / 15 | 1 / 15 |
| identity result後にcontentを別step | 2 / 15 | 15 / 15 | 14 / 15 |

Candidate146設計は、identity resultがdrift停止を変え得るためidentityとcontentを別operationにすると定義した。F01 iteration 1はこれに反し、source、status、test、pwd / branch / HEADを同じmodel stepから発行した。

一方、評価TaskSpecが要求するのは最初のeditまたはrequired command前のidentity確認である。read前の確認ではない。そのrunは共同result受領後に初めてartifact変更へ進んだため、quality上の違反ではない。

この差は、Candidate146がTaskSpecより強いread停止境界を独自に追加したことを示す。

## KPI比較

| case | candidate | token中央値 | elapsed中央値 | cached input中央値 |
| --- | --- | ---: | ---: | ---: |
| F01 | C125 | 104,663 | 63.337秒 | 62,464 |
| F01 | C145 | 154,553 | 88.154秒 | 119,296 |
| F01 | C146 | 163,027 | 78.913秒 | 127,488 |
| F02 | C125 | 124,094 | 78.648秒 | 83,968 |
| F02 | C145 | 196,118 | 114.228秒 | 166,144 |
| F02 | C146 | 187,207 | 100.687秒 | 141,824 |
| F03 | C125 | 99,202 | 68.374秒 | 70,656 |
| F03 | C145 | 166,152 | 93.882秒 | 115,968 |
| F03 | C146 | 119,762 | 86.818秒 | 84,736 |

正式な3 case集約ではCandidate145 `521,159 token / 307.558秒`に対し、Candidate146は`497,706 token / 290.298秒`だった。quality中央値は両方`100.000`である。

しかしF01 / F02のmodel step中央値は増え、F03は不変だった。よって集約KPI低下はCandidate146の追加軸による改善証拠ではない。N=5の記述差としてだけ保持する。

Candidate125との差はF01でtoken`+55.76%`・elapsed`+24.59%`、F02で`+50.86%`・`+28.02%`、F03で`+20.72%`・`+26.97%`残る。

## 解釈

Candidate146の原因仮説は不成立だった。C145のsource / test観測はすでに共同発行されており、個別command resultごとにmodelへ戻っていなかった。

支持された差は、C125が大半のrunで開始identityとcontentを同じmodel stepへ入れ、C145以降が両者を分離したことである。TaskSpecの停止効果はartifact変更とrequired commandへ及ぶが、許可済みreadには及ばない。

次に検討するなら、consumer closureを強化しない。resultが失効できる後続operation classを限定する`result_effect_scope`を扱う。開始identityと許可済みreadを共同発行し、identity result受領まではartifact変更とrequired commandだけを閉じる設計である。

詳細は[`Candidate146 model step boundary監査`](../../docs/candidate146-model-step-boundary-audit.md)を正本とする。

## 状態

`f01_f02_f03_n5_evaluated / quality_gate_passed / c145_joint_issue_already_15_of_15 / c146_incremental_closure_not_demonstrated / start_identity_design_boundary_14_of_15 / aggregate_kpi_lower_not_attributable / c125_cost_target_failed / result_registered / stopped`

## 結論表

| gate / 比較 | 実測 | 判定 |
| --- | ---: | --- |
| valid / score `4` | 15 / 15 | quality pass |
| score `3`以下 | 0件 | pass |
| C145 source / test共同発行 | 15 / 15 | baselineで成立済み |
| C146 source / test共同発行 | 15 / 15 | 増分なし |
| C146開始identity分離 | 14 / 15 | design gate fail |
| C146 - C145 token中央値 | `-4.50%` | lower / 帰属不能 |
| C146 - C145 elapsed中央値 | `-5.61%` | lower / 帰属不能 |
| C125 case別token / elapsed目標 | 3 / 3 caseで高い | fail |
| F04 / F07 / Standard14 / N>5 | 未発行 | stopped |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |
