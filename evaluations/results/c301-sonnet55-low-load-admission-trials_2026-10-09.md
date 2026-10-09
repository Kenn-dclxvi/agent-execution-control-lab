# 負荷を見て次のrunを始める発行の条件の試行（C301のSonnet 5.5 low、Standard14 N=5、2026-10-09）

2026-10-09。同時に動かすrunの本数の上限（24）だけでは、どのセルが混ざるかでマシンの負荷が変わった。そのため、実行中の負荷を見て空きがあるときだけ次のrunを始める発行の条件（`campaign_dispatch.admission`、`cpu_busy_below` r1、#368）を作り、C301のSonnet lowで条件の値を三通り試した。**三つとも有効70件すべてが4点だった。コマンドの実行時間は、本数の上限だけでSonnetを24本流したときの38.3秒から、21〜23秒に揃った。経過時間の揺れの大部分は、モデルの応答時間（182〜250秒）だった。** 系列の発行の条件は、CPU使用率70%以下・間隔1秒（r5）とする。

## 背景

[C304の最初の計測](c304-claude-sonnet55-low-standard14-n5_2026-10-09.md)では、Sonnet lowだけを本数の上限24で流したため、Sonnetの同時実行が平均21.6本になった。Solと一緒に流したC301〜C303では平均7〜8本だった。テストを実行するケースの経過時間が14〜35%延び、基準と比べられなかった。旧系列では、1反復分の14ケースずつ区切って流していたため、Sonnetだけでも最大14本に収まっていた。

## 条件

- prompt identity：C301（`the-caption-3ce91a4-outcome-binding-uniform-markdown-r1`）。プロファイルは`-r3`と同じで、発行の条件と、並び順に使う見積もり時間だけが違う。
- 発行の条件：上限24本の内側で、直前1秒のCPU使用率（`top`のuser＋sys）が上限以下のとき、または実行中のrunがないときだけ次を始める。始めた後は、決めた間隔を空けてから次を判断する。待つ間も、並べた順（重いrunから順）どおりに始める。
- 並び順の見積もり時間：C301の一つの待ち行列での計測の、ケースごとの経過時間の中央値に更新した（記録の項目で、比較条件ではない）。

| プロファイル | CPU使用率の上限 | 間隔 |
| --- | ---: | ---: |
| [`-r4`](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r4.json) | 70% | 3秒 |
| [`-r5`](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r5.json) | 70% | 1秒 |
| [`-r6`](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r6.json) | 40% | 1秒 |

三つはそれぞれ比較条件が違う。互いの差をプロンプトの効果として扱わない。

## 結果

| 計測 | 品質 | 費用（USD） | 経過時間（秒） | 生のトークン（参考） |
| --- | --- | ---: | ---: | ---: |
| r4（70%・3秒） | 4点70件 | 0.6692（0.6479〜0.6803） | 245.91（232.44〜259.19） | 785,817 |
| r5（70%・1秒） | 4点70件 | 0.6811（0.6634〜0.6938） | 286.68（269.85〜343.71） | 822,676 |
| r6（40%・1秒） | 4点70件 | 0.6565（0.6432〜0.6823） | 317.92（298.37〜343.61） | 793,822 |

## 発行の動きと経過時間の内訳

[診断の記録](c301-c304-sonnet-dispatch-load-diagnostics_2026-10-09.json)。経過時間の内訳は、transcriptの時刻から、モデルの応答（ツールの結果から次の応答まで）とコマンドの実行（応答からツールの結果まで）に分けた、1反復あたりの中央値である。

| 計測 | Sonnetの同時実行（最大・平均） | CPU使用率（平均・90%点・最大） | 空きを待ったrun | 全体の所要 | モデルの応答 | コマンドの実行 |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| C301-r3（Solと一緒、本数の上限だけ） | 12・7.6 | ― | ― | 200秒 | 205.3秒 | 26.4秒 |
| C304（Sonnetだけ、本数の上限だけ） | 24・21.6 | ― | ― | 77秒 | 212.9秒 | 38.3秒 |
| r4（70%・3秒） | 7・3.9 | 32・63・76% | 1件 | 329秒 | 182.1秒 | 21.2秒 |
| r5（70%・1秒） | 13・8.1 | 43・63・69% | 2件 | 191秒 | 225.5秒 | 22.7秒 |
| r6（40%・1秒） | 12・6.2 | 41・62・83% | 9件 | 266秒 | 249.9秒 | 22.2秒 |

- 負荷を見て始める条件では、コマンドの実行時間が21〜23秒に揃った。上限と間隔の違い（70%と40%、3秒と1秒）では差がなかった。
- r4では、本数を決めていたのはCPUの上限ではなく、3秒の間隔だった。全体の所要が長くなった。
- 経過時間の差の大部分は、モデルの応答時間の違いである。テストを実行しないケースも同じ向きに延びていた。モデルの応答時間は計測の時間帯で20〜30%揺れ、この側では制御できない。
- 三つとも、発行の順番は並べた順どおりだった。

## 判断

系列の発行の条件は、r5（CPU使用率70%以下、間隔1秒）とする。コマンドの実行時間はr4と同じ水準に抑えられ、全体の所要が最も短い。r5を、この条件でのC301のSonnet lowの基準とする。採用、release、本体反映は行っていない。

## 一次アーティファクト

| 計測 | 登録結果 | analysis | selection | 品質監査 | 発行前の記録 | 発行の記録 |
| --- | --- | --- | --- | --- | --- | --- |
| r4 | [`dc92e875…`](dc92e875543f4803b357f5e3f469255a.json) | [analysis](c301-admission-r4-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json) | [selection](c301-admission-r4-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json) | [品質監査](c301-admission-r4-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json) | [記録](c301-admission-r4-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json) | [記録](c301-admission-r4-claude-sonnet55-low-standard14-n5_2026-10-09-dispatch-summary.json) |
| r5 | [`c1738e00…`](c1738e0016864d5095f408be6805e9b0.json) | [analysis](c301-admission-r5-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json) | [selection](c301-admission-r5-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json) | [品質監査](c301-admission-r5-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json) | [記録](c301-admission-r5-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json) | [記録](c301-admission-r5-claude-sonnet55-low-standard14-n5_2026-10-09-dispatch-summary.json) |
| r6 | [`05cc6cd7…`](05cc6cd7d4ef4511a04390c14ae8430c.json) | [analysis](c301-admission-r6-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json) | [selection](c301-admission-r6-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json) | [品質監査](c301-admission-r6-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json) | [記録](c301-admission-r6-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json) | [記録](c301-admission-r6-claude-sonnet55-low-standard14-n5_2026-10-09-dispatch-summary.json) |
