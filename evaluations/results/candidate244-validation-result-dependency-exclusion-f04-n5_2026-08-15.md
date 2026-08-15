# Candidate244 検証途中結果への発行依存の閉鎖 F04 N=5

## 結論

Candidate244はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。3つのrequired commandは5 / 5件ですべて順に個別成功し、shell commandへの結合と許可外driftは0件だった。

一方、3 / 5件では`npm ci`、`npm run lint`、`npm run build`を三つの別custom tool callから発行し、各途中結果をmodelへ返してから次を発行した。一つの発行判断から個別commandを実行したのは2 / 5件に留まった。対象の依存関係を閉じ切れなかったため`mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-validation-result-dependency-exclusion-r1`
- bundle SHA-256: `e2ac41057d44d72f74ce89f569893723651cdbfd23ec9aa7180d4af0e0e39945`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate244 result: `5311ccb065ff404b9f08ccacb23e2269`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate244-validation-result-dependency-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| `npm ci`、lint、buildの欠落 | 0 / 5 |
| required commandの順序違反 | 0 / 5 |
| required commandのshell結合 | 0 / 5 |
| 一つの発行判断から3 commandを個別実行 | 2 / 5 |
| 途中結果後に次commandを別発行 | 3 / 5 |
| 失敗後の依存command発行 | 対象失敗なし、`not_exercised` |

本文はCandidate243比で`14,146 -> 13,180 bytes`、966 bytes減った。しかし、短縮した五文は3件で途中結果への発行依存を禁止として消費されず、成功した2件の実行形だけを根拠に成立へ補完しない。

## KPI

| 指標 | Candidate147 | Candidate244 | 差 |
| --- | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 281,762 | +130,592（+86.39%） |
| elapsed中央値 | 91.431秒 | 87.873秒 | -3.558秒（-3.89%） |

token増加と経過時間短縮は同時に観測されたが、機序不通過のため五文の効果として扱わない。

## 状態

`f04_n5_completed / quality_passed / mechanism_failed_3_of_5 / cost_increased / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](5311ccb065ff404b9f08ccacb23e2269.json)、[品質監査](candidate244-validation-result-dependency-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate244-validation-result-dependency-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。
