# Candidate276 Standard14 GPT-6 Sol Low（2026-09-26）

Candidate276をGPT-6 Sol・reasoning `low`でStandard14各5回、計70件実行した。70件すべて実行・採点でき、除外は0件だった。全70件の採点分布はScore 4が66件、Score 2が3件、Score 0が1件。N=5比較用に固定選択された70件の品質中央値は96.43点、全エージェントトークン中央値は2,171,991、経過時間中央値は633.49秒。

保存済みControl-Free GPT-6 Sol Lowと同じ互換条件・実行層で比較した。選択サンプルの中央値は、品質が92.86点から96.43点へ+3.57ポイント、トークンは-344,974（-13.71%）、経過時間は+15.62秒（+2.53%）だった。この数値は固定Standard14・Sol Low条件での観測であり、一般的な効果や採用判断を示さない。

| 指標 | Control-Free Low | Candidate276 Low | 差 |
| --- | ---: | ---: | ---: |
| 品質中央値（0–100） | 92.86 | 96.43 | +3.57ポイント |
| 全エージェントトークン中央値 | 2,516,965 | 2,171,991 | -344,974（-13.71%） |
| 経過時間中央値 | 617.87秒 | 633.49秒 | +15.62秒（+2.53%） |

品質監査の診断値は、command protocol違反0件、owner / producer evidence不適格55件。これらの診断値はRating v14の得点へ加算・減算していない。

- Candidate276登録result ID: `8a1160d8419c4c20ae2809a2af1b54f4`。Compatibility key: `7d28e37b39852da8633180a8639d377188521fdda06edcf219e423ba1cd346a8`。
- 実行前preflight receiptは`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate276-sol6-low-medium-standard14-n5-cli0156-20260926-r1/batch-002/preflight-receipt.json`。Low・Medium両方で140枠を事前照合し、修正版batch-002の140件が有効、除外0件だった。 初回batchの140呼出しはControl-Free側のbundle情報が残っていて実行前に拒否され、resultには含めていない。
- 詳細な全70件採点: [quality audit](candidate276-execution-control-sol6-low-standard14-n5-quality-audit-r1_2026-09-26.json)
- 保存済みControl-Freeとの比較: [comparison view](candidate276-control-free-comparison-sol6-low-standard14-n5_2026-09-26.json)
- ケース別比較: [内訳](candidate276-control-free-case-breakdown-sol6-low-standard14-n5_2026-09-26.json)
- 固定条件、実行および採点の証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate276-sol6-low-medium-standard14-n5-cli0156-20260926-r1`
