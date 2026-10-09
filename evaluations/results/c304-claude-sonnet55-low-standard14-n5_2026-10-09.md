# C304のSonnet 5.5 low、Standard14 N=5（2026-10-09）

2026-10-09。[C304](../../docs/candidate304-c301-file-read-line-cap-design.md)（C301へ「1回のツール呼び出しで、一つのファイルの本文を300行を超えて受け取らない。」を加えたもの）を、利用者の指示でSonnet lowだけ測った。Solは、Sonnet lowの結果を見て測る価値を判断する。計測は2回行った。

- **1回目（Sonnetだけ、本数の上限24）：** 70件すべて4点。Sonnetの同時実行が平均21.6本になり、基準のC301（Solと一緒に流し、Sonnetは平均7.6本）とマシンの負荷が違った。待ち行列に入れるセルの組み合わせは比較条件に入っておらず、発行前の確認で検出できなかった。発行した後に分かった違いであり、この計測はC301と比べない。
- **2回目（負荷を見て始める条件）：** 70件すべて4点。[発行の条件の試行](c301-sonnet55-low-load-admission-trials_2026-10-09.md)で決めた条件（CPU使用率70%以下、間隔1秒）で、同じ条件のC301（`-r5`）と比べた。**費用−1.20%、経過時間−1.54%で、どちらも基準の幅の中だった。**

## 2回目：基準C301（`-r5`）との比較

| 指標 | C301 `-r5`の中央値（幅） | C304の中央値（幅） | 差（%） | 基準の幅に対する位置 |
| --- | ---: | ---: | ---: | --- |
| 品質（0〜100） | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | +0.00% | 幅の中 |
| 費用（USD） | 0.6811（0.6634〜0.6938） | 0.6729（0.6624〜0.7079） | −1.20% | 幅の中 |
| 経過時間（秒） | 286.68（269.85〜343.71） | 282.28（275.82〜316.06） | −1.54% | 幅の中 |
| 生のトークン（参考） | 822,676（801,774〜857,412） | 842,809（828,853〜886,772） | +2.45% | 幅の中 |

プロファイル：[C304 `-r2`](../profiles/c304-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r2.json)。C301 `-r5`とは、prompt identityとプロファイル名だけが違う。比較は`compare-analyses`による（[記録](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-c301-r5-comparison.json)）。

経過時間の内訳（1反復あたりの中央値）は、C301 `-r5`がモデルの応答225.5秒・コマンドの実行22.7秒、C304が224.1秒・22.5秒だった（[診断の記録](c301-c304-sonnet-dispatch-load-diagnostics_2026-10-09.json)）。

## 処理の適切さと機序の診断（合否にしない）

- TaskSpecが求める確認は、評価の仕組みが取るコマンドの記録では全件で成功していた。
- 1回の取得で300行を超えて受け取った件数は、C301 `-r5`、C304ともに0件だった。この条件のC301では、Sonnet lowはもともと300行を超えて読んでいなかった。
- `Read`の使い方は変わった。300行以内のファイルで範囲を指定した`Read`は14件から24件、範囲を指定しない`Read`は21件から36件に増えた。小さいファイルまで分けて読む、やりすぎた適用が出ている。費用は幅の中だった。
- 1回目の計測でも同じ傾向だった（300行以内のファイルで範囲を指定した`Read`がC301-r3の9件から20件、同じファイルを2回以上読んだrunが3件から8件）。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- 2回目：[登録結果](fbf325e77fd741dc86c6b58a73bdc9ee.json)・[analysis](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)・[発行の記録](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-dispatch-summary.json)・[C301 `-r5`との比較](c304-admission-claude-sonnet55-low-standard14-n5_2026-10-09-c301-r5-comparison.json)
- 1回目（[プロファイル `-r1`](../profiles/c304-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r1.json)）：[登録結果](0b60599d3063460a8713a98b6be4b948.json)・[analysis](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)・[発行の記録](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)・[C301-r3との比較（発行の条件が違うため参照しない）](c304-sonnetonly-claude-sonnet55-low-standard14-n5_2026-10-09-c301-comparison.json)
