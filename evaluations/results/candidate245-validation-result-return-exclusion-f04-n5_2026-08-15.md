# Candidate245 検証途中結果の返却許可閉鎖 F04 N=5

## 結論

Candidate245はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。3つのrequired commandは5 / 5件ですべて順に個別成功し、shell commandへの結合、protocol violation、許可外driftは0件だった。

一方、4 / 5件では`npm ci`、`npm run lint`、`npm run build`を三つの別custom tool callから発行し、各途中結果をmodelへ返してから次を発行した。一つの発行境界から個別commandを実行したのは1 / 5件だけである。Candidate244の3 / 5件より反例が1件増え、対象の返却許可を閉じ切れなかったため`mechanism_failed / stopped`とする。追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-validation-result-return-exclusion-r1`
- bundle SHA-256: `2ae47626da9d7afbba5a1e9dc0aaacea0886b3728af9bed137ef1f6b65747930`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate243 `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- counterexample only: Candidate244 `the-caption-3ce91a4-validation-result-dependency-exclusion-r1`
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate245 result: `23d351a41dde4c6eb4a4bcd32cdfbbd4`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate245-validation-result-return-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| `npm ci`、lint、buildの欠落 | 0 / 5 |
| required commandの順序違反 | 0 / 5 |
| required commandのshell結合 | 0 / 5 |
| 一つの発行境界から3 commandを個別実行 | 1 / 5 |
| 途中結果後に次commandを別発行 | 4 / 5 |
| 失敗後の依存command発行 | 対象失敗なし、`not_exercised` |

4件のtraceでは、検証開始前に全commandと停止条件を述べた後も、各commandを別custom tool callとして発行した。途中に利用者向けmessageは挟まなかったが、command resultは毎回modelへ返り、reasoningを経て次のcallが発行された。「判断側」という環境非依存の役割名は、実行model自身またはcustom tool return境界へ安定して対応づけられなかった。

## KPI

| 指標 | Candidate147 | Candidate244 | Candidate245 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 281,762 | 337,752 | +186,582（+123.43%） |
| elapsed中央値 | 91.431秒 | 87.873秒 | 85.376秒 | -6.055秒（-6.62%） |

Candidate245のtoken中央値はCandidate244より55,990（19.87%）多い。経過時間は短くなったが、品質・機序の停止条件と総使用tokenの停止条件をともに通過しない。

## 状態

`f04_n5_completed / quality_passed / mechanism_failed_4_of_5 / cost_increased / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](23d351a41dde4c6eb4a4bcd32cdfbbd4.json)、[品質監査](candidate245-validation-result-return-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate245-validation-result-return-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。
