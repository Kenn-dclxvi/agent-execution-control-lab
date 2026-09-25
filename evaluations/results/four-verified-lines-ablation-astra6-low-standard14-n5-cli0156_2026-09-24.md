# Candidate275 Standard14 N=5 GPT-6 Astra Low（2026-09-24）

CLI 0.156.1、Candidate275、GPT-6 Astra、reasoning lowで、Standard14の14ケースを各5回、計70件計測した。70件すべて有効・採点可能で、全件Score 4、除外・再試行は0件だった。

| 指標 | 結果 |
| --- | ---: |
| Score 4 | 70 / 70件 |
| 品質スコア中央値 | 100.00% |
| 全エージェントトークン中央値 | 1,772,618 |
| 総所要時間中央値 | 669.08秒 |

トークンと総所要時間は、各反復の14ケース合計を求めた後、5反復の中央値を指標ごとに算出した。並列実行全体の壁時計時間は160.40秒で、この合計時間とは異なる。

## 入出力トークンとAPI費用の目安

70 runのCodex usage記録を合算すると、入力は8,820,103 token（うちキャッシュ入力7,700,992、非キャッシュ入力1,119,111）、出力は63,800 token、cache writeは0 tokenだった。これは各runの合計であり、上表の「全エージェントトークン中央値」とは集計単位が異なる。

[OpenAI APIの標準料金](https://developers.openai.com/api/docs/pricing)にあるGPT-6 Astraの短文脈単価（入力 $10 / 100万token、キャッシュ入力 $1 / 100万token、出力 $50 / 100万token）を当てはめると、API費用は合計 **約 $22.08**（入力 $18.89、出力 $3.19）、1 runあたり平均 **約 $0.32** の目安となる。Codex CLIでの実行はAPI直接利用ではないため、これは実請求額ではなく、記録された入出力数と公開単価からの換算値である。キャッシュ入力を割引扱いせず通常入力単価で計算した場合は約 $91.39。

## 固定条件と証拠

- [プロファイル](../profiles/four-verified-lines-ablation-astra6-low-standard14-n5-cli0156-r1.json): CLI 0.156.1、GPT-6 Astra / low、Standard14 N=5、Rating v14、並列上限24
- プロンプト: `the-caption-3ce91a4-four-verified-lines-ablation-r1`、bundle SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`
- 今日のC275計測から固定ケース、fixture、TaskSpecを再利用し、指定条件の独立計測として実施した。
- 登録result: `a1cd9cadd61b43bb8ad13cc2b4a65f2f`、content SHA-256 `9a30ee765b8b08310063292f93133cfbd5c2e8531e7eec35ebcb92d9a209f143`
- [登録JSON](four-verified-lines-ablation-astra6-low-standard14-n5-cli0156_2026-09-24.json)、[品質監査](four-verified-lines-ablation-astra6-low-standard14-n5-quality-audit-r1.json)
- 実行条件の確認記録: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-astra6-low-standard14-n5-cli0156-20260924-r1/measurement-preflight.json`
- 実行証拠: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/four-verified-lines-astra6-low-standard14-n5-cli0156-20260924-r1/cycle`。圧縮・検証済み証拠は`compact/execution-evidence.tar.zst`に保存した。

採用、release、本体反映の判断はこの計測には含めない。
