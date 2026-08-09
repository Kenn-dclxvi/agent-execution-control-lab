# PRレビュー held-out比較 r3

## 目的

資格確認と校正に使っていない固定ケースで、review方法をmodelへ委ねるControl-Freeと、Opusを1人の関係レビュー役として固定する構成を同じ入力条件で比較する。`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3件をKPIとして保存し、特定のquality scoreを比較前の合否条件にしない。

このrevisionは、r2が比較対象へClaude Code純正相当Coreを含めていた範囲を改める。PRR-C01/r4の校正では、関係レビュー役をOpusへ固定した3件がすべて測定成立かつquality score `4`であり、次に確認する価値がある構成として選んだ。Coreの過去resultは診断履歴として保持するが、この比較へ入れない。

## 固定する比較

Evaluation setは`pr-review-held-out-three-r1 / r1`、case membershipは`PRR-C02/r2`、`PRR-C03/r2`、`PRR-C06/r2`とする。case、oracle、rating contract、target repository refを変更しない。

Control-Freeは保存済みの3件を再利用する。3件とも測定が成立しており、quality score `1 / 4 / 4`を品質KPIとしてそのまま保持する。同じslotを再実行しない。

新規に発行するのは、関係レビュー役を1人だけ起動し、そのmodelをOpusへ固定する3件である。root model、Action revision、model-visible入力、権限、timeout、構造化出力、採点、all-agent token accountingをControl-Freeと一致させる。review topologyとそれを指定するpromptだけを比較軸とする。

## 実行前ゲート

次の条件をすべて満たした場合だけOpus側の3 slotを発行する。

1. 独立case設計監査が成立している。
2. 保存済みControl-Free 3件で測定が成立し、3 KPIが取得できている。
3. Opus側のprofileで、case、model role、Action revision、permission、timeout、token accounting、停止条件を固定している。
4. Control-FreeとOpus側の実効条件を機械照合し、review topologyとprompt以外の差分がないことをpreflight receiptへ保存している。

quality scoreの値はゲートに含めない。有効なcaseでの見逃し、余分なfinding、不完全なfindingは品質KPIとして比較へ含める。caseまたは測定自体が不成立の場合だけ、当該resultを比較へ登録しない。

## 実行と境界

Opus側は3ケースを各1回、独立したatomic runとして実行する。設定上の`max_workers`は`24`、実際のdispatch concurrencyは`3`とする。品質missは他caseの発行を停止しない。environment failureまたは測定不成立が判明した場合は、新しい比較slotを追加せず、同じcaseの同じrepetitionだけを新しいattempt identityで回復できる。

評価基盤は3 KPIと互換性だけを記録し、winner、KPIの優先順位、採用、release、本体反映を決めない。
