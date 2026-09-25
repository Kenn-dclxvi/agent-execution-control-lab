# Candidate276 Standard14 GPT-6 Luna Medium（2026-09-25）

Candidate276をGPT-6 Luna・reasoning `medium`でStandard14各5回、計70件実行した。70件すべて実行・採点でき、除外は0件。全70件の採点分布はScore 4が68件、Score 1が1件、Score 0が1件だった。N=5比較用に固定選択された70件の品質中央値は100.00点、全エージェントトークン中央値は2,330,083、経過時間中央値は681.60秒。

保存済みControl-Free GPT-6 Luna Mediumと同じ互換条件・実行層で比較した。選択サンプルの中央値は、品質が92.86点から100.00点へ7.14ポイント高く、トークンは179,467（7.15%）少なく、経過時間は31.91秒（4.47%）短かった。この結果は今回の固定Standard14・Luna Medium条件での観測であり、一般的な因果効果や採用判断を示さない。

| 指標 | Control-Free Medium | Candidate276 Medium | 差 |
| --- | ---: | ---: | ---: |
| 品質中央値（0–100） | 92.86 | 100.00 | +7.14ポイント |
| 全エージェントトークン中央値 | 2,509,550 | 2,330,083 | -179,467（-7.15%） |
| 経過時間中央値 | 713.51秒 | 681.60秒 | -31.91秒（-4.47%） |

品質監査上の診断値は、command protocol違反0件、owner / producer evidence不適格55件。これら診断値はRating v14の得点へ加算・減算していない。

- Candidate276 [登録result](candidate276-execution-control-luna6-medium-standard14-n5-cli0156_2026-09-25.json) ID: `5236bce8e4bb429bb94eff10db07184f`
- Candidate276 result SHA-256: `6e2b21ca1b7918668f3bc62d5ee527ade98d5c59462ade435d21e9700d334cc0`
- Compatibility key: `d0faab551226ab7ab360a30ebc8dcc46ec8c303187705796ee66769b484c2464`
- 実行前preflight: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate276-luna6-medium-standard14-n5-20260925-r1/batch-002/preflight-receipt.json`。最初のtemplateにFree側のbundle hashが残っていたため、その70試行は評価へ含めず、修正後のpreflightを通した70件だけを採点・登録した。
- 詳細な全70件採点: [quality audit](candidate276-execution-control-luna6-medium-standard14-n5-quality-audit-r1_2026-09-25.json)
- 保存済みControl-Free比較: [comparison view](candidate276-control-free-comparison-luna6-medium-standard14-n5_2026-09-25.json)
- 生の実行証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate276-luna6-medium-standard14-n5-20260925-r1`
