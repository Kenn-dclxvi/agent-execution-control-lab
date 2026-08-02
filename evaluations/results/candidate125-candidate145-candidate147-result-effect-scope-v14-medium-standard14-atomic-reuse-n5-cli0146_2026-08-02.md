# Candidate147 Rating v14 Medium Standard14 atomic reuse N=5

## 結論

Candidate147のStandard14 N=5は70 / 70件がscore `4`だった。先行F01 / F02 / F03の15 runを再利用し、不足55 runだけを発行した。新規55件のexcluded attempt、controller error、score `3`以下はすべて0件だった。

Standard14集約中央値はCandidate145比でtoken `-146,118`（`-9.17%`）、elapsed `-256.529秒`（`-23.13%`）だった。Candidate125比はtoken `+46,401`（`+3.31%`）、elapsed `+6.166秒`（`+0.73%`）まで縮まった。

変更前command-bearing model step中央値はCandidate145比で14 case中9 caseが減少し、5 caseは同じで、増加したcaseはなかった。開始identityと許可readを分けない`result_effect_scope`はF01 / F02 / F03以外にも作用した。

ただしF06はCandidate145比でtoken `+28.09%`だった。F06の変更前step中央値は`2 → 2`で減らず、Candidate147の高token 3件は、2件の追加instruction / authority確認と1件の完了確認重複に対応した。これは局所残差であり、N=5から発生確率やCandidate147文言への因果を確定しない。

## Identityと実行

- candidate: `the-caption-3ce91a4-result-effect-scope-r1`
- direct parent: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`（Candidate145）
- bundle SHA-256: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- evaluation set: `the-caption-standard14-r1`
- cases / N / configured M: `14 / 5 / 24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- formal Candidate145 reference result: `071438f43b304001b8b062b238b2af7c`
- formal Candidate125 reference result: `96fb571308de4c08a7aeed0faefb7d72`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- Candidate147 full pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- reused / newly issued / total valid: `15 / 55 / 70`
- excluded: `0`
- selection / analysis: `544f66647d354794958acc2e9397c7be / 16758ebbaef040328797739cd92f02fe`
- registered result: `f7baeadc5bd44399ac13cc0e0a8aff48`
- atomic comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`

Candidate145の固定Layer 1からStandard14全14 caseのfixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingを再生成せず継承した。preflightは55 slotを発行前に機械照合し、Candidate145と同じcompatibility keyを固定した。

Candidate147のF01 / F02 / F03各5件は、先行targeted評価で登録済みだった。同じprompt identityとcase別effective conditionへ一致したためfull poolで再利用し、再実行していない。

## 品質

- score `4`: 70 / 70
- score `3`以下: 0 / 70
- 新規controller error: 0 / 55
- 新規excluded attempt: 0 / 55
- 新規command protocol violation: 0 / 55
- monthly review numeric location exact: 5 / 5

変更taskはrequired outcome、許可変更path、focused / full validation、終了条件を満たした。clarification、out-of-scope停止、inventory review、monthly reviewも各TaskSpecの成果条件を満たした。

これはStandard14 N=5のquality passである。N=5は低頻度の品質退行を否定するstability証拠ではない。

## 全体KPI

| candidate | score中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate125 | 100.000 | 1,401,225 | 6,860,266 | 846.377秒 | 4,253.165秒 |
| Candidate145 | 100.000 | 1,593,744 | 8,017,070 | 1,109.072秒 | 5,311.458秒 |
| Candidate147 | 100.000 | 1,447,626 | 7,217,373 | 852.543秒 | 4,310.065秒 |

Candidate147はCandidate145より両KPIが低い。Candidate125との差はtoken `+3.31%`、elapsed `+0.73%`であり、Candidate145の`+13.74% / +31.04%`から大きく縮まった。

## case別KPI

表の差はCandidate147の各case中央値を基準相手の中央値と比較した値である。

| case | C147 token | C147 elapsed | token vs C145 | elapsed vs C145 | token vs C125 | elapsed vs C125 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 19,195 | 12.148秒 | -50.37% | -46.39% | +9.92% | -32.31% |
| A02 | 129,085 | 73.379秒 | -12.26% | -10.35% | -8.54% | -21.50% |
| F01 | 107,202 | 66.424秒 | -30.64% | -24.65% | +2.43% | +4.87% |
| F02 | 128,236 | 100.607秒 | -34.61% | -11.92% | +3.34% | +27.92% |
| F03 | 104,320 | 70.866秒 | -37.21% | -24.52% | +5.16% | +3.64% |
| F04 | 151,170 | 91.431秒 | -5.81% | -15.98% | -9.07% | -9.79% |
| F05 clarify | 37,242 | 26.725秒 | -0.95% | -0.33% | +2.12% | +26.12% |
| F05 out-of-scope | 37,366 | 25.291秒 | +1.24% | +21.43% | +1.34% | +27.59% |
| F06 | 151,542 | 79.393秒 | +28.09% | -5.27% | +52.77% | +18.13% |
| F07 canonical | 102,504 | 72.547秒 | -12.04% | -15.83% | +7.75% | +31.22% |
| F07 dependency | 87,284 | 54.324秒 | -14.27% | -31.64% | +9.08% | -6.06% |
| F08 | 113,067 | 56.343秒 | -5.09% | -32.77% | -3.67% | -20.30% |
| F10 inventory | 87,934 | 61.546秒 | -15.52% | -36.07% | +1.43% | -8.43% |
| F10 monthly | 93,096 | 51.796秒 | -0.53% | -7.78% | -1.90% | +4.72% |

Candidate145比ではtokenとelapsedがともに12 / 14 caseで低い。F05 out-of-scopeは両方がわずかに高く、F06はtokenだけが大きく高い。

## model stepによる全体影響

model stepは`command_execution`件数ではなく、`item.completed / agent_message`を境界として数えた。変更taskでは最初のfile changeより前にcommandを発行したmodel step数、無変更taskではterminal responseより前のcommand-bearing step数を比較した。

| case | C145中央値 | C147中央値 | 差 |
| --- | ---: | ---: | ---: |
| A01 | 1 | 0 | -1 |
| A02 | 2 | 1 | -1 |
| F01 | 2 | 1 | -1 |
| F02 | 2 | 1 | -1 |
| F03 | 2 | 1 | -1 |
| F04 | 2 | 2 | 0 |
| F05 clarify | 1 | 1 | 0 |
| F05 out-of-scope | 1 | 1 | 0 |
| F06 | 2 | 2 | 0 |
| F07 canonical | 2 | 1 | -1 |
| F07 dependency | 2 | 1 | -1 |
| F08 | 2 | 1 | -1 |
| F10 inventory | 4 | 3 | -1 |
| F10 monthly | 3 | 3 | 0 |

9 caseで一step減り、5 caseは不変だった。増加したcaseはない。F01 / F02 / F03だけに固定したcase ruleではなく、operation class別のresult effect scopeとして複数の変更task、review task、clarification taskへ作用した。

## F06残差

F06のCandidate147 tokenは`103,657〜169,908`で、中央値は`151,542`だった。Candidate145は`98,485〜145,098`、中央値`118,458`だった。

Candidate147の高token側3件は次の挙動に対応した。

1. 2件はtarget testを読む初期段階で、`AGENTS.md`の検索、`.agents`確認、`tests/AGENTS.md`取得を追加した。
2. 1件はrequired validation後の`git diff --check`と`git diff --name-only`を二度発行した。
3. 残る2件には上記追加経路がなく、tokenは`103,657 / 125,382`だった。

Candidate145 F06では5件とも追加instruction / authority探索がなく、完了確認の同一command重複もなかった。Candidate147の新しい`DECISION_BOUNDARY`は`read target / permission`を明示するため、authority確認を目立たせた可能性はある。ただしこれは5件の対応から得た推測であり、因果と発生確率は未確定である。

F06では変更前step中央値が減っていない。したがって、Candidate147の一step削減効果で追加観測costを相殺できず、case別tokenが上昇したと解釈できる。

## 解釈

事実として、Candidate147はStandard14全体の品質を維持しながら、Candidate145で増えたcostの大半を戻した。Candidate125との全体差もtoken `3.31%`、elapsed `0.73%`まで縮まった。

また、変更前step低下はF01 / F02 / F03だけでなく9 / 14 caseに現れた。したがって、狭いcase固有挙動ではなく、先行resultの停止効果を影響されるoperation classへ限定する一般境界としての支持が得られた。

一方、F06の追加authority確認と完了確認重複は残る。これは品質失敗ではなく、全体KPIも悪化させていない。しかしCandidate125相当のcostを安定して達成したと判断する前に、F06の増加がN=5の偶然か、`read target / permission`文言による局所副作用かを保存traceと追加sampleで切り分ける必要がある。

次は新しいCandidateを作らない。Candidate147 F06を小さい追加単位で観測し、score `3`以下なら停止する。authority探索率、完了確認重複率、token分布がCandidate145履歴と同程度かを先に判定する。

## 状態

`standard14_n5_evaluated / quality_gate_passed / result_effect_scope_generalized_9_of_14_cases_lower_step / aggregate_cost_both_lower_than_c145 / c125_aggregate_cost_near_target / f06_local_token_residual / result_registered / adoption_not_decided`

## 結論表

| gate / 比較 | 実測 | 判定 |
| --- | ---: | --- |
| Standard14 valid / score `4` | 70 / 70 | quality pass |
| score `3`以下 | 0件 | pass |
| reused / newly issued | 15 / 55 | atomic reuse pass |
| 変更前step中央値 | 9 case低下 / 5同値 / 0上昇 | generalization supported |
| C147 - C145 token中央値 | `-9.17%` | lower |
| C147 - C145 elapsed中央値 | `-23.13%` | lower |
| C147 - C125 token中央値 | `+3.31%` | near target |
| C147 - C125 elapsed中央値 | `+0.73%` | near target |
| F06 token vs C145 | `+28.09%` | local residual |
| stability / adoption / release | 未判断 | not decided |
