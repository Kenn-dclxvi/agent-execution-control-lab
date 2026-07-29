# Candidate81 observation delivery executor A/B Rating v14 Medium F02 N=5

## 結論

sealed observation deliveryは5 / 5 runで直接tool result配送を0件にした。しかしmodel再入はcontrol / treatmentとも中央値`7`回、合計`36`回で変わらなかった。品質は両条件5 / 5件がscore `4`だった。

treatmentのcontrol比は、all-agent token中央値`+5,188`（`+1.92%`）、elapsed中央値`-3.215`秒（`-3.26%`）である。token削減とmodel再入削減を再現していないため、elapsedだけの差を改善と扱わない。状態を`executor_f02_evaluated / mechanism_enforced / no_reentry_reduction / stopped`とする。

## Identity

- TaskSpec / set: `the-caption-planning-first-f02-r1` / `r1`
- prompt: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model / reasoning / N / M: `gpt-5.6-sol` / `medium` / `5` / `5`
- runtime: Codex CLI `0.146.0` / Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- control result: `f17659cfc8c64e24b4e40acc82778948`
- control compatibility key: `8407a8a083007429473ed339f773f39e8b0a638abd332a9dff5dc15394e3e17a`
- treatment result: `060d1bc7c3954e96bcb14b0fe124823e`
- treatment compatibility key: `05a1259cca8efb8aa46cdc13dffba1d101a054ad2a04bac7135dd6de11ac85b0`

TaskSpec、case revision、fixture、prompt、rating、model、reasoning、permission、反復条件は変更していない。差はtreatmentの`comparison_conditions.executor_parameters.observation_delivery`だけである。この差はcompatibility keyへ含まれるため、通常のprompt比較viewへ混ぜずexecutor A/Bとして診断した。

## 3 KPI

| condition | score 4 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| control | 5 / 5 | `270,361` | `1,369,086` | `98.613`秒 | `497.624`秒 |
| treatment | 5 / 5 | `275,549` | `1,417,138` | `95.398`秒 | `480.561`秒 |
| treatment - control | `0` | `+5,188`（`+1.92%`） | `+48,052`（`+3.51%`） | `-3.215`秒（`-3.26%`） | `-17.063`秒（`-3.43%`） |

| iteration | control token | treatment token | control elapsed | treatment elapsed |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `296,850` | `275,549` | `109.073`秒 | `95.398`秒 |
| 2 | `276,514` | `285,289` | `109.620`秒 | `98.221`秒 |
| 3 | `270,361` | `265,489` | `82.328`秒 | `88.935`秒 |
| 4 | `262,146` | `239,436` | `97.989`秒 | `86.462`秒 |
| 5 | `263,215` | `351,375` | `98.613`秒 | `111.546`秒 |

## Mechanism診断

`observation-delivery-audit/v1`は、root rolloutでmodelへ返った外側code resultと直接function resultを数えた。nested tool resultそのものはmodel-visible resultへ数えない。

| 診断 | control | treatment | 差 |
| --- | ---: | ---: | ---: |
| mechanism passed | `4 / 5` | `5 / 5` | `+1` |
| 直接tool result | `1` | `0` | `-1` |
| model再入中央値 | `7` | `7` | `0` |
| model再入合計 | `36` | `36` | `0` |
| model-visible result bytes中央値 | `102,970` | `115,912` | `+12,942`（`+12.57%`） |
| model-visible result bytes合計 | `524,543` | `566,858` | `+42,315`（`+8.07%`） |

controlの直接result 1件はiteration 1の`wait`である。残るcontrol 4件も外側code callだけを使い、各run 7回modelへ戻った。treatmentは直接経路を閉じたが、外側code call自体をまとめず、iteration順に`7 / 7 / 7 / 7 / 8`回modelへ戻った。このため直接tool禁止は経路種別を固定しただけで、operation wave数を減らしていない。

## 判定

- quality gate: `passed`（両条件5 / 5 score `4`）
- delivery mechanism gate: `passed`（treatment 5 / 5、直接result 0）
- model reentry reduction gate: `failed`（中央値差0、合計差0）
- token gate: `failed`（中央値`+1.92%`、合計`+3.51%`）
- elapsed: `improved_only`（中央値`-3.26%`、tokenと再入は改善せず）
- prompt Candidate、標準14、採用、release、本体反映: 未作成・未実施・未判断

次の境界はtool種別の禁止ではなく、複数の外側code callを一つのterminal waveへbindする必要がある。正常な中間code returnを禁止し、失敗、unknown、permission要求、または全operation終端だけをreturn可能にするexecutor contractが必要である。

## 保存証跡

- control result content SHA-256: `d8a7e6779e2ff00a29aa1e7fe0f5ce1fdb144adddc7897bd2ae8653d02677aa2`
- treatment result content SHA-256: `ff37cb48093f6c9fca8e2d3cc490507bcabff0407ca5100f181374e76e2737a0`
- control execution archive SHA-256: `0be850614284c3fb9d8c05d67a3c16421958ab3e714b006147599a2b04cbabf5`
- treatment execution archive SHA-256: `566fbc6685e01fdff88dc69a5374197c6cbec80931a23cf1923b82b8ce832b86`
- control final archive SHA-256: `4c62156abadc976456dd948a7aedf1ecd840daf2cc342fedf9c5a9fde133b30d`
- treatment final archive SHA-256: `607c04577677789b140df8bf4426bc467ff46cbf819e6bcc859e55dc99e0af2d`

model起動前のadapter配線不具合で停止したtreatment `batch-001`は診断履歴として分離した。5 attemptすべてが同じ`NameError`で終了し、valid slotとmodel tokenは0件である。修正後の`batch-002`だけを上記N=5へ使用した。
