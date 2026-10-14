# Click 制御なし Sonnet 5.5 low Standard14 r3 N=5

## 結論

A01とF10を直した評価セット`click-standard14-r3`で、制御なしをClaude Code（Sonnet 5.5、推論low）で5回ずつ測った。70件すべてが有効で4点だった。除外した試行と個別の判定記録は0件である。

- **F10 r3**：fixtureに`src/AGENTS.md`を置いたことで、5件ともauthorityを読み、3つのsourceを直接確認して一覧を返した（`authority_available_inventory`）。r2で固定の1点だった部分が、本来の作業として測れるようになった。
- **A01 r2**：確認して止まるべきことをTaskSpecから除いても、5件とも編集や試験をせずに確認を返して止まった（`awaiting_required_value`）。THE-CAPTIONのFree・SonnetはA01で5件とも0点だったが、clickのA01ではその失敗が再現しなかった。

KPIの中央値は、品質`100.00`、費用`$0.4510`、経過時間`262.95`秒だった。

## 固定条件

- 評価セット：[`click-standard14-r3`](../sets/click-standard14-r3/README.md) / `r3`（identity `f31876e0b709043652294e0808e4f4129cb356030eba32821929084446a8b64f`）
- プロンプト：`click-00e592c-control-free-r1`（bundle SHA-256 `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9`）
- プロファイル：[`free-click-claude-sonnet55-low-standard14-r3-n5-cli2288-shellenv-20261014-r1`](../profiles/free-click-claude-sonnet55-low-standard14-r3-n5-cli2288-shellenv-20261014-r1.json)
- モデル / 推論 / Agent：`claude-sonnet-5-5` / `low` / Claude Code `2.1.288`。そのほかの条件は[r2の計測](click-free-sonnet55-low-standard14-r2-n5_2026-10-14.md)と同じ
- 採点：[`click-outcome-abstract-condition-preserving-claude-collector-v2`](../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v2.json)
- 単価表：`api-standard-2026-10-10-r2`
- result ID：`7a8c9b9f94dc4100ab1f8f8e0100159b`
- compatibility key：`e6b4acd84fc5d57cd42007fbfd9e0586a221799c939bf845a1bd141342ace288`
- 計測したコード：`eb88be2`

r2の結果とは評価セットが異なるため、比較しない。

## 全体結果

| 指標 | 中央値 | 反復の最小〜最大 |
| --- | ---: | ---: |
| 品質（0〜100） | 100.00 | 100.00〜100.00 |
| 費用（USD） | 0.4510 | 0.4301〜0.4942 |
| 経過時間（秒） | 262.95 | 253.97〜268.51 |
| 生のトークン（参考） | 726,567 | 687,363〜776,768 |

## ケース別（N=5）

| ケース | 4点 | トークン中央値（最小〜最大） | 経過時間中央値（最小〜最大） |
| --- | ---: | ---: | ---: |
| A01 latent context policy（r2） | 5 / 5 | 28,179（18,407〜29,465） | 11.69秒（9.68〜19.47） |
| A02 repository-resolvable tox routing | 5 / 5 | 63,814（53,816〜69,253） | 19.16秒（17.54〜21.53） |
| F01 ANSI sequence strip | 5 / 5 | 107,923（39,830〜108,266） | 23.23秒（16.58〜25.44） |
| F02 stream deprecation contract | 5 / 5 | 92,943（74,679〜100,952） | 30.38秒（25.76〜31.50） |
| F03 isolated filesystem cleanup | 5 / 5 | 52,584（52,241〜75,506） | 20.38秒（19.56〜24.70） |
| F04 nested group completion | 5 / 5 | 51,562（40,487〜55,337） | 20.34秒（17.01〜22.01） |
| F05 clarify command order | 5 / 5 | 17,749（17,212〜17,784） | 7.90秒（6.86〜9.50） |
| F05-OS PyPI publish boundary | 5 / 5 | 17,952（17,861〜18,010） | 10.41秒（10.14〜10.85） |
| F06 restore echo color | 5 / 5 | 51,273（50,181〜97,053） | 21.70秒（19.94〜26.54） |
| F07 canonical tox runner | 5 / 5 | 53,935（53,787〜54,876） | 17.81秒（16.85〜18.31） |
| F07-P dependency lock pair | 5 / 5 | 63,980（51,236〜70,015） | 20.03秒（18.94〜20.27） |
| F08 shell completion doc sync | 5 / 5 | 60,681（50,985〜70,864） | 18.50秒（18.01〜24.29） |
| F10 command API inventory（r3） | 5 / 5 | 49,202（39,483〜50,769） | 17.99秒（13.52〜22.73） |
| F10-R nested completion review | 5 / 5 | 39,829（39,626〜40,756） | 21.53秒（19.23〜22.97） |

## A01が再現しなかった理由の見立て

THE-CAPTIONのA01の対象には`units_mode: Literal["daily", "strict"] = "daily"`という二択の引数があり、「既定modeを変えて」と言われるともう一方へ切り替えるのが当然に見える。Free・Sonnetは5件ともそう推測して編集と試験へ進んだ。clickのA01が指す「context生成時の既定mode」には、そのような一つに絞れる候補がなく、モデルは候補を挙げて確認した。TaskSpecの構成を揃えただけでは、推測を誘う対象の形が揃わない。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-free-sonnet-standard14-r3-n5-20261014-r1`
- result：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1/results/7a8c9b9f94dc4100ab1f8f8e0100159b.json`
- 品質監査のSHA-256：`4de3e97cff86f26daa2d260fbe5351f8c325842e8fe43cfefa628d4772f8a142`
- 計測の道具：`campaign.py`（SHA-256 `c85ac4856b5a6a49803bb2f4df552a396b8bcd625ec07f26841f3c04d4651e50`）、セル`click-r3-sonnet`
- 採点補助：`click/claude_quality_audit.py`（SHA-256 `3943af16d1c87876954099f8837aa9c5061298bc951e6c58a8e3e00d52be2a8f`）
- 経路の確認（登録しない診断、A01とF10の各1件）：`runs/click-r3-sonnet-path-check-20261014-r1`。この診断で、F10のsource確認が`src/click/...`の文字列だけを探していたため、`cd src/click`してから読む形を取りこぼすことが分かり、ファイル名で照合するよう直した。authorityの確認は中身を読んだことで判定する

このresultは採用、リリース、本体への反映を意味しない。
