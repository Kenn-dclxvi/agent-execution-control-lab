# Candidate191 explicit review operation applicability実装監査

> **位置づけ**: M7機序失敗の修正版／静的検証済み／評価未開始

## 結論

Candidate191 `the-caption-3ce91a4-explicit-review-operation-applicability-r1`を、Candidate190のStandard14機序失敗だけを修正する新identityとして作成した。Candidate190の70件は診断証拠として保持し、評価済みprompt本文やresultは上書きしていない。

修正軸はreview controlの適用境界である。TaskSpecまたは適用authorityがreviewを現在subjectに必要な独立operationとして直接名指しし、review criterion、allowed result kind、result consumerおよびexecution independenceを明示値で固定した場合だけ`review_control_applicable=true`とする。criterion owner、`non_machine_risk`、静的確認、独立確認、成果確認またはtest-contract確認の語列だけではreview operation、worker、producer、spawnまたはresultを作らない。

## 方向を変える具体的反例

Standard14 F02のTaskSpecは`non_machine_risk=test-contract、owner=independent contract check`と記載するが、独立review operation、allowed review result kind、review result consumerまたは独立producer executionを要求していない。Candidate190は5件中3件でreview workerを起動し、子agentのreadに14件を超えるmachine-bound exit code欠落を生じさせた。同じ構造はF03の1件とF04の4件でも発生した。

この反例により、Candidate190の「criterion ownerだけでproducerを選ばない」という一般禁止だけでは足りず、`REVIEW_REQUIREMENT`側でも明示review operationを正の適用条件にし、欠けたfieldの推論補完を禁止する必要があると判断した。

## 変更内容

- C147で独立責務だった`OWNER_ROLE`を復元し、criterion owner、`non_machine_risk`、静的確認および独立確認の語列は独立producer executionの明示ではなく、それらだけからreview operationやspawnを補完しないと明記した。
- `REVIEW_REQUIREMENT`へ`explicit_review_operation_fixed`を追加し、reviewを必要な独立operationとして直接名指しした場合だけ適用するようにした。
- `review_control_applicable=false`ではreview operation、packet、producer、spawn、review resultおよびreview admissionを作らないと固定した。

ADR9 r2のreview必要ケースは、model-visible契約がreview operation、result kind、consumerおよびexecution independenceを明示するため、この正の条件を満たす。Standard14のowner metadataだけのケースは満たさない。完全性は後続試験で検証し、静的レビューだけを成功証明にしない。

## 変更量と非最適化

| prompt | root `AGENTS.md` UTF-8 bytes | C147比 | Candidate190比 |
|---|---:|---:|---:|
| Candidate147 | 10,772 | 基準 | `-35.47%` |
| Candidate190 | 16,692 | `+54.96%` | 基準 |
| Candidate191 | 17,989 | `+67.00%` | `+7.77%` |

1,297 bytesの増加は、過去の最適化経路のような圧縮、条項削減、review起動削減を目的としていない。むしろ、Candidate190で統合後削除していたC147の`OWNER_ROLE`を独立責務として復元し、正の適用条件と非適用時の禁止成果物を明示した結果である。prompt量は採用根拠にも失敗根拠にもせず、制御成立後のM8で品質・機序と分離して測る。

## bundle identity

- prompt identity: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- root `AGENTS.md` SHA-256: `570a425f952d9a23876923bf6896d3fb9cdaaaa060e0ee5cbc55a052dd4e87fd`
- direct parent: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- changed target: `AGENTS.md`だけ
- evaluation status: `not_evaluated`

静的試験は、非変更targetのidentity、19条項順、独立`OWNER_ROLE`、明示review operation gate、owner語列からの補完禁止、Candidate190のcurrent/prior admission境界維持およびruntime本文の歴史的identity不在を確認する。

## 状態

`candidate191_created / m7_counterexample_addressed / static_verification_passed / evaluation_not_started / not_adopted / not_released / not_projected`

## 後続評価

本監査時点の`not_evaluated`は構築時状態として保持する。後続の[Standard14 F02・F03・F04 N=5](../evaluations/results/candidate191-explicit-review-operation-applicability-standard14-f02-f03-f04-n5_2026-08-12.md)は限定退行gateを通過した。先行[ADR9 r2 review必要6ケースN=5](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5_2026-08-12.md)はterminal/result経路30 / 30を満たし、[訂正機序監査r3](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json)で83件をcollector誤検出と確認した。その30件を再利用してADR01・ADR02・ADR08を各5件追加した[ADR9 r2全9ケースN=5](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md)は45 / 45 Score 4かつ機序通過となった。[M6 ADR05・ADR07・ADR09 N=20](../evaluations/results/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md)も累積60 / 60 Score 4かつ訂正基準の機序監査を通過した。[Standard14全14ケースN=5](../evaluations/results/candidate191-explicit-review-operation-applicability-standard14-full-n5_2026-08-12.md)は既存15件再利用・不足55件追加で累積70 / 70 Score 4かつ機序通過となった。M5、M6およびM7は完了したが、M8、採用、releaseおよびprojectionは未完了である。
