# C319 4モデル Standard14 N=5（THE-CAPTION）

## 結論

C319（C318の2行目に、指示や正本は依頼が名指ししたものと作業ツリーで見つかったものだけを使い、存在を確かめていない場所を指定して探さない、という1文を加える。[設計記録](../../docs/candidate319-c318-unconfirmed-location-search-design.md)）を、THE-CAPTIONのStandard14で4モデル各N=5測った。

- 品質は4モデルとも70件すべて4点で、C318と同じだった。
- CodexがFreeのころから行っていた、存在しない`.agents`・`.codex`を指定して失敗する探索が、ほぼなくなった。作業ツリーにある階層ごとの指示（`src/AGENTS.md`など）を読む動作は変わらなかった。
- 費用と経過時間は、Codexの2モデルとSonnetでC318より増えた。ただしC318とC319は別の時間帯に測っており、同じ時間帯に流したClickのCodexでは、C318との差は費用で約+5〜6%にとどまった（[ClickのC319](../targets/click/results/click-c319-four-models-standard14-r4-n5_2026-10-15.md)）。THE-CAPTIONの差には時間帯の影響が大きく含まれていると見られ、変更による差とは断定しない。

| モデル | 存在しない場所を指定して失敗した探索（Free → C316 → C318 → C319） | 階層ごとの指示を読んだrun（C318 → C319） |
| --- | --- | --- |
| GPT-6.1 Sol Low | 20 → 13 → 15 → 1（各70件中） | 44 → 45 |
| GPT-6 Astra Low | 7 → 6 → 4 → 0 | 45 → 46 |

| モデル | 指標 | C318の中央値（幅） | C319の中央値（幅） | 差 | C318の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | --- |
| Sol Low | 費用（USD） | 0.6608（0.6098〜0.7530） | 0.8305（0.7567〜0.8681） | +25.68% | 幅より上 |
| Sol Low | 経過時間（秒） | 411.17（401.61〜413.94） | 463.32（447.19〜469.96） | +12.68% | 幅より上 |
| Astra Low | 費用（USD） | 3.4791（3.3986〜3.9015） | 3.9898（3.7197〜5.0876） | +14.68% | 幅より上 |
| Astra Low | 経過時間（秒） | 491.76（476.70〜512.26） | 658.16（611.86〜695.33） | +33.84% | 幅より上 |
| Sonnet low | 費用（USD） | 0.6017（0.5621〜0.6115） | 0.6321（0.5870〜0.6552） | +5.06% | 幅より上 |
| Sonnet low | 経過時間（秒） | 240.77（237.07〜246.44） | 264.53（243.07〜266.05） | +9.87% | 幅より上 |
| Opus low | 費用（USD） | 1.1292（1.1171〜1.1767） | 1.1275（1.0770〜1.1606） | −0.15% | 幅の中 |
| Opus low | 経過時間（秒） | 256.11（244.96〜262.43） | 257.93（238.59〜273.40） | +0.71% | 幅の中 |

品質は4モデルとも100.00（4点70件）で差はない。費用は単価表`api-standard-2026-10-10-r2`で両方を数え直した値。

## 固定条件

- 評価セット：`the-caption-standard14-r1`
- プロンプト：`the-caption-3ce91a4-unconfirmed-location-search-r1`（bundle SHA-256 `516945120d2952c0508da76e715c7ea01446f9917175a0be0c0572ccfafb450c`）。C318とroot `AGENTS.md`の1文だけが違う
- 発行：C318と同じ`one_queue_across_cells`（4モデルを一つの待ち行列）。計測は2026-10-15 08:06〜08:19 UTC（C318は05:07〜05:19 UTC）
- 計測したコード：`98cad61`

| モデル | プロファイル | result ID |
| --- | --- | --- |
| Sol Low | `c319-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261015-r1` | `be5df1a42230486dab801fde7fd8975c` |
| Astra Low | `c319-astra6-low-standard14-n5-cli0159-isolated-shellenv-20261015-r1` | `df19190ddddb46fca18ebacf89cc8aa6` |
| Sonnet low | `c319-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261015-r1` | `6b4c0472a5d94e32bf0049ce1fc1bd7e` |
| Opus low | `c319-claude-opus55-low-standard14-n5-cli2288-shellenv-20261015-r1` | `54dabec8718c47fb9bfb1c46332beaba` |

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/c319-standard14-n5-20261015-r1`
- 探索の件数は、各runの`all-agent-command-evidence/evidence.json`の`failed_commands`に`.agents`または`.codex`を含むコマンドがあるrunを数えた。Freeは`runs/free-{sol,astra}-admission-20261010-r1`、C316は`runs/c316-{sol,astra}-admission-20261012-r1`

このresultは採用、リリース、本体への反映を意味しない。
