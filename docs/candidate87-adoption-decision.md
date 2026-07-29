# Candidate87採用判断

## 結論

Candidate87は採用しない。Candidate作業を停止し、releaseを作成せず、THE-CAPTION本体へのruntime projectionも承認しない。現在の採用・投影済み基準はCandidate81のままとする。

状態は次のように分離する。

| lifecycle | 現在状態 |
| --- | --- |
| evaluation | `standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher` |
| adoption | `not_adopted` |
| candidate work | `stopped` |
| release | `not_created` |
| runtime projection | `not_authorized` |

この判断は2026-07-29の採用判断である。[標準14の一次評価result](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)に保存した当時の`adoption_not_decided`を変更しない。

## 判断根拠

互換なRating v14、Medium、標準14項目、各`N=5`では、Candidate81とCandidate87がともに70 / 70件でscore `4`だった。品質差は観測されていない。

一方、Candidate87 minus Candidate81の集約中央値はall-agent tokenが`+117,040`（`+6.09%`）、elapsedが`+12.330`秒（`+1.35%`）だった。両KPIが増えた。routeもCandidate81が70 / 70件root-onlyだったのに対し、Candidate87は65 / 70件root-onlyで、5 / 70件が独立contractまたはsource check Workerを使った。

Candidate87はD01でCandidate86よりproducer内部のinvocation分割コストを下げた。しかし、すでに採用・投影済みのCandidate81を置き換える品質上または運用上の利得は標準14で確認できなかった。したがって、集約コストとroute安定性の悪化を受け入れて置き換える根拠がない。

## 系列の完了境界

Candidate82からCandidate89までのサブエージェント制御系列は、この判断で完了・停止とする。既存bundle、設計、profile、resultは評価証拠として保持する。新しいCandidate、prompt、profile、model run、release、runtime projectionは作成しない。

再開するのは、次のいずれかを満たした場合だけである。

1. freshなCandidate81互換traceで、criterion metadataを別operationへ昇格する同じoperation誤分解を再観測した。
2. TaskSpecへ、別のterminal resultまたは別のproducer identityをrequired outcomeとする明示要件が追加された。

再開時もCandidate87をそのまま採用しない。まず[`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)の`operation_identity_ready`作成前gateへ戻り、変更軸と事前gateを新しい判断単位として固定する。
