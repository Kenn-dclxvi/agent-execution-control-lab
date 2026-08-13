# Candidate196 materialized adjudication control実装監査

> **状態**: `candidate_created / static_verification_passed / not_evaluated`

## 結論

Candidate196 `the-caption-3ce91a4-materialized-adjudication-control-r1`を、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の直接child full bundleとして作成した。変更targetはroot `AGENTS.md`だけであり、その他18 targetのmanifest entryはCandidate147と同一である。

Candidate195をprompt親にはしていない。Candidate195の保存結果と原因分析は、発行前判定の非operation化8件とreview judgement dependencyの非ticket化1件を再現する設計証拠としてだけ用いた。実装は[M2設計](post-candidate195-review-control-m2-materialized-adjudication-design.md)と[M3方向review](post-candidate195-review-control-m3-direction-review.md)で固定した30責任へC147の制御を再配置したものである。

## identity

| 項目 | 値 |
|---|---|
| prompt identity | `the-caption-3ce91a4-materialized-adjudication-control-r1` |
| direct parent | `the-caption-3ce91a4-result-effect-scope-r1` |
| content relation | `direct_child_full_bundle` |
| changed targets | `AGENTS.md` |
| bundle SHA-256 | `352eee02c72101769d374d398db4aae061f4e97a38dc24fa283af8a87e839e2c` |
| evaluation status | `not_evaluated` |
| release / projection | `not_created / not_projected` |

## 実装した構造

- repository tool発行前に、既受領inputだけをcanonical JSONへ変換するno-side-effect control commandを、そのmodel response唯一のtool invocationとして実行する。
- terminal success receiptがmodelへ返った次のmodel stepでだけ、receiptに列挙したtool identityとmethodへ完全一致する操作を発行する。
- receipt後にTaskSpec、ticket、permission、predecessor resultまたはmethod inventoryが変わればreceiptを失効する。
- requested resultが`HEAD / HEAD^ / HEAD^^`の三値tupleの場合、現在HEADしか返さないmethodを既知schema不適合として発行前に除外する。
- review judgementを`COUNTEREXAMPLE_ADJUDICATION`、`NO_COUNTEREXAMPLE_ADJUDICATION`、`UNAVAILABLE_ADJUDICATION`へ分け、固定優先順と固有dependencyを持たせる。
- counterexampleは全固定witnessのOR closureで判定し、一件のfalseまたはcertificate外missingから後続result kindへ進めない。

## 静的検証

次を機械確認した。

1. `verify_bundle()`が成功する。
2. `baseline_identity`と`content_relation.source_prompt_identity`がCandidate147を指す。
3. Candidate147とCandidate196のtarget集合が一致する。
4. `AGENTS.md`以外の18 manifest entryがCandidate147と同一である。
5. root本文のtop-level labelがM2の30責任と同名・同順である。
6. materialized receipt、model-step分離、input drift失効、exact issuance、method schema eligibility、三result-kind adjudicationおよびcertificate-local dependencyが本文に存在する。
7. 旧抽象発行機構名、過去Candidate名および評価case名をprompt本文へ混入していない。

## 境界

この監査が確定するのはartifactの構造とidentityだけである。prompt挙動、品質、機構、採用、releaseまたはtarget本体へのprojectionは成立していない。評価profileと評価runは別アーティファクト単位で固定する。

`candidate_created / c147_direct_parent / changed_target_AGENTS_only / responsibilities_30 / materialized_adjudication_implemented / result_kind_adjudication_split / static_verification_passed / not_evaluated / adoption_not_decided / release_not_created / projection_not_performed`
