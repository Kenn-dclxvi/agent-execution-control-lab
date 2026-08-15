# Candidate246 検証途中結果のAI返却許可閉鎖 F04 N=5

## 結論

Candidate246はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。3つのrequired commandは5 / 5件ですべて順に個別成功し、shell commandへの結合、protocol violation、許可外driftは0件だった。

5 / 5件が`npm ci`、`npm run lint`、`npm run build`を一つのcustom tool call内の個別実行として発行し、途中resultをAIへ返してから残りを別発行したrunは0件だった。Candidate245の1 / 5件から5 / 5件へ変わり、対象機序は`mechanism_passed`とする。

一方、総使用token中央値は`183,187`で、Candidate147の`151,170`より32,017（21.18%）多い。固定したコスト停止条件に従い`targeted_passed / cost_not_reduced / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- bundle SHA-256: `5710bd511526b71a6c216b745579bb114424ac0f2e6290ca4b5eff8842e85b5f`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate243 `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- counterexample only: Candidate244、Candidate245
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate246 result: `01453868f25c4013bce7813a14ab1bb9`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate246-validation-result-ai-return-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| `npm ci`、lint、buildの欠落 | 0 / 5 |
| required commandの順序違反 | 0 / 5 |
| required commandのshell結合 | 0 / 5 |
| 一つの発行境界から3 commandを個別実行 | 5 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 0 / 5 |
| 失敗後の依存command発行 | 対象失敗なし、`not_exercised` |

Candidate244の「次の発行判断に使わない」とCandidate245の「判断側へ返さない」は、それぞれ3 / 5件、4 / 5件に別発行を残した。Candidate246が返却先を`AI`と明記すると5 / 5件で閉じた。F04 N=5の範囲では、抽象的な役割名ではなく、resultを実際に受け取る主体を明示することが必要だった。

## KPI

| 指標 | Candidate147 | Candidate245 | Candidate246 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 337,752 | 183,187 | +32,017（+21.18%） |
| elapsed中央値 | 91.431秒 | 85.376秒 | 74.342秒 | -17.089秒（-18.69%） |

Candidate246のtoken中央値はCandidate245より154,565（45.76%）少なく、elapsed中央値も11.034秒（12.92%）短い。ただしC147のtoken水準には届いていない。

## 状態

`f04_n5_completed / quality_passed / mechanism_passed_5_of_5 / targeted_passed / cost_not_reduced / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](01453868f25c4013bce7813a14ab1bb9.json)、[品質監査](candidate246-validation-result-ai-return-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate246-validation-result-ai-return-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。
