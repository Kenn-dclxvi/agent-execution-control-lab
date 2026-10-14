# Click 制御なし Sonnet 5.5 low Standard14 r2 N=5

## 結論

制御プロンプトを置かない条件で、ClickのStandard14 r2をClaude Code（Sonnet 5.5、推論low）で5回ずつ測った。70件すべてが有効で採点でき、F10以外の13ケースは65件すべてが4点だった。F10の5件は、Repository Authority（`src/AGENTS.md`）がないため`authority_unavailable`で停止し、既存の契約どおり1点だった。除外した試行、再実行、個別の判定記録はいずれも0件である。

KPIの中央値は、品質`94.64`、費用`$0.4157`、経過時間`264.81`秒だった。これはClickでClaude Codeを測った最初の結果で、THE-CAPTIONのC316と同じ計測経路と単価表で集計した。今後ClickでCandidateをSonnetで測るときの基準になる。

## 固定条件

- 評価セット：`click-standard14-r2` / `r2`（identity `bbba58d8eb5c3dc6719a155d031d886917c2fed7bec19faf9a43dd65705f7ebe`）。2026-07-31のC125の計測で固定したLayer 1を、変更せずに評価セットの保管場所へ登録し、そこから複製した
- プロンプト：`click-00e592c-control-free-r1`（bundle SHA-256 `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9`）。中身は空のルート`AGENTS.md`だけで、Claude Codeが読む`CLAUDE.md`は置いていない
- プロファイル：[`free-click-claude-sonnet55-low-standard14-r2-n5-cli2288-shellenv-20261014-r1`](../profiles/free-click-claude-sonnet55-low-standard14-r2-n5-cli2288-shellenv-20261014-r1.json)
- モデル / 推論：`claude-sonnet-5-5` / `low`
- Agent / CLI：Claude Code `2.1.288`。個人設定の切り離し、シェル環境（`fixed-path-workspace-venv-r1`）、使用量の数え方（`claude-v1`）、許可（`bypassPermissions`）は、THE-CAPTIONのC316までのSonnetセルと同じ
- 対象側の条件：ケース、TaskSpec、対象のcommit（`pallets/click` `00e592c`）、必須コマンド、Python環境（`0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`）は、C125のプロファイルと同じ
- 採点：[`click-outcome-abstract-condition-preserving-claude-collector-v1`](../rating-contracts/click-outcome-abstract-condition-preserving-claude-collector-v1.json)。v10のケース規則をそのまま使い、証跡の収集だけをClaude Codeのtranscriptに差し替えた
- 発行：全セルで一つの待ち行列、合計24本まで、負荷を見て発行（`cpu_busy_below` r1）
- 単価表：`api-standard-2026-10-10-r2`
- result ID：`4a03de7bfa7d47b59e94104f78f58227`
- compatibility key：`2f20ee67b5d6b0212b8f4d1013676025b4227ff532b8e58504c6d40756327314`
- 計測したコード：`3553d32`

推論の強さは、Clickの通常比較で使ってきた`medium`ではなく、THE-CAPTIONのSonnetセルと同じ`low`にした。そのため、7月のCodex（`gpt-5.6-sol`、`medium`）の結果とは、モデル、推論、Agentのいずれも異なり、比較しない。

## 全体結果

| 指標 | 中央値 | 反復の最小〜最大 |
| --- | ---: | ---: |
| 品質（0〜100） | 94.64 | 94.64〜94.64 |
| 費用（USD） | 0.4157 | 0.3966〜0.4708 |
| 経過時間（秒） | 264.81 | 248.92〜269.75 |
| 生のトークン（参考） | 646,050 | 628,858〜702,932 |

| 項目 | 結果 |
| --- | ---: |
| 有効 / 採点可能 | `70 / 70` |
| 点数の分布 | 4点 65件、1点 5件 |
| F10の経路 | `authority_unavailable` 5件 |
| 除外した試行 | 0件 |
| 個別の判定記録 | 0件 |
| 待ち行列全体の実行時間 | 204.88秒 |

## ケース別（N=5）

経過時間は各runの実行時間で、全体の経過時間（14ケースの合計）とは別の値である。

| ケース | 4点 | トークン中央値（最小〜最大） | 経過時間中央値（最小〜最大） |
| --- | ---: | ---: | ---: |
| A01 latent context policy | 5 / 5 | 18,251（17,789〜18,326） | 9.81秒（8.87〜23.17） |
| A02 repository-resolvable tox routing | 5 / 5 | 65,477（53,252〜79,505） | 23.07秒（18.43〜24.73） |
| F01 ANSI sequence strip | 5 / 5 | 39,863（39,486〜40,141） | 18.05秒（17.10〜22.56） |
| F02 stream deprecation contract | 5 / 5 | 99,287（78,471〜127,156） | 33.28秒（27.77〜47.42） |
| F03 isolated filesystem cleanup | 5 / 5 | 52,833（52,554〜53,046） | 20.33秒（19.85〜20.98） |
| F04 nested group completion | 5 / 5 | 40,954（40,299〜55,189） | 18.95秒（15.85〜20.50） |
| F05 clarify command order | 5 / 5 | 17,644（17,561〜17,802） | 8.30秒（6.98〜9.71） |
| F05-OS PyPI publish boundary | 5 / 5 | 17,995（17,905〜18,022） | 10.50秒（10.23〜15.79） |
| F06 restore echo color | 5 / 5 | 61,478（51,565〜87,913） | 22.92秒（22.13〜29.84） |
| F07 canonical tox runner | 5 / 5 | 53,892（52,927〜55,109） | 18.26秒（17.84〜21.09） |
| F07-P dependency lock pair | 5 / 5 | 64,856（54,156〜78,580） | 20.71秒（19.28〜27.22） |
| F08 shell completion doc sync | 5 / 5 | 50,833（40,391〜62,536） | 17.04秒（13.17〜21.07） |
| F10 command API inventory | 0 / 5 | 18,496（18,417〜37,968） | 9.55秒（8.64〜14.30） |
| F10-R nested completion review | 5 / 5 | 39,998（39,187〜54,930） | 19.07秒（16.43〜20.67） |

F10は品質の後退ではない。TaskSpecが求めるRepository Authorityがバンドルにないため、sourceだけから推測せずに停止する固定の経路である。5件とも、未完了の項目としてCLICK-F10-C1とC2を挙げ、指定された3つのsourceを読まずに止まっていた。

## 採点の方法

採点補助は、7月のCodex用の監査（`audit_click_standard14*.py`）と同じ規則を、Claude Codeの証跡の置き場所に合わせて書き直したものである。変更されたpath、必須コマンドの成否、禁止された試験や公開操作の有無を機械的に確かめ、確認を返すケースやレビューのケースでは応答を語句で読む。語句の読み取りで条件を満たさないrunがあれば、そのrunの証跡を契約に照らして読み、判定記録を残さない限り点数を確定しない作りにした。今回はそうしたrunがなく、判定記録は0件だった。F10は、`authority_unavailable`で停止し、未完了の項目を挙げ、sourceを読まず（Bashのコマンドと`Read`ツールの両方を確認）、変更がなければ1点とする。

## 証拠

- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/click-free-sonnet-standard14-r2-n5-20261014-r1`
- result：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1/results/4a03de7bfa7d47b59e94104f78f58227.json`
- 品質監査のSHA-256：`be197ad0fb8f4185fea94beaf7ebb17bb9c3cb73d8c65707eb7b4da9fbffc817`
- 計測の道具：`campaign-tools/single-prompt-r1/campaign.py`（SHA-256 `b61c928fc1effc190f1914cff34bb0ab0a3d0611c1bbc41dba0248089c18540e`）、セル`click-sonnet`
- 採点補助：`campaign-tools/single-prompt-r1/click/claude_quality_audit.py`（SHA-256 `587e241e0b043008715f6c6fbcdbce123c39f41501012a296d31be5c59c836b4`）
- 元のプロファイルと雛形の作成：`campaign-tools/single-prompt-r1/click/derive_sonnet_base.py`（SHA-256 `ccaf6599dd71df87e5f9a04d6d0712219d31d565856620c087954eec2f121e7e`）
- 経路の確認（登録しない診断、4ケース各1件）：`runs/click-sonnet-path-check-20261014-r1`

このresultは、ClickでSonnet 5.5 lowの制御なしの基準を測ったことを示す。採用、リリース、本体への反映は意味しない。
