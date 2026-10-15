# Click C319 4モデル Standard14 r4 N=5

## 結論

C319（C316の1行目の2文目を、依頼や指示が既存の状態などから結果を決めるよう指定していない場合に限り、2行目に、指示や正本は依頼が名指ししたものと作業ツリーで見つかったものだけを使い、存在を確かめていない場所を指定して探さない、という1文を加える。[C318の設計記録](../../../../docs/candidate318-c316-delegated-state-source-design.md)、[C319の設計記録](../../../../docs/candidate319-c318-unconfirmed-location-search-design.md)）を、ClickのStandard14 r4で4モデル各N=5測り、保存済みのFree（指示を含まない1文の比較元）とC316と比べた。

- 品質：Codex（Sol、Astra）とOpusは70件すべて4点。Sonnetは、Freeでも起きるF06の判断の落とし穴（テストを足さずに終了）が1件あった。C316で起きていたCodexのF07-Pの誤った停止とF06の探索の失敗による停止は、0件だった。
- 費用：4モデルともFreeより低く、Freeの幅より下だった。C316とは4モデルとも幅の中で、差は−3.21%〜−0.07%だった。
- 経過時間：Codexで延びたが、計測の時間帯が違い、変更による差とは断定しない。

## FreeとC316との比較

| モデル | 指標 | Freeの中央値（幅） | C316の中央値（幅） | C319の中央値（幅） | Free比 | C316比 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Sol Low | 品質 | 92.86（92.86〜100.00） | 94.64（94.64〜100.00） | 100.00 | +7.69%（幅の中） | +5.66%（幅の中） |
| Sol Low | 費用（USD） | 0.7288（0.6221〜0.8898） | 0.6362（0.6059〜0.7623） | 0.6158（0.5483〜0.6214） | −15.51%（幅より下） | −3.21%（幅の中） |
| Sol Low | 経過時間（秒） | 414.88（355.66〜429.74） | 344.39（329.75〜365.93） | 431.86（414.18〜439.99） | +4.09%（幅より上） | +25.40%（幅より上） |
| Astra Low | 品質 | 100.00（92.86〜100.00） | 94.64（89.29〜100.00） | 100.00 | ±0（幅の中） | +5.66%（幅の中） |
| Astra Low | 費用（USD） | 4.3002（3.4656〜4.3063） | 3.3927（3.1070〜3.4935） | 3.2875（3.0134〜3.3295） | −23.55%（幅より下） | −3.10%（幅の中） |
| Astra Low | 経過時間（秒） | 458.33（410.13〜515.64） | 385.51（379.18〜411.26） | 594.45（581.04〜630.41） | +29.70%（幅より上） | +54.20%（幅より上） |
| Sonnet low | 品質 | 92.86（92.86〜92.86） | 100.00（94.64〜100.00） | 100.00（94.64〜100.00） | +7.69%（幅より上） | ±0（幅の中） |
| Sonnet low | 費用（USD） | 0.5502（0.5355〜0.6189） | 0.5233（0.5093〜0.5406） | 0.5229（0.5049〜0.5396） | −4.95%（幅より下） | −0.07%（幅の中） |
| Sonnet low | 経過時間（秒） | 288.11（267.68〜291.03） | 234.65（229.45〜250.31） | 236.73（229.31〜239.95） | −17.83%（幅より下） | +0.89%（幅の中） |
| Opus low | 品質 | 100.00 | 100.00 | 100.00 | ±0 | ±0 |
| Opus low | 費用（USD） | 1.0023（0.9967〜1.0137） | 0.9935（0.9648〜1.0123） | 0.9768（0.9582〜1.0221） | −2.55%（幅より下） | −1.68%（幅の中） |
| Opus low | 経過時間（秒） | 276.02（265.33〜296.05） | 253.38（248.34〜264.34） | 241.12（234.14〜276.07） | −12.64%（幅より下） | −4.84%（幅より下） |

差はC319の、比べる相手に対する差。位置は相手の5反復の幅に対するもの。費用は単価表`api-standard-2026-10-10-r2`で数え直した値。比べたFreeとC316はいずれも累積前のN=5（Free：Claude Code 2026-10-14、Codex 2026-10-15 00:11〜。C316：Claude Code 2026-10-14、Codex 2026-10-15 00:11〜）で、C319（2026-10-15 08:19〜08:38 UTC）とは時間帯が違う。

## 品質

| モデル | Free（N=5）の4点未満 | C316（N=5）の4点未満 | C319（N=5）の4点未満 |
| --- | --- | --- | --- |
| Sol Low | A01 3件 | F07-P 4件 | なし |
| Astra Low | A01 1件 | F07-P 3件、F06 2件 | なし |
| Sonnet low | A01 5件 | F06 1件 | F06 1件（Freeでも起きる判断の落とし穴） |
| Opus low | なし | なし | なし |

存在しない`.agents`・`.codex`を指定して失敗した探索（Codex、各70件中）は、Sol 3件、Astra 2件だった（同じ時間に同じ待ち行列で流したC318の追加分ではSol 7件、Astra 11件。C316のN=5ではSol 11件、Astra 11件。FreeのN=5では0件）。

## 固定条件

- 評価セット：`click-standard14-r4` / `r4`
- プロンプト：`click-00e592c-unconfirmed-location-search-r1`（bundle SHA-256 `6fa96f2d6b72c4b0b9f3c2955e26dc4875ef36ca9152f6b605714a3d8b0cb462`）
- 発行：FreeとC316と同じ条件。Claude Codeは`one_queue_across_cells`、Codexは`one_queue_across_cells_and_prompts`（C319を、C318の追加5回分と同じ待ち行列に混ぜた）
- 採点：Claude Codeは`claude-collector-v3`、Codexは`v11`。個別の判定記録は、C319のSonnetのF06（テストを足さずに終了、1点）と、同じ待ち行列のC318の追加分のAstraのF06 2件（探索の失敗で停止、1点）
- 事前の局所の確認（登録しない診断、`runs/click-c319-codex-search-check-20261015-r1`）：F06・F01・A02をSol・Astraで各5回。失敗した存在しない場所の探索は2 / 30件
- 計測したコード：`98cad61`

| モデル | プロファイル | result ID |
| --- | --- | --- |
| Sol Low | `c319-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `c45d0de720bc4bacb0622e12a0626f6d` |
| Astra Low | `c319-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `95a40250320c49d6a567392a5db7bd52` |
| Sonnet low | `c319-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `b66c728a5dd14e508583d5ec0e831b49` |
| Opus low | `c319-click-claude-opus55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `2a46c1958f6244b88ae01ced1b7fb278` |
| Sol Low C318（累積N=10、同じ待ち行列の相手） | `c318-click-sol61-low-standard14-r4-n10-cli0159-isolated-shellenv-20261015-r2` | `ec8364bd3ff14786a9f3576a788a2337` |
| Astra Low C318（累積N=10、同上） | `c318-click-astra6-low-standard14-r4-n10-cli0159-isolated-shellenv-20261015-r2` | `cc25881158cf4b08aa844b01004d83cc` |

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-c319-claude-standard14-r4-n5-20261015-r1`、`runs/click-c319-codex-standard14-r4-n5-20261015-r1`（待ち行列の記録は`campaign-round-1/`）、`runs/click-c318-codex-standard14-r4-n10-20261015-r1`
- 比較したFree：[Sonnet](click-free-loaded-c316-sonnet55-low-standard14-r4-n5_2026-10-14.md)、[Opus](click-free-loaded-c316-opus55-low-standard14-r4-n5_2026-10-14.md)、[Sol・Astra](click-free-loaded-c316-sol61-astra6-low-standard14-r4-n5_2026-10-15.md)のN=5
- THE-CAPTIONでの結果：[C319 4モデル](../../../results/c319-four-models-standard14-n5_2026-10-15.md)

このresultは採用、リリース、本体への反映を意味しない。
