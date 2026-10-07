# C287のClaude Code Opus 5.5 medium・Standard14 N=2計測

2026-10-07。利用者の残りトークンの都合により、[PR #332](https://github.com/Kenn-dclxvi/agent-execution-control-lab/pull/332)の全14ケースを各2回、計28件で実施した。**全28件が4点だったが、N=2へ揃えたC280比でトークンは+43.57%、経過時間は+10.13%増えた。コスト改善は確認できなかった。** 除外と再試行は0件で、自動でNを追加していない。

## 条件と比較

Claude Code 2.1.288、`claude-opus-5-5`、推論設定`medium`、並列上限24、全エージェントトークン計上である。C286の条件と同じケース、fixture、TaskSpec、実行ファイル、評価コード、permission、個人設定の隔離、tool、plugin、採点契約を維持し、本文identityとprofile ID、反復数だけを変更した。発行前の照合記録を保存してから28枠を発行した。

比較基準のC280は保存済みプールから各ケース2件を選び、N=2のselection resultへ登録した。C286も保存済みプールから各ケース2件を選び、参考比較にした。両者とも`select-runs`の既定順序で固定し、結果を見て選び直していない。比較相手の新しいモデル実行は行っていない。N=5の中央値とは混ぜていない。

| 条件 | 4点 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値（秒） |
| --- | ---: | ---: | ---: | ---: |
| C280 | 28 / 28 | 100.00 | 1,039,131.0 | 416.25 |
| C286 | 28 / 28 | 100.00 | 1,328,959.5 | 434.23 |
| C287 | 28 / 28 | 100.00 | 1,491,925.5 | 458.42 |

中央値は、14ケース合算の各反復値を2回分集計した値である。トークンにはcacheの読み込みと作成を含む。N=2で観測した結果であり、N=5での再現性は確認していない。実行日時と待ち行列が異なるため、時間差を本文だけの因果効果とは断定しない。

C280比はトークン+43.57%、経過時間+10.13%。両指標の増加を退行として記録する。

C286比はトークン+12.26%、経過時間+5.57%。両指標の増加を退行として記録する。

## 読み取りの診断と判断の限界

変更前のモデル応答はC280が97回、C286が72回、C287が69回だった。一方、変更前のツール結果量は261,518、506,262、637,204バイトだった。範囲指定を含む読み取りは24、13、14回、同じファイルの追加参照は3、14、7回、切り詰められた出力の保存ファイルの参照は1、10、3回だった。C287では応答、読み直し、保存ファイル参照がC286より減った一方、読み取る量は増えていた。この診断だけでトークン増加を単一の原因へ確定しない。

名指しされたファイルがある22件では、最初にツールを呼び出す応答より後に初めて読んだ件数はC280が14件、C286が0件、C287が2件だった。文字列から直接抽出できる読み取りを分類しており、取得内容の完全な証明ではない。subagentは各条件とも0件だった。root以外の本文は変更していない。

採点は固定されたClaude用契約と既存の自動品質監査による。独立した人間の盲検採点ではない。必須コマンドの個別Bash実行を求める評価基盤の指示は変更しておらず、C284の一括検証指示との衝突も今回の比較条件として維持した。command protocol違反は0件、担当と生成者の証跡は28件とも取得不能の診断であり、品質の減点にはしていない。品質を維持するためにコスト増加が必要だったかは、この集計では確認していない。

## 証拠保存と実行時間

全28件を個別登録し、採点時の差分、実行証拠、Claude transcriptを検証済みarchiveへ保存した。標準seal・compactはClaudeのschemaへ対応していないため、既存のClaude系列と同じ汎用archive作成・検証を使用し、元workspaceも保持した。標準seal・compactによるworkspace削除の完了は主張しない。

日本時間2026-10-07 21:19:56〜21:20:47に実行し、待ち行列全体の壁時計時間は50.85秒だった。表の経過時間は各反復の14ケース合算値であり、この壁時計時間とは異なる。実行・採点・比較は完了。追加反復、本文の改訂、採用、release、本体反映は行っていない。

## 個別run

| ケース | 反復 | 得点 | 全エージェントトークン | 経過時間（秒） |
| --- | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 1 | 4 | 20,588 | 15.85 |
| TC-A01-LATENT-MODE-POLICY | 2 | 4 | 20,652 | 17.52 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 1 | 4 | 124,452 | 45.29 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 2 | 4 | 142,461 | 48.93 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 1 | 4 | 170,336 | 46.18 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 2 | 4 | 164,779 | 47.41 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 1 | 4 | 254,997 | 47.33 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 2 | 4 | 173,752 | 41.87 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 1 | 4 | 111,404 | 41.18 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 2 | 4 | 94,994 | 36.15 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 1 | 4 | 229,976 | 44.65 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 2 | 4 | 234,039 | 45.51 |
| TC-F05-CLARIFY-UNITS-MODE | 1 | 4 | 21,754 | 13.59 |
| TC-F05-CLARIFY-UNITS-MODE | 2 | 4 | 21,903 | 13.83 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 1 | 4 | 22,176 | 14.24 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 2 | 4 | 21,520 | 12.00 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 1 | 4 | 152,260 | 40.86 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 2 | 4 | 137,066 | 41.29 |
| TC-F07-CANONICAL-V4-RUNNER | 1 | 4 | 115,466 | 35.25 |
| TC-F07-CANONICAL-V4-RUNNER | 2 | 4 | 117,234 | 35.44 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 1 | 4 | 97,826 | 40.09 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 2 | 4 | 76,018 | 29.85 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 1 | 4 | 125,921 | 35.47 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 2 | 4 | 140,642 | 25.97 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 1 | 4 | 43,786 | 25.17 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 2 | 4 | 43,672 | 26.16 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 1 | 4 | 52,423 | 25.33 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 2 | 4 | 51,754 | 24.43 |

## 一次記録

[登録結果](7a1e630f4a7a41c0aaa4a37e3306e1cb.json)、[条件・集計記録](claude-opus55-c287-standard14-n2-cli2288_2026-10-07.json)、[品質監査](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-quality-audit.json)、[読み取り診断](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-diagnostics.json)、[atomic集計](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-atomic-analysis.json)、[今回のselection](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-selection.json)。

[C280のN2基準result](b23f5f3735d44a0aa79f0c592c995bc7.json)、[C280のselection](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c280-n2-selection.json)、[C280集計](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c280-n2-analysis.json)、[C280比較](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c280-comparison.json)。[C286のselection](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c286-n2-selection.json)、[C286集計](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c286-n2-analysis.json)、[C286比較](claude-opus55-c287-standard14-n2-cli2288_2026-10-07-c286-comparison.json)。
