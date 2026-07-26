# Candidate71 / Candidate80 root validation wrapper Rating v13 Medium F04 N=10

## 結論

Candidate80は同一課題の1-step validation closureをCandidate71の5 / 10から9 / 10へ改善した。ただし、作成前gateで固定した10 / 10には届かなかったため、`targeted_evaluated / stopped`とする。

成果品質は両条件とも10 / 10でscore `4`だった。tokenとelapsedは診断値であり、prompt安定性の合否条件には使わない。

この結果はF04 r2、reasoning effort `medium`、command evidence protocol v1、各`N=10`の対象試験に限定する。標準14項目、採用、release、runtime projectionへ読み替えない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| evaluation set | `the-caption-prompt-stability-f04-r1` |
| case | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2 |
| model | `gpt-5.6-sol` |
| reasoning effort | `medium` |
| command evidence protocol | v1 |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 各`N=10` |
| effective max workers | `M=10` |
| token accounting | all-agent v1 |

両profileの差は`profile_id`と`prompt_set_identity`だけである。compatibility keyは両resultとも`18427cd26b3f7fe2d3ba4c992cee2e1598df9833cc3e7c6fcc12aa1f38a1ea43`で一致した。

## 一次result

| prompt | result ID | content SHA-256 | valid / rateable | score分布 |
| --- | --- | --- | ---: | --- |
| Candidate71 | `98b7c2e95f83445f90acdde9576337c9` | `23399e9a7ee00ee1a172c9ab13d5866545ae2f953485cc850efde716f60e816e` | 10 / 10 | `4 = 10` |
| Candidate80 | `a8b1411e91914dd1a5824d614200fba1` | `2fd9e3bba9b9fb25530c3fa02bee180baf306a602ad60268c3d7486d3bb02bfb` | 10 / 10 | `4 = 10` |

両条件ともexcluded attempt、required command欠落、protocol違反、順序違反、workspace drift、worker起動は0件だった。

## 3 KPI

| KPI | Candidate71 | Candidate80 | C80 - C71 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 211,822 | 219,093 | +7,271 | +3.43% |
| elapsed中央値 | 98.305秒 | 104.975秒 | +6.670秒 | +6.78% |
| all-agent token合計 | 2,317,863 | 2,280,210 | -37,653 | -1.62% |
| elapsed合計 | 1,004.083秒 | 1,032.660秒 | +28.577秒 | +2.85% |

## 保存traceの行動診断

一つのcustom tool call内で`npm ci`、lint、buildを列挙順の個別`exec_command`として実行したrunを「1-step closure」と数えた。

| diagnostic | Candidate71 | Candidate80 | C80 - C71 |
| --- | ---: | ---: | ---: |
| 1-step closure run | 5 / 10 | 9 / 10 | +4 |
| validation custom tool call合計 | 20 | 12 | -8 |
| validation間agent commentary | 9 | 2 | -7 |
| 全custom tool call | 82 | 75 | -7 |
| assistant message | 66 | 62 | -4 |
| validation前custom tool call | 51 | 53 | +2 |
| post-validation custom tool call | 11 | 10 | -1 |
| post-validation source / diff readを行ったrun | 9 / 10 | 9 / 10 | 0 |

Candidate80でclosureしなかったのはiteration 5の1件だけだった。このrunはvalidation開始前に「指定順」「まず依存関係」と記述し、`npm ci`のresultをmodelへ返した後、lint、buildを別custom tool callとして実行した。

## 考察

事実として、root wrapper方法を`VALIDATION_CLOSURE`へ直接固定すると、Candidate71より1-step closureの再現率は40 percentage point上がった。一方、1件はwrapperを使わず、3 commandをトップレベルの逐次tool callへ分割した。

推測として、後段のTaskSpecとcommand evidence protocol v1にある「順に」「1 commandずつ個別」という表現を、そのrunが「resultをmodelへ返してから次commandを発行する」と解釈した可能性がある。内部推論は確定できないが、保存traceの逐次commentaryとtool call外形はこの解釈と整合する。

protocol v2では同じroot wrapper方法が後段のmodel-visible TaskSpec側にも明示され、10 / 10だった。したがって、prompt-onlyで次に検証できる一つの判断点は、root prompt側で「順に」「個別」をwrapper内の発行順・invocation単位として定義し、command間でresultをmodelへ返す意味ではないと固定することである。

## 判定

- Candidate80は作成前gate 9の「1-step closureが10 / 10未満」に該当する。
- Candidate80へ補助predicateを追加しない。
- Candidate80を標準14項目、採用、release、runtime projectionへ進めない。
- 次候補を作る場合はCandidate71を直接sourceとし、上記の解釈競合だけを一つの置換predicateとして扱う。
