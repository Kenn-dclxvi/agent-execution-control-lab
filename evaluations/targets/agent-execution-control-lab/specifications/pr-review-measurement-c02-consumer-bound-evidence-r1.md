# Candidate171 C02開発測定 r1

この仕様は、Candidate171をCase PRR-C02/r2で独立に3回実行し、品質、all-agent token、経過時間を測定する条件を固定する。PRR-C02/r2はCandidate170の分析とCandidate171の設計に使用済みであるため、この測定は開発用であり、held-out効果を主張しない。

## 比較条件

- 直接の基準は、同じCase、モデル構成、Action revision、権限、採点契約で測定が成立したCandidate170のRun Resultとする。
- Candidate169の保存済みRun Resultは、C02で得られた品質とKPIの補助参照として保持する。
- 変更するprompt identityはCandidate171だけとする。fixture、TaskSpec、review contract、rating contract、root SonnetとOpus関係レビュー役1人の構成、権限、timeout、all-agent token集計は変えない。
- Candidate171は、evidenceの取得を固定件数のreadへ結び付けず、未確定の判定項目と現在欠けている観測値へ結び付ける。

## 実行と判定

- repetition 1、2、3を別のworkflow dispatchとして発行する。
- 各Run Resultでは、測定成立とquality scoreを分ける。quality missだけでは残りの反復を停止しない。
- KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3つだけとする。
- fixture-toolの操作数、操作種別、batch、token価格区分は診断情報として保存する。
- 固定read数をmechanismの合否条件にしない。現在のhookでは、各evidence取得がどの未確定predicateに結び付いていたかを機械的に証明できないため、consumer bindingは`observed_not_machine_qualified`として明示する。

## 主張の境界

この3反復は、Candidate171が既知のC02でCandidate170の品質低下を回復できるか、その際のtokenと時間がどう変わるかを調べる開発測定である。一般化、fresh held-out効果、model ranking、採用、release、ターゲット本体への反映は、この測定だけでは判断しない。
