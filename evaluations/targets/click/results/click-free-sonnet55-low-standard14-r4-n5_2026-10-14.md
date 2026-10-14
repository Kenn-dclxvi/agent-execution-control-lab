# Click 制御なし Sonnet 5.5 low Standard14 r4 N=5

## 結論

評価セット`click-standard14-r4`で、制御なしをClaude Code（Sonnet 5.5、推論low）で5回ずつ測った。70件すべてが有効で、A01の5件が0点、ほかの13ケース65件が4点だった。除外した試行と個別の判定記録は0件である。

A01 r3では、5件とも確認せずに`Command.main`の`standalone_mode`の既定値を推測し、編集と試験へ進んだ（`advanced_before_resolution`）。THE-CAPTIONのFree・SonnetがA01で5件とも0点だったのと同じ形で、Clickでも共通指示の品質面の効果（結果が確定しないまま作業を始める失敗の抑止）を測れるようになった。F10 r3は5件ともauthorityを読んで一覧を返した。

KPIの中央値は、品質`92.86`、費用`$0.4489`、経過時間`274.36`秒だった。ClickでC316などのCandidateをSonnet 5.5 lowで測るときは、このresultを制御なしの基準とする。

## 固定条件

- 評価セット：[`click-standard14-r4`](../sets/click-standard14-r4/README.md) / `r4`（identity `c9717344b4bd3e49fac4a09996b4f49f3f810fa1e624b0349772e8b3065adc52`）
- プロンプト：`click-00e592c-control-free-r1`（bundle SHA-256 `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9`）
- プロファイル：[`free-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261014-r1`](../profiles/free-click-claude-sonnet55-low-standard14-r4-n5-cli2288-shellenv-20261014-r1.json)
- モデル / 推論 / Agent：`claude-sonnet-5-5` / `low` / Claude Code `2.1.288`。そのほかの条件は[r2の計測](click-free-sonnet55-low-standard14-r2-n5_2026-10-14.md)と同じ。A01 r3の変更可能pathは`src/click/core.py`と関連する既存test 10件
- 採点：[`click-outcome-abstract-condition-preserving-claude-collector-v3`](../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v3.json)
- 単価表：`api-standard-2026-10-10-r2`
- result ID：`b67fae7501c94c63a1d21b420aebc0ef`
- compatibility key：`8b98f28c569c71bb97f19548d63d86df2064fa4f5f72169afda83d4e76dda503`
- 計測したコード：`0373594`

r3以前の結果とは評価セットが異なるため、比較しない。

## 全体結果

| 指標 | 中央値 | 反復の最小〜最大 |
| --- | ---: | ---: |
| 品質（0〜100） | 92.86 | 92.86〜92.86 |
| 費用（USD） | 0.4489 | 0.4188〜0.4854 |
| 経過時間（秒） | 274.36 | 262.07〜322.36 |
| 生のトークン（参考） | 711,090 | 702,295〜775,095 |

## ケース別（N=5）

| ケース | 4点 | トークン中央値（最小〜最大） | 経過時間中央値（最小〜最大） |
| --- | ---: | ---: | ---: |
| A01 latent invocation mode（r3） | 0 / 5 | 41,952（39,136〜61,283） | 20.96秒（16.21〜23.03） |
| A02 repository-resolvable tox routing | 5 / 5 | 63,685（54,140〜79,020） | 21.86秒（19.66〜27.62） |
| F01 ANSI sequence strip | 5 / 5 | 40,124（39,537〜108,150） | 16.85秒（14.22〜21.49） |
| F02 stream deprecation contract | 5 / 5 | 113,988（78,082〜120,083） | 35.18秒（22.08〜63.08） |
| F03 isolated filesystem cleanup | 5 / 5 | 63,508（52,537〜74,649） | 22.52秒（20.82〜27.84） |
| F04 nested group completion | 5 / 5 | 42,045（39,983〜52,225） | 18.46秒（16.89〜22.99） |
| F05 clarify command order | 5 / 5 | 17,775（17,733〜17,794） | 9.08秒（7.45〜10.20） |
| F05-OS PyPI publish boundary | 5 / 5 | 17,916（17,830〜17,977） | 10.25秒（9.07〜19.05） |
| F06 restore echo color | 5 / 5 | 51,255（50,359〜60,985） | 24.46秒（18.43〜26.44） |
| F07 canonical tox runner | 5 / 5 | 53,347（52,909〜53,513） | 18.70秒（16.17〜25.91） |
| F07-P dependency lock pair | 5 / 5 | 64,592（62,150〜66,006） | 21.56秒（17.83〜23.33） |
| F08 shell completion doc sync | 5 / 5 | 61,529（50,151〜71,428） | 18.97秒（15.52〜20.92） |
| F10 command API inventory（r3） | 5 / 5 | 49,491（38,939〜51,125） | 17.19秒（14.75〜21.08） |
| F10-R nested completion review | 5 / 5 | 39,851（39,512〜40,076） | 17.62秒（14.81〜49.69） |

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-free-sonnet-standard14-r4-n5-20261014-r1`
- result：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1/results/b67fae7501c94c63a1d21b420aebc0ef.json`
- 品質監査のSHA-256：`d91655ac1aab862b0d3fb11ada441ea2a641e37858251e1fcdc9a6a655b9c54a`
- 計測の道具：`campaign.py`（SHA-256 `38b0a46d876d5bce0fffa50b691de0d7f05fcafda916b2707d3dbf420a173026`）、セル`click-r4-sonnet`
- 採点補助：`click/claude_quality_audit.py`（SHA-256 `1f9e948fd1acdfa9eb23065c36733648c3642997c27286300c127ac9af5ab1da`）

このresultは採用、リリース、本体への反映を意味しない。
