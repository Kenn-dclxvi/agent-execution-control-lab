# Candidate204 portable execution core F01 / F02 / F03 N=5結果

> **結果**: `15 / 15 valid / Score 4 = 15 / quality_passed / mechanism_failed / stopped`

## 結論

Candidate204 `the-caption-3ce91a4-portable-execution-core-r1`をF01 r3、F02 r1、F03 r2で各5回、合計15 atomic runs実行した。15 / 15がvalidで、excluded attempt、controller error、required command failure、command protocol違反および許可外変更は0件だった。固定Rating v14では15 / 15がScore 4で、品質gateは通過した。

一方、15 / 15すべてで開始identityだけを最初に発行し、そのresultを受領してから許可readへ進んだ。M3で固定したportable mechanismは、identity resultがreadを禁止せずtargetも変えない場合に偽dependencyを作らないことを要求する。全件不一致なので機構gateは不通過とする。

停止条件に従いStandard14全体、N拡張、採用、releaseおよびprojectionへ進めない。

## Identity

- candidate: Candidate204
- prompt: `the-caption-3ce91a4-portable-execution-core-r1`
- bundle SHA-256: `d9c90d877e97479d95e5be51306111b221dd7e53c5c921e14599fb39df1faf5e`
- evaluation set: `the-caption-standard14-r1`
- coverage: F01 r3 / F02 r1 / F03 r2、各N=5
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`
- configured M: `24`
- compatibility key: `a1264d0c1bc19834f7ac43266bc2d1489bfddfae171ce7356cb20d4ce5c9cb11`
- registered result: `15313d0d0ffc4dffa3a2e18edff25c2d`
- result content SHA-256: `fb1f3e0195e5f4b3417589db7b4c70e044555f7db31eb623b5b17f931024535a`
- selection / analysis: `c59665b634ca4bce9f35cd3ca4618958 / 3c6855a9be284c4598f4be02cefbe8a8`

## 品質

| 項目 | 結果 |
|---|---:|
| requested / valid | 15 / 15 |
| Score 4 | 15 / 15 |
| excluded / external failure | 0 / 0 |
| successful / failed command | 114 / 0 |
| command protocol violation | 0 |
| unexpected changed path | 0 |

F01は`src/domain/market_units_snapshot.py`、F02は`src/app/v4_engine.py`と`src/domain/collection_history_updater.py`、F03は`src/infra/context_repository.py`だけを変更した。各runでfocused validationと`main_verify.sh`が成功した。

owner-producer診断は`failed 10 / not_applicable 5`だった。Standard14の3ケースは独立producer executionを要求していないため、owner metadataだけから別producerを作らないことは期待経路であり、Rating v14では診断に限定する。

## portable mechanism

| predicate | 期待 | 実測 | 判定 |
|---|---:|---:|---|
| identity判定待ちによる許可read先送り | 0 / 15 | 15 / 15 | failed |
| identityと許可readを初回groupで発行 | 15 / 15 | 0 / 15 | failed |
| child / unwanted producer | 0 / 15 | 0 / 15 | pass |
| command protocol violation | 0 / 15 | 0 / 15 | pass |
| unexpected changed path | 0 / 15 | 0 / 15 | pass |

全15 rolloutの最初のagent message後から次のagent message前までを初回command groupとして監査した。各groupは`pwd / branch / HEAD / status`の開始identityだけを含み、source、testまたは適用instructionのreadは次groupへ置かれた。

prompt本文から`same model step`を削除して`既知に独立なeligible invocation間へ、判断結果を変えないdependencyを追加しない`へ一般化しただけでは、実際の発行遷移を作れなかった。

## KPI

quality・mechanism gate不通過なので、Candidate147との効率比較は確定しない。Candidate204単独の記述値だけを保持する。

| 指標 | Candidate204 |
|---|---:|
| quality中央値 | 100.000 |
| all-agent token中央値 | 759,157 |
| elapsed中央値 | 311.713秒 |
| token合計 | 3,770,082 |
| elapsed合計 | 1,568.945秒 |

上の中央値は3ケースを同じiterationへ束ねたselection中央値である。C147参照値との差を、mechanism不通過後の効率改善として解釈しない。

## 一次証拠

- [品質監査](candidate204-portable-execution-core-f01-f02-f03-n5-quality-audit-r1.json)
- [機構監査](candidate204-portable-execution-core-f01-f02-f03-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate204-portable-execution-core-f01-f02-f03-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate204-portable-execution-core-f01-f02-f03-n5-execution-preparation-audit.md)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate204-portable-execution-core-f01-f02-f03-n5-20260813-r1`

## 状態

`candidate204_targeted_completed / valid_15 / score4_15 / quality_passed / isolated_identity_15_of_15 / mechanism_failed / stopped / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
