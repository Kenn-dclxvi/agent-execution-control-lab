# Candidate136 effect-local change admission設計

## 結論

Candidate136はCandidate135を直接親とし、criterion-span request authorityを保持したまま、変更前effect stateの個別bindと初回change admissionだけを追加する。全effectの完全観測を開始gateにせず、reference definition closureとglobal preimage gateは追加しない。

## Identity

- prompt identity: `the-caption-3ce91a4-effect-local-change-admission-r1`
- direct parent: Candidate135 `the-caption-3ce91a4-criterion-span-request-authority-r1`
- changed rule: `EVIDENCE_GATE`
- changed axis: initial artifact変更へ入れるeffectの個別admission
- unchanged: criterion-span検索語authority、continuation回数、Candidate128のeffect closure / recovery、Point 4・6

## Predicate

`effect_prechange_state(effect)`を、admission済みprechange contentに基づく`satisfied / unsatisfied / unobserved`の三値とする。

`initial_change_effect_set`には`unsatisfied`へbindした全effectだけを入れる。`satisfied`は保持し、`unobserved`は推測で変更しない。`unobserved`は別の`unsatisfied` effectの変更開始拒否には使わない。全required effectが閉じるまでvalidationへ進まない条件はCandidate128の`required_effects_closed`を維持する。

## F04 N=5 gate

- valid / rateable / score `4`: 5 / 5
- score `3`以下: 0 / 5
- criterion外lexeme混入: 0 / 5
- 未充足effectの必要変更: 5 / 5
- 開始状態で充足済みeffectの変更: 0 / 5
- initial atomic apply failure: 0 / 5
- 未観測effectによる別の未充足effectのfalse stop: 0 / 5
- required Node validation完備: 5 / 5

一件でもscore `3`以下、充足済みeffectの再変更、必要変更抑止、validation欠落があれば停止する。通過した場合もF04固有成功へ一般化せず、次にF02とF07を各N=5でpreservation確認する。

## 実測結果

F04 N=5はscore `4 / 3 = 4 / 1`で停止した。effect-local admissionは、必要変更5 / 5、充足済みeffect変更0 / 5、initial patch失敗0 / 5で成立した。低Score 1件も観測済み未充足effectを変更したが、親C135のlexeme集合から別criterion memberが脱落し、そのeffectを未観測のままclosureで停止した。F02、F07へ進めない。

## 結論表

| 課題 | Candidate136 |
| --- | --- |
| request source boundary | C135を保持 |
| effect state | effectごとの三値bind |
| initial change | unsatisfiedだけ |
| unobserved effect | 推測変更せず、別effectを止めない |
| closure / recovery | C128を保持 |
| 初段 | F04 N=5、M=24 |
| 実測 | score 4 / 3 = 4 / 1、停止 |
