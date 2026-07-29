# Candidate81 / Candidate94 operation criterion totality Rating v14 Medium 標準14 N=5

## 結論

Candidate81とCandidate94を、Codex CLI `0.146.0`、Rating v14、Medium、標準14項目各`N=5`、global queue `M=24`の同一条件で新規実行した。両条件とも70 / 70件がvalid・rateableで、excluded attemptは0件だった。

Candidate81は70 / 70件がscore `4`だった。Candidate94はscore `4 / 1 = 69 / 1`で、A02 iteration 5がrepository authorityから解決できる正規routeを質問して停止し、`run.sh`の修正と試験を実施しなかった。Candidate94設計の「score `4`未満が1件でもあれば停止する」という条件に該当するため、現在状態を`standard14_evaluated / quality_gate_failed / stopped`とする。

Candidate94 minus Candidate81の5 iteration集約中央値差は、quality `0.000`、all-agent token `+220,485`（`+10.91%`）、elapsed `+55.241`秒（`+6.02%`）だった。quality中央値`100.000`は4 / 5 iterationが全件score `4`だったためであり、1件の品質失敗を打ち消す根拠にはしない。

## Identity

- evaluation set: `the-caption-standard14-r1`
- set identity SHA-256: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- cases: 標準14項目、各`N=5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- execution: global queue / `M=24`
- Codex CLI: `0.146.0`
- Python fixture runtime: `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`
- compatibility key: `c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c`
- C81 result: `820cd025a1b34f6eb22f4903ce63cc21`
- C81 content SHA-256: `7542cef84fdc77079fdf45fef8da731d358cf36a29192fc580c9968dd742b198`
- C94 result: `fdc86bfd09a349d5a64b768c0adf450a`
- C94 content SHA-256: `d6499dd2bd68588f0927dc586e7210d28f1507fdfad7dffc5d0e6d0bd34a4ca4`

保存済みC81 Rating v14標準14resultはCodex CLI `0.144.0`条件だった。CLI差を隠して比較しないため、C81とCandidate94を`0.146.0`条件で各70件新規実行した。両profileはprofile IDとprompt identity以外を同一とし、Evaluation set、case revision、TaskSpec、fixture、oracle、required validation、rating、model、reasoning、M / Nを変更していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | `70 / 70` | `100.000` | `2,020,899` | `9,829,950` | `916.914`秒 | `4,637.405`秒 |
| Candidate94 | `70 / 69` | `100.000` | `2,241,384` | `11,047,831` | `972.154`秒 | `4,845.308`秒 |
| Candidate94 - C81 | score 4 `-1` | `0.000` | `+220,485`（`+10.91%`） | `+1,217,881`（`+12.39%`） | `+55.241`秒（`+6.02%`） | `+207.904`秒（`+4.48%`） |

## 品質失敗

低得点は次の1件だけだった。

- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING`
- iteration: `5`
- run ID: `851b97526bb449e4ac2e0b257faf1747`
- score: `1`
- failures: `a02_canonical_route_mismatch`、`a02_changed_paths_mismatch`、`a02_abstract_test_evidence_missing`
- rating: repositoryから一意に解決できる正規routeを質問し、修正と試験へ進まなかった

これはvalid run内の成果未達であり、external failure、除外、採点不能とは扱わない。Candidate94の変更がA02失敗の原因であるという因果までは、この単一N=5結果から一般化しない。

## 診断境界

- command protocol violation: C81 `0`、Candidate94 `0`
- monthly review numeric location exact: C81 `5 / 5`、Candidate94 `5 / 5`
- owner-producer evidence inadmissible: C81 `55 / 70`、Candidate94 `53 / 70`

owner-producer evidenceはRating v14ではdiagnostic onlyである。標準14にはCandidate94設計で固定したSender不一致、producer terminal後のresult欠落、`unavailable` terminal failureの専用caseがない。この結果をtargeted gate通過、`owner=none` route成立、`unavailable`機構成立の証拠へ読み替えない。

## 実行順序と状態境界

Candidate94設計はtargeted評価通過前の標準14を停止していたが、2026-07-30のユーザーによる標準14 N=5の明示依頼を実行順変更のauthorityとして扱った。targeted評価自体は未実施であり、未通過のままである。

- 標準14実行: `completed`
- 標準14品質: `quality_gate_failed`
- Candidate94 state: `standard14_evaluated / stopped`
- targeted mechanism gate: `not_evaluated`
- 採用、release、THE-CAPTION本体反映: 未実施・未判断

事前停止条件に従い、失敗確認後の再試行、別ratingでの再採点、targeted評価、追加Candidate、release作成、本体反映へ進めない。

## 保存場所

- C81 profile: [`candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2`](../profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json)
- Candidate94 profile: [`candidate94-operation-criterion-totality-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](../profiles/candidate94-operation-criterion-totality-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- C81 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-20260730-r2`
- Candidate94 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate94-operation-criterion-totality-v14-reasoning-medium-standard14-global-m24-n5-cli0146-20260730-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146-20260730-r1.json`

raw run archiveはverification checkoutに保持し、このrepositoryへcommitしない。
