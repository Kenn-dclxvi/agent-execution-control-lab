# Candidate191 explicit review operation applicability Standard14全14ケース N=5

> **結果**: `70 / 70 valid / Score 4 = 70 / mechanism_passed / M7_passed`

## 結論

Candidate191をCandidate176の保存済みStandard14 N=5 resultへ互換bindし、限定評価済みのF02、F03、F04各5件を再利用して、他11ケースの不足55件だけを発行した。追加55 / 55、累積70 / 70件がvalid、除外0件、Score `4 = 70`となった。

全70件が単一sessionで完了し、子agentと不要review producerは0件だった。収集した562 commandのうち561件が成功し、command protocol violationは0件だった。A02のread-only locator command 1件はshell quoting誤りで失敗したが、required commandではなく、後続の成果、検証、terminalおよび品質判定へ影響していない。これをM7機序失敗へは数えない。

terminal補完、context漏洩、検証順序違反、result効果の過剰伝播、危険なartifact変更およびunexpected changed pathも0件だった。したがってCandidate191はStandard14の品質条件と機序条件を満たし、M7を通過する。これは採用、releaseまたはprojectionを意味しない。次はM8で、制御成立後の複雑性と効率を別判断として測る。

## 互換性

- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- reference result ID: `a0702207f03a4cb18c8b501329b74023`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- pool key: `60cac4f9994f8d8e088ae044862a16760ad27ac5804d5f089ce04e7e7475a25e`
- selection ID: `dbf4d0fa286945a3a159a9f1472c2a57`
- analysis ID: `b6593841ab56482ba0ad3f488cd8c32f`
- registered result ID: `da6ada84ac07426d8c66dddddcb08fdc`
- result content SHA-256: `a83e30e8fd650e98be90e0da7f9218d11252b0f1a1e2316394c46861558dee37`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-standard14-full-n5-20260812-r1`
- max workers: `24`

## 品質と機序

| 判定 | Candidate176 | Candidate190 | Candidate191 | 結論 |
|---|---:|---:|---:|---|
| valid | 70 / 70 | 70 / 70 | 70 / 70 | 維持 |
| Score 4 | 70 / 70 | 70 / 70 | 70 / 70 | 維持 |
| 不要review producer | 0 | 8 | 0 | Candidate190の退行を解消 |
| command protocol violation | 0 | 37 | 0 | 退行なし |
| unexpected changed path | 0 | 0 | 0 | 退行なし |
| monthly numeric location exact | 5 / 5 | 4 / 5 | 5 / 5 | 回復 |

owner-producer evidenceはv14契約上`diagnostic_only`であり、55件の`failed`を品質failureへ混ぜていない。一方、owner metadataだけから独立review operationを補完したかは別の機序predicateで判定し、Candidate191では0件だった。

## 再利用と発行範囲

Candidate191の限定Standard14 result `6cbac394f6dc46aea5da398c867df2f5`からF02、F03、F04の15件を再利用した。`plan-missing --desired-count 5`で不足を確定し、他11ケースの55件だけを発行した。TPOまたは別比較系列は追加していない。

最初のLayer 1候補はF01 fixture digest不一致でslot発行前に拒否した。保存済み基準resultと一致するLayer 1へ差し替え、互換条件を緩和せずpreflightを再実行した。

## 一次証拠

- [登録result](da6ada84ac07426d8c66dddddcb08fdc.json)
- [品質監査](candidate191-explicit-review-operation-applicability-standard14-full-n5-audit-r1.json)
- [機序監査](candidate191-explicit-review-operation-applicability-standard14-full-n5-mechanism-audit-r1.json)
- [評価profile](../profiles/candidate191-explicit-review-operation-applicability-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- [評価設計](../../docs/candidate191-explicit-review-operation-applicability-standard14-full-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate191-explicit-review-operation-applicability-standard14-full-n5-execution-preparation-audit.md)

## 状態

`M7_passed / 70_valid / 70_score4 / reuse_15 / new_55 / unwanted_review_producer_zero / command_protocol_violation_zero / M8_not_started / adoption_not_decided / release_not_created / projection_not_performed`
