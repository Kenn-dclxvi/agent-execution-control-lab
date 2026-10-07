# C280のClaude Code Sonnet 5.5 low・Standard14 N=5計測（2026-10-08）

2026-10-08。利用者の指示で、C280をSonnet 5.5（`claude-sonnet-5-5`）の推論設定`low`で、全14ケース各5回、計70件測った。Sonnet 5.5で測った保存済みの結果はなく、比較相手を持たない単独の計測である。**有効70件すべてが4点だった。品質中央値100、全エージェントトークン中央値832,616、経過時間中央値297.94秒。** 除外と再試行は0件だった。

## 条件

[C280 Opus 5.5 lowのプロファイル](../profiles/c280-claude-opus55-low-standard14-n5-cli2288-r1.json)から、次の点を変えた（[今回のプロファイル](../profiles/c280-claude-sonnet55-low-standard14-n5-cli2288-r1.json)）。

- モデルを`claude-sonnet-5-5`にした。全runで、使われたモデルが`claude-sonnet-5-5`だけであることを確かめた。
- 評価コードは、`main`のコミット`c18d183`のものを使った。比較条件に記録する評価コードのSHA-256も、このコードから計算した。C280 Opus lowは`1b63a42`のコードで測っている。
- 発行方式は、実際に使った`wave_barrier`をプロファイルに記録した。C280 Opus lowのプロファイルは`global_queue`と記載していたが、実際の発行は同じ`wave_barrier`である。

Claude Code 2.1.288、推論設定`low`、権限、ツール、プラグイン一覧、採点契約、ケース、fixture、TaskSpecは、C280 Opus lowと同じである。評価セットとfixtureは、C280で固定したLayer 1を写して使った。発行前に1回だけ実際に起動し、起動時の環境がプロファイルと一致することを確かめた（[発行前の記録](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08-preflight.json)）。日本時間2026-10-08 05:07:55〜05:11:30に実行した。

C280のidentityは`the-caption-3ce91a4-execution-control-outcome-binding-r1`、bundle SHA-256は`cac81e81eb5d66582a119042b034c457a1b2415fb6959ce2d03bcd0250fc5ea0`である。

## 結果

| 条件 | 4点 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: | ---: |
| C280 Sonnet 5.5 low（今回） | 70 / 70 | 100.00 | 832,616 | 297.94秒 |

中央値は、14ケースを合算した各反復の値を5回分集計した値である。反復ごとの合計は、トークンが797,727〜930,027、経過時間が288.0〜423.9秒だった。経過時間は反復1と2（411.1秒、423.9秒）が反復3〜5（288.0〜297.9秒）より長かった。発行は14件ずつの波を順に待つ方式であり、この差の原因は分解していない。

参考として、[C280 Opus 5.5 low](claude-opus55-low-c280-standard14-n5-cli2288_2026-10-08.md)はトークン中央値719,243、経過時間中央値270.93秒だった。ただし、モデルが違うので、両者の差はプロンプトの効果として扱わない。評価コードの版も異なる。

## 機序の診断

[診断](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08-mechanism-diagnostics.json)は、C280 Opus lowと同じ抽出で集計した。

| 条件 | ルートの本文がツール出力に現れたrun | `src`の本文 | `tests`の本文 | 検証の呼び出し | 失敗した呼び出し | 終了コードのずれの候補 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C280 Sonnet low | 4 / 70 | 11 | 0 | 76 | 1 | 0 |

失敗した検証の呼び出し1件も、品質は4点だった。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- [登録結果](c84fd22753d248e588e586cb8022ea1e.json)・[品質監査](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08-quality-audit.json)
- [発行前の記録](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08-preflight.json)・[機序の診断](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08-mechanism-diagnostics.json)
