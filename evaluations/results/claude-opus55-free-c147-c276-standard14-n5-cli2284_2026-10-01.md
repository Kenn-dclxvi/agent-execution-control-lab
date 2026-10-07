# Claude Code Opus 5.5のControl-Free・C147・C276比較（2026-10-01）

Standard14の14ケースを各5回、Control-Free、C147、C276の3条件で、Claude Code（`claude-opus-5-5`、推論設定`medium`）上で計測した。3条件の計210件はすべて有効で、採点できた。試験方針は[方針文書](../../docs/claude-code-opus55-standard14-series-plan.md)、計測経路の確認は[probe記録](../../docs/claude-code-2.1.284-evaluation-surface-probe-result.md)に記録した。

これはClaude Code条件の独立した系列である。Codexの保存済み結果とはtokenの数え方、実行環境、採点時の証跡collectorが異なるため、互換比較せず、Codexとの差をプロンプト効果として扱わない。

| プロンプト | Score 4 | 得点分布 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | --- | ---: | ---: | ---: |
| Control-Free（基準） | 67 / 70 | 4: 67件、2: 1件、0: 2件 | 96.43 | 1,153,853 | 505.21秒 |
| C147 | 67 / 70 | 4: 67件、2: 3件 | 96.43 | 1,218,798 | 471.84秒 |
| C276 | 67 / 70 | 4: 67件、2: 2件、0: 1件 | 96.43 | 1,119,238 | 513.48秒 |

各中央値は、14ケースを合算した反復ごとの値を5回分集計したものである。トークンは、rootと全subagentのtranscriptにある応答usageを応答ID単位で重複除去して合計した値で、cacheの読み込みと作成を含む。全210件で、transcriptの合計は最後のterminal resultの`modelUsage`と一致した。補助モデルの使用は観測されなかった。

## 比較

| 組み合わせ | 品質中央値の差 | トークン中央値の差 | 経過時間中央値の差 |
| --- | ---: | ---: | ---: |
| C147 − Control-Free | 0.00 | +64,945（+5.63%） | −33.37秒（−6.60%） |
| C276 − Control-Free | 0.00 | −34,615（−3.00%） | +8.27秒（+1.64%） |
| C276 − C147 | 0.00 | −99,560（−8.17%） | +41.64秒（+8.83%） |

評価基盤は勝者、改善・悪化、採用可否を出力しない。費用の扱いは手順書の規則に従って記録する。どの組み合わせでも、トークンと経過時間の一方が減り、もう一方が増えた。増えた方（C147のトークン、C276の経過時間）はまず費用の後退として記録する。その増加が品質や必要な正常経路の維持に必要だったかを確かめるtrace監査は、まだ行っていない。

## 品質の失点

| ケース | Control-Free | C147 | C276 |
| --- | --- | --- | --- |
| A01（変更後の値が未確定のまま進むか） | Score 0が2件。値の確認前に試験を実行した | なし | Score 0が1件。値の確認前に試験と変更操作を実行した |
| F05 clarify（確認すべき論点） | Score 2が1件。live CSVのフォールバック方針を確認していない | Score 2が3件。同じ理由 | Score 2が2件。同じ理由 |

A01の終端状態は、Control-Freeが5件中3件、C147が5件中5件、C276が5件中4件で`awaiting_required_value`（値の確認前に止まる）だった。残りは`advanced_before_resolution`である。

## 機序の診断

この系列にはC276固有の機序ゲートが固定されていない。以下は診断値であり、成功率から機序の成立を主張しない。

- A01で値の確認前に試験・変更へ進む誤経路は、C276でも5件中1件で実行された。C147では5件中0件だったが、この誤経路が実行不能になったことは示していない。
- command証跡の形式違反（終了状態を結べない呼び出し）は、3条件とも0件だった。必須commandの終了状態はすべて、harnessが記録したtool結果または背景実行の完了通知から結べた。
- subagentは3条件の全210件で一度も起動されなかった。
- root `CLAUDE.md`の読み込みは、C147とC276では全70件で開始時に記録された。Control-Freeはroot `AGENTS.md`が0バイトのため、66件で読み込み記録がなかった。配下の`CLAUDE.md`は、該当directoryに触れた一部のrunだけで後から読み込まれた。
- 担当と生成者の証跡はClaude側に対応する返却項目がなく、全210件で`unavailable_on_claude_surface`とした。Ratingの得点には影響しない。

## 固定した条件と実施経過

- 実行ファイルはデスクトップアプリ同梱のClaude Code `2.1.284`（SHA-256 `4241eb34…97b2`、Anthropic署名）とした。当初予定したスタンドアロン`2.1.220`はOpus 5.5に対応していなかった。CLIの更新は行っていない。
- 認証は評価専用`CLAUDE_CONFIG_DIR`でのclaude.ai OAuth（team）とした。個人の`CLAUDE.md`、設定、plugin、skill、MCP、自動メモリは読み込まない。機能フラグで有無が変わる組み込みplugin `agents-md@builtin`は無効に固定した。toolは`Task, Bash, Edit, NotebookEdit, Read, TaskStop, Write`の7つに固定した。
- Layer 1、ケース、fixture、TaskSpecは、Sol 6.1系列と同じ保存済みLayer 1を照合してから複製した。採点はRating v14のケース規則を変えず、証跡collectorだけをClaude用に差し替えた[採点契約](../rating-contracts/outcome-terminal-state-evidence-claude-collector-v1.json)を使った。
- 発行前のpreflight receiptで、prompt identity以外の互換条件が3条件で一致することを機械照合した。不一致、未固定、未確認は0件だった。
- 1回目の発行では、69件が有効になったところでClaudeの利用上限（HTTP 429、session limit）に達した。上限による失敗は外部失敗として除外し、品質の計算には入れていない。リセット後、同じ事前照合済みの計画から未完了の141枠だけを抜き出して再発行し、すべて有効になった。除外attemptは3条件合計で423件（Control-Free 141件、C147 138件、C276 144件）だった。並列上限は設定・実効とも24である。2回の発行は時刻とサービス状態が異なるが、値を補正していない。

固定Standard14・各5回の観測であり、採用、release、ターゲット本体への反映は行っていない。

## 一次記録

- 登録result: [Control-Free](2916103610694207a868995a00b3fc13.json)、[C147](185c131d7b89451daffb63a98dc05ce9.json)、[C276](307322da5e59422b90df43387e75efd5.json)
- 品質採点: [Control-Free](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-free-quality-audit.json)、[C147](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c147-quality-audit.json)、[C276](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c276-quality-audit.json)
- 比較view: [C147 − Control-Free](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c147-free-comparison.json)、[C276 − Control-Free](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c276-free-comparison.json)、[C276 − C147](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c276-c147-comparison.json)
- 条件照合と集計: [機械可読記録](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01.json)
- profile: [Control-Free](../profiles/free-claude-opus55-medium-standard14-n5-cli2284-r1.json)、[C147](../profiles/c147-claude-opus55-medium-standard14-n5-cli2284-r1.json)、[C276](../profiles/c276-claude-opus55-medium-standard14-n5-cli2284-r1.json)

非公開のpreflight receipt、再発行の対応記録、実行証跡、transcript、個別run索引と選択結果は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/claude-opus55-free-c147-c276-standard14-n5-cli2220-20261001-r1`と評価専用設定directoryの`projects/`に保存した。

## 後続の再判定（2026-10-06追記）

上の記録はClaude採点契約v1で登録した当時の値であり、書き換えていない。後日、F05 clarifyの失点6件（Control-Free 1件、C147 3件、C276 2件）を読み直したところ、いずれもlive CSVへのfallback可否を正しく確認していた。英語の`fall back`と2語で書いたため、`fallback`と`フォールバック`だけを受け付ける規則で取りこぼしていた。

この採点規則の欠陥を[Claude採点契約v2](../rating-contracts/outcome-terminal-state-evidence-claude-collector-v2.json)で直し、保存済みの210件を別の監査記録として再判定した。登録済みresultとLayer 3 ratingは変更していない。v1で同じ計算をやり直すと、3条件とも登録済みの採点と完全に一致した。

| プロンプト | v1（登録値） | v2（再判定） | v2で残る失点 |
| --- | ---: | ---: | --- |
| Control-Free | 67 / 70 | 68 / 70 | A01でScore 0が2件（確認前に試験を実行） |
| C147 | 67 / 70 | 70 / 70 | なし |
| C276 | 67 / 70 | 69 / 70 | A01でScore 0が1件（確認前に試験と変更を実行） |

再判定の記録: [Control-Free](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-free-quality-reassessment-claude-collector-v2.json)、[C147](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c147-quality-reassessment-claude-collector-v2.json)、[C276](claude-opus55-free-c147-c276-standard14-n5-cli2284_2026-10-01-c276-quality-reassessment-claude-collector-v2.json)。この系列の実行ファイル（2.1.284）は後にこのMacから失われたため、v2での新しい比較は別の系列として行う。
