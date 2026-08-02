# Candidate147採用判断

## 結論

Candidate147を採用する。

採用の中心理由は、Candidate143から引き継いだrequired outcome全体の安全境界と、Candidate145で成立したlifecycle consumer gateを維持しながら、result待ちの範囲を実際に影響を受けるoperation classへ限定し、品質・安定性・コストの三条件を同時に満たしたことである。

状態は次のように分離する。

| lifecycle | 現在状態 |
| --- | --- |
| evaluation | `standard14_n100_evaluated / quality_stability_gate_passed / mechanism_gate_passed / aggregate_cost_recovered` |
| adoption | `adopted` |
| release | `not_created` |
| runtime projection | `not_projected` |

この判断は2026-08-03のユーザーによる明示的な採用判断に基づく。一次evaluation resultに保存した当時の`adoption_not_decided`は変更しない。release作成とTHE-CAPTIONへの投影は別判断とするため、現在のruntimeはCandidate125のままである。

## 採用理由

### 1. 全体品質と反復安定性

Candidate147の[`Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)は、14 caseすべてで各100件へ到達し、1,400 / 1,400件がscore `4`だった。score `3`以下、excluded attempt、controller error、command protocol violationは0件だった。N=29、53、77、100の各waveでも停止条件へ該当せず、一方向のcost増加もなかった。

現在投影済みのCandidate125は、後続の[`Standard14 N=100追試`](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)でcase別30件のregistered poolまで進んだ時点で、F04にscore `2`を5件観測した。Candidate147では同じF04を含むStandard14全体をN=100まで完走し、低Scoreを観測しなかった。この安定性差を、C125から採用対象を更新する主要根拠とする。

### 2. 狙った制御が実挙動で成立した

Candidate147は、resultの停止効果をtask全体へ広げず、そのresultがtarget、permission、method、stop conditionを変え得るoperation classだけを待たせる。これは単なる実行順の短縮ではなく、待つ必要がある操作と、既に許可されたreadを分ける制御境界である。

F01 / F02 / F03各N=5では、開始identityと初回許可readの共同model stepが15 / 15件で成立した。同じ共同resultを受領する前のartifact変更とrequired validationは0 / 15件だった。したがって、安全gateを緩めて先に変更したのではなく、影響を受けないreadだけを安全に同時発行したことを確認できた。

### 3. C143・C145の安全性を保ったままcostを戻した

Candidate147はCandidate145を直接親とし、`DECISION_BOUNDARY`の一軸だけを`result_effect_scope`へ置換した。Candidate143のrequired outcome implementation bind、Candidate144のvalidation predicate / method境界、Candidate145のlifecycle consumer gateは保持している。C125のexact target set、single-target continuation、固定spanのような個別手続きは継承していない。

同一N=5互換条件のStandard14では、Candidate145比でtoken中央値`-9.17%`、elapsed中央値`-23.13%`だった。F01 / F02 / F03の集約ではtoken`-25.97%`、elapsed`-22.34%`で、変更前model step中央値も3 caseすべて`2 → 1`となった。これにより、C145で追加した安全境界のcostを、狙ったmechanismによって回収したと判断できる。

### 4. C125のcost水準へ戻った

Candidate147 Standard14 N=100の中央値はtoken`1,394,412.5`、elapsed`831.914秒`だった。保存済みCandidate125 N=5の中央値に対して記述上はtoken`-0.49%`、elapsed`-1.71%`であり、少なくとも分布中央はC125と同程度の水準へ戻った。

ただし、Candidate147はN=100、Candidate125の正式集約はN=5である。同数sampleのpaired比較ではないため、「Candidate147がCandidate125より統計的に低cost」とは主張しない。採用理由はC125への数値上の勝利ではなく、C145比の互換比較でcostを下げ、C125付近の水準でN=100安定性を得たことである。

### 5. 制御軸を他のtaskへ一般化できる

`result_effect_scope`は開始identity専用の手続きではない。schema確認が生成操作だけを止める場合、permission確認がexternal sendだけを止める場合、dependency確認がinstallだけを止める場合にも、「resultが変え得るoperation classだけを待つ」という同じ境界を適用できる。

このため、特定caseのpath、command、read数、target数へ依存する対処より、今後のprompt制御へ再利用しやすい。

## 受容するrisk

F06ではauthority追加readが21 / 100件に残った。発生群のtoken中央値`160,327`は非発生群`104,230`より`53.82%`高く、高token裾との関連がある。一方、F06全体のtoken中央値はN=29以降約`105k`で安定し、100 / 100件がscore `4`だった。この経路を残存cost riskとして受容する。

評価は`gpt-5.6-sol / medium`に固定されている。他modelやreasoning水準への採用を意味しない。

採用はrelease承認またはruntime投影を意味しない。release bundleの構築、内容同一性の検証、THE-CAPTIONへの投影は、明示的に依頼された別作業とする。
