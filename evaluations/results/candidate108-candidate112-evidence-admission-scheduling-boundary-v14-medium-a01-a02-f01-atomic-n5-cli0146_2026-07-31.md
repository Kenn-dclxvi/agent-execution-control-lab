# Candidate112 evidence admission / scheduling boundary targeted結果

## 結論

Candidate112のA01 r2 / A02 r2 / F01 r3各N=5は、15 / 15件がvalid・rateable・score `4`だった。保存済みCandidate108の同じ15 atomic runとの互換比較では、3 caseを合算したtoken中央値が`+14,869`（`+3.53%`）、elapsed中央値が`-6.768`秒（`-3.10%`）だった。

一方、狙ったevidence scheduling制御は成立しなかった。tool callはCandidate108の`122`回から`138`回へ`+16`回、model stepは`137`回から`153`回へ`+16`回となった。3 caseすべてでtool callとmodel stepが増えている。qualityは維持し、case別token中央値は全caseで低下したが、逐次model returnを減らした結果とはbindできない。事前停止条件に従い、Standard14へ進めず停止する。

## 固定条件

- candidate: `the-caption-3ce91a4-evidence-admission-scheduling-boundary-r1`
- bundle SHA-256: `0a543a6439d73bfe76ad47daf28507b4b5d731bf9b22d4749edf12f2586ae56e`
- direct parent / reference: Candidate108
- cases: `TC-A01-LATENT-MODE-POLICY` r2 / `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2 / `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: case別に5
- profile上のM: 24
- candidate pool key: `eb8b13a3f016e9f5c905cfd5b7adc8c21b792bfcd88acdfa065695569605d951`
- comparison key: `4e4bb890ed87c028e2cfaec57bbd4813bcd970c7298c8f31aa580fcb803e0854`
- reference result ID: `bf0e18fedb054cd2a558fbb3d89ec0b9`
- candidate result ID: `c18e58f383ca4280b1405d0cc5ca51f9`

保存済みCandidate108 Standard14 poolから対象3 caseの15 runだけを選択し、`register-selection-result`で基準resultへ登録した。Candidate108の再実行は0件である。Candidate112の15 slotは一つのglobal queueへ入れ、readyな全slotをM=24の下で並列実行した。15 / 15 valid、attempt 15、excluded 0、実時間は`102.285`秒だった。

## 3 KPI

| 項目 | Candidate108 | Candidate112 | C112 - C108 |
| --- | ---: | ---: | ---: |
| quality中央値 | `100.0` | `100.0` | `0.0` |
| token中央値 | `420,683` | `435,552` | `+14,869`（`+3.53%`） |
| elapsed中央値 | `218.560`秒 | `211.792`秒 | `-6.768`秒（`-3.10%`） |

case別ではtoken中央値が3 caseすべてで低下した。一方、elapsedはA01とF01で悪化した。

| case | token中央値 C108 | token中央値 C112 | 差 | elapsed中央値 C108 | elapsed中央値 C112 | 差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `78,687` | `69,408` | `-9,279`（`-11.79%`） | `40.516`秒 | `45.028`秒 | `+4.512`秒（`+11.14%`） |
| A02 | `200,556` | `190,033` | `-10,523`（`-5.25%`） | `99.226`秒 | `87.760`秒 | `-11.466`秒（`-11.56%`） |
| F01 | `152,145` | `137,030` | `-15,115`（`-9.93%`） | `77.992`秒 | `78.970`秒 | `+0.978`秒（`+1.25%`） |

15 runのtoken合計は`2,185,593 -> 2,092,729`で`-92,864`（`-4.25%`）だった。これはcase別中央値と同方向だが、selection iterationは実行時の共通sampleではない。一次KPIは固定result schemaのiteration合算中央値を使い、合計値だけでgateを通さない。

## evidence scheduling挙動

| case | tool call C108 | tool call C112 | model step C108 | model step C112 | agent message C108 | agent message C112 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `20` | `28` | `25` | `33` | `18` | `15` |
| A02 | `52` | `55` | `57` | `60` | `26` | `28` |
| F01 | `50` | `55` | `55` | `60` | `25` | `24` |
| 合計 | `122` | `138` | `137` | `153` | `69` | `67` |

agent messageは`-2`件だったが、tool callとmodel stepはともに`+16`件だった。A01は変更へ進まない確認停止caseであるにもかかわらず、tool callとmodel stepが各`+8`件となった。複数の開始状態確認を一つのshell invocationへまとめたrunもあったが、15件全体として独立evidenceの逐次model returnは減っていない。

観測したreadはTaskSpec、開始状態、target artifact、適用instruction、repository内authority探索の範囲だった。許可外変更、command protocol違反、成果不成立は0件である。ただし、admissionを維持したこととschedulingを改善したことは別であり、後者は不成立である。

## 判断

Candidate112の変更軸は詰めない。理由は、prompt上でadmissionとschedulingを分離しても、rootが単一operationを担当する実行面では各tool resultごとのmodel returnが残り、狙ったstep削減へ結び付かなかったためである。具体的なtool、shell grouping、executor動作をpromptへ追加指定する方向にも進まない。

次に再開するなら、Candidate108を基準に別のprompt predicateを作る前に、A01 / A02 / F01で増えた個別tool callの必要性をtrace単位で分類する。とくにA01のauthority探索と開始状態確認が、terminal dispositionを変えないのに追加されたかを先に見る。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate112-evidence-admission-scheduling-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- comparison preflight SHA-256: `928d60973a2535321a90575443c082fbb6c8aae3450204e2f40650e30cb5d85f`
- execution archive SHA-256: `d71e56a5f68cc202cc2a500ca153972658b3bcbee5c849c73fc5326b8174a2fe`
- final compact archive SHA-256: `fbed59608565aa6125b134be639a2fb4820b65a13661c797c91f2de5d7970b9f`
- quality audit SHA-256: `b8cbc29543daeed88cf0e183b26c3affd4c14e78b1183bb7e5af0d5015783fc8`
- behavior audit SHA-256: `882c50b10d449c3fb8a11abcf7bf96ea7d309b30d62e3e6207c6eb4f9ee54fb2`
- result comparison SHA-256: `1072f4eee447ec63b6a1a9a0305a614f51b05acc35add6d5ed19a65d12a3feb3`

## 状態

`targeted_a01_a02_f01_evaluated / quality_gate_passed / case_token_medians_lower / aggregate_cost_tradeoff / evidence_scheduling_not_demonstrated / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。
