# C318 4モデル Standard14 N=5（THE-CAPTION）

## 結論

C318（C316の1行目の2文目を、依頼や指示が既存の状態などから結果を決めるよう指定していない場合に限る。[設計記録](../../docs/candidate318-c316-delegated-state-source-design.md)）を、THE-CAPTIONのStandard14で4モデル各N=5測り、保存済みのC316（N=5）と比べた。4モデルとも70件すべてが4点で、C316と同じだった。THE-CAPTIONのStandard14には依頼が結果を既存の状態に委ねるケースがなく、この計測は、変更がC316の効果を壊さないかの確認である。

| モデル | 指標 | C316の中央値（幅） | C318の中央値（幅） | 差 | C316の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | --- |
| GPT-6.1 Sol Low | 品質 | 100.00 | 100.00 | ±0 | 幅の中 |
| GPT-6.1 Sol Low | 費用（USD） | 0.6421（0.5709〜0.6803） | 0.6608（0.6098〜0.7530） | +2.92% | 幅の中 |
| GPT-6.1 Sol Low | 経過時間（秒） | 505.65（505.30〜546.89） | 411.17（401.61〜413.94） | −18.69% | 幅より下 |
| GPT-6 Astra Low | 品質 | 100.00 | 100.00 | ±0 | 幅の中 |
| GPT-6 Astra Low | 費用（USD） | 4.1229（3.8843〜4.8369） | 3.4791（3.3986〜3.9015） | −15.62% | 幅より下 |
| GPT-6 Astra Low | 経過時間（秒） | 497.36（461.66〜514.70） | 491.76（476.70〜512.26） | −1.13% | 幅の中 |
| Claude Code Sonnet 5.5 low | 品質 | 100.00 | 100.00 | ±0 | 幅の中 |
| Claude Code Sonnet 5.5 low | 費用（USD） | 0.6216（0.6097〜0.6469） | 0.6017（0.5621〜0.6115） | −3.21% | 幅より下 |
| Claude Code Sonnet 5.5 low | 経過時間（秒） | 232.75（227.61〜239.83） | 240.77（237.07〜246.44） | +3.45% | 幅より上 |
| Claude Code Opus 5.5 low | 品質 | 100.00 | 100.00 | ±0 | 幅の中 |
| Claude Code Opus 5.5 low | 費用（USD） | 1.1249（1.1058〜1.1410） | 1.1292（1.1171〜1.1767） | +0.39% | 幅の中 |
| Claude Code Opus 5.5 low | 経過時間（秒） | 247.12（244.60〜254.00） | 256.11（244.96〜262.43） | +3.64% | 幅より上 |

費用は単価表`api-standard-2026-10-10-r2`で両方を数え直した値。

- 品質は4モデルとも変わらなかった。A01（結果が決まる前に作業を始める失敗）は4モデルとも0件で、2文目の適用を狭めてもA01の確認と停止は保たれた。
- 費用と経過時間の差は、C316の測定（2026-10-12）とC318の測定（2026-10-15）で日と時間帯が違うことに加え、Codexでは別のrunとのキャッシュの共有の状態も違うため、変更による差とは断定しない。AstraのC316は、単独で最初に流した計測で最初のリクエストがキャッシュに乗らないrunが多かった（[診断の記録](codex-first-request-cache-order-diagnostics_2026-10-10.json)）。

## 固定条件

- 評価セット：`the-caption-standard14-r1`
- プロンプト：`the-caption-3ce91a4-delegated-state-source-r1`（bundle SHA-256 `55c3204a092f9f6053d97c7797bb7b6153e6a5f9e086842cbfae1219ab866fa0`）。C316とroot `AGENTS.md`の1文だけが違う
- 発行：C316と同じ`one_queue_across_cells`（C318は4モデルを一つの待ち行列に入れた。C316はモデルごとに別の計測）、合計24本まで、負荷を見て発行。計測は2026-10-15 05:07〜05:19 UTC
- 計測したコード：`138e844`

| モデル | プロファイル | result ID |
| --- | --- | --- |
| Sol Low | `c318-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261015-r1` | `c95c201aff894a59ae64a94f9ea49e5d` |
| Astra Low | `c318-astra6-low-standard14-n5-cli0159-isolated-shellenv-20261015-r1` | `22b32f2fb85346cd91e34c9cc3a50904` |
| Sonnet low | `c318-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261015-r1` | `673bda4980cf4de0b24127a9c58e7d9d` |
| Opus low | `c318-claude-opus55-low-standard14-n5-cli2288-shellenv-20261015-r1` | `1979d183a6a74735b39b75192a94da2f` |

比較したC316：`runs/c316-{sol,astra,sonnet,opus}-admission-20261012-r1`（[4モデルの比較](free-c316-four-models-standard14-n5_2026-10-12.md)）。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/c318-standard14-n5-20261015-r1`
- Clickでの結果：[ClickのC318](../targets/click/results/click-c318-four-models-standard14-r4-n5_2026-10-15.md)

このresultは採用、リリース、本体への反映を意味しない。
