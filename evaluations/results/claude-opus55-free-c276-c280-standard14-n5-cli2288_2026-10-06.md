# Claude Code Opus 5.5のControl-Free・C276・C280比較（2026-10-06）

Standard14の14ケースを各5回、Control-Free、C276、C280の3条件で、Claude Code 2.1.288（`claude-opus-5-5`、推論設定`medium`）上で計測した。3条件の計210件はすべて有効で、採点できた。C280の設計は[設計記録](../../docs/candidate280-outcome-binding-closure-design.md)に、計測前に固定した。

2026-10-01の系列で使った実行ファイル2.1.284がこのMacから失われたため、この系列は3条件をすべて新しく測った独立の系列である。2026-10-01の結果とは比較せず、旧系列との差をプロンプトの効果として扱わない。

| プロンプト | Score 4 | 得点分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | --- | ---: | ---: | ---: |
| Control-Free（基準） | 68 / 70 | 4: 68件、0: 2件 | 100.00 | 1,196,005 | 501.72秒 |
| C276 | 70 / 70 | 4: 70件 | 100.00 | 1,057,346 | 431.57秒 |
| C280 | 70 / 70 | 4: 70件 | 100.00 | 1,058,318 | 448.52秒 |

各中央値は、14ケースを合算した反復ごとの値を5回分集計したものである。トークンは、rootと全subagentのtranscriptにある応答usageを応答ID単位で重複除去して合計した値で、cacheの読み込みと作成を含む。

## 比較

| 組み合わせ | 品質中央値の差 | トークン中央値の差 | 経過時間中央値の差 |
| --- | ---: | ---: | ---: |
| C280 − C276（主比較） | 0.00 | +972（+0.09%） | +16.95秒（+3.93%） |
| C280 − Control-Free | 0.00 | −137,687（−11.51%） | −53.20秒（−10.60%） |
| C276 − Control-Free | 0.00 | −138,659（−11.59%） | −70.14秒（−13.98%） |

評価基盤は勝者、改善・悪化、採用可否を出力しない。手順書の規則に従うと、C280はC276に対して品質が同じで、トークンと経過時間がともに増えたため、費用の後退として記録する。増加幅はトークン0.09%、経過時間3.93%である。C280とC276は、どちらもControl-Freeに対してトークンと経過時間がともに減った。

## 品質の失点

Control-FreeのA01で2件がScore 0だった。どちらも変更後の値を確認する前に試験を実行していた（`advanced_before_resolution`、変更操作はなし）。C276とC280に失点はなかった。

F05 clarifyは3条件とも全件Score 4だった。この系列はClaude採点契約v2で採点しており、英語の`fall back`による確認も受け付けている。

## 機序の診断

以下は3 KPIの差の原因を調べるための診断値で、独立した合否条件ではない。

**A01の終わり方**

| 条件 | 確認待ちで停止 | 確認前に試験 | 推測で変更 | ツール呼び出し数（各run） | トークン中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| Control-Free | 3 | 2 | 0 | 7, 4, 4, 6, 7 | 91k | 51秒 |
| C276 | 5 | 0 | 0 | 3, 2, 2, 2, 3 | 32k | 32秒 |
| C280 | 5 | 0 | 0 | 1, 1, 1, 1, 1 | 19k | 21秒 |

- C280は5件とも、依頼が指定した開始状態の確認だけを行い、対象コードを読まずに未確定の値を確認して終えた。設計どおり、結果が未確定の間の調査・試験・変更は一度も起きなかった。
- C276も今回は5件とも確認待ちで止まったが、各runで対象コードを1〜2回読んでいた。2026-10-01の系列で観測した、消去法で値を補って変更へ進む経路は、今回のN=5では再現しなかった。そのため、この系列ではC276とC280の品質差は観測されていない。
- C280のA01では、C276よりトークン中央値が約13k、経過時間中央値が約11秒少なかった。

**A01以外の経路**

- C280で、結果が明示されたケースに新しい停止や確認は起きなかった。A01以外の12ケースは3条件とも全件Score 4だった。
- C280の経過時間の増加は、主にF06とA02に現れた。F06の経過時間は3条件とも約30秒と約64秒の二つに分かれる。遅いrunでは、時間のかかる試験をharnessが自動で背景実行に切り替え、その完了を待っていた（完了通知が2回記録された）。モデルが背景実行を指定した例はなかった。この待ちに当たった回数は、Control-Freeが5回中2回、C276が1回、C280が3回である。
- A02では、C280のトークン中央値が83k（C276は64k、Control-Freeは80k）、経過時間中央値が43秒（C276は31秒）だった。全件Score 4で停止や確認はなく、ツール呼び出し数の中央値は5（C276は4）だった。差はこの1ケースの5回に限った観測で、原因はまだ特定していない。

**その他**

- subagentは3条件の全210件で起動されなかった。
- 担当と生成者の証跡は、Claude側に対応する返却項目がないため、全210件で`unavailable_on_claude_surface`とした。得点には影響しない。

## 固定した条件と実施経過

- 実行ファイルはデスクトップアプリ同梱のClaude Code 2.1.288（SHA-256 `73f02668…e775`、Anthropic署名）を、アプリの更新で消えないよう評価用ディスクへ複製して固定した。各runの開始時にSHA-256とversionを照合した。
- 認証は評価専用`CLAUDE_CONFIG_DIR`でのclaude.ai OAuth（team）とした。ログインが切れていたため、計測前に利用者が再ログインした。個人の`CLAUDE.md`、設定、plugin、skill、MCP、自動メモリは読み込まない。toolは`Task, Bash, Edit, NotebookEdit, Read, TaskStop, Write`の7つに固定した。
- 組み込みpluginは`cc-plugin-sec-default@builtin`と`cc-plugin-telemetry@builtin`の2つに固定した。`cc-plugin-sec-default`はTeam組織で強制されるポリシー層で、利用者側の設定では無効化できない。2.1.284の系列にはなかった項目であり、3条件に共通の実行環境として扱う。機能フラグで出入りする他の組み込みplugin（`plugin-authoring`など）は、flag settingsで無効にした。
- Layer 1、ケース、fixture、TaskSpecは、2026-10-01の系列と同じ保存済みLayer 1を照合してから複製した。採点は[Claude採点契約v2](../rating-contracts/outcome-terminal-state-evidence-claude-collector-v2.json)を使った。
- 発行前のpreflight receiptで、prompt identity以外の互換条件が3条件で一致することを機械照合した。不一致、未固定、未確認は0件だった。
- 1回目の発行では、115件が有効になったところでClaudeの利用上限（HTTP 429、session limit）に達した。上限による失敗は外部失敗として除外し、品質の計算には入れていない。上限の解除後、同じ事前照合済みの計画から未完了の95枠だけを再発行し、すべて有効になった。除外attemptは3条件合計で285件（Control-Free 93件、C276 90件、C280 102件）である。並列上限は24とした。2回の発行は時刻とサービス状態が異なるが、値を補正していない。
- 1回目の再発行は、評価枠を発行する前に設定隔離の確認で止まった。上限の解除を確かめるため、評価用のフラグを付けずにCLIを起動したことで、アカウントに同期されたpluginとskillが設定directoryへ作成されたためである。正式runがすべて終わった後の作成で、計測済みのrunには影響しない。作成された2つのdirectoryを削除し、隔離確認が通ることを確かめてから再発行した。

固定Standard14・各5回の観測であり、採用、release、ターゲット本体への反映は行っていない。

## 一次記録

- 登録result: [Control-Free](aff3ca28282a452bb75b004506dfa1e1.json)、[C276](b3a245079bb94501a58c1fa5e08ec8c6.json)、[C280](10a2d444d80f4987a6a4d74e22fb8937.json)
- 品質採点: [Control-Free](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-free-quality-audit.json)、[C276](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-c276-quality-audit.json)、[C280](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-c280-quality-audit.json)
- 比較view: [C280 − C276](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-c280-c276-comparison.json)、[C280 − Control-Free](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-c280-free-comparison.json)、[C276 − Control-Free](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06-c276-free-comparison.json)
- 条件照合と集計: [機械可読記録](claude-opus55-free-c276-c280-standard14-n5-cli2288_2026-10-06.json)
- profile: [Control-Free](../profiles/free-claude-opus55-medium-standard14-n5-cli2288-r1.json)、[C276](../profiles/c276-claude-opus55-medium-standard14-n5-cli2288-r1.json)、[C280](../profiles/c280-claude-opus55-medium-standard14-n5-cli2288-r1.json)
- Candidate: [C280 bundle](../../prompts/candidates/the-caption-3ce91a4-execution-control-outcome-binding-r1/manifest.json)

非公開のpreflight receipt、再発行の対応記録、実行証跡、transcript、個別run索引と選択結果は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/claude-opus55-free-c276-c280-standard14-n5-cli2288-20261006-r1`と評価専用設定directoryの`projects/`に保存した。
