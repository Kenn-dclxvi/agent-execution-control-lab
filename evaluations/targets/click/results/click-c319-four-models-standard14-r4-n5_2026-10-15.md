# Click C319 4モデル Standard14 r4 N=5

## 結論

C319（C318の2行目に、指示や正本は依頼が名指ししたものと作業ツリーで見つかったものだけを使い、存在を確かめていない場所を指定して探さない、という1文を加える。[設計記録](../../../../docs/candidate319-c318-unconfirmed-location-search-design.md)）を、ClickのStandard14 r4で4モデル各N=5測った。CodexはC318の追加5回分と同じ待ち行列に混ぜて流し、同じ時間帯での差を見た。

- 品質：Codex（Sol、Astra）とOpusは70件すべて4点。Sonnetは、Freeでも起きるF06の判断の落とし穴（テストを足さずに終了）が1件あった。
- F06の探索の失敗による停止：同時に流したC318の追加分ではAstraで2件起きたが、C319では0件だった。
- 存在しない`.agents`・`.codex`を指定して失敗する探索：同時に流した分で、Sol 7 → 3件、Astra 11 → 2件（各70件中）。
- 費用：同時に流したC318の追加分と比べ、1反復の中央値でSol +4.9%（0.5763 → 0.6047）、Astra +6.2%（3.1138 → 3.3073）。コマンドの数はほぼ同じで、ケースごとの差は増減が入り混じっていた。

## C318との比較

### 同じ待ち行列で同時に流した分（Codex）

| モデル | 1反復の費用の中央値（C318 → C319） | コマンドの合計 | 失敗したコマンド | 失敗した存在しない場所の探索 | 4点未満 |
| --- | ---: | ---: | ---: | ---: | --- |
| Sol Low | 0.5763 → 0.6047 | 451 → 447 | 17 → 18 | 7 → 3 | なし → なし |
| Astra Low | 3.1138 → 3.3073 | 410 → 444 | 21 → 7 | 11 → 2 | F06 2件 → なし |

C318側は、C318の累積N=10の計測のうち、この待ち行列で足した5回分（`runs/click-c318-codex-standard14-r4-n10-20261015-r1`）だけを使った。

### 保存済みのC318（N=5）との比較

| モデル | 指標 | C318の中央値（幅） | C319の中央値（幅） | 差 | C318の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | --- |
| Sol Low | 費用（USD） | 0.5112（0.4620〜0.5419） | 0.6158（0.5483〜0.6214） | +20.45% | 幅より上 |
| Sol Low | 経過時間（秒） | 366.00（361.64〜390.58） | 431.86（414.18〜439.99） | +18.00% | 幅より上 |
| Astra Low | 費用（USD） | 3.0880（2.8058〜3.1679） | 3.2875（3.0134〜3.3295） | +6.46% | 幅より上 |
| Astra Low | 経過時間（秒） | 497.16（458.96〜506.90） | 594.45（581.04〜630.41） | +19.57% | 幅より上 |
| Sonnet low | 費用（USD） | 0.5237（0.5089〜0.5430） | 0.5229（0.5049〜0.5396） | −0.15% | 幅の中 |
| Sonnet low | 経過時間（秒） | 224.23（216.89〜235.74） | 236.73（229.31〜239.95） | +5.58% | 幅より上 |
| Opus low | 費用（USD） | 0.9881（0.9786〜1.0048） | 0.9768（0.9582〜1.0221） | −1.14% | 幅より下 |
| Opus low | 経過時間（秒） | 255.31（234.20〜268.86） | 241.12（234.14〜276.07） | −5.56% | 幅の中 |

保存済みのC318（05:19〜05:39 UTC）とC319（08:19〜08:38 UTC）は時間帯が違う。同じ時間帯に流したC318の追加分自体も、保存済みのC318よりSolで約13%高かった。Codexの差の大半は時間帯によるものと見られる。

## 固定条件

- 評価セット：`click-standard14-r4` / `r4`
- プロンプト：`click-00e592c-unconfirmed-location-search-r1`（bundle SHA-256 `6fa96f2d6b72c4b0b9f3c2955e26dc4875ef36ca9152f6b605714a3d8b0cb462`）。C318とroot `AGENTS.md`の1文だけが違う
- 発行：C318と同じ条件。Claude Codeは`one_queue_across_cells`、Codexは`one_queue_across_cells_and_prompts`（C319とC318の追加5回分を混ぜる）
- 採点：Claude Codeは`claude-collector-v3`、Codexは`v11`。個別の判定記録は、C319のSonnetのF06（テストを足さずに終了、1点）と、C318の追加分のAstraのF06 2件（探索の失敗で停止、1点）
- 事前の局所の確認（登録しない診断、`runs/click-c319-codex-search-check-20261015-r1`）：F06・F01・A02をSol・Astraで各5回。失敗した存在しない場所の探索はC318の15 / 30件に対して2 / 30件
- 計測したコード：`98cad61`

| モデル | プロファイル | result ID |
| --- | --- | --- |
| Sol Low | `c319-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `c45d0de720bc4bacb0622e12a0626f6d` |
| Astra Low | `c319-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `95a40250320c49d6a567392a5db7bd52` |
| Sonnet low | `c319-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `b66c728a5dd14e508583d5ec0e831b49` |
| Opus low | `c319-click-claude-opus55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `2a46c1958f6244b88ae01ced1b7fb278` |
| Sol Low C318（累積N=10） | `c318-click-sol61-low-standard14-r4-n10-cli0159-isolated-shellenv-20261015-r2` | `ec8364bd3ff14786a9f3576a788a2337` |
| Astra Low C318（累積N=10） | `c318-click-astra6-low-standard14-r4-n10-cli0159-isolated-shellenv-20261015-r2` | `cc25881158cf4b08aa844b01004d83cc` |

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-c319-claude-standard14-r4-n5-20261015-r1`、`runs/click-c319-codex-standard14-r4-n5-20261015-r1`（待ち行列の記録は`campaign-round-1/`）、`runs/click-c318-codex-standard14-r4-n10-20261015-r1`
- THE-CAPTIONでの結果：[C319 4モデル](../../../results/c319-four-models-standard14-n5_2026-10-15.md)

このresultは採用、リリース、本体への反映を意味しない。
