# Candidate226 結果影響範囲 A02 N=5

## 結論

Candidate226はA02の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。品質条件は通過した。

一方、開始状態の確認結果によってreadの要否、対象、許可、方法および停止条件が変わらないにもかかわらず、その結果を受け取ってからreadを別に発行した経路を4 / 5件で観測した。開始状態の確認とreadを同じinvocationから発行したのは1 / 5件だった。事前停止条件に従い、機序条件を不通過とし、A01は発行しない。

状態は`a02_n5_completed / quality_passed / mechanism_failed_4_of_5 / stopped / a01_not_started / adoption_not_decided / release_not_created / projection_not_performed`とする。

## 固定条件

- prompt: `the-caption-3ce91a4-human-result-effect-scope-r1`、bundle SHA-256 `5545d75864a396a6eedbc3212c24e6f5cd0322a35313fdaa04f3e29b5f8b25dd`。
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2、N=5。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24、all-agent token accounting v1。
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`。
- comparison baseline: Candidate147の保存済みA02 N=5 result `c08d676a0d97424f88dc2ab1d7fe2961`。新しいbaseline runは発行していない。

実行前の互換条件、保存済みLayer 1のA02限定bindingおよび5件の発行許可は[実行準備監査](../../docs/candidate226-human-result-effect-scope-a02-n5-execution-preparation-audit.md)を正本とする。

## 品質とcost

| 指標 | Candidate147 A02 | Candidate226 A02 | 差 |
| --- | ---: | ---: | ---: |
| valid / rateable | 5 / 5 | 5 / 5 | 0 |
| Score `4` | 5 / 5 | 5 / 5 | 0 |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 129,085 | 180,515 | +51,430（+39.84%） |
| elapsed中央値 | 73.379秒 | 83.742秒 | +10.363秒（+14.12%） |

N=5の記述比較であり、機序不通過をcost差で補わない。

## 機序判定

4件では開始状態の確認を一つのcommand invocationとして完了した後、`run.sh`などのreadを別のcommand invocationとして発行した。開始状態の結果はTaskSpec上、readの対象や許可を変更しないため、この分離はreadに不要な待機依存を作っている。

残る1件は開始状態の確認と`run.sh`等のreadを同じinvocationから発行しており、対象の待機依存を作らなかった。したがって機序結果は1 / 5通過、4 / 5不通過である。

登録resultは[`7935883b701a4c1b93dba54820fcde6e.json`](7935883b701a4c1b93dba54820fcde6e.json)、採点内訳は[`candidate226-human-result-effect-scope-a02-n5-quality-audit-r1.json`](candidate226-human-result-effect-scope-a02-n5-quality-audit-r1.json)、機序内訳は[`candidate226-human-result-effect-scope-a02-n5-mechanism-audit-r1.json`](candidate226-human-result-effect-scope-a02-n5-mechanism-audit-r1.json)を正本とする。
