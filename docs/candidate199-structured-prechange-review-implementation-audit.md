# Candidate199 構造化変更前review実装監査

> **状態**: `candidate_created / static_verification_passed / not_evaluated`

## 結論

Candidate199 `the-caption-3ce91a4-structured-prechange-review-r1`を、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の直接child full bundleとして作成した。変更対象はroot `AGENTS.md`だけで、開始stop scopeを所有する`START_BOUNDARY`、`implementation_bound`後の遷移置換、artifact変更直前の`PRECHANGE_REVIEW`を一つの時系列構造として実装した。

Candidate191の責任構造は`PRECHANGE_REVIEW`内部の八責任として使ったが、Candidate191のprompt本文、外側operation分解、観測atom体系、保存result再利用または逐次発行は継承していない。Candidate175からはoperation readinessと観測結果の分離、専用producer、許可fieldだけのpacket形成という成立経路だけを使い、直接親またはprompt差分元にしていない。Candidate198の`selected_operations`、包含最小集合、候補再選択および`REVIEW_SELECTION`も継承していない。

## identity

| 項目 | 値 |
|---|---|
| candidate number | Candidate199 |
| prompt identity | `the-caption-3ce91a4-structured-prechange-review-r1` |
| direct parent | `the-caption-3ce91a4-result-effect-scope-r1` |
| content relation | `direct_child_full_bundle` |
| changed target | `AGENTS.md` |
| bundle SHA-256 | `b2bc74e96f9ebf64bf977f766ec25ed1b429663acee59b64bfe570a9f91d654a` |
| root `AGENTS.md` bytes | `16,011` |
| evaluation status | `not_evaluated` |
| release / projection | `not_created / not_projected` |

## 実装内容

### `START_BOUNDARY`

TaskSpecが開始identity predicateとmismatch時の禁止operation classを直接固定した場合だけ適用する。mismatch時にreadも禁止される場合はidentity一件だけを最初に発行し、readが禁止されずidentity resultで必要性やpermissionが変わらない場合はC147の`DECISION_BOUNDARY`に従って共同発行できる。

required identity value全件を原理的に返せないmethodは選ばない。実resultだけがfield不足の場合はouter taskを早期`unavailable`にせず、C147の`METHOD`で同じpredicateへ継続する。本条項は最初の実repository operation集合だけを所有し、review、変更、validationまたは全operation選択を所有しない。

### `EVIDENCE_GATE`の遷移置換

C147のevidence admission、追加evidence条件および`implementation_bound`定義は保持した。変更したのは、`implementation_bound=true`後に直ちにartifact変更へ進む一文だけである。

- 明示review非適用: artifact変更へ進む
- 明示review適用: `PRECHANGE_REVIEW`へ進む
- review適用時: admissible `no_counterexample_found`までartifact変更を発行しない

変更前evidence operationを再開せず、review非適用経路へreview operation、packet、producer、observationまたは追加model stepを作らない。

### `PRECHANGE_REVIEW`

`APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT`を一条項内の八責任として実装した。責任名は状態所有を示すだけで、八operation、八tool callまたは八model stepを要求しない。

reviewは、TaskSpecまたは適用中authorityが現在の変更predicate、独立producer、criterion、allowed result kind、対応変更であるconsumerおよびnonempty required scopeを直接固定した場合だけ適用する。permission denied、packet形成不能または禁止入力を分離不能な場合はrootが補完せず、reviewerも変更も発行しない。

三result kindは別terminal条件を持つ。真正counterexampleは無関係なmissingで失効させず、`no_counterexample_found`はrequired scopeと必要manifest全件を要求し、`unavailable`は未解決predicateとそれを閉じ得るnon-value observationへbindする。admissible resultの効果は対応変更だけへ限定する。

## 静的検証

次を機械確認した。

1. `verify_bundle()`が成功する。
2. direct parentとsource prompt identityがCandidate147を指す。
3. target集合がCandidate147と一致する。
4. `AGENTS.md`以外の18 manifest entryがCandidate147と同一である。
5. root promptのtop-level条項はC147の13件に`START_BOUNDARY`と`PRECHANGE_REVIEW`を加えた15件である。
6. C147の12条項は逐語一致し、`EVIDENCE_GATE`だけが固定した遷移差分を持つ。
7. `START_BOUNDARY`、三result kind条件、八責任、current resultだけの境界が存在する。
8. Candidate175、Candidate191、Candidate198、評価case identityおよびprivate oracleはruntime promptに含まれない。
9. bundle identity snapshotへCandidate199を追加した。

設計・方向レビューとCandidate198既存回帰を含む静的試験は別途実行し、全件成功を確認する。

## 境界

本監査が確定するのはartifact identity、設計との構造一致、C147保持範囲および禁止した継承経路の不在だけである。prompt挙動、品質、機構、KPI、採用、releaseまたはtarget本体へのprojectionは証明しない。

次の別アーティファクト単位はADR9 r2全9ケース各N=5の評価設計である。評価設計ではmodel-visible input、quality oracle、開始dependency、reviewer cardinality、packet情報封鎖、三result kind、current result admission、artifact境界、required command、互換条件および停止条件を実行前に固定する。profileまたは評価slotはその後に作成する。

`candidate199_created / c147_direct_parent / start_boundary_added / evidence_gate_transition_only / prechange_review_added / responsibility_not_model_step / current_result_only / changed_target_AGENTS_only / static_verification_passed / not_evaluated / release_not_created / projection_not_performed`
