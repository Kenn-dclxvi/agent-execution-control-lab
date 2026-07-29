# Candidate81 / Candidate95 required judgment owner boundary Rating v14 Medium 標準14 N=5

## 結論

Candidate81とCandidate95を、Codex CLI `0.146.0`、Rating v14、Medium、標準14項目各`N=5`、global queue `M=24`の互換条件で比較した。両方とも70 / 70件がvalid・rateable・score `4`で、excluded attemptと品質failureは0件だった。

Candidate95のA02も5 / 5件がscore `4`だった。先行targeted A02 N=5と合わせて、Candidate94で観測した不要なowner clarificationは今回の固定条件では再現しなかった。ただし、単一の標準14 N=5から他条件での普遍的な解消までは主張しない。

Candidate95 minus Candidate81の5 iteration集約中央値差は、quality `0.000`、all-agent token `+52,902`（`+2.62%`）、elapsed `+66.952`秒（`+7.30%`）だった。品質gateは通過したが、集約costはtoken・elapsedとも増えた。現在状態を`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。採用、release、本体反映は行わない。

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
- C95 result: `648b4dec10ba4ce191f76be1ee184bf9`
- C95 content SHA-256: `ec5ab689294b1002f07a2745eef3ff4ddf776ddb205d6044e11c9722569a189b`

Candidate95 profileはC81 CLI `0.146.0` profileからprompt identityだけを変更した。Evaluation set、case revision、TaskSpec、fixture、oracle、required validation、rating、model、reasoning、M / Nは変更していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | `70 / 70` | `100.000` | `2,020,899` | `9,829,950` | `916.914`秒 | `4,637.405`秒 |
| Candidate95 | `70 / 70` | `100.000` | `2,073,801` | `10,294,830` | `983.865`秒 | `4,889.970`秒 |
| Candidate95 - C81 | score 4 `0` | `0.000` | `+52,902`（`+2.62%`） | `+464,880`（`+4.73%`） | `+66.952`秒（`+7.30%`） | `+252.565`秒（`+5.45%`） |

## A02と診断境界

- A02: 5 / 5件がvalid・rateable・score `4`
- command protocol violation: 0件
- monthly review numeric location exact: 5 / 5件
- owner-producer evidence inadmissible: 55 / 70件

owner-producer evidenceはRating v14ではdiagnostic onlyであり、品質failureではない。A02では3 / 5件のevent traceに`owner=none`の明示があり、残り2件も正規routeの修正とrequired validationを完了した。1件は`run.sh`の履歴確認に`git log`と`git blame`を使ったが、Git authorをcriterion ownerへbindせず、owner clarificationにも進まなかった。

## 状態境界

- targeted A02: `quality_gate_passed / route_gate_passed`
- 標準14品質: `quality_gate_passed`
- aggregate cost: `both_higher`
- Candidate95 state: `standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`
- 採用、release、THE-CAPTION本体反映: 未実施・未判断

Candidate81は採用・投影済みbaselineのままである。Candidate95の品質通過を採用、release、projectionへ自動昇格しない。

## 保存場所

- C81 profile: [`candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2`](../profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json)
- Candidate95 profile: [`candidate95-required-judgment-owner-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](../profiles/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- Candidate95 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-20260730-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-n5-cli0146-20260730-r1.json`
- final compact archive SHA-256: `cc3a3456b58652c43129b5a33f1fd016f7b7c2162723ba145431171ed809c846`

raw run archiveはverification checkoutに保持し、このrepositoryへcommitしない。
