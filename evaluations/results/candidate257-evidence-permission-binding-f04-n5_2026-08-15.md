# Candidate257 必要判定・観測値・resultの発行permission対応 F04 N=5

## 結論

Candidate257はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。

しかし、開始確認と必要readの共同発行、影響しない複数確認の同一model step発行、発行前の必要判定を確定できない調査の排除、required validationの単一発行判断は、すべて0 / 5件だった。全runが最初の`App.tsx` readのresultを受け取ってから続きのreadを発行し、required validationも`npm ci`、`npm run lint`、`npm run build`を三つのtool callへ分けた。

総使用token中央値は`170,598`で、Candidate147の`151,170`より19,428（12.85%）、Candidate254の`147,796`より22,802（15.43%）多い。Candidate256の`172,998`より2,400（1.39%）少ないが、機序不成立を覆さない。`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-evidence-permission-binding-r1`
- bundle SHA-256: `73f671c8a9b83b411c5187382b1d937ed765536ae9692856f48518b52a46d03a`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate254
- not inherited: Candidate255、Candidate256
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate257 result: `9245a0ebaae9449aa13222d5e5c53d54`

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| 開始確認と必要readの共同発行 | 0 / 5 |
| 影響しない複数確認を別stepへ分けなかった | 0 / 5 |
| 発行前の必要判定を一回で確定できない調査を発行しなかった | 0 / 5 |
| required validationの単一発行判断 | 0 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |

## KPI

| 指標 | Candidate147 | Candidate254 | Candidate256 | Candidate257 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 147,796 | 172,998 | 170,598 | +19,428（+12.85%） |
| elapsed中央値 | 91.431秒 | 73.572秒 | 75.796秒 | 79.796秒 | -11.635秒（-12.73%） |

## C147との差

C147は`evidence_consumer_ready`を発行permissionの条件にしているが、Candidate257はその関係を自然文に置換しただけでは、最初のreadが必要判定を確定できるかという境界として実行されなかった。さらに、`EVIDENCE_GATE`冒頭を置換した影響が開始共同発行と検証の境界へ波及し、Candidate254で残っていた成立経路まで失われた。

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_0_of_5 / independent_check_boundary_passed_0_of_5 / evidence_permission_binding_passed_0_of_5 / validation_mechanism_passed_0_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](9245a0ebaae9449aa13222d5e5c53d54.json)、[品質監査](candidate257-evidence-permission-binding-f04-n5-quality-audit-r1.json)、[機序監査](candidate257-evidence-permission-binding-f04-n5-mechanism-audit-r1.json)を一次証拠とする。
