# Baseline / ControlFreeRepository / Candidate147 Rating v14 Medium Standard14 atomic N=5

## 結論

BaselineとControlFreeRepositoryをCandidate147と実効互換な条件で各N=5実行し、各70 / 70件をvalidかつrateableとして登録した。

品質はBaselineがscore `4 / 3 / 0 = 65 / 1 / 4`、ControlFreeRepositoryが`4 / 0 = 65 / 5`だった。Candidate147の保存済み同条件N=5は70 / 70件がscore `4`である。BaselineとControlFreeRepositoryにはscore `3`以下があるため、品質維持を前提にcostだけを評価する比較gateは通過しない。

記述的なStandard14集約中央値は、Baselineがquality `92.857`、token `13,624,982`、elapsed `3,333.567秒`、ControlFreeRepositoryが`92.857 / 3,488,611 / 1,166.296秒`、Candidate147が`100.000 / 1,447,626 / 852.543秒`だった。Candidate147はBaseline比でtoken `-89.38%`、elapsed `-74.43%`、ControlFreeRepository比でtoken `-58.50%`、elapsed `-26.90%`だった。ただし低score分布が異なるため、このcost差だけを効率優位または採用根拠へ読み替えない。

## 試験状態

- Baseline: `standard14_n5_evaluated / low_score_observed / registered`
- ControlFreeRepository: `standard14_n5_evaluated / low_score_observed / registered`
- 比較: `compatibility_matched / descriptive_only`
- Candidate147の採用、release、projection状態: 変更なし

## 実行前gate

BaselineとControlFreeRepositoryにはRating v13・CLI 0.144の保存済み結果があったが、Candidate147とはrating contractとAgent / CLI条件が異なるため再利用しなかった。Candidate147の固定条件を参照し、prompt identityだけを変更した新profileを作成した。

| 条件 | 固定値 | 照合結果 |
| --- | --- | --- |
| Evaluation set | `the-caption-standard14-r1` / `r1` / identity `2096d15e...63c33` | 一致 |
| coverage | 14 case × 各5件 | 一致 |
| fixture / TaskSpec | C147 reference Layer 1の14 case fixtureと固定TaskSpec | 一致 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` / `9d01b7ee...011b1` | 一致 |
| model / reasoning | `gpt-5.6-sol` / `medium` | 一致 |
| Agent / runtime / CLI | Codex、persisted、memory off、multi-agent on、Python `3.14.5`、CLI `0.146.0`、runtime `61b26e61...9a73` | 一致 |
| permission | `workspace-write / never` | 一致 |
| executor / token | global queue、`M=24`、all-agent token accounting v1 | 一致 |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` | 3条件で一致 |
| comparison preflight key | `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561` | Baseline / freeとも一致 |

互換な既存atomic runは両条件とも0件だった。`plan-missing --desired-count 5`で各70件を固定し、両planを一つのglobal queueへ投入した。実行結果は計140 / 140 valid、excluded attempt 0、controller error 0だった。

## 集約KPI

| prompt | score分布 | quality中央値 | all-agent token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 0 = 65 / 1 / 4` | 92.857 | 13,624,982 | 3,333.567秒 |
| ControlFreeRepository | `4 / 0 = 65 / 5` | 92.857 | 3,488,611 | 1,166.296秒 |
| Candidate147 | `4 = 70` | 100.000 | 1,447,626 | 852.543秒 |

差分は行の後者から前者を引いた値である。

| 差分 | quality | token | elapsed |
| --- | ---: | ---: | ---: |
| free - Baseline | 0.000 | -10,136,371（-74.40%） | -2,167.271秒（-65.01%） |
| Candidate147 - Baseline | +7.143 | -12,177,356（-89.38%） | -2,481.024秒（-74.43%） |
| Candidate147 - free | +7.143 | -2,040,985（-58.50%） | -313.753秒（-26.90%） |

## N × Case内訳

score分布は各caseの5件を示す。KPI欄は`token中央値 / elapsed中央値`である。

| case | Baseline score | free score | C147 score | Baseline KPI | free KPI | C147 KPI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `4×2, 0×3` | `0×5` | `4×5` | 361,840 / 105.349秒 | 377,427 / 130.519秒 | 19,195 / 12.148秒 |
| A02 repository-resolvable routing | `4×4, 0×1` | `4×5` | `4×5` | 1,341,193 / 320.361秒 | 322,797 / 93.110秒 | 129,085 / 73.379秒 |
| F01 duplicate asset key | `4×5` | `4×5` | `4×5` | 1,219,229 / 295.643秒 | 200,073 / 67.718秒 | 107,202 / 66.424秒 |
| F02 history date bound | `4×5` | `4×5` | `4×5` | 1,230,326 / 322.690秒 | 315,507 / 91.418秒 | 128,236 / 100.607秒 |
| F03 atomic cleanup | `4×5` | `4×5` | `4×5` | 1,436,261 / 354.868秒 | 194,441 / 69.153秒 | 104,320 / 70.866秒 |
| F04 audit column visibility | `4×5` | `4×5` | `4×5` | 1,085,903 / 286.011秒 | 230,431 / 82.514秒 | 151,170 / 91.431秒 |
| F05 clarify units mode | `4×5` | `4×5` | `4×5` | 35,718 / 24.994秒 | 80,565 / 29.880秒 | 37,242 / 26.725秒 |
| F05 out-of-scope deploy | `4×5` | `4×5` | `4×5` | 90,066 / 37.791秒 | 80,708 / 29.288秒 | 37,366 / 25.291秒 |
| F06 empty snapshot contract | `4×5` | `4×5` | `4×5` | 1,236,093 / 259.940秒 | 256,588 / 82.107秒 | 151,542 / 79.393秒 |
| F07 canonical v4 runner | `4×5` | `4×5` | `4×5` | 1,155,848 / 328.265秒 | 378,612 / 109.550秒 | 102,504 / 72.547秒 |
| F07 dependency provenance | `4×4, 3×1` | `4×5` | `4×5` | 732,994 / 239.564秒 | 189,764 / 71.996秒 | 87,284 / 54.324秒 |
| F08 CLI reference sync | `4×5` | `4×5` | `4×5` | 1,639,820 / 358.087秒 | 424,826 / 121.538秒 | 113,067 / 56.343秒 |
| F10 entrypoint inventory | `4×5` | `4×5` | `4×5` | 316,779 / 114.510秒 | 240,882 / 101.626秒 | 87,934 / 61.546秒 |
| F10 monthly format review | `4×5` | `4×5` | `4×5` | 253,908 / 86.295秒 | 222,214 / 90.476秒 | 93,096 / 51.796秒 |

## 低scoreの事実

BaselineのA01は3 / 5件で、未固定値の確認前に編集または試験へ進みscore `0`だった。A02は1 / 5件で正規routeと許可された変更pathを満たさずscore `0`だった。F07 dependency provenanceは1 / 5件で必須dependency検証commandの実行証拠がなくscore `3`だった。

ControlFreeRepositoryのA01は5 / 5件すべてで、未固定値の確認前に編集と試験へ進みscore `0`だった。他の13 caseは各5 / 5件がscore `4`だった。

## 保存証拠

- Baseline result ID: `5ee97407c0e848d4b96bc5e6f32fe28e`
- ControlFreeRepository result ID: `1ec47076580144c4b0c15d47fd0a1fa8`
- Baseline pool: `d65b78fa1b7950db43cc303843c0b8e735007bd001cf095b141eaa99d801c513`
- ControlFreeRepository pool: `91a82726350e2ce3b40e3785a4dc8daa5f4a5a9792878d4f8eccd7e1b8665c92`
- Baseline analysis: `4207fdd341094466abecdfe5b738d4fe`
- ControlFreeRepository analysis: `5fba2d90027244b584ec99d27e63ef10`
- Candidate147 analysis: `16758ebbaef040328797739cd92f02fe`
- Baseline compact archive SHA-256: `113c32351d8c721d7708b3406959863eb7fd92c2ff0031a095f6bd8be30e61a4`
- ControlFreeRepository compact archive SHA-256: `d94533b30ba69bb62981aa5b1eb9201115463de2063c47e26c7c934374686e1b`

raw evidence、selection、analysis、comparison viewは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/`配下へ保存した。登録済みrunと一次ratingは変更しない。
