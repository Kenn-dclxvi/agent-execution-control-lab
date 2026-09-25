# Candidate275（4文版）Standard14 N=5 GPT-6 Sol Low（2026-09-24）

Candidate275をGPT-6 Sol、reasoning lowでStandard14の14ケース各5回、計70 run計測した。70件すべて有効・採点可能で、除外attemptは0件だった。

| 指標 | 結果 |
| --- | ---: |
| Score 4 / Score 2 | 68 / 2 |
| 品質スコア中央値 | 100.00% |
| 全エージェントトークン中央値 | 2,163,785 |
| 総所要時間中央値 | 603.17秒 |

Score 2の2件はともに`TC-F10-MONTHLY-FORMAT-TEST-REVIEW`で、review findingに必要なseverity、対象path、誤binding、またはCLI影響が不足した。ほかの68件はScore 4だった。

保存済みの[Control-Free GPT-6 Sol Low result](d141469e2cdd48bda75f1772a285ee0a.json)と互換キー`7d28e37b39852da8633180a8639d377188521fdda06edcf219e423ba1cd346a8`が一致した。Control-FreeはScore 4が65 / 70件、品質中央値92.86%、トークン中央値2,516,965、総所要時間中央値617.87秒。今回の固定試験でCandidate275はトークンが14.03%少なく、総所要時間が2.38%短かった。N=5の観測値であり、未評価条件での効果は示さない。

## 固定条件と証拠

- プロンプト: `the-caption-3ce91a4-four-verified-lines-ablation-r1`、bundle SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`
- [プロファイル](../profiles/four-verified-lines-ablation-sol6-low-standard14-n5-cli0156-r1.json): GPT-6 Sol / low、CLI 0.156.1、Rating v14、並列上限24
- 基準result: `d141469e2cdd48bda75f1772a285ee0a`
- 登録result: `a59674094efe4d5e9063b58b533f7408`、content SHA-256 `3e8b2873f43b29e14fce387b0ec54296acf5d3f5705d3824cfe6efa83de383b2`
- [登録JSON](four-verified-lines-ablation-sol6-low-standard14-n5-cli0156_2026-09-24.json)、[品質監査](four-verified-lines-ablation-sol6-low-standard14-n5-quality-audit-r1.json)
- 事前照合と実行証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-sol6-low-standard14-n5-20260924-r1`。実行前に70 slotを許可したreceiptは`cycle/layer1/comparison-preflight.json`、seal済み証拠は`compact/execution-evidence.tar.zst`に保存した。

採用、release、本体反映の判断はこの計測には含めない。
