# GPT-6 Free・C274主要条件の統合比較（2026-09-24）

GPT-6 Astra Low、GPT-6 Sol Medium、GPT-6 Luna Highについて、同一モデル・推論設定のFreeとC274を対にして整理した。GPT-5.6 Sol MediumのFree結果も従来比較との接続用に記載する。各条件はStandard14の14ケースを5反復、計70件である。全条件で70件が有効、除外0件だった。

## Free

| モデル / 推論 | Score 4 / 0 | 入力token中央値 | 出力token中央値 | 全agent token中央値 | 総所要時間中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Astra / low | 70 / 0 | 2,020,189 | 13,567 | 2,033,901 | 777.51秒 |
| GPT-6 Sol / medium | 65 / 5 | 2,870,088 | 24,297 | 2,894,385 | 813.13秒 |
| GPT-6 Luna / high | 65 / 5 | 3,104,244 | 37,160 | 3,141,404 | 1,043.65秒 |
| GPT-5.6 Sol / medium | 65 / 5 | 3,695,723 | 40,514 | 3,734,191 | 1,777.42秒 |

各反復の14ケースを合算し、その5反復の中央値を表示した。入力・出力の中央値も反復ごとに合算した後、それぞれ個別に中央値を求めている。GPT-5.6 Sol Mediumは2026-09-04のFree結果で、参考として含めた。

## C274

| モデル / 推論 | Score 4 / 0 | 入力token中央値 | 出力token中央値 | 全agent token中央値 | 総所要時間中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-6 Astra / low | 70 / 0 | 未記録 | 未記録 | 1,474,356 | 631.48秒 |
| GPT-6 Sol / medium | 70 / 0 | 1,789,594 | 20,281 | 1,809,875 | 681.90秒 |
| GPT-6 Luna / high | 70 / 0 | 1,768,213 | 40,173 | 1,808,386 | 975.93秒 |

Astra C274の登録記録には総tokenはあるが、入力・出力の内訳がないため「未記録」とした。

| モデル / 推論 | C274のFree比：token中央値 | C274のFree比：時間中央値 | Score 4件数の変化 |
| --- | ---: | ---: | ---: |
| GPT-6 Astra / low | −27.51% | −18.78% | 70 → 70 |
| GPT-6 Sol / medium | −37.47% | −16.14% | 65 → 70 |
| GPT-6 Luna / high | −42.43% | −6.49% | 65 → 70 |

この3組はそれぞれの組内で互換条件が一致し、prompt identityが比較対象である。各組はStandard14、Rating v14、全agent token accounting v1を用いる。モデル・推論設定をまたいだ差は同一条件比較ではない。

## API通常料金による参考換算

下表の費用は各条件70件分の全入力・出力tokenを合算し、キャッシュ入力の割引を使わず通常入力単価で計算した推定値である。実際のCodex Free請求額ではない。評価の価格換算はStandard短文脈の価格を使う。2026-09-24確認の料金は、GPT-6 Astraが入力/出力$10/$50、GPT-6 Solが$2/$10、GPT-6 Lunaが$0.10/$0.50、GPT-5.6 Solが$4/$20（いずれも100万token当たり）。GPT-5.6 Solは公式掲載の期間限定価格で、少なくとも2026-11-21まで適用予定とされている（[OpenAI API公式価格表](https://developers.openai.com/api/docs/pricing)）。

### Free

| 対象条件 | 品質点 / 280 | 推定費用（70件） | 品質点 / US$ |
| --- | ---: | ---: | ---: |
| GPT-6 Luna High | 260 | $1.7103 | 152.02 |
| GPT-6 Sol Medium | 260 | $29.8646 | 8.71 |
| GPT-5.6 Sol Medium | 260 | $77.9621 | 3.33 |
| GPT-6 Astra Low | 280 | $107.5424 | 2.60 |

### C274

| 対象条件 | 品質点 / 280 | 推定費用（70件） | 品質点 / US$ |
| --- | ---: | ---: | ---: |
| GPT-6 Luna High | 280 | $0.9846 | 284.37 |
| GPT-6 Sol Medium | 280 | $18.6049 | 15.05 |
| GPT-6 Astra Low | 280 | 算出不可 | — |

各表の順位は、それぞれの条件内での参考値である。Astra C274は入力・出力内訳がないため費用を算出できない。API料金を使った試算であり、実際の請求額、短文脈を超える入力の費用、個別ツール料金を表すものではない。

費用計算に用いた70件合計の入力・出力tokenは次のとおり。金額は`(input × 入力単価 + output × 出力単価) ÷ 1,000,000`で求めた。Astra C274は合計内訳も保存されていない。

### Free

| 条件 | 入力token合計 | 出力token合計 |
| --- | ---: | ---: |
| GPT-6 Astra Low | 10,406,887 | 69,470 |
| GPT-6 Sol Medium | 14,322,312 | 122,000 |
| GPT-6 Luna High | 16,135,258 | 193,618 |
| GPT-5.6 Sol Medium | 18,468,544 | 204,395 |

### C274

| 条件 | 入力token合計 | 出力token合計 |
| --- | ---: | ---: |
| GPT-6 Sol Medium | 8,784,611 | 103,572 |
| GPT-6 Luna High | 8,854,709 | 198,318 |
| GPT-6 Astra Low | 未記録 | 未記録 |

## 解釈の範囲

C274では3組すべてで総token中央値と総所要時間中央値が下がった。AstraはFreeでも70件すべてScore 4で、品質件数の差はなかった。SolとLunaではFreeのScore 0が各5件だったのに対し、C274では全件Score 4となった。固定された70件内の観測であり、別の課題や運用条件でも再現するとは限らない。

GPT-5.6 Sol MediumはFreeのみ記載する。2026-09-04、Codex CLI 0.153.3の70件でScore 4が65件、Score 0が5件、全agent token中央値3,734,191、総所要時間中央値1,777.42秒だった。この条件と対になるC274結果は登録済み資料で確認できなかったため、GPT-5.6とのC274効果や他モデルとのモデル単独差は主張しない。9月24日のGPT-6 Sol/Luna結果はCodex CLI 0.156.1であり、Astraや5.6 Solの結果は実施日・CLI版も異なるため、モデル横断の数値は記述比較に限る。

## 一次結果と計測記録

- Free全モデルのtoken内訳・価格表：[Control-Freeモデル比較](control-free-model-reasoning-comparison_2026-09-24.md)
- GPT-6 Astra Low C274：[登録result](441d4233560c47f089a2938935aa8d19.json)、[推論設定間比較](candidate274-astra-low-medium-high-xhigh-standard14-n5_2026-09-08.md)
- GPT-6 Sol Medium Free：[登録result](a26f63cd6a1b497ba5fa37ee0b35d370.json)
- GPT-6 Sol Medium C274：[登録result](7a1e38da9ccb4269b37b26ff9d18df32.json)、[計測記録](candidate274-sol6-medium-standard14-n5-cli0156_2026-09-24.md)
- GPT-6 Luna High Free/C274：[登録resultと費用内訳](candidate147-candidate274-luna6-high-standard14-n5-cli0156_2026-09-24.md)
- GPT-5.6 Sol Medium Free：[登録result](d5fcd68143a94c9e8df7d988c5eba8a2.json)
