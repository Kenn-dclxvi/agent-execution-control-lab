# Candidate275（4文版）Standard14 N=5 GPT-6 Sol Medium（2026-09-24）

Candidate275をGPT-6 Sol、reasoning mediumでStandard14の14ケース各5回、計70 run計測した。70件すべて有効・採点可能で、除外attemptは0件だった。

| 指標 | 結果 |
| --- | ---: |
| Score 4 / Score 2 | 69 / 1 |
| 品質スコア中央値 | 100.00% |
| 全エージェントトークン中央値 | 2,444,384 |
| 総所要時間中央値 | 776.91秒 |

Score 2の1件は`TC-F10-MONTHLY-FORMAT-TEST-REVIEW`で、review findingに必要なseverity、対象path、誤binding、またはCLI影響が不足した。ほかの69件はScore 4だった。

保存済みの[Control-Free GPT-6 Sol Medium result](a26f63cd6a1b497ba5fa37ee0b35d370.json)と互換キー`2298346c3f5a78792a712d1dc5162ba88e90af5d89bc31d08d3fa4a97403116d`が一致した。Control-FreeはScore 4が65 / 70件、品質中央値92.86%、トークン中央値2,894,385、総所要時間中央値813.13秒。今回の固定試験でCandidate275はトークンが15.55%少なく、総所要時間が4.45%短かった。N=5の観測値であり、未評価条件での効果は示さない。

## 固定条件と証拠

- プロンプト: `the-caption-3ce91a4-four-verified-lines-ablation-r1`、bundle SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`
- [プロファイル](../profiles/four-verified-lines-ablation-sol6-medium-standard14-n5-cli0156-r1.json): GPT-6 Sol / medium、CLI 0.156.1、Rating v14、並列上限24
- 基準result: `a26f63cd6a1b497ba5fa37ee0b35d370`
- 登録result: `3ac998f726ee46a08c00b50f7a890518`、content SHA-256 `3d23a6c92f69a1a5414d87c2bad5bda92519dafbc19e45bbd19033d8b5a99589`
- [登録JSON](four-verified-lines-ablation-sol6-medium-standard14-n5-cli0156_2026-09-24.json)、[品質監査](four-verified-lines-ablation-sol6-medium-standard14-n5-quality-audit-r1.json)
- 事前照合と実行証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-sol6-medium-standard14-n5-20260924-r1`。実行前に70 slotを許可したreceiptは`cycle/layer1/comparison-preflight.json`、seal済み証拠は`compact/execution-evidence.tar.zst`に保存した。

採用、release、本体反映の判断はこの計測には含めない。
