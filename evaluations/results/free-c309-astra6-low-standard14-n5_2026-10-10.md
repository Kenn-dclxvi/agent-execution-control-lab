# FreeとC309のGPT-6 Astra Low、Standard14 N=5（2026-10-10）

2026-10-10。利用者の依頼で、Free（rootの`AGENTS.md`を空にしたもの）と[C309](../../docs/candidate309-c307-final-check-unit-design.md)を、GPT-6 Astra Lowで新しい試験として測った。条件は、Sol LowとSonnet lowの[Free・C301・C309の比較](free-c301-c309-sol61-low-sonnet55-low-standard14-n5_2026-10-10.md)、および[Opus 5.5 lowの計測](free-c309-claude-opus55-low-standard14-n5_2026-10-10.md)と同じ（実行環境の切り離し、費用のKPI、負荷を見て次のrunを始める発行。CPU使用率70%以下、間隔1秒）。C301のAstra Lowは測っていない。**Freeは4点68件・0点2件（A01）、C309は70件すべて4点だった。C309はFree比で費用−32.09%、経過時間−25.55%で、どちらもFreeの幅より下だった。**

## 条件

- プロファイル：[Free](../profiles/free-astra6-low-standard14-n5-cli0159-isolated-shellenv-20261010-r1.json)、[C309](../profiles/c309-astra6-low-standard14-n5-cli0159-isolated-shellenv-20261010-r1.json)。Sol Lowの同名のプロファイルとは、モデル名（`gpt-6-astra`）だけが違う。旧系列でも、Astra LowとSol Lowのプロファイルの違いはモデル名だけだった。並び順の見積もり時間は、Astraの実測がないためSol Lowの値を使った（記録の項目で、比較条件ではない）。
- FreeとC309は、それぞれ一つの待ち行列で、Free、C309の順に続けて流した。
- 単価表：GPT-6 Astraを加えた新しい版[`api-standard-2026-10-10-r2`](../price-tables/api-standard-2026-10-10-r2.json)。Astraの単価は、OpenAIのAPI料金ページ（標準）による。100万トークンあたり、入力$10、キャッシュ読み取り$1、出力$50で、一回の入力が272Kを超える長文では入力$20、キャッシュ読み取り$2、出力$75。Codexはキャッシュ書き込みを報告しないため、書き込みの単価は使わない。既存の版は書き換えていない。今回のrunに長文の区分に入ったものはなかった。

## 結果

| 指標 | Free | C309 | 差（%） | Freeの幅に対する位置 |
| --- | ---: | ---: | ---: | --- |
| 品質（0〜100） | 100.00（92.86〜100.00） | 100.00（100.00〜100.00） | +0.00% | 幅の中 |
| 4点の件数 | 68 / 70（A01の2件が0点） | 70 / 70 | ― | ― |
| 費用（USD） | 6.1484（5.6532〜6.4405） | 4.1757（3.8056〜4.3880） | −32.09% | 幅より下 |
| 経過時間（秒） | 634.75（605.93〜728.74） | 472.55（462.74〜492.66） | −25.55% | 幅より下 |
| 生のトークン（参考） | 2,256,298（2,043,822〜2,689,294） | 1,503,826（1,456,453〜1,632,628） | −33.35% | 幅より下 |

比較は`compare-analyses`による（[記録](c309-astra6-low-standard14-n5_2026-10-10-free-comparison.json)）。

## ケースごとの費用（診断、合否にしない）

[診断の記録](free-c309-astra6-low-standard14-n5_2026-10-10-diagnostics.json)。各ケースの5反復の中央値。

| ケース | Free（USD） | C309（USD） | 差（%） |
| --- | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 0.3923 | 0.0799 | −79.6% |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 0.9245 | 0.3578 | −61.3% |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 0.6598 | 0.4362 | −33.9% |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 0.7827 | 0.5562 | −28.9% |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 0.4705 | 0.2862 | −39.2% |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 0.5718 | 0.4174 | −27.0% |
| `TC-F05-CLARIFY-UNITS-MODE` | 0.0777 | 0.0852 | +9.7% |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 0.0783 | 0.0859 | +9.6% |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 0.4933 | 0.3757 | −23.8% |
| `TC-F07-CANONICAL-V4-RUNNER` | 0.4049 | 0.3400 | −16.0% |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 0.3886 | 0.2038 | −47.6% |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 0.3960 | 0.3728 | −5.9% |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 0.2970 | 0.2087 | −29.7% |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 0.2148 | 0.2054 | −4.4% |

- 費用の減少は、コマンドを実行する多くのケースに広がっている。A01とA02の減り方が特に大きい。
- 費用の小さいF05の2ケースは、C309で約1割増えた。rootの`AGENTS.md`の分だけ入力が増えたためと見られる（因果は未確認）。
- FreeのA01の0点2件は、変更後の方針を確認する前に編集または試験へ進んだもので、Opus lowのFreeの0点と同じ失敗だった。
- C309の一文目（状態の確認の置き場所）の遵守は、この計測では数えていない。

採用、追加反復、release、本体反映は行っていない。

## 追記（2026-10-10）：流した順番とキャッシュ

この計測の費用の差は、流した順番の影響を大きく含む。FreeとC309は一本ずつ順に流しており、Codexの共通の先頭部分（12,288トークン）のキャッシュは、別のrunや別のプロンプトの間でも共有される。先に流したFreeでは、最初のリクエストがキャッシュに乗らなかったrunが70件中36件あり、序盤に集中した（時刻順に14件ずつ13、7、8、6、2件）。後のC309は13件だった。キャッシュの当たり外れを揃えた見積もりでは、C309のFree比の費用の差は−24.2%（登録済みのKPIでは−32.09%）になる。この見積もりは登録済みのKPIとは計算経路が違う参考値であり、上の結果と登録済みのresultは書き換えていない。[診断の記録](codex-first-request-cache-order-diagnostics_2026-10-10.json)。比べるプロンプトを一つの待ち行列に混ぜて流す発行を用意したが（[`evaluations/AGENTS.md`](../AGENTS.md)の「互換条件」）、その発行での測り直しはしていない。

## 一次アーティファクト

- Free：[登録結果](3f92ebb6c83d43d5ac1b3f5499a145d4.json)・[analysis](free-astra6-low-standard14-n5_2026-10-10-analysis.json)・[selection](free-astra6-low-standard14-n5_2026-10-10-selection.json)・[品質監査](free-astra6-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](free-astra6-low-standard14-n5_2026-10-10-prepare-receipt.json)・[発行の記録](free-astra6-low-standard14-n5_2026-10-10-dispatch-summary.json)
- C309：[登録結果](3a8d37f16e104f89b77e4597d7be502a.json)・[analysis](c309-astra6-low-standard14-n5_2026-10-10-analysis.json)・[selection](c309-astra6-low-standard14-n5_2026-10-10-selection.json)・[品質監査](c309-astra6-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](c309-astra6-low-standard14-n5_2026-10-10-prepare-receipt.json)・[発行の記録](c309-astra6-low-standard14-n5_2026-10-10-dispatch-summary.json)・[Freeとの比較](c309-astra6-low-standard14-n5_2026-10-10-free-comparison.json)
- 両方：[診断の記録](free-c309-astra6-low-standard14-n5_2026-10-10-diagnostics.json)
