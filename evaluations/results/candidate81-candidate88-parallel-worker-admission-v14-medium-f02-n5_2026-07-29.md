# Candidate81 / Candidate88 parallel Worker admission Rating v14 Medium F02 N=5

## 結論

Candidate88はF02の5 / 5件でvalid・rateable・score `4`だった。required outcome、required command、許可path、終了条件を全件で満たし、excluded attemptは0件である。

一方、AI裁量Workerを4 / 5件で起動し、そのうちiteration 3と4はWorker完了を待ってからrequired validationを開始した。設計時に固定した「逐次Workerが1件でもあれば停止」に該当する。

Candidate88 minus Candidate81の中央値差も、quality `0.000`、all-agent token `+80,914`（`+26.28%`）、elapsed `+8.646`秒（`+8.03%`）であり、両コストKPIが悪化した。Candidate88を`targeted_f02_evaluated / stopped`とし、F04、D01、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C88 result: `97ef616cca42433792dc30885a314b7a`
- C88 content SHA-256: `17186a48d8e779779d095ee0218496de86a883570f1a9b9d12236bc643e52e0a`

既存F02 r1のEvaluation set、TaskSpec、fixture、oracle、allowed path、required validationは変更していない。C81 / C88 profileはprofile IDとprompt identity以外のcomparison conditionsを一致させた。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C88 | 5 / 5 | `388,800` | `1,966,901` | `482,013` | `116.275`秒 | `616.452`秒 | `170.915`秒 |
| C88 - C81 | `0` | `+80,914` | `+515,353` | `+147,476` | `+8.646`秒 | `+5.631`秒 | `+8.563`秒 |

token合計は`+35.50%`、elapsed合計は`+0.92%`だった。

## Paired diagnostic

| iteration | route | token差 | elapsed差 |
| ---: | --- | ---: | ---: |
| 1 | root-only | `-50,550` | `-48.585`秒 |
| 2 | Workerとrequired validationを同じwaveで開始 | `+191,001` | `+1.723`秒 |
| 3 | Worker完了後にrequired validation開始 | `+147,476` | `-34.877`秒 |
| 4 | Worker完了後にrequired validation開始 | `+60,602` | `+20.262`秒 |
| 5 | Workerとrequired validationを同じwaveで開始 | `+166,824` | `+67.109`秒 |

iteration 3は対応runよりelapsedが短いが、保存trace上はWorker待機後にrequired validationを開始している。実測時間の偶然の短縮でroute違反を反転させない。

## Worker route

| route | run数 | child token |
| --- | ---: | ---: |
| root-only | 1 | `0` |
| same-wave Worker | 2 | `178,501` |
| sequential Worker | 2 | `187,580` |
| 合計 | 5 | `366,081` |

Workerあり4 runはすべて`/root/independent_contract_check`を一つ起動した。同一operationの別Workerへの再割当てとWorker result欠落は0件だった。

Candidate88全体のC81比token増加`+515,353`に対しchild tokenは`366,081`である。C88 root token合計もC81比`+149,272`だったため、悪化をchild tokenだけへ帰属させない。

iteration 4ではchildのcommand `.`に`missing_machine_bound_exit_code`が1件記録された。required validationではなく診断用child invocationのcommand evidenceである。rootのrequired validationは成功しているためquality failureへ格上げしない。

## Gate

- quality gate: `passed`（5 / 5 score `4`）
- parallel Worker admission: `failed`（sequential Worker 2件）
- cost gate: `failed`（token / elapsed中央値ともCandidate81より大きい）
- Candidate88 state: `targeted_f02_evaluated / stopped`
- F04、D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate88-parallel-worker-admission-v14-medium-f02-n5-20260729-r1.json`
