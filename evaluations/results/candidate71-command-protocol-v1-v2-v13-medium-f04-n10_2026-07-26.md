# Candidate71 command protocol v1 / v2 Rating v13 Medium F04 N=10診断

## 結論

command evidence protocol v2は、狙った1-step validation closureを安定化した。v1の5 / 10に対してv2は10 / 10だった。

一方、品質は同じで、all-agent token中央値はほぼ横ばい、elapsed中央値は微増し、token合計とelapsed合計は増えた。したがってv2は`behavior_gate_passed / efficiency_gate_not_passed`とする。現時点では今後の標準profileへ採用しない。

この結果はCandidate71、F04 r2、reasoning effort `medium`、各`N=10`のprotocol診断に限定する。protocol revisionが異なるため、両resultを互換Layer 4 comparisonへ混ぜない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-validation-closure-r1` |
| evaluation set | `the-caption-command-protocol-f04-r1` |
| case | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2 |
| model | `gpt-5.6-sol` |
| reasoning effort | `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 各`N=10` |
| effective max workers | `M=10` |
| token accounting | all-agent v1 |

prompt、case、TaskSpec、target ref、fixture、permission、rating、repetitionは同一である。comparison conditionの`command_evidence_protocol`だけをv1からv2へ変更した。この差によりcompatibility keyは意図どおり分かれた。

## protocol差

- v1: required commandを個別`exec_command`として実行し、structured exitを保存する。
- v2: root producerが1回のcustom exec wrapper内から、列挙順に個別`tools.exec_command`を実行する。nonzeroまたはunavailableで後続を止め、完了済み全resultを一度だけmodelへ返す。shell compound commandは許可しない。

## 一次result

| protocol | result ID | content SHA-256 | compatibility key | valid / rateable | score分布 |
| --- | --- | --- | --- | ---: | --- |
| v1 | `0ba7b7a64a2645dd822d4e0be722f95a` | `606cbd490a8c22cb8a5fb59fc4f4fb0da12c0bfaf2309c4c73f11df9039d8ad9` | `c7850d351d658c9a855d6c296c88dcbd0becf4987b4788dca616e809f371d1bf` | 10 / 10 | `4 = 10` |
| v2 | `f2be181cd3374a53a3db43384120a891` | `08dc9c83b790464341c7f1440f1bb4dc22b3d0ad970a8f034e905f6d072f8c0a` | `c795968bac3f1508d394c11c200779ca9bd93bf6a4efb7ddb84f5f14d22f7ed3` | 10 / 10 | `4 = 10` |

両条件ともexcluded attempt、required command欠落、protocol違反、workspace drift、worker起動は0件だった。

## 3 KPIの記述差

| KPI | v1 | v2 | v2 - v1 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 201,184 | 200,932 | -252 | -0.13% |
| elapsed中央値 | 104.243秒 | 104.592秒 | +0.349秒 | +0.34% |
| all-agent token合計 | 1,950,488 | 2,079,842 | +129,354 | +6.63% |
| elapsed合計 | 1,043.361秒 | 1,071.397秒 | +28.036秒 | +2.69% |

これは異なるcompatibility key間のdiagnosticな記述差であり、公式Layer 4差ではない。

v2のtoken合計増加`129,354`のうちinput token増加は`126,874`、98.08%だった。output token増加は`2,480`だった。

## 保存traceの行動診断

一つのcustom tool call内で`npm ci`、lint、buildを列挙順の個別`tools.exec_command`として実行したrunを1-step closureと数えた。

| diagnostic | v1 | v2 | v2 - v1 |
| --- | ---: | ---: | ---: |
| 1-step closure run | 5 / 10 | 10 / 10 | +5 |
| validation custom tool call合計 | 20 | 10 | -10 |
| validation間agent commentary | 6 | 0 | -6 |
| 全custom tool call | 76 | 73 | -3 |
| assistant message | 67 | 60 | -7 |
| validation前custom tool call | 47 | 52 | +5 |
| post-validation custom tool call | 9 | 11 | +2 |
| post-validation source / diff read | 9 | 11 | +2 |

v2はvalidation中間のmodel再入を全runで消した。一方、validation前後のcustom tool callが増え、全custom tool call差は`-3`にとどまった。token長尾はv2 iteration 8から10に集中し、closureだけではtask全体の探索・確認costを制御できなかった。

## 考察

事実として、root wrapperをmodel-visible protocolへ明示すれば、Mediumでも1-step closureを10 / 10へ固定できた。Candidate79のprompt文言追加が0 / 5だったことと合わせると、順序付き個別invocationの方法はroot promptの抽象predicateより、実行protocolへ直接bindした方が外形挙動へ強く作用する。

ただし効率KPIは改善しなかった。推測として、v2の長いmodel-visible指示によるinput増加と、validation外の探索ばらつきが、削減したvalidation再入costを相殺した可能性がある。内部推論は確定できないが、input token増加が総token増加の98.08%を占めることと、validation前後tool call増加はこの解釈と整合する。

## 判定と次の境界

- v2のbehavior gateは通過した。
- v2のefficiency gateは通過していない。
- Candidate71のpromptは変更しない。
- Candidate79は停止状態を維持する。
- v2を今後の標準profileへ自動採用しない。
- 採用、release、runtime projectionを行わない。

次に検討できるのは、長いmodel-visible説明ではなく、executorが直接受け取る構造化`ordered invocation group` primitiveである。これはprompt変更でもv2採用でもなく、executor capabilityの別revisionとして設計し、個別command evidenceとfail-stopを維持したままmodel-visible input増加を避けられるかを確認する。
