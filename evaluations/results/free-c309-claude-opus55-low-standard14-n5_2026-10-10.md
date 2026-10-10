# FreeとC309のClaude Code Opus 5.5 low、Standard14 N=5（2026-10-10）

2026-10-10。利用者の依頼で、Free（rootの`AGENTS.md`を空にしたもの）と[C309](../../docs/candidate309-c307-final-check-unit-design.md)を、Opus 5.5 lowで測った。条件は、Sol LowとSonnet lowの[Free・C301・C309の比較](free-c301-c309-sol61-low-sonnet55-low-standard14-n5_2026-10-10.md)と同じ（実行環境の切り離し、費用のKPI、負荷を見て次のrunを始める発行。CPU使用率70%以下、間隔1秒）。C301のOpus lowは測っていない。**Freeは4点69件・0点1件（A01）、C309は70件すべて4点だった。C309はFree比で費用−6.64%（Freeの幅より下）、経過時間−1.09%（幅の中）だった。**

## 条件

- プロファイル：[Free](../profiles/free-claude-opus55-low-standard14-n5-cli2288-shellenv-20261010-r1.json)、[C309](../profiles/c309-claude-opus55-low-standard14-n5-cli2288-shellenv-20261010-r1.json)。Sonnet lowの同名のプロファイルとは、モデル名（`claude-opus-5-5`）だけが違う。旧系列のC280でも、Opus lowとSonnet lowのプロファイルの違いはモデル名だけだった。並び順の見積もり時間は、Opusの実測がないためSonnet lowの値を使った（記録の項目で、比較条件ではない）。
- 単価表：Claude Opus 5.5を加えた新しい版[`api-standard-2026-10-10`](../price-tables/api-standard-2026-10-10.json)。既存の版`api-standard-2026-10-09`は書き換えていない。Opus 5.5の単価は、Claude Codeに同梱のClaude APIの資料による（入力$4、出力$20、キャッシュ読み取り$0.20、キャッシュ書き込みは入力の1.25倍（5分）と2倍（1時間）、いずれも100万トークンあたり）。最初の集計は、単価表にOpus 5.5がなかったため止まり、この版で集計し直した。Sol LowとSonnet lowの他の計測（`api-standard-2026-10-09`）と、費用の値を混ぜて比べない。（同日追記）この記述は改めた。単価表は計測の条件ではなく比較のときに選ぶもので、比べる両方を同じ単価表で各runの使用量の内訳から数え直せば比べられる（`compare-analyses --price-table --registry`、[`evaluations/AGENTS.md`](../AGENTS.md)の「3 KPI」）。版の違いを理由に測り直さない。`api-standard-2026-10-10`のSol LowとSonnet lowの単価は`api-standard-2026-10-09`と同じで、両方を新しい版で数え直しても費用は変わらない。

## 結果

| 指標 | Free | C309 | 差（%） | Freeの幅に対する位置 |
| --- | ---: | ---: | ---: | --- |
| 品質（0〜100） | 100.00（92.86〜100.00） | 100.00（100.00〜100.00） | +0.00% | 幅の中 |
| 4点の件数 | 69 / 70（A01の1件が0点） | 70 / 70 | ― | ― |
| 費用（USD） | 1.2731（1.2379〜1.3126） | 1.1886（1.1750〜1.2014） | −6.64% | 幅より下 |
| 経過時間（秒） | 269.41（261.43〜292.21） | 266.47（258.93〜286.12） | −1.09% | 幅の中 |
| 生のトークン（参考） | 750,215（712,173〜828,516） | 697,666（652,152〜717,799） | −7.00% | 幅より下 |

比較は`compare-analyses`による（[記録](c309-claude-opus55-low-standard14-n5_2026-10-10-free-comparison.json)）。

## 処理の適切さと機序の診断（合否にしない）

[診断の記録](free-c309-claude-opus55-low-standard14-n5_2026-10-10-diagnostics.json)。

| 項目 | Free | C309 |
| --- | ---: | ---: |
| A01で方針の確認前に編集・試験へ進んだrun（0点） | 1 / 5 | 0 / 5 |
| 最後の確認の応答に状態の確認が入ったrun（遵守） | 15 / 25 | 16 / 27 |
| 最後の変更の後に状態を確かめずに報告したrun | 0 | 0 |
| 最後の確認の後の応答 | 12（状態の確認9、退避された出力の読み取り3） | 14（すべて状態の確認） |
| F06・F07の`git diff --check`の成功 | 10/10 | 10/10 |
| `main_verify.sh`をそのままの形で実行 | 3 / 20 | 0 / 22 |

- C309の一文目（状態の確認を最後の確認と同じ応答で行う）の遵守率は、Opus lowで16/27（59%）にとどまった。Sonnet low（28/32）とSol Low（35/35）より低い。遵守しなかったrunは、最後の確認の次の応答で状態の確認を1回だけ行っていた。状態の確認を省いたrunも、重ねたrunもなかった。
- Freeでも状態の確認は省かれていなかった。Opus lowでは、C309の一文目がなくても完了条件の確認は行われ、一文目は置き場所をそろえる効果が小さい。
- C309では、退避された出力の読み取りがなくなり、`main_verify.sh`はすべて出力を絞る形で実行された。

採用、追加反復、release、本体反映は行っていない。

## 追記（2026-10-10）：流した順番とキャッシュ

Codexの計測（Sol Low、Astra Low）では、一本ずつ順に流すと、先に流した計測の最初のリクエストがキャッシュに乗らず費用で不利になっていた。Opus lowでは、FreeとC309の140件すべてで最初のリクエストがキャッシュに乗っており（共通の先頭部分6,039トークン）、この影響はなかった。[診断の記録](codex-first-request-cache-order-diagnostics_2026-10-10.json)。

## 一次アーティファクト

- Free：[登録結果](616b1cf5c6ed46e8bc40f0a36f944cb2.json)・[analysis](free-claude-opus55-low-standard14-n5_2026-10-10-analysis.json)・[selection](free-claude-opus55-low-standard14-n5_2026-10-10-selection.json)・[品質監査](free-claude-opus55-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](free-claude-opus55-low-standard14-n5_2026-10-10-prepare-receipt.json)・[発行の記録](free-claude-opus55-low-standard14-n5_2026-10-10-dispatch-summary.json)
- C309：[登録結果](8378d3c9a0414c81a180f3f8fd33a8b8.json)・[analysis](c309-claude-opus55-low-standard14-n5_2026-10-10-analysis.json)・[selection](c309-claude-opus55-low-standard14-n5_2026-10-10-selection.json)・[品質監査](c309-claude-opus55-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](c309-claude-opus55-low-standard14-n5_2026-10-10-prepare-receipt.json)・[発行の記録](c309-claude-opus55-low-standard14-n5_2026-10-10-dispatch-summary.json)・[Freeとの比較](c309-claude-opus55-low-standard14-n5_2026-10-10-free-comparison.json)
- 両方：[診断の記録](free-c309-claude-opus55-low-standard14-n5_2026-10-10-diagnostics.json)
