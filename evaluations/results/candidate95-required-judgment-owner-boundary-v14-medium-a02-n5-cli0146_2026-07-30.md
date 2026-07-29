# Candidate95 required judgment owner boundary Rating v14 Medium A02 N=5

## 結論

Candidate95をA02 r2、Rating v14、reasoning `medium`、Codex CLI `0.146.0`、各`N=5`、global queue `M=5`で実行した。5 / 5件がvalid・rateable・score `4`で、excluded attemptは0件だった。

5件すべてでrepository authorityから正規entrypoint `src.app.entrypoints.v4_daily_main`を解決し、`run.sh`だけを変更し、既存testを成功させた。owner clarification、Git authorによるowner探索、品質failureは0件だった。Candidate95のA02 targeted gateは通過した。

## 固定条件

- prompt identity: `the-caption-3ce91a4-required-judgment-owner-boundary-r1`
- bundle SHA-256: `8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190`
- evaluation set: `the-caption-standard14-r1` / A02 r2だけ
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model: `gpt-5.6-sol`
- reasoning: `medium`
- Codex CLI: `0.146.0`
- repetition: `N=5`
- outer concurrency: global queue `M=5`
- permission: `workspace-write / never`

TaskSpec、fixture、rating、model、reasoning、CLI、permission、NはCandidate94標準14のA02条件から変更していない。対象caseと外側concurrencyが異なるため、Candidate94標準14resultとのtoken・elapsed差を互換KPI比較として扱わない。

## 結果

| 指標 | Candidate95 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score分布 | `4 = 5` |
| quality中央値 | `100.000` |
| all-agent token中央値 | `231,696` |
| all-agent token合計 | `1,172,124` |
| elapsed中央値 | `73.441`秒 |
| elapsed合計 | `377.388`秒 |
| excluded attempt | `0` |
| quality failure | `0` |
| command protocol violation | `0` |

各iterationのscoreはすべて`4`だった。5件すべてで次を確認した。

- final `run.sh` SHA-256: `4def3a7305b7a58f8555978c1c6dc1b5179de7a291aa159bc011e60e9021ed42`
- final changed paths: `run.sh`だけ
- successful test evidence: あり
- canonical route mismatch: 0件
- owner clarification: 0件
- Git `log` / `blame`によるowner探索: 0件

## Gateと現在状態

Candidate95設計のA02 targeted必須条件を満たした。現在状態を`targeted_a02_evaluated / quality_gate_passed / route_gate_passed / standard14_not_started`とする。

この結果だけでは標準14全体の品質、採用、release、本体反映を判断しない。次の許可済み段階は、同じRating v14、Medium、CLI `0.146.0`条件の標準14 N=5である。

## Evidence

- result ID: `8ac03547d69e45e785160b32df533069`
- result content SHA-256: `04b5180651e4a753737fee89876aeed676872e2b177f4b2a4aaa2efe85308fe1`
- compatibility key: `e5740fe6edb0efabde9aaab3ccb624d31984ddeaa6fc32076a82266b313b9833`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-20260730-r1`
- compact archive SHA-256: `f979e218966072e9e73f2fa1bf6cc7b94069eb5aba3c940b90732dbdf05ee4da`
- [Candidate95 profile](../profiles/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1.json)
- [Candidate95 design](../../docs/candidate95-required-judgment-owner-boundary-design.md)
