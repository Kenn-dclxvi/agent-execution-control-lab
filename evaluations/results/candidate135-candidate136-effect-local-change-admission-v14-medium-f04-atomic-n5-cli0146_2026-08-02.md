# Candidate135 / Candidate136 F04 targeted result

## 結論

Candidate136のF04 N=5はscore `4 / 3 = 4 / 1`だった。score `3`が1件出たためCandidate136を停止し、F02、F07、追加24件、Standard14へ進めない。

effect-local admission自体は狙いどおり動いた。5 / 5件が未充足`hasAuditKey`だけを変更し、開始状態で充足済みの`colSpan`変更、initial atomic apply failure、必要変更の抑止はすべて0 / 5件だった。

Score 3 runも必要な一行変更は適用した。しかしcriterion lexeme集合から`colSpan`が抜け、continuation出力の配送範囲内でその開始状態を観測できなかった。Candidate136は未観測effectを推測変更せず、別の未充足effectの変更も止めなかった。その後、Candidate128のclosureを維持してvalidation開始前に停止した。したがって低Score原因はeffect-local admissionではなく、親C135から残るPoint 2 evidence coverageの不安定性である。

## 固定条件

- candidate: `the-caption-3ce91a4-effect-local-change-admission-r1`
- parent: `the-caption-3ce91a4-criterion-span-request-authority-r1`
- bundle SHA-256: `932e373eef211686e04ed6d1961dd9c3470f552af3bc130f8d8f6fccbddcce32`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- pool: `2e86c52eb87938cd776aa9635dc607c9c27fb070da5e21e1b90b948a434e2f82`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `d2304a0f6f4c4890beb393f62a026823`
- analysis: `1a770effd43246999a09788a17cd2ad2`
- registered result: `42e5940bfd994e449878e6c536b80185`
- excluded attempt: 0

保存済みF04 reference result `cea34faab78149119808da7c59628955`を実行前にbindした。prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合し、preflightが5 slotを承認した後だけ発行した。

## 結果

| iteration | run | score | effect admission | artifact変更 | validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `bbc4261163564872a4c1222f01598711` | 4 | 未充足だけ | `hasAuditKey`一行 | 3 / 3成功 |
| 2 | `b187a52f5b834503b8f9da0d6cb72b53` | 3 | 未充足だけ、`colSpan`は未観測hold | `hasAuditKey`一行 | 0 / 3、closureで停止 |
| 3 | `76cdaffd8f504a5382215361cfff6dd8` | 4 | 未充足だけ | `hasAuditKey`一行 | 3 / 3成功 |
| 4 | `5b5c82bc019e4060a2cdcfb19c31a42b` | 4 | 未充足だけ | `hasAuditKey`一行 | 3 / 3成功 |
| 5 | `b0941195d7fc42ebbe565582d161c9c0` | 4 | 未充足だけ | `hasAuditKey`一行 | 3 / 3成功 |

5件中央値はquality `100.000`、token `162,400`、elapsed `76.379`秒だった。1件がrequired validation前に停止したため、効率改善や採用の判断には使わない。

## effect-local admissionの判定

全5件で、開始状態の固定`hasAuditKey = true`を未充足effectへbindし、その一行だけを変更した。動的`colSpan`を変更へ戻したrunは0件だった。初回patch失敗も0件であり、C135低Scoreの「必要hunkと不要hunkの結合」は再発しなかった。

iteration 2では`colSpan`が未観測だった。それでも観測済み未充足`hasAuditKey`を変更したため、Candidate129の3 / 5件で起きたtarget全体の開始拒否は再発していない。三値bindのうち`unobserved`を別effectの開始拒否に使わない境界は成立した。

## Score 3の切り分け

iteration 2のcontinuation requestは`audit_match_key`と`Audit Key`だけを検索し、criterionに明記された`colSpan`を集合へ入れなかった。その後に241行目以降の全contentを同じcommandで要求したが、model-visibleな配送結果は途中で切れ、空表示cellまで届かなかった。

agentは未観測`colSpan`を推測で変更しなかった。`hasAuditKey`の一行変更後も全required effectがclosedとは証明できないため、`npm ci`、lint、buildを開始せず停止した。この停止はclosureを守る保守側動作であり、validationへ推測で進むよう緩めない。

C136の追加predicateで修正すべき残差ではない。C135の`criterion_request_lexeme_set`が明示lexeme全件を安定して選べなかったため、必要effectの開始状態が未観測になった。次はPoint 2に戻り、なぜ構文的に明示されたmemberが集合から脱落するかを保存済みtraceで調査する。

## 汎用性の解釈

F04 N=5だけでは言語横断の品質を証明しない。ただし、三値effect stateの構造について次を観測した。

- 観測済み未充足effectは5 / 5で変更できた。
- 観測済み充足済みeffectは5 / 5で保持した。
- 未観測effectがあっても、別の観測済み未充足effectの変更は止めなかった。
- 未観測effectを推測でclosedにせず、validationも開始しなかった。

この構造はF02の複数source effectやF07のdependency pairにも適用可能だが、C136は品質停止したため実測へ進めない。適用可能性をpreservation passへ読み替えない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / effect_local_admission_passed / required_edit_5_of_5 / satisfied_effect_change_0_of_5 / initial_apply_failure_0_of_5 / unobserved_effect_did_not_block_other_edit_1_of_1 / criterion_lexeme_omission_1_of_5 / validation_complete_4_of_5 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 4 / 5 | fail / stop |
| score `3`以下 | 0 / 5 | 1 / 5 | fail / stop |
| 未充足effectの必要変更 | 5 / 5 | 5 / 5 | pass |
| 充足済みeffectの変更 | 0 / 5 | 0 / 5 | pass |
| initial atomic apply failure | 0 / 5 | 0 / 5 | pass |
| 未観測effectによる別effectの変更抑止 | 0 / 5 | 0 / 5 | pass |
| criterion外lexeme混入 | 0 / 5 | 0 / 5 | pass |
| 全criterion lexemeをcontinuation集合へ保持 | 5 / 5 | 4 / 5 | fail |
| required validation完備 | 5 / 5 | 4 / 5 | fail |
