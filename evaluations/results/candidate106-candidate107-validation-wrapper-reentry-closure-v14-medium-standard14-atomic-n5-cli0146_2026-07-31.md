# Candidate106 / Candidate107 validation wrapper再入closure Rating v14 Medium 標準14 atomic N=5

## 結論

Candidate107を標準14項目で各5 sample、計70 atomic run実行した。70 / 70件がvalid・rateable・score `4`で、excluded attemptと再試行は0件だった。

保存済みCandidate106から選択した5 sampleとの互換比較では、Candidate107 minus Candidate106の中央値差はquality `0.000`、all-agent token `-181,469`（`-10.65%`）、elapsed `+74.332`秒（`+8.53%`）だった。tokenとelapsedの方向が分かれたため、効率の一方向改善とは扱わない。

今回の依頼は、F03 B20の事前gateで停止していたStandard14を明示的に再開した試験である。Standard14品質は通過したが、保存済みF03 B20のouter deadline違反4 / 100件は失効しない。Candidate107の現在状態は`targeted_f03_b20_evaluated / standard14_evaluated_by_explicit_reopen / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`とする。採用、release、runtime projection、本体反映は行わない。

## 実行前gate

| 項目 | 値 |
| --- | --- |
| reference | Candidate106 atomic import / legacy result `6a5b44bde1194ac3b3ff28ee3aea4a1e` |
| candidate | `the-caption-3ce91a4-validation-wrapper-reentry-closure-r1` |
| bundle SHA-256 | `72c6f4b8818065300ca24fd0a42bdf49ce834ae44d4f2406da497f98c064c50d` |
| Evaluation set | `the-caption-standard14-r1/r1` |
| legacy compatibility key | `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561` |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / Python | Codex CLI `0.146.0` / Python `3.14.5` |
| execution | pair-block-longest-first global queue / `M=24` |
| requested selection | 14 case × 5 sample = 70 run |

Candidate106の保存済みresultをatomic registryへimportし、同じ実効条件からCandidate107の空poolを作成した。既存complete sampleは0件だったため、不足5 sample・70 runだけをdispatch planへ固定した。70 capsuleはすべて`execution-capsule/v3`で、`binding.sample_id`を持ち、`repetition_condition`を持たない。`comparison-preflight/v2`が70 slotを承認した後にだけ実行した。

Layer 1のAPFS cloneで`0700`が`0755`へ変わる既存不具合をpreflightが検知した。clone commandへ属性保持を追加し、コピー前後のfixture identity完全一致を確認してからcycleを再生成した。失敗した準備cycleから評価slotは発行していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Candidate106 | `70 / 70` | `100.000` | `1,704,606` | `871.164`秒 |
| Candidate107 | `70 / 70` | `100.000` | `1,523,137` | `945.496`秒 |
| C107 - C106 | score 4 `0` | `0.000` | `-181,469`（`-10.65%`） | `+74.332`秒（`+8.53%`） |

両条件は同じexecution stratumで各5 sampleを選択した。strata balanceは`matched`である。

## Candidate107 sample別内訳

| sample | quality | token | elapsed |
| ---: | ---: | ---: | ---: |
| 1 | `100.000` | `1,629,740` | `945.496`秒 |
| 2 | `100.000` | `1,570,346` | `960.186`秒 |
| 3 | `100.000` | `1,523,137` | `979.503`秒 |
| 4 | `100.000` | `1,507,011` | `930.000`秒 |
| 5 | `100.000` | `1,421,382` | `881.552`秒 |

sample番号はselection内の表示順であり、run identityまたは実行時の束ではない。各sampleは共通`sample_id`を持つ14個の独立runから構成する。

## Case別中央値

差はCandidate107 minus Candidate106である。

| case | C107 token | token差 | C107 elapsed | elapsed差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | `57,368` | `-38,442`（`-40.12%`） | `31.892`秒 | `-4.752`秒（`-12.97%`） |
| A02 | `125,559` | `-59,888`（`-32.29%`） | `93.383`秒 | `+4.462`秒（`+5.02%`） |
| F01 | `127,797` | `-5,688`（`-4.26%`） | `75.447`秒 | `+9.368`秒（`+14.18%`） |
| F02 | `173,000` | `-26,418`（`-13.25%`） | `92.597`秒 | `+20.220`秒（`+27.94%`） |
| F03 | `114,264` | `-19,168`（`-14.37%`） | `91.298`秒 | `+19.679`秒（`+27.48%`） |
| F04 | `177,437` | `+14,735`（`+9.06%`） | `94.084`秒 | `+16.234`秒（`+20.85%`） |
| F05 clarify | `36,708` | `-2,317`（`-5.94%`） | `24.447`秒 | `+3.780`秒（`+18.29%`） |
| F05 out-of-scope | `36,962` | `-2,686`（`-6.77%`） | `21.392`秒 | `-5.091`秒（`-19.22%`） |
| F06 | `121,869` | `-30,093`（`-19.80%`） | `77.012`秒 | `+2.167`秒（`+2.90%`） |
| F07 canonical | `111,001` | `-17,674`（`-13.74%`） | `83.780`秒 | `+12.758`秒（`+17.96%`） |
| F07 dependency | `93,147` | `-11,254`（`-10.78%`） | `58.705`秒 | `+5.456`秒（`+10.25%`） |
| F08 | `123,474` | `-3,838`（`-3.01%`） | `79.943`秒 | `+2.108`秒（`+2.71%`） |
| F10 entrypoint | `104,709` | `-1,738`（`-1.63%`） | `72.478`秒 | `+8.721`秒（`+13.68%`） |
| F10 monthly | `94,050` | `-3,263`（`-3.35%`） | `59.121`秒 | `+6.512`秒（`+12.38%`） |

Candidate107のtoken中央値は13 / 14 caseで小さく、elapsed中央値は2 / 14 caseで小さかった。N=5の観測範囲を超えた因果または統計的有意性は主張しない。

## 診断と保存

- command protocol violation: `0 / 70`
- monthly review numeric location exact: `5 / 5`
- owner-producer evidence inadmissible: `55 / 70`。Rating v14ではdiagnostic onlyであり、scoreを変更しない
- runner: `70 / 70 valid`、attempt `70`、excluded `0`
- 70 run実行時間: `227.243`秒
- execution archive SHA-256: `e1794a6a5da7c2795e9c931c63d1a833126c0c65bad5b465f980b325583bc710`
- Candidate106 selection: `0343907dab504c04866e539f88b93206`
- Candidate107 selection: `0664c42c26e449d3ac75be736b4d54a5`
- Candidate106 analysis: `a7b2a2b7929c410d8b8ba37411e8037b`
- Candidate107 analysis: `d54796a02a564e288c4c2dc567f256ca`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146-20260731-r1`

raw evidenceとatomic registryはverification領域に保持し、このrepositoryへcommitしない。
