# Candidate275 Standard14 GPT-6計測の集約（2026-09-24）

同一のCandidate275（4文版）をGPT-6 Luna、Sol、Astraで計測したStandard14 N=5の記録を集約した。6条件はいずれもCLI 0.156.1、固定Standard14、14ケース×5回である。プロンプトbundleは全条件で同一（SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`）。各条件の一次resultと個別記録を参照元として保持する。

条件ごとの登録result ID、採点分布、usage内訳、単価、換算額を含む[機械可読集約](candidate275-standard14-model-reasoning-summary_2026-09-24.json)も保存した。

| モデル / 推論 | Score 4 | 全エージェントtoken中央値 | 総所要時間中央値 | 入力token合計（キャッシュ分） | 出力token合計 | API費用目安 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Luna High | 69 / 70（訂正反映後70 / 70） | 2,448,245 | 937.95秒 | 12,034,658（10,635,776） | 155,525 | $0.32 |
| GPT-6 Luna xHigh | 70 / 70 | 2,716,023 | 1,560.93秒 | 13,281,394（11,650,560） | 297,487 | $0.43 |
| GPT-6 Luna Max | 70 / 70 | 2,737,921 | 1,717.13秒 | 13,649,236（11,964,672） | 351,332 | $0.46 |
| GPT-6 Sol Low | 68 / 70 | 2,163,785 | 603.17秒 | 10,639,546（9,464,192） | 73,280 | $4.98 |
| GPT-6 Sol Medium | 69 / 70 | 2,444,384 | 776.91秒 | 11,904,900（10,682,752） | 107,260 | $5.65 |
| GPT-6 Astra Low | 70 / 70 | 1,772,618 | 669.08秒 | 8,820,103（7,700,992） | 63,800 | $22.08 |

全条件の品質スコア中央値は100.00%、各70件は有効で除外0件だった。Sol LowのScore 2は2件、Sol Mediumは1件で、いずれもF10月次レビューのfinding情報不足だった。Luna Highは登録result上でScore 3が1件残るが、別途保存された採点訂正を反映すると70件すべてScore 4になる。元のwrite-once resultは変更していない。

## トークンと費用の算出

入出力tokenは各条件の70 runに含まれる全エージェントusage記録を合算した。括弧内のキャッシュ入力tokenは入力合計の内数であり、費用計算では通常入力tokenと分けた。費用は[OpenAI API標準料金](https://developers.openai.com/api/docs/pricing)の短文脈単価を使用し、モデルごとに非キャッシュ入力・キャッシュ入力・出力へ単価を適用した。cache writeは全条件で0件。表示額は条件ごとの70 run合計を米ドルで丸めた目安であり、Codex CLI利用分の実請求額ではない。個別要求で入力が272K tokenを超える場合の長文脈料金も、run単位の要求内訳を特定できないため含めていない。

全6条件を単純合算すると入力70,329,837 token（うちキャッシュ62,098,944）、出力1,048,684 token、API標準料金換算約$33.93となる。この合算額は6条件全体の費用換算用であり、各条件の比較指標ではない。

## 元の計測記録

- [GPT-6 Luna High](four-verified-lines-ablation-luna6-high-standard14-n5-cli0156_2026-09-24.md) — 登録result、採点訂正、条件別証跡を記載。
- [GPT-6 Luna xHigh](four-verified-lines-ablation-luna6-xhigh-standard14-n5-cli0156_2026-09-24.md)
- [GPT-6 Luna Max](four-verified-lines-ablation-luna6-max-standard14-n5-cli0156_2026-09-24.md)
- [GPT-6 Sol Low](four-verified-lines-ablation-sol6-low-standard14-n5-cli0156_2026-09-24.md)
- [GPT-6 Sol Medium](four-verified-lines-ablation-sol6-medium-standard14-n5-cli0156_2026-09-24.md)
- [GPT-6 Astra Low](four-verified-lines-ablation-astra6-low-standard14-n5-cli0156_2026-09-24.md)

モデルと推論設定が異なる条件をまとめた記録であり、表の差をモデルまたは推論設定単独の因果効果とは解釈しない。採用、release、本体反映もこの集約記録では判断しない。
