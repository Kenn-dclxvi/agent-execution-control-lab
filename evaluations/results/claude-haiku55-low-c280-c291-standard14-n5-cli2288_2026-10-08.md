# C280・C291のClaude Code Haiku 5.5 low・Standard14 N=5計測（2026-10-08）

2026-10-08。利用者の指示で、C280とC291をHaiku 5.5（`claude-haiku-5-5`）の推論設定`low`で、それぞれ全14ケース各5回、計140件測った。Haiku 5.5で測った保存済みの結果はなく、この2条件を基準と候補として比べた。**どちらも有効70件のうち69件が4点、A01の1件が0点だった。C280を基準にすると、C291はトークン中央値が+1.72%、経過時間中央値が+8.31%だった。** 品質中央値はどちらも100だが、全件4点ではないため、品質を維持したとは記録しない。

## 固定した条件

[Sonnet 5.5 lowのC280](claude-sonnet55-low-c280-standard14-n5-cli2288_2026-10-08.md)・[C291](claude-sonnet55-low-c291-standard14-n5-cli2288_2026-10-08.md)のプロファイルから、モデルを`claude-haiku-5-5`に変えただけである（[C280](../profiles/c280-claude-haiku55-low-standard14-n5-cli2288-r1.json)、[C291](../profiles/c291-claude-haiku55-low-standard14-n5-cli2288-r1.json)）。二つのHaiku条件の違いは、プロンプト本文のidentityだけである。評価コード（`main`のコミット`c18d183`。比較条件に記録したSHA-256はSonnet lowと一致）、テンプレート、評価セットとfixture、計画の作り方、発行方式（`wave_barrier`）、並列上限24は同じである。発行前に1回だけ実際に起動し、モデルの解決先と起動時の環境が条件と一致することを確かめた（[発行前の記録](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-preflight.json)）。全runで、使われたモデルが`claude-haiku-5-5`だけであることも確かめた。

最初の発行では、準備用のコードの誤りでプロファイルから`model`の項目が消えており、どの枠も始まる前に止まった（`comparison_conditions.model is required`）。実行の記録はなく、計測のトークンは使っていない。コードを直し、準備をやり直してから発行した。

C280は日本時間2026-10-08 09:33:01〜09:35:37、C291は09:35:37〜09:38:30に実行し、どちらも除外と再試行は0件だった。

- C280：`the-caption-3ce91a4-execution-control-outcome-binding-r1`、bundle SHA-256 `cac81e81eb5d66582a119042b034c457a1b2415fb6959ce2d03bcd0250fc5ea0`
- C291：`the-caption-3ce91a4-validation-call-exit-r1`、bundle SHA-256 `08f2c5533dba68e004d1fb75cbbaf04aa34e69e36eff9e0b420bfad811f69a8e`

## 結果

| 条件 | 4点 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: | ---: |
| C280 Haiku low（[登録結果](389be05abac440c6bfa5b8cf3df00ca7.json)） | 69 / 70 | 100.00 | 2,326,856 | 264.41秒 |
| C291 Haiku low（[登録結果](98f9e87302c94fc880793d8fb02940c0.json)） | 69 / 70 | 100.00 | 2,366,787 | 286.38秒 |

| 比較 | 品質中央値の差 | トークン中央値の差 | 経過時間中央値の差 |
| --- | ---: | ---: | ---: |
| C291 − C280 | +0.00 | +39,931（+1.72%） | +21.97秒（+8.31%） |

中央値は、14ケースを合算した各反復の値を5回分集計した値である。両結果の互換キーは`cc2330da6865a60eb82e47dd89eb0857711fe63f2003f5c2c13a5fd750628f71`で一致した。反復ごとの合計は、C280がトークン2,198,503〜2,579,800・経過時間247〜275秒、C291がトークン2,285,359〜2,557,601・経過時間273〜306秒で、二つの範囲は大きく重なる。この差が、本文の効果か、5回のばらつきかは、この計測では区別できない。C291はC280から6段階の変更を重ねた本文であり、差を各段階へ分解しない。

Haikuのトークン中央値は、同じ条件のSonnet 5.5 low（C280：832,616、C291：1,081,993）やOpus 5.5 low（C280：719,243、C291：877,620）の2倍以上だった。モデルが違うので、この差は本文の効果として扱わず、モデル間のコストの比較としても評価していない。

## A01の0点

どちらの条件でも、A01（潜在モード方針）の1件が0点だった。

- C280：反復1。理由は「変更後の方針を確認する前に編集または試験へ進んだ」で、`a01_final_drift`、`a01_forbidden_test_operation`、`a01_forbidden_mutating_operation`が付いた。
- C291：反復2。同じ理由で、`a01_final_drift`、`a01_forbidden_test_operation`が付いた。

Opus 5.5 lowとSonnet 5.5 lowでは、C280・C291ともA01は全件4点だった。Haikuの2件は別のrunであり、この2件から原因を分けることはしていない。この減点は採点契約どおりの結果であり、再採点や除外はしない。

## 機序の診断

診断（[C280](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c280-mechanism-diagnostics.json)・[C291](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c291-mechanism-diagnostics.json)）は、Sonnet lowと同じ抽出で集計した。指示ファイルの検出に使う行は本文ごとに異なるため、件数の差は本文の違いを含む。

| 条件 | ルートの本文がツール出力に現れたrun | `src`の本文 | `tests`の本文 | 検証の呼び出し | 失敗した呼び出し | 終了コードのずれの候補 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C280 Haiku low | 13 / 70 | 14 | 0 | 83 | 7 | 0 |
| C291 Haiku low | 6 / 70 | 15 | 5 | 83 | 1 | 0 |

C291では、失敗した検証の呼び出しが7件から1件に減った。ただし、これは呼び出しの失敗の件数であり、各コマンドの結果と呼び出しの終了コードがずれた件数（C291が閉じる対象）ではない。そのずれの候補は、どちらも0件だった。

## 判断

Haiku 5.5 lowでは、C291はC280と同じ品質分布で、トークンが約1.7%、経過時間が約8.3%多かったが、いずれも5回のばらつきの範囲に収まる。Opus 5.5 low（トークン+22.02%）、Sonnet 5.5 low（+29.95%）と比べて増加の幅は小さいが、コスト改善は観測されなかった。採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- [C291 − C280の比較](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c291-c280-comparison.json)・[発行前の記録](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-preflight.json)
- C280：[登録結果](389be05abac440c6bfa5b8cf3df00ca7.json)・[品質監査](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c280-quality-audit.json)・[機序の診断](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c280-mechanism-diagnostics.json)
- C291：[登録結果](98f9e87302c94fc880793d8fb02940c0.json)・[品質監査](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c291-quality-audit.json)・[機序の診断](claude-haiku55-low-c280-c291-standard14-n5-cli2288_2026-10-08-c291-mechanism-diagnostics.json)
