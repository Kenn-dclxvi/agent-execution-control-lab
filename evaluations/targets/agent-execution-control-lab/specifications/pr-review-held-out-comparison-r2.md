# PRレビュー held-out比較 r2

## 目的

資格確認と校正に使っていない固定ケースで、Claude Code純正相当Coreと、Opusを1人の関係レビュー役として使う構成を同じ入力条件で測定する。`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3件を比較可能なKPIとして保存し、特定のquality scoreを比較前の合否条件にしない。

このrevisionは、r1がControl-Freeの全ケースへquality score `4`を要求したため、有効な品質差を比較前に除外していた問題を改める。r1のprofile、preflight、一次result、停止receiptは履歴として変更しない。

## 固定するケースと既存result

Evaluation setは`pr-review-held-out-three-r1 / r1`、case membershipは`PRR-C02/r2`、`PRR-C03/r2`、`PRR-C06/r2`のまま変更しない。case、oracle、rating contractを既存resultへ合わせて変更しない。

Control-Freeの3件はすべて、要求model、構造化出力、all-agent token、経過時間、fixture access、権限拒否0件を確認済みである。quality score `1 / 4 / 4`をそのまま有効な品質観測として保持し、再実行しない。

## 比較前ゲート

次の条件をすべて満たした場合だけ比較スロットを発行する。

1. 独立case設計監査が成立している。
2. 対象caseのControl-Free resultで測定が成立し、3 KPIが取得できている。
3. Claude Code純正相当CoreとOpus関係レビュー役について、promptまたはreview topology以外の実効互換条件が一致するpreflight receiptを保存している。
4. 各方式のmodel role、Action revision、permission、timeout、token accounting、停止条件を実行前に固定している。

quality scoreの値は2と3の成立条件に含めない。caseまたは測定の不備と判定されたresultは比較へ入れないが、有効なcaseでの見逃し、余分なfinding、不完全なfindingは品質KPIとして含める。

## 実行と境界

Claude Code純正相当CoreとOpus関係レビュー役を、同じ3ケースで各1回実行する。各runは独立したatomic resultとして保存する。Control-Freeの保存済み3件は参考条件として同じ3 KPIを併記できるが、再実行しない。

設定上の`max_workers`は`24`に固定する。target ref、fixture、TaskSpec、review contract、root model、Action revision、permission、timeout、token accountingを一致させる。tool call、model step、subagent構成は診断情報であり、KPIへ追加しない。

評価基盤は数値と互換性だけを記録し、winner、KPIの優先順位、採用、release、本体反映を決めない。
