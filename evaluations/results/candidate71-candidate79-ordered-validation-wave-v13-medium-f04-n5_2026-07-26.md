# Candidate71 / Candidate79 ordered validation wave Rating v13 Medium F04 N=5

## 結論

Candidate79の制御は有効ではなかった。F04の成果品質は維持したが、狙ったvalidation closureはCandidate71の3 / 5から0 / 5へ悪化した。all-agent tokenとelapsedも増えたため、Candidate79は`targeted_evaluated / stopped`とする。

この結果はF04 r2、reasoning effort `medium`、各`N=5`の対象試験に限定する。標準14項目、採用、release、runtime projectionへ読み替えない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| evaluation set | `the-caption-ordered-validation-wave-f04-r1` |
| case | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2 |
| model | `gpt-5.6-sol` |
| reasoning effort | `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 各`N=5` |
| effective max workers | `M=5` |
| token accounting | all-agent v1 |

両profileの差は`profile_id`と`prompt_set_identity`だけである。compatibility keyは両resultとも`c4368a396eb7c1b51fd27d385d88fa3a159a6c7b1ec80500b3dfe2b640888a72`で一致した。

## 一次result

| prompt | result ID | content SHA-256 | valid / rateable | score分布 |
| --- | --- | --- | ---: | --- |
| Candidate71 | `bf1eb512fb8f4ca0b02e6730f38404f4` | `0632ca42c6f5a37a39eb5779163290ea24c8351f976c83b3e970c8bd6aa75c37` | 5 / 5 | `4 = 5` |
| Candidate79 | `eabcbd0358f145b69d66a5402cb3ff0a` | `6004aa6f0dd1e5695cf38fb8bd33b2f895415b671d16032a0f9a3d6446592529` | 5 / 5 | `4 = 5` |

両条件ともexcluded attempt、required command欠落、protocol違反、workspace drift、worker起動は0件だった。

## 3 KPI

| KPI | Candidate71 | Candidate79 | C79 - C71 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 225,041 | 263,038 | +37,997 | +16.88% |
| elapsed中央値 | 104.990秒 | 107.598秒 | +2.608秒 | +2.48% |
| all-agent token合計 | 1,103,856 | 1,323,234 | +219,378 | +19.87% |
| elapsed合計 | 506.446秒 | 531.979秒 | +25.533秒 | +5.04% |

公式Layer 4 viewの中央値差はquality `0.000`、token `+37,997`、elapsed `+2.608秒`である。

## 保存traceの行動診断

required commandは`npm ci`、lint、buildの3件である。一つのcustom tool call内で3件を順序付き個別`exec_command`として実行したrunを「1-step closure」と数えた。

| diagnostic | Candidate71 | Candidate79 | C79 - C71 |
| --- | ---: | ---: | ---: |
| 1-step closure run | 3 / 5 | 0 / 5 | -3 |
| validation custom tool call合計 | 9 | 15 | +6 |
| validation間agent commentary | 3 | 5 | +2 |
| 全custom tool call | 38 | 47 | +9 |
| assistant message | 31 | 35 | +4 |
| post-validation custom tool call | 5 | 5 | 0 |
| post-validation source / diff readを行ったrun | 4 / 5 | 5 / 5 | +1 |

Candidate71はiteration 1、2、5で3 commandを一つのwrapperへ閉じた。Candidate79は5 runすべてで3 commandを3回のcustom tool callへ分けた。したがって、増加の中心はterminal後の探索ではなく、狙っていたvalidation中間のmodel再入と、その前後の実行step増加である。

## 考察

事実として、`dependency order`と「先行success時だけ後続を発行する」を追加したCandidate79は、同一model stepへの収束を増やさなかった。逆に逐次tool callを5 / 5へ固定した。

推測として、Mediumは「先行successを確認してから後続を発行する」を、wrapper内部のfail-stopではなく、各tool resultをmodelへ返して判断する指示として解釈した可能性が高い。内部推論自体は保存traceから確定できないが、3回のcustom tool callへ分割した外形は全runで確認できる。

また、今回のCandidate71は1-step closureが3 / 5だった。先行の標準14項目Medium result内のF04では0 / 5だったため、この挙動には反復またはcampaign文脈によるばらつきがある。両campaignはevaluation setと実効worker条件が異なるのでKPI互換比較には使わない。今回のCandidate79判定には、同じtargeted compatibility keyで新規実行したCandidate71だけを基準にした。

## 判定

Candidate79は作成前gate 9の「中間再入が減らない」「token / elapsedが期待と逆方向」に該当する。

- Candidate79へ補助predicateを追加しない。
- 標準14項目へ進めない。
- Candidate71へ還元しない。
- 採用、release、runtime projectionを行わない。

今回の反証から還元できる設計上の知見は、「先行success」をroot promptへ追加するだけではwrapper内部fail-stopを指定できず、逐次model判断を強め得るという点である。再検討する場合はprompt語句の追加ではなく、command evidence protocolまたはexecutor capabilityとして一つのmodel step内の順序付き個別invocationを明示的に表現できるかを、prompt変更とは別の試験軸で扱う。
