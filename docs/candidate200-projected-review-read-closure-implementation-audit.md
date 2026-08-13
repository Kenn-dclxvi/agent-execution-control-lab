# Candidate200 投影済みreview read閉包実装監査

> **状態**: `candidate_created / static_verification_passed / not_evaluated`

## 結論

Candidate200 `the-caption-3ce91a4-projected-review-read-closure-r1`を、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の直接child full bundleとして作成した。変更対象はroot `AGENTS.md`だけである。開始境界、`implementation_bound`後の条件付き遷移、artifact変更直前のreviewをC147上で再構成し、packet投影とreviewer read permissionを同じ閉包へbindした。

Candidate199はprompt親ではない。45件中一件でreviewerが禁止fieldを含む元sourceを再読した事実だけを反例として使用した。新実装は投影済みsourceをreviewerから閉じ、reviewerが直接観測する正確なtarget集合を分離し、root先読みとmixed readを禁止する。

## identity

| 項目 | 値 |
|---|---|
| candidate number | Candidate200 |
| prompt identity | `the-caption-3ce91a4-projected-review-read-closure-r1` |
| direct parent | `the-caption-3ce91a4-result-effect-scope-r1` |
| content relation | `direct_child_full_bundle` |
| changed target | `AGENTS.md` |
| bundle SHA-256 | `f2aff1f0a24594eaa3fca0a5d9584e9ad24e339b0e7d2eeca0e1c02b49839f60` |
| root `AGENTS.md` bytes | `17,318` |
| evaluation status | `not_evaluated` |
| release / projection | `not_created / not_projected` |

## 実装内容

`START_BOUNDARY`は開始identity resultが禁止範囲を変え得る場合だけ最初の発行集合を制御し、そのterminal後はC147通常経路へ戻す。`EVIDENCE_GATE`はC147のevidence admissionを保持し、`implementation_bound`後の直結変更だけをreview適用有無の分岐へ置換した。

`PRECHANGE_REVIEW`は`APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / READ_CLOSURE / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT`の九責任を一条項で持つ。責任分離はtool callやmodel step数を増やす命令ではない。

- `packet_projection_ready`は許可field-valueとprovenanceだけからpacketを形成する。
- `projected_source_closed`は投影入力または禁止inputを含むsource全体をreviewerから閉じ、field選択、hash、存在確認も禁止する。
- `reviewer_observation_read_set`はreviewer自身が観測するexact targetの有限集合であり、rootは先読みしない。
- `reviewer_read_admissible`は一invocation内の全targetがread set内かつclosed sourceでない場合だけ成立する。
- closed sourceまたは集合外targetを許可targetと同じinvocationへ混ぜたreadは全体を不許可にする。
- current review resultは、使用した全readがadmissibleな場合だけ受理する。

## 静的検証

次を機械確認した。

1. `verify_bundle()`が成功する。
2. direct parentとsource prompt identityがCandidate147を指す。
3. target集合がCandidate147と一致する。
4. `AGENTS.md`以外の18 manifest entryがCandidate147と同一である。
5. root promptはC147の13条項へ`START_BOUNDARY`と`PRECHANGE_REVIEW`を加えた15条項である。
6. C147の12条項は逐語一致し、`EVIDENCE_GATE`だけが固定した遷移差分を持つ。
7. 九責任、packet projection、closed source、reviewer-owned observation、mixed read禁止、current result限定が存在する。
8. 歴史Candidate名、評価case identity、private oracleおよび共通operation選択をruntime promptへ含めていない。
9. bundle identity snapshotへCandidate200を追加した。

## 境界

本監査が確定するのはartifact identity、設計との構造一致、C147保持範囲および禁止したread経路の静的な不在だけである。prompt挙動、品質、機構、採用、releaseまたはprojectionは証明しない。

次の別アーティファクト単位でADR9 r2全9ケース各N=5を事前固定する。比較条件をpreflightで一致させ、45件のcandidate slotだけを発行する。一件でも品質または機構が不通過ならvalid resultを保持して停止し、Standard14を開始しない。

`candidate200_created / c147_direct_parent / projected_source_closed / reviewer_owned_observation / mixed_read_forbidden / current_result_only / changed_target_AGENTS_only / static_verification_passed / not_evaluated / release_not_created / projection_not_performed`
