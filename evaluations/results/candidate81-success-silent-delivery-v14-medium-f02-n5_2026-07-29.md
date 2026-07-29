# Candidate81 success-silent delivery Rating v14 Medium F02 N=5

## 結論

結果本文を意味圧縮せず、判断不要な成功resultだけをmodelへ配送しないexecutor protocolは5 / 5 runで成立した。品質は5 / 5件がscore `4`だった。

保存済みsealed observation delivery control比で、all-agent token中央値は`275,549 → 226,326`、`-49,223`（`-17.86%`）、合計は`1,417,138 → 1,111,067`、`-306,071`（`-21.60%`）だった。elapsed中央値は`95.398 → 79.832`秒、`-15.566`秒（`-16.32%`）である。

成功validationのmodel-visible bytesは合計`203,050 → 1,378`、中間messageは`25 → 5`件になった。model-visible result全体も合計`566,858 → 350,459`、`-216,399`（`-38.18%`）だった。状態を`executor_f02_evaluated / quality_passed / mechanism_passed / cost_reduced / f04_not_started`とする。

## Identity

- TaskSpec / set: `the-caption-planning-first-f02-r1` / `r1`
- prompt: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model / reasoning / N / M: `gpt-5.6-sol` / `medium` / `5` / `5`
- runtime: Codex CLI `0.146.0` / Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- control result: `060d1bc7c3954e96bcb14b0fe124823e`
- treatment result: `73314064a8334e56ab656b114ecda2ca`
- treatment compatibility key: `dcabe8819e270d7724a6aaf58958dc022dea82e7e57e98dd35deeb161d0c3f1a`

TaskSpec、case revision、fixture、prompt、rating、model、reasoning、permission、反復条件、sealed observation deliveryは変更していない。差はtreatmentの`comparison_conditions.executor_parameters.success_delivery`だけである。compatibility keyが異なるため、通常のprompt比較viewへ混ぜずexecutor A/Bとして診断した。

## 3 KPI

| condition | score 4 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| sealed control | 5 / 5 | `275,549` | `1,417,138` | `95.398`秒 | `480.561`秒 |
| success-silent | 5 / 5 | `226,326` | `1,111,067` | `79.832`秒 | `427.517`秒 |
| treatment - control | `0` | `-49,223`（`-17.86%`） | `-306,071`（`-21.60%`） | `-15.566`秒（`-16.32%`） | `-53.044`秒（`-11.04%`） |

| iteration | token | elapsed | model再入 | model-visible result bytes |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `231,260` | `79.832`秒 | `7` | `62,687` |
| 2 | `226,326` | `76.494`秒 | `6` | `85,541` |
| 3 | `224,432` | `76.494`秒 | `6` | `86,008` |
| 4 | `229,323` | `86.285`秒 | `7` | `52,019` |
| 5 | `199,726` | `108.411`秒 | `6` | `64,204` |

## Mechanism診断

| 診断 | sealed control | success-silent | 差 |
| --- | ---: | ---: | ---: |
| success delivery mechanism | 未適用 | `5 / 5` | - |
| validation model-visible bytes合計 | `203,050` | `1,378` | `-201,672`（`-99.32%`） |
| 中間message件数 | `25` | `5` | `-20`（`-80.00%`） |
| 中間message bytes合計 | `7,635` | `1,134` | `-6,501`（`-85.15%`） |
| model再入中央値 | `7` | `6` | `-1`（`-14.29%`） |
| model再入合計 | `36` | `32` | `-4`（`-11.11%`） |
| model-visible result bytes中央値 | `115,912` | `64,204` | `-51,708`（`-44.61%`） |
| model-visible result bytes合計 | `566,858` | `350,459` | `-216,399`（`-38.18%`） |

各runはrequired validationを一つのouter code call内から列挙順に個別発行した。全成功時にstdout / stderrを返さず、完全なcommand文字列とexit codeだけを一度返した。required command evidenceは5 / 5件で2 commandともsuccessfulだった。

iteration 4では`wait`の直接resultが1件あったため、旧observation delivery auditは4 / 5である。ただし`wait`はvalidation raw outputを含まず、success delivery auditは5 / 5である。この1件を隠さず診断値として保持する。

## 判定

- quality gate: `passed`（5 / 5 score `4`）
- success delivery mechanism gate: `passed`（5 / 5）
- required command evidence: `passed`（5 / 5）
- token gate: `passed`（中央値`-17.86%`、合計`-21.60%`）
- elapsed gate: `passed`（中央値`-16.32%`、合計`-11.04%`）
- F04、標準14、採用、release、本体反映: 未実施・未判断

この結果が示すのはF02の成功経路だけである。失敗resultのunchanged deliveryは成功runでは発火していないため、別のfailure probeなしに保証済みと扱わない。次は同じexecutor policyをF04の互換control / treatmentで確認する。

## 保存証跡

- treatment result content SHA-256: `3b0c00b95b21f078256d26c77ebe6be6708722b7eeb340986d3a292f1b6173fd`
- treatment execution archive SHA-256: `5281605299ecbc03543ba3e982afc6ec5fc678a9ef3b6d16f24b453553974e33`
- treatment final archive SHA-256: `b4979c5663eee1e04ff2f534ca881e8be7f05a42d3f0c2ff7cb0725df71b3b53`
