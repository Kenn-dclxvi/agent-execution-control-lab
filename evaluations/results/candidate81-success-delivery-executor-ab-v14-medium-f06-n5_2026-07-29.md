# Candidate81 success delivery executor A/B Rating v14 Medium F06 N=5

## 結論

pytest成功rawをmodelへ配送しないexact allowlist treatmentは、model-visible resultをcontrol比で中央値`-67.33%`、合計`-64.47%`へ減らした。一方、all-agent tokenは中央値`+41.76%`、合計`+22.29%`、elapsedは中央値`+25.94%`、合計`+7.63%`だった。両条件とも5 / 5件がscore `4`である。

したがって「成功出力を減らす機構」は成立したが、「総tokenと時間を減らす制御」は成立していない。model再入は中央値`4 → 7`、合計`22 → 31`へ増えた。現在状態を`executor_f02_f06_evaluated / quality_passed / output_reduced / cost_control_failed / stopped`とする。Std14、採用、release、本体反映へ進めない。

## Comparison identity

- TaskSpec / set: `the-caption-validation-fast-path-f06-r1` / `r1`
- case: `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2`
- evaluation set identity SHA-256: `4efcb48c2b31280e5eb613962d0367d00b1e151e79c6375cf36a45bf8dcc63a5`
- fixture identity SHA-256: `6bd345bda75157b6d29a373a74ca9d9352f429751e33e5bd9e601cbbef63ef06`
- prompt: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model / reasoning / N / M: `gpt-5.6-sol` / `medium` / `5` / `5`
- runtime: Codex CLI `0.146.0` / Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- control result: `a688714236ae45efa80fe5356517630c`
- treatment result: `69f1aab2e1ac4be3b59301d89aa1b61e`

controlとtreatmentはTaskSpec、fixture、prompt、rating、model、reasoning、permission、observation delivery、M / Nを一致させた。差はtreatmentの`comparison_conditions.executor_parameters.success_delivery`だけである。executor parameter差によりcompatibility keyは異なるため、通常のprompt comparisonではなくexecutor A/B診断として扱う。

## 3 KPI

| condition | score 4 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| control | 5 / 5 | `126,409` | `678,337` | `72.664`秒 | `401.020`秒 |
| exact allowlist treatment | 5 / 5 | `179,199` | `829,560` | `91.509`秒 | `431.612`秒 |
| treatment - control | `0` | `+52,790`（`+41.76%`） | `+151,223`（`+22.29%`） | `+18.846`秒（`+25.94%`） | `+30.592`秒（`+7.63%`） |

| iteration | control token | treatment token | control elapsed | treatment elapsed |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `119,996` | `192,737` | `66.232`秒 | `91.515`秒 |
| 2 | `125,377` | `184,065` | `71.487`秒 | `91.509`秒 |
| 3 | `178,296` | `179,199` | `110.235`秒 | `101.673`秒 |
| 4 | `126,409` | `160,880` | `72.664`秒 | `73.847`秒 |
| 5 | `128,259` | `112,679` | `80.402`秒 | `73.068`秒 |

## Outputとroute診断

| 診断 | control | treatment | treatment - control |
| --- | ---: | ---: | ---: |
| model-visible result bytes中央値 | `64,376` | `21,029` | `-43,347`（`-67.33%`） |
| model-visible result bytes合計 | `285,133` | `101,304` | `-183,829`（`-64.47%`） |
| model再入中央値 | `4` | `7` | `+3`（`+75.00%`） |
| model再入合計 | `22` | `31` | `+9`（`+40.91%`） |
| treatment local raw evidence | - | `10件 / 896,030 bytes` | - |
| treatment raw pytest marker流入 | - | `0 / 5` | - |

事実として、treatmentは成功rawのmodel流入を防いだ。一方、result削減量よりもmodel再入と実行経路の増加が大きく、総tokenは増えた。

原因について確定できるのは、control / treatment差が`success_delivery`だけであり、treatmentでmodel再入が増えたことまでである。wrapper命令の追加、wrapper commandの選択、receipt処理のどれが再入増加の主因かは、このN=5だけでは分離できない。

## 判定

- quality gate: `passed`（両条件5 / 5 score `4`）
- output reduction gate: `passed`
- token gate: `failed`（中央値・合計とも増加）
- elapsed gate: `failed`（中央値・合計とも増加）
- Std14、採用、release、本体反映: 未実施・停止

同じmodel-visible wrapper方式をStd14へ広げない。再開する場合は、modelへwrapper選択を要求せず、元のpytest commandをexecutor側で透過的にinterceptできる境界が実装可能な場合だけ、別executor revisionとして事前gateを固定する。単なるreceipt短縮や追加prompt指示は、本結果が示したmodel再入増加を解消しないため次revisionの根拠にしない。

## 保存証跡

- control result content SHA-256: `735cae63fc4ae648df21acccc6c1410523b167d8e02242cf6dc81c9e5267f2f4`
- control compatibility key: `3c8ee2ce3bffdef2bd5cbed08cb4ed56db4f614e5f53687c2d6367476e38e9e5`
- control execution archive SHA-256: `db6af6d69402abbd872bc71eed229ae45adf703584d0aee31e12cda8955d66af`
- control execution seal SHA-256: `7c1a8b76a984a4c458c7d3c142d3122e92b29e42fff729e9c241eaf11404fc99`
- control final archive SHA-256: `28b4da8c2212c5bb96ed5fe0e5c54e0dd25b0edebbf42a753fdfe7e59947b39f`
- treatment result content SHA-256: `9a9309cfc075b72f1ccbd7f0b78d6869e4c5cab58b83b2e6577c8f06c4f1bcf4`
- treatment final archive SHA-256: `7a412a2282f51973aa024a8aa0a92e8b840971cd9cb790b2fc580d98f74861ad`
