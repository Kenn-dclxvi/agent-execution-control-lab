# PRレビュー held-out比較 r1

## 目的

資格確認と校正に使っていない固定ケースで、Claude Code純正相当Coreと、Opusを1人の関係レビュー役として使う構成を同じ入力条件で測定する。評価基盤は品質、all-agent token、経過時間を記録し、優劣、採用、release、本体反映を判断しない。

## 固定するケース

`PRR-C02/r2`、`PRR-C03/r2`、`PRR-C06/r2`を`pr-review-held-out-three-r1`として固定する。対象repositoryはcommit `16f9637d33791abd839d5c7d57b6616e03930949`、tree `c6d21c0bba62f5065c9e685f021a90ae2f004290`とする。

3ケースは、複数pathの関係、単一pathの履歴破壊、findingを返さないclean controlをそれぞれ一件ずつ扱う。既存ケースの表現や過去のreviewer出力を正解として移植しない。

## 実行順

1. 独立したcase設計監査で、期待findingとclean controlをmodel-visible入力だけから導出できることを確認する。
2. 同じ3ケースをcontrol-free条件で各1回実行する。全件で測定が成立し、quality score `4`になった場合だけ次へ進む。
3. Claude Code純正相当CoreとOpus関係レビュー役を、同じ3ケースで各1回実行する。各runは独立したatomic resultとして保存する。

設定上の`max_workers`は`24`に固定する。control-freeの品質確認結果を見てcase、oracle、rating contractを変更しない。比較する二方式では、target ref、fixture、TaskSpec、review contract、root model、Action revision、permission、timeout、token accountingを同一にし、レビュー手順とmodel role topologyだけを比較軸にする。

## ゲート

独立case設計監査、control-free品質確認、二方式の互換条件を証明するpreflight receiptのいずれかが欠ける場合は、比較スロットを発行しない。一件でもcontrol-freeのscoreが`4`未満なら、その結果を方式差へ使わず、比較を停止する。

正式KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3件とする。tool call、model step、subagent構成は診断情報であり、KPIへ追加しない。
