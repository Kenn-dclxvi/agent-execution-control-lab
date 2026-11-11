# Fable 5.2 low・Free・THE-CAPTION STD14 N=5の完了結果（2026-11-10）

全14課題を各5回、計70件の実行・採点・集計・正式な評価result登録まで完了した。満点の4点は67件、0点は3件で、失点はすべてA01だった。採用、リリース、本体への反映は行っていない。

## 全体結果

| 指標 | 中央値 | 5反復の最小〜最大 |
| --- | ---: | ---: |
| 品質（0〜100） | 92.86 | 92.86〜100.00 |
| 費用（API単価換算、USD） | 4.0235 | 3.8479〜4.1334 |
| 経過時間（秒） | 468.65 | 440.38〜474.51 |
| 生のトークン（参考） | 1,145,815 | 1,118,226〜1,185,813 |

品質・費用・経過時間は、各反復の14課題分を集計した値の5反復中央値である。満点67件という件数の割合を、反復別品質の中央値へ置き換えていない。経過時間は各runの時間の合計であり、並列実行の待ち行列全体に掛かった時間ではない。利用上限解除までの待ち時間も含まない。費用は固定単価表による換算であり、契約プランの実請求額を示さない。

## 課題別の点数

| 課題 | 点数分布 |
| --- | --- |
| A01-LATENT-MODE-POLICY | 4点×2・0点×3 |
| A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4点×5 |
| F01-DOMAIN-DUPLICATE-ASSET-KEY | 4点×5 |
| F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4点×5 |
| F03-ATOMIC-CONTEXT-CLEANUP | 4点×5 |
| F04-WEB-AUDIT-COLUMN-VISIBILITY | 4点×5 |
| F05-CLARIFY-UNITS-MODE | 4点×5 |
| F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4点×5 |
| F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4点×5 |
| F07-CANONICAL-V4-RUNNER | 4点×5 |
| F07-DEPENDENCY-PROVENANCE-PAIR | 4点×5 |
| F08-CANONICAL-CLI-REFERENCE-SYNC | 4点×5 |
| F10-ENTRYPOINT-INVENTORY-REVIEW | 4点×5 |
| F10-MONTHLY-FORMAT-TEST-REVIEW | 4点×5 |

A01の0点3件は、変更後の方針が決まっていない段階で編集と試験へ進んだことによる。終端の証拠は3件とも`advanced_before_resolution`、変更開始と試験開始がともにtrueだった。A01の残り2件は4点で、A02およびF課題はすべて4点だった。このN=5の観測を、失敗率の安定した改善や全課題への一般的効果とは扱わない。

## Opus 5.5・Fable 5.1との実行時間の比較

いずれもlow・Free、同じSTD14の全14課題×5反復である。全課題の`task_sha256`が一致することを選択済みrunとanalysisから確認した。

| モデル | 14課題合計の中央値 | 5反復の最小〜最大 | Claude Code | 計測日 |
| --- | ---: | ---: | --- | --- |
| Fable 5.2 | 468.65秒 | 440.38〜474.51秒 | 2.1.317 | 2026-11-10 |
| Fable 5.1 | 558.25秒 | 489.18〜602.06秒 | 2.1.288 | 2026-10-18〜19 |
| Opus 5.5 | 269.41秒 | 261.43〜292.21秒 | 2.1.288 | 2026-10-10 |

Fable 5.2の時間は、Fable 5.1より16.0%短く、Opus 5.5より74.0%長かった。途中で確認した6課題だけの比較ではFable 5.1比約6%短かったが、全14課題が揃った結果は上記の値になった。

モデルだけでなくCLIの版、組み込みエージェントとプラグイン、計測日時が異なる。保存済み条件で観測された差として示し、モデルだけによる速度差とは断定しない。実行時間にはツールと検証の時間も含む。[比較記録](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-time-comparison.json)に、各モデルの参照元とSHA-256、時間の幅、差を保存した。品質の満点件数は、今回67／70件、Fable 5.1が65／70件、Opus 5.5が69／70件だった。

## 実行条件と中断からの再開

- モデル：`claude-fable-5-2`、推論設定`low`
- プロンプト：`the-caption-3ce91a4-control-free-repository-r1`、bundle SHA-256 `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`
- 評価セット：`the-caption-standard14-r1`、各課題N=5
- 対象commit：`3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- CLI：Claude Code 2.1.317、固定実行ファイルSHA-256 `577c8ac6411ef57dd741e3c491e89f57ff6f42bb835a5ac5d4f496c29f14c5d5`
- 同時実行上限24、CPU負荷に応じて開始を待つ条件を固定
- 採点契約：`outcome-terminal-state-evidence-claude-collector-v2`
- 単価表：`api-standard-2026-11-10`
- プロファイル：[free-claude-fable52-low-standard14-n5-cli2317-shellenv-20261110-r1](../profiles/free-claude-fable52-low-standard14-n5-cli2317-shellenv-20261110-r1.json)

[認証と旧CLIによる中断](free-claude-fable52-low-standard14-n5_2026-11-10.md)を経て、この実行条件の第1回で31件を採点・独立登録した。その後の利用上限による117試行は除外し、品質の失敗として数えていない。[途中経過](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10.md)は当時の記録として保持する。

利用者の指示で2026-11-10 14:50（日本時間）までこのチャットで待機し、第2回の不足39件だけを発行した。第2回は39／39件が有効、除外0件で、待ち行列全体の経過は149.94秒だった。第1回の31件は再実行していない。2回とも保管場所からLayer 1を複製し、プロファイル、Layer 1、発行計画、全capsuleの一致を確認したうえで発行した。起動時の実行環境照合、使用量の内訳、採点契約に従う確認を通して登録した。

STD14外で起動確認の応答が1件発生した事実と0.072852 USDのCLI報告は、[認証復旧記録](free-claude-fable52-low-standard14-n5_2026-11-10-authentication-recovery.json)に別記した。この応答および旧CLIの失敗試行は、70件の選択と上表のKPIに含めていない。

## 保存した証拠

- 正式result ID：`73c4b0ab11c74b299822ec5029482410`、[result](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-result.json)
- [選択した70件](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-selection.json)、[KPI集計](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-analysis.json)
- [2回分の採点と証拠の要約](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-quality-audit.json)
- [発行前確認記録の参照とSHA-256](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed-preflight.json)
- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/free-fable52-standard14-n5-cli2317-20261110-r1`
- 一次registry：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1`

生の実行ログ、認証情報、実行作業木はリポジトリへ含めていない。
