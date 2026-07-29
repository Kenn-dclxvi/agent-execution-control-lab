# 実行制御としてのprompt設計 第2版

## BaselineからCandidate81までを、Rating v13・Medium・標準14項目の最新互換resultで比較する

> [!IMPORTANT]
> **位置付け**: この文書は、本リポジトリの研究成果を最新の互換比較に絞って整理した第2版の総説である。契約・評価状態・採用・release・本体反映の正本ではない。数値とidentityはリンク先の一次artifactを正本とする。研究状態は2026-07-29時点である。

---

## 要旨

本研究は、AIエージェントへ与えるpromptを文章ではなく**実行制御**として扱う。実行制御とは、仕様確定、producer選択、委譲、検証、停止をどの条件で進めるかを定める境界である。

第2版では、過去Candidateの個別resultを時系列に並べない。BaselineからCandidate81までのうち、同じ評価集合、rating contract、model、reasoning、runtime、TaskSpec、反復条件に揃う7条件だけを主比較とする。

- Baseline
- ControlFreeRepository
- Candidate5
- Candidate35
- Candidate43
- Candidate71
- Candidate81

固定条件はRating v13、reasoning `medium`、標準14項目、各`N=5`、global queue `M=24`である。各条件70 run、合計490 runを比較する。7条件は同じcompatibility keyを持つ。

主要結果は次の4点である。

1. **Baselineは7条件中でtokenとelapsedが最大だった。** all-agent token中央値は`11,977,774`、elapsed中央値は`3,568.742`秒、quality中央値は`92.857`だった。
2. **root promptを0 byteにしただけでcostは大きく下がったが、品質欠陥は残った。** ControlFreeRepositoryはBaseline比でtoken中央値`-70.80%`、elapsed中央値`-64.97%`だった。一方、A01の5 / 5件がscore `0`で、quality中央値は`92.857`だった。
3. **Candidate43で品質分布が閉じ、Candidate71でcostがさらに下がった。** C43とC71はともに70 / 70件がscore `4`だった。C71はC43比でtoken中央値`-29.19%`、elapsed中央値`-10.59%`だった。
4. **Candidate81は効率改善ではなく検証経路の安定化である。** C81は70 / 70件がscore `4`で、複数required command caseの1-step closureをC71の`30 / 35`から`35 / 35`へ改善した。C71比ではtoken中央値`-0.30%`だが、elapsed中央値は`+5.78%`、token合計は`+0.28%`だった。

したがって、C81までの到達点は「promptを短くしてcostを下げた」ではない。**Baselineが誘発していた不要経路を除き、仕様未確定時の誤開始をC43で閉じ、既知の検証集合に対するmodel再入をC71で減らし、required commandの発行方法をC81で安定化した**と整理できる。

---

## 1. 第2版の比較境界

### 1.1 比較する問い

本版が扱う問いは一つである。

> 同じ14課題を同じmodel・runtime・採点条件で実行したとき、BaselineからC81までの代表的なprompt setは、成果品質、all-agent token、elapsedをどう変えたか。

KPIは次の3つに限定する。

| KPI | 意味 |
| --- | --- |
| `quality_score` | model-visibleな成果条件と禁止境界を満たしたか |
| all-agent `total_tokens` | rootと全descendant sessionの最終usage合計 |
| `elapsed_seconds` | campaignの実測所要時間 |

model step、tool call、Worker数、command protocol、1-step closureは原因を説明するdiagnosticであり、KPIへ追加しない。

### 1.2 「BaselineからC81まで」の意味

Candidate番号は単一の直線的な親子関係ではない。途中には診断枝、停止Candidate、異なるratingやreasoningで測ったresultがある。

本版はC1〜C81の全Candidateを同じ表へ並べない。比較条件の一致を優先し、最新のRating v13・Medium・標準14項目resultを持つ7条件を代表点として選ぶ。

7条件の選定には、次の3基準をすべて使った。compatibilityの一致は必要条件だが、それだけで主表へ追加しない。

| 選定基準 | 内容 |
| --- | --- |
| 互換性 | Rating v13、Medium、標準14項目、`N=5`、`M=24`、runtime、TaskSpec、compatibility keyが一致する |
| 比較上の役割 | 事前に固定した6条件比較のanchor、または同じkeyへ接続されたC81 endpointである |
| 解釈上の役割 | Baseline、0 byte対照、初期完了制御、root-only構造、quality境界、cost境界、安定性境界のいずれかを重複なく表す |

| 条件 | この比較で表す制御段階 | root `AGENTS.md` |
| --- | --- | ---: |
| Baseline | 比較起点となる固定済み指示書 | 5,980 bytes |
| ControlFreeRepository | root制御を0 byteにし、path-scoped authorityだけを残す対照 | 0 bytes |
| Candidate5 | Baseline系列へ完了条件まで継続する境界を追加 | 7,725 bytes |
| Candidate35 | root execution controlを残し、legacy role / process surfaceをstub化 | 3,235 bytes |
| Candidate43 | 未固定の成果値を推測せず、authorityで確定できる場合だけ開始 | 3,980 bytes |
| Candidate71 | decision boundaryとrequired-validation closureでmodel再入を抑制 | 4,987 bytes |
| Candidate81 | 「順に」「個別」を一つのroot wrapper内の発行順へ固定 | 5,525 bytes |

C41やC69は重要な中間成果だが、この7条件と同じRating v13・Medium・標準14項目resultを持たないため、互換性基準を満たさない。C78は互換な標準14 resultを持つが、project-index仮説を検証して停止した別枝であり、事前固定した6 anchorまたはC81 endpointではない。したがって主表へ加えない。

この選定はC41、C69、C78の評価価値を否定しない。**第2版の一つの表で何を比較するか**だけを限定する。系譜と各枝の状態は[`candidate-history.md`](candidate-history.md)を正本とする。

### 1.3 比較しないもの

本版は次を行わない。

- rating revisionやreasoning effortが異なる過去resultの連結
- Candidate番号順をそのまま因果系列とする解釈
- 7条件以外のCandidateを未評価または失敗とみなすこと
- KPI差を自動的にwinner、採用、release、本体反映へ変換すること
- C81の標準14 resultから、未測定課題や別modelへ一般化すること

---

## 2. 方法

### 2.1 固定した互換条件

| 条件 | 固定値 |
| --- | --- |
| evaluation set | `the-caption-standard14-r1` revision `r1` |
| set identity SHA-256 | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| target | `THE-CAPTION@3ce91a403f9e0c83f29d56bbe9e7b449b713445d` |
| target tree | `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| Agent | Codex CLI `0.144.0`、memories disabled |
| permission | `workspace-write`、approval `never` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 14 case × `N=5` = 70 run / condition |
| scheduling | global queue、`M=24` |
| token accounting | all-agent / `v1` |
| compatibility key | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` |

7条件の意図した差はprompt set identityである。case、TaskSpec、fixture、oracle、required validation、rating、runtime、M/Nは一致する。

### 2.2 `high`から`medium`への移行

前版が参照した主要な過去比較はreasoning `high`を中心としていた。第2版の7条件比較は、2026-07-26以降の通常Candidate比較で採用した`medium`へ全条件を揃えた**新しい実行result**である。`high` resultのtokenやelapsedを換算して作った表ではない。

C71の6水準追試では、`medium`と`high`はいずれも70 / 70件がscore `4`だった。`medium`は`high`比でtoken中央値`-9.73%`、elapsed中央値`-14.86%`だった。さらにBaseline、ControlFreeRepository、C5、C35、C43、C71の6条件では、High / Mediumのtoken・elapsed順序がどちらも`C71 → C43 → ControlFreeRepository → C35 → C5 → Baseline`だった。この観測を受け、通常比較を`medium`へ移した。

ただしreasoning effortはcompatibility conditionである。HighとMediumは別compatibility keyであり、水準間の差は記述的な診断にとどまる。C81の同一条件resultはMediumであり、**第2版の7条件表はHigh上のC81挙動や、HighからMediumへの因果効果を示さない。**

正本は[`C71 reasoning 6水準 result`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)、[`High 6条件 result`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)、[`Medium 6条件 result`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)である。

### 2.3 評価課題

標準14項目は、実装、レビュー、確認停止、repository authorityからの仕様解決を含む。

- F01〜F08: 実装・検証・依存関係・同期境界
- F10: inventoryおよびmonthly review
- A01: repositoryから未固定値を確定できない場合の確認停止
- A02: repository規則から一意に決まる正規経路の解決

各条件を14 case × 5回実行した。valid runはすべて0〜4で採点し、unrateableを許可しない。

### 2.4 7条件resultの接続

BaselineからC71までの6条件は一つの比較resultへ登録されている。C81はC71との別result文書だが、同じcompatibility keyへ登録され、C71の既存resultを固定参照している。

したがって本版は、次の2つの一次resultを7条件の一つの互換集合として接続する。

- [`Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 Medium Rating v13 標準14 N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)
- [`C71 / C81 validation wrapper precedence Rating v13 Medium 標準14 N=5`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)

---

## 3. 最新互換比較の結果

### 3.1 3 KPI

| 条件 | score分布 | quality中央値 | token中央値 | elapsed中央値 | 70件token合計 | 70件elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 1 / 0 = 63 / 2 / 1 / 4` | 92.857 | 11,977,774 | 3,568.742秒 | 64,096,747 | 18,583.648秒 |
| ControlFreeRepository | `4 / 0 = 65 / 5` | 92.857 | 3,496,976 | 1,250.057秒 | 17,173,925 | 6,225.500秒 |
| Candidate5 | `4 / 0 = 65 / 5` | 92.857 | 8,425,533 | 2,368.815秒 | 44,924,675 | 12,277.277秒 |
| Candidate35 | `4 / 0 = 65 / 5` | 92.857 | 4,920,365 | 1,716.646秒 | 23,912,141 | 8,535.144秒 |
| Candidate43 | `4 = 70` | 100.000 | 2,716,869 | 1,061.204秒 | 13,769,064 | 5,309.023秒 |
| Candidate71 | `4 = 70` | 100.000 | 1,923,688 | **948.869秒** | **9,475,504** | **4,754.179秒** |
| Candidate81 | `4 = 70` | 100.000 | **1,917,979** | 1,003.744秒 | 9,502,252 | 4,993.269秒 |

太字は各列の最小値である。quality中央値だけでなくscore分布も併記する。

結果は一つのwinnerへ収束しない。

- token中央値最小: Candidate81
- elapsed中央値、token合計、elapsed合計の最小: Candidate71
- score `4 = 70`: Candidate43、Candidate71、Candidate81
- 検証発行の1-step closure: Candidate81

### 3.2 Baselineとの差

| 条件 | quality中央値差 | token中央値差 | elapsed中央値差 |
| --- | ---: | ---: | ---: |
| ControlFreeRepository | 0.000 | `-8,480,798`（`-70.80%`） | `-2,318.685`秒（`-64.97%`） |
| Candidate5 | 0.000 | `-3,552,241`（`-29.66%`） | `-1,199.927`秒（`-33.62%`） |
| Candidate35 | 0.000 | `-7,057,409`（`-58.92%`） | `-1,852.096`秒（`-51.90%`） |
| Candidate43 | `+7.143` | `-9,260,905`（`-77.32%`） | `-2,507.538`秒（`-70.26%`） |
| Candidate71 | `+7.143` | `-10,054,086`（`-83.94%`） | `-2,619.873`秒（`-73.41%`） |
| Candidate81 | `+7.143` | `-10,059,795`（`-83.99%`） | `-2,564.998`秒（`-71.87%`） |

C81の70件合計はBaseline比でtoken `-54,594,495`（`-85.18%`）、elapsed `-13,590.379`秒（`-73.13%`）だった。

これらは同一条件の記述差である。採用順位や個別predicateの単独因果効果ではない。

### 3.3 品質分布

低得点は次の条件に集中した。

| 条件 | case | 件数 | 主なfailure |
| --- | --- | ---: | --- |
| Baseline | A01 | 4 | 未固定値の確認前に変更・試験へ進行、または値未確定のまま終了 |
| Baseline | A02 | 2 | 既存test成功証拠不足、またはcanonical routeと変更pathが未達 |
| Baseline | F07 dependency | 1 | model-visibleなdependency確認commandを未実行 |
| ControlFreeRepository | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate5 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate35 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate43 | — | 0 | — |
| Candidate71 | — | 0 | — |
| Candidate81 | — | 0 | — |

ControlFreeRepository、C5、C35はcostをBaselineより下げたが、A01を閉じなかった。C43以降だけが70 / 70件のscore `4`を記録した。

したがって、0 byte対照のcostだけを見て最適と判断できない。**必要な制御は、削除後に残る具体的な品質欠陥を閉じる境界である。**

### 3.4 C43からC71

C43とC71はともに70 / 70件がscore `4`だった。C71はC43比で次を記録した。

| KPI | C43 | C71 | C71 - C43 |
| --- | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 |
| token中央値 | 2,716,869 | 1,923,688 | `-793,181`（`-29.19%`） |
| elapsed中央値 | 1,061.204秒 | 948.869秒 | `-112.335`秒（`-10.59%`） |
| token合計 | 13,769,064 | 9,475,504 | `-4,293,560`（`-31.18%`） |
| elapsed合計 | 5,309.023秒 | 4,754.179秒 | `-554.844`秒（`-10.45%`） |

C43は成果値を確定できるauthority境界を閉じた。C71はその品質を維持しながら、既知の非依存invocationとrequired validationをまとめ、result受領後の判断回数を減らした。

この比較が示すのは、C71全体とC43全体の差である。C69由来の`DECISION_BOUNDARY`とC71の`VALIDATION_CLOSURE`を、このresultだけで個別に因果分解しない。

### 3.5 C71からC81

| KPI | C71 | C81 | C81 - C71 |
| --- | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 |
| token中央値 | 1,923,688 | 1,917,979 | `-5,709`（`-0.30%`） |
| elapsed中央値 | 948.869秒 | 1,003.744秒 | `+54.875`秒（`+5.78%`） |
| token合計 | 9,475,504 | 9,502,252 | `+26,748`（`+0.28%`） |
| elapsed合計 | 4,754.179秒 | 4,993.269秒 | `+239.090`秒（`+5.03%`） |

この差は、C81の安定化と同時に観測されたcostとして保持する。採用判断では、1-step closure `+5 / 35`に対し、elapsed中央値`+54.875`秒、elapsed合計`+239.090`秒というtrade-offがある。

一方、N=5の一つのcampaignだけから、1-step closureの安定化がelapsed増加を**引き起こした**とは確定できない。独立反復による分布幅の推定や、wrapper precedenceだけのelapsed因果分解は行っていない。したがって本版は「安定化の代償としてelapsedを支払った」と断定せず、**安定化とelapsed増加を同時に観測した**と記述する。

C81の主成果は3 KPIの改善ではない。複数required commandを持つ7 caseで、全commandを一つのcustom wrapperから個別invocationとして発行する1-step closureを安定させたことである。

| 複数required command case | C71 | C81 |
| --- | ---: | ---: |
| F01 | 5 / 5 | 5 / 5 |
| F02 | 5 / 5 | 5 / 5 |
| F03 | 5 / 5 | 5 / 5 |
| F04 | 0 / 5 | 5 / 5 |
| F06 | 5 / 5 | 5 / 5 |
| F07 canonical | 5 / 5 | 5 / 5 |
| F07 dependency | 5 / 5 | 5 / 5 |
| 合計 | `30 / 35` | `35 / 35` |

差はF04の`0 / 5 → 5 / 5`である。C81は「順に」「1 commandずつ個別」という後段の表現を、複数回のmodel再入ではなく、一つのwrapper内の発行順とinvocation単位へ固定した。

したがってC81は、**C71と同等のquality・token水準で、required commandの発行経路を安定化したCandidate**である。速度改善または総cost削減は主張しない。

---

## 4. 何がcostとqualityを分けたか

### 4.1 prompt byte数では説明できない

root promptの静的byte数とruntime tokenは一致しない。

| 条件 | root bytes | token中央値 |
| --- | ---: | ---: |
| ControlFreeRepository | 0 | 3,496,976 |
| Candidate35 | 3,235 | 4,920,365 |
| Candidate43 | 3,980 | 2,716,869 |
| Candidate71 | 4,987 | 1,923,688 |
| Candidate81 | 5,525 | 1,917,979 |
| Baseline | 5,980 | 11,977,774 |
| Candidate5 | 7,725 | 8,425,533 |

C43からC81ではroot promptが`3,980 → 5,525 bytes`へ増えた一方、token中央値は`2,716,869 → 1,917,979`へ減った。BaselineはC81と近い静的byte数だが、token中央値は約6.25倍だった。

削減対象は文字列そのものではなく、文字列が誘発する探索、委譲、model再入、再read、再検証である。

### 4.2 0 byteは下限対照であり完成形ではない

ControlFreeRepositoryは、Baselineのroot promptが大きなruntime costを誘発していたことを示す。一方、A01は5 / 5件がscore `0`だった。

この結果は二つの極端な解釈を否定する。

- 詳細なpromptを書けば品質が上がる、とは限らない。
- promptを削除し切れば最適になる、とは限らない。

必要なのは、0 byte条件に一般的な手順を戻すことではない。残った具体的欠陥へ、最小のauthority・decision・terminal境界を追加することである。

### 4.3 C43はqualityの転換点である

C35までの3条件とControlFreeRepositoryは、いずれもA01の5件を閉じなかった。C43は、変更後の値を直接要求するrepository authorityがある場合だけ実行を開始し、それ以外は編集・試験前に確認する境界を固定した。

最新互換比較では、C43、C71、C81だけが70 / 70件でscore `4`である。したがって本版ではC43をquality分布の転換点として扱う。

ただし、N=5で欠陥が0件だったことを将来の完全保証へ一般化しない。

### 4.4 C71はcostの転換点、C81は安定性とelapsed trade-offを残した終点である

C71はC43と同じscore分布を維持し、token中央値を`-29.19%`、elapsed中央値を`-10.59%`下げた。最新互換比較では、qualityを維持した明確なcost差はここにある。

C81はC71比のtoken中央値が`-0.30%`だが、token合計`+0.28%`、elapsed中央値`+5.78%`、elapsed合計`+5.03%`だった。したがってC81を追加の効率改善として扱わない。

C81の採用判断では、F04を含む発行経路の`35 / 35`安定化と、このelapsed増加を別の判断軸として同時に扱う必要がある。両者の同時観測はtrade-offだが、因果関係は未分離である。quality、cost、prompt stabilityを一つのwinner判定へ畳み込まない。

---

## 5. 評価、採用、release、本体反映

この比較resultは数値と診断を保存する。winnerや採用可否は出力しない。

C81には次の状態が別々に存在する。

| 状態 | 結果 |
| --- | --- |
| evaluation | `standard14_evaluated / quality_gate_passed / prompt_stability_gate_passed` |
| release approval | `approved` |
| runtime projection | `projected` |
| THE-CAPTION反映 | PR [#343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)、統合commit `592e73aae4f5cf71964efea0d49836e8c894cbbc` |

評価resultだけで後三者を推論しない。C81のrelease、approval、projectionは、評価後の明示判断として別artifactに記録されている（正本: [`Candidate81 release README`](../prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md)）。

---

## 6. 限界

1. **単一model・単一runtimeである。** `gpt-5.6-sol`とCodex CLI `0.144.0`以外へ一般化しない。
2. **対象はTHE-CAPTIONの14 caseに限る。** 別repository、別言語、未収録課題への再現は未確認である。
3. **反復は各case `N=5`である。** 低頻度の誤経路が存在しないとは主張しない。
4. **7条件は代表点であり、単一直系ではない。** 表中の隣接差を個別predicateの単独因果効果へ変換しない。
5. **Rating v13に固定した比較である。** v14を含む別ratingのresultを再採点または混合していない。
6. **HighからMediumへの連続性は限定的である。** 6条件の順序は両水準で一致したが、reasoningごとにcompatibility keyが異なる。C81のHigh互換resultは本版の7条件表に存在しない。
7. **中央値だけでは分布を表せない。** score分布と70件合計を併記し、C71とC81のような中央値・合計・elapsedの方向差を隠さない。
8. **採点は独立blind raterではなく固定契約によるauditである。** contractとcollectorの欠陥が結論へ影響し得る。
9. **C81の1-step closureはdiagnosticである。** 3 KPIへ追加せず、未測定caseの安定性へ一般化しない。elapsed増加との因果関係も確定していない。

---

## 7. 結論

最新の互換条件でBaselineからC81までの代表7条件を整理すると、結論は次のとおりである。

1. Baselineはquality中央値`92.857`、token中央値`11,977,774`、elapsed中央値`3,568.742`秒で、7条件中最も高costだった。
2. ControlFreeRepositoryはBaseline比でtoken中央値`-70.80%`、elapsed中央値`-64.97%`だったが、A01の5 / 5件がscore `0`だった。
3. Candidate43は未固定値のauthority境界を閉じ、70 / 70件のscore `4`へ到達した。
4. Candidate71は同じscore分布を維持し、C43比でtoken中央値`-29.19%`、elapsed中央値`-10.59%`だった。
5. Candidate81は70 / 70件のscore `4`を維持し、1-step closureを`30 / 35 → 35 / 35`へ改善した。
6. C81はC71比でtoken中央値`-0.30%`だが、elapsed中央値`+5.78%`、elapsed合計`+5.03%`、token合計`+0.28%`である。安定化とcost増加を同時に観測したが、因果関係は未分離であり、追加の効率改善とは判断しない。
7. Baseline比でC81はquality中央値`+7.143`、token中央値`-83.99%`、elapsed中央値`-71.87%`だった。

この結果を一文でまとめる。

> **C81までの改善は、promptの短文化ではなく、不要な実行経路を除去し、仕様確定・model再入・検証発行の境界を順に閉じた結果である。**

---

## 参考

### 一次result

- [`Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 Medium Rating v13 標準14 N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)
- [`C71 / C81 validation wrapper precedence Rating v13 Medium 標準14 N=5`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [`Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 High Rating v13 標準14 N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)
- [`C71 reasoning 6水準 Rating v13 標準14 N=5`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)

### 設計・状態の正本

- 評価のLayerと互換条件: [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)
- 評価実行手順: [`evaluation-loop-manual.md`](evaluation-loop-manual.md)
- prompt制御の設計原則: [`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- Candidate系譜: [`candidate-history.md`](candidate-history.md)
- Candidate81設計: [`candidate81-validation-wrapper-precedence-design.md`](candidate81-validation-wrapper-precedence-design.md)
- Candidate index: [`prompts/candidates/README.md`](../prompts/candidates/README.md)
- release / approval / projection: [`prompts/releases/README.md`](../prompts/releases/README.md)
- Candidate81 release: [`the-caption-3ce91a4-validation-wrapper-precedence-release-r1`](../prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md)
