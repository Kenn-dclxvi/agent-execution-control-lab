# Fable 5.2 low・Free・STD14 N=5の途中経過（2026-11-10）

認証を復旧して計測を再開し、有効31件を採点・独立登録した。31件はすべて4点だった。その後、Claudeの5時間利用上限に達したため残り39件は未完了である。14課題×5反復の全70件は揃っていないため、全体の品質・費用・経過時間を集計しておらず、正式な評価resultも登録していない。

## 固定条件

- 対象：THE-CAPTION、固定commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 評価セット：`the-caption-standard14-r1`、14課題×5反復
- プロンプト：Free、`the-caption-3ce91a4-control-free-repository-r1`
- モデル：`claude-fable-5-2`、推論設定`low`
- Claude Code：2.1.317、固定実行ファイルのSHA-256 `577c8ac6411ef57dd741e3c491e89f57ff6f42bb835a5ac5d4f496c29f14c5d5`
- 同時実行上限24、CPU負荷に応じた開始制御、既存の採点契約`outcome-terminal-state-evidence-claude-collector-v2`
- [プロファイル](../profiles/free-claude-fable52-low-standard14-n5-cli2317-shellenv-20261110-r1.json)、[単価表](../price-tables/api-standard-2026-11-10.json)

固定されたLayer 1を保管場所から複製し、プロファイル、発行計画、全capsuleとの照合を通した。起動時の構成と使用量の内訳が検証された有効runだけを採点・登録した。CLI 2.1.288とは異なる実行条件として保存し、旧CLIでの失敗試行を混ぜていない。

## 認証の復旧

[中断と復旧の記録](free-claude-fable52-low-standard14-n5_2026-11-10.md)に、過去の手順、空の計測用キーチェーン項目の除去、OAuthログインの成功、旧CLIがFable 5.2に非対応だったことを保存した。今回の認証はCLIがキーチェーンに保存し、計測時と同じ起動環境で利用できることを確認した。通常環境の設定や指示を評価環境へ複製していない。

## 完了件数

| 課題 | 有効・採点済み | 残り |
| --- | ---: | ---: |
| A01-LATENT-MODE-POLICY | 0 | 5 |
| A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 5 | 0 |
| F01-DOMAIN-DUPLICATE-ASSET-KEY | 5 | 0 |
| F02-CROSS-LAYER-HISTORY-DATE-BOUND | 5 | 0 |
| F03-ATOMIC-CONTEXT-CLEANUP | 5 | 0 |
| F04-WEB-AUDIT-COLUMN-VISIBILITY | 5 | 0 |
| F05-CLARIFY-UNITS-MODE | 0 | 5 |
| F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 0 | 5 |
| F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 0 | 5 |
| F07-CANONICAL-V4-RUNNER | 5 | 0 |
| F07-DEPENDENCY-PROVENANCE-PAIR | 0 | 5 |
| F08-CANONICAL-CLI-REFERENCE-SYNC | 0 | 5 |
| F10-ENTRYPOINT-INVENTORY-REVIEW | 1 | 4 |
| F10-MONTHLY-FORMAT-TEST-REVIEW | 0 | 5 |

[途中経過の記録](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-partial.json)に31件のrun ID、課題別の不足数、次の発行前確認記録のSHA-256を保存した。全体品質の判断で重要なA01はまだ未計測であるため、31件が4点だったことをSTD14全体の成立へ広げない。

## 未完了と再開

サービスは`You've hit your 5-hour limit · resets 2:50pm (Asia/Tokyo)`と返した。復旧後の第1回は有効31件、利用上限による除外117試行で終わった。上限到達後の試行を品質の失敗として採点していない。

同じ実行条件の保存済み31件を再利用し、不足39件だけの第2回計画を作成した。Layer 1、プロファイル、計画、capsuleの照合は通過し、39件の発行許可記録を保存済みである。第2回の評価はまだ発行していない。サービスが示したリセット時刻は2026-11-10 14:50（日本時間）。

計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/free-fable52-standard14-n5-cli2317-20261110-r1`。次の計画は`fable/round-2`にある。採用、リリース、本体反映は行っていない。

## 後続の完了結果（2026-11-10 14:52以降）

利用者の指示で14:50まで待機し、不足39件の実行・採点・登録を完了した。全70件の集計と正式resultは[完了結果](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed.md)を参照する。この文書と途中経過JSONは、利用上限による中断時点の記録として保持する。
