# Click C318 4モデル Standard14 r4 N=5

## 結論

C318（C316の1行目の2文目を、依頼や指示が既存の状態などから結果を決めるよう指定していない場合に限る。[設計記録](../../../../docs/candidate318-c316-delegated-state-source-design.md)）を、ClickのStandard14 r4で4モデル各N=5測り、保存済みのC316（N=5）と比べた。

CodexのF07-Pで起きていた誤った停止は、C318では0件になった（C316のN=5ではSol 4 / 5、Astra 3 / 5、累積N=20ではSol 11 / 20、Astra 10 / 20）。A01の失敗は4モデルとも0件のままで、Freeで起きていた失敗を抑える効果は保たれた。

| モデル | 指標 | C316の中央値（幅） | C318の中央値（幅） | 差 | C316の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | --- |
| GPT-6.1 Sol Low | 品質 | 94.64（94.64〜100.00） | 100.00（100.00〜100.00） | +5.66% | 幅の中 |
| GPT-6.1 Sol Low | 費用（USD） | 0.6362（0.6059〜0.7623） | 0.5112（0.4620〜0.5419） | −19.64% | 幅より下 |
| GPT-6.1 Sol Low | 経過時間（秒） | 344.39（329.75〜365.93） | 366.00（361.64〜390.58） | +6.28% | 幅より上 |
| GPT-6 Astra Low | 品質 | 94.64（89.29〜100.00） | 100.00（94.64〜100.00） | +5.66% | 幅の中 |
| GPT-6 Astra Low | 費用（USD） | 3.3927（3.1070〜3.4935） | 3.0880（2.8058〜3.1679） | −8.98% | 幅より下 |
| GPT-6 Astra Low | 経過時間（秒） | 385.51（379.18〜411.26） | 497.16（458.96〜506.90） | +28.96% | 幅より上 |
| Claude Code Sonnet 5.5 low | 品質 | 100.00（94.64〜100.00） | 100.00（100.00〜100.00） | ±0 | 幅の中 |
| Claude Code Sonnet 5.5 low | 費用（USD） | 0.5233（0.5093〜0.5406） | 0.5237（0.5089〜0.5430） | +0.07% | 幅の中 |
| Claude Code Sonnet 5.5 low | 経過時間（秒） | 234.65（229.45〜250.31） | 224.23（216.89〜235.74） | −4.44% | 幅より下 |
| Claude Code Opus 5.5 low | 品質 | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | ±0 | 幅の中 |
| Claude Code Opus 5.5 low | 費用（USD） | 0.9935（0.9648〜1.0123） | 0.9881（0.9786〜1.0048） | −0.54% | 幅の中 |
| Claude Code Opus 5.5 low | 経過時間（秒） | 253.38（248.34〜264.34） | 255.31（234.20〜268.86） | +0.76% | 幅の中 |

費用は単価表`api-standard-2026-10-10-r2`で両方を数え直した値。

## 品質

| モデル | C316（N=5）の4点未満 | C318（N=5）の4点未満 |
| --- | --- | --- |
| Sol Low | F07-P 4件 | なし |
| Astra Low | F07-P 3件、F06 2件 | F06 1件 |
| Sonnet low | F06 1件 | なし |
| Opus low | なし | なし |

- **F07-P**：C318では、Codexの10件すべてが、既存のlockと隣接するgroupに合わせて`pytest<0`を`pytest`へ直し、必須gateを通した。事前の局所の確認（登録しない診断、`runs/click-c318-codex-f07p-a01-check-20261015-r1`）でも、Sol・Astraの10件すべてが停止しなかった。
- **A01**：4モデルとも、編集も試験もせずに確認を返して止まった。
- **AstraのF06（1件）**：C316でも起きた、自分で実行した存在しない`.agents`・`.codex`の探索の失敗を、環境failureと見なして止まる形である。この探索はC318でも残り（Sol 9 / 70、Astra 17 / 70。C316はSol 11 / 70、Astra 11 / 70、Freeは1 / 140）、C318の変更の対象外である。

## 費用と経過時間

CodexのSolとAstraで費用が下がった差には、F07-Pで止まっていたrunが作業して検証するようになった分の増加と、C316とC318の計測の時間帯の違いの両方が含まれる。経過時間はCodexで延び、Claude Codeではほぼ同じか短くなった。経過時間の差は計測の時間帯で揺れるため、変更による差とは断定しない。

## 固定条件

- 評価セット：`click-standard14-r4` / `r4`
- プロンプト：`click-00e592c-delegated-state-source-r1`（bundle SHA-256 `24a1f47997809da7aeb5ae522ee075f25a9cec1a9c014e4009f4fdfb0f679cab`）。C316とroot `AGENTS.md`の1文だけが違う
- 発行：C316と同じ条件。Claude Code（Sonnet、Opus）は`one_queue_across_cells`、Codex（Sol、Astra）は`one_queue_across_cells_and_prompts`で、C318を制御なし（1文）の追加5回分と同じ待ち行列に混ぜた（制御なしのpoolは累積N=25になった）。計測は2026-10-15 05:19〜05:39 UTC
- 採点：Claude Codeは`claude-collector-v3`、Codexは`v11`。個別の判定記録は2件（SonnetのF10：応答中の否定の「authority_unavailableの条件には当たらず」を停止と誤検知、4点。AstraのF06：探索の失敗で停止、1点）
- 計測したコード：`138e844`

| モデル | プロファイル | result ID |
| --- | --- | --- |
| Sol Low | `c318-click-sol61-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `5e38509652e3428ca499566d4a5d5181` |
| Astra Low | `c318-click-astra6-low-standard14-r4-n5-cli0159-isolated-shellenv-20261015-r1` | `1b8ba6e04ac8424689bdbe9df5450abd` |
| Sonnet low | `c318-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `0b224957f83e401aabf185e649226b4e` |
| Opus low | `c318-click-claude-opus55-low-standard14-r4-n5-cli2288-shellenv-20261015-r1` | `47a306e254a84faa8bc29dbcda77fa05` |
| Sol Low 制御なし（累積N=25） | `free-loaded-click-sol61-low-standard14-r4-n25-cli0159-isolated-shellenv-20261015-r3` | `3028509e6f7d4da586870b72e3f37026` |
| Astra Low 制御なし（累積N=25） | `free-loaded-click-astra6-low-standard14-r4-n25-cli0159-isolated-shellenv-20261015-r3` | `88e5f475f9854c3fb63dc57156c319f4` |

比較したC316：[Sonnet](click-free-loaded-c316-sonnet55-low-standard14-r4-n5_2026-10-14.md)、[Opus](click-free-loaded-c316-opus55-low-standard14-r4-n5_2026-10-14.md)、[Sol・Astra](click-free-loaded-c316-sol61-astra6-low-standard14-r4-n5_2026-10-15.md)のN=5。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-c318-claude-standard14-r4-n5-20261015-r1`、`runs/click-c318-codex-standard14-r4-n5-20261015-r1`（待ち行列の記録は`campaign-round-1/`）、`runs/click-free-loaded-codex-standard14-r4-n25-20261015-r1`
- THE-CAPTIONでの結果：[C318 4モデル](../../../results/c318-four-models-standard14-n5_2026-10-15.md)

このresultは採用、リリース、本体への反映を意味しない。
