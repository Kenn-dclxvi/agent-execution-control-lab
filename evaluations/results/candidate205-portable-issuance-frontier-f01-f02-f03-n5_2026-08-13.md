# Candidate205 portable issuance frontier F01 / F02 / F03 N=5結果

> **結果**: `15 / 15 valid / Score 4 = 15 / quality_passed / mechanism_failed / stopped`

## 結論

Candidate205 `the-caption-3ce91a4-portable-issuance-frontier-r1`をF01 r3、F02 r1、F03 r2で各5回、合計15 atomic runs実行した。15 / 15がvalidかつScore 4で、excluded attempt、controller error、required command failure、command protocol違反および許可外変更は0件だった。品質gateは通過した。

一方、command event順の再監査では、15 / 15件が開始identity commandのterminal後に許可read commandを開始していた。旧監査で共同発行とした1件は、二つのcommand間にagent messageがなかっただけで、identity完了後の別tool発行だった。固定した機構基準は15 / 15を要求するため不通過である。

停止条件に従いStandard14全体、N拡張、採用、releaseおよびprojectionへ進めない。

## Identity

- candidate: Candidate205
- prompt: `the-caption-3ce91a4-portable-issuance-frontier-r1`
- bundle SHA-256: `94cd1c2bdf12da74d8700daa95d15f98e70e6578fbca7a0f96b5ee6108827a53`
- evaluation set: `the-caption-standard14-r1`
- coverage: F01 r3 / F02 r1 / F03 r2、各N=5
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`
- configured M: `24`
- compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- registered result: `b37d060fcf6c4fb7abb668b2cb89a754`
- result content SHA-256: `0de15ca928500189b7a7bb494c59b1e780d38091215e0305ea02403fef875ad9`
- selection / analysis: `62b5d8c8788a450ea846f5d412384659 / bc4a9f299c354167a5c9be3644304360`

## 品質

| 項目 | 結果 |
|---|---:|
| requested / valid | 15 / 15 |
| Score 4 | 15 / 15 |
| excluded / external failure | 0 / 0 |
| successful / failed command | 147 / 0 |
| command protocol violation | 0 |
| unexpected changed path | 0 |

owner-producer診断は`failed 10 / not_applicable 5`だった。3ケースは独立producer executionを要求していないため、Rating v14では診断に限定する。

## issuance mechanism

| predicate | 期待 | 実測 | 判定 |
|---|---:|---:|---|
| identity判定待ちによる許可read先送り | 0 / 15 | 15 / 15 | failed |
| identity完了前に許可read commandを開始 | 15 / 15 | 0 / 15 | failed |
| identity result前のartifact変更・required validation | 0 / 15 | 0 / 15 | pass |
| child / unwanted producer | 0 / 15 | 0 / 15 | pass |
| command protocol violation | 0 / 15 | 0 / 15 | pass |
| unexpected changed path | 0 / 15 | 0 / 15 | pass |

全15 rolloutをcommand event順で再監査した。F02 iteration 5の`c62f31d690124e26833046aa99e6ce22`は二つのcommand間にagent messageがなかったが、identity commandのcompleted event後にread commandのstarted eventが記録されていた。他14件もidentityをterminalにしてからreadを別発行している。

したがってC204の0 / 15からC205の1 / 15へ改善したという旧解釈を撤回する。`ISSUANCE`一責任の追加だけでは、C147の発行対象集合の構成、result消費前の全件発行、収集障壁を復元できたと判定できない。原因は一項目へ限定せず、[`C147機能分解の再分析`](../../docs/c147-functional-decomposition-reanalysis.md)へ戻す。

## KPI

quality・mechanism gate不通過なので、Candidate147との効率比較は確定しない。Candidate205単独の記述値だけを保持する。

| 指標 | Candidate205 |
|---|---:|
| quality中央値 | 100.000 |
| all-agent token中央値 | 770,346 |
| elapsed中央値 | 322.191秒 |
| token合計 | 3,879,658 |
| elapsed合計 | 1,600.668秒 |

上の中央値は3ケースを同じiterationへ束ねたselection中央値である。C147参照値との差を、mechanism不通過後の効率改善として解釈しない。

## 一次証拠

- [登録result](b37d060fcf6c4fb7abb668b2cb89a754.json)
- [品質監査](candidate205-portable-issuance-frontier-f01-f02-f03-n5-quality-audit-r1.json)
- [機構監査](candidate205-portable-issuance-frontier-f01-f02-f03-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate205-portable-issuance-frontier-f01-f02-f03-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate205-portable-issuance-frontier-f01-f02-f03-n5-execution-preparation-audit.md)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate205-portable-issuance-frontier-f01-f02-f03-n5-20260813-r1`

## 状態

`candidate205_targeted_completed / valid_15 / score4_15 / quality_passed / strong_event_order_coissued_0_of_15 / isolated_identity_15_of_15 / mechanism_failed / stopped / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
