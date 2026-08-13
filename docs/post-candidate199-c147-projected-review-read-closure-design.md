# Candidate199停止後のC147投影済みreview read閉包設計

> **状態**: `design_fixed / c147_direct_base / one_failure_mechanism / projected_source_read_closed / reviewer_observation_read_only / direction_review_required / candidate_not_created`

## 結論

次案はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接基盤とし、Candidate199のprompt本文を親または差分元にしない。Candidate199のADR9 r2で成立した開始境界、review適用、producer起動、三result kind、result admissionおよび対応変更への効果を設計要件として再構成し、失敗した一機序だけを閉じる。

失敗機序は、rootが禁止fieldを除外したpacketを形成しても、reviewerの`allowed read`に禁止fieldを含む元sourceが残り、reviewerが元source全体を再読できたことである。次案ではpacket形成とreviewer read permissionを同じ閉包へbindする。packetへ投影済みのsourceはreviewerにとって`closed_source`となり、直接readを禁止する。reviewerが直接readできるのは、packet形成時点で未観測のままreviewer observationとして固定されたdescriptor targetだけとする。

## Candidate作成前の固定事項

1. 基準promptはCandidate147であり、Candidate199ではない。
2. review非適用の最短正常経路は、C147 evidence、`implementation_bound`、artifact変更、required validation、terminalである。
3. 保存trace `aede414c698741c7b4c5d8b99a179163`では、reviewerが`design-admission.json`とmissing manifestを同一commandで再読し、元source内の禁止canaryをtool resultへ取り込んだ。
4. C147の`CONTEXT`は`allowed read / forbidden input`を固定するが、許可fieldを投影した後に元sourceのread permissionを失効させる関係を持たない。TaskSpecもroot packetへ禁止sourceを入れないことは要求するが、投影後のreviewer自身による元source再読を機械的に閉じない。
5. 追加するpredicateは`packet_projection_ready`、`projected_source_closed`、`reviewer_observation_read_set`および`reviewer_read_admissible`である。置換対象はC147の変更直結遷移であり、開始境界と変更前review lifecycleを同じ構造内に再構成する。
6. これらはpacket境界とread permissionを一つの閉包にするため分離不能である。projectionだけではC199の再読を防げず、read禁止だけではreviewerが必要なmissing observationを取得できない。
7. 新たな判断点は、sourceがpacketへ投影済みか、descriptor targetが未観測reviewer observationか、発行readが後者のexact pathだけか、の三点である。新しいrepository探索、ticket、receiptまたはreviewer追加は作らない。
8. ADR9 r2全9ケースN=5でScore 4を45 / 45、開始identity、reviewer cardinality、result admission、result effect、projected source再読0件、reviewer-owned observation readのpath一致、artifact境界およびrequired commandを確認する。
9. 一件でもScore 3以下、禁止source read、許可外read、reviewer過不足、result不一致またはartifact不一致があればvalid resultを保持して停止し、Standard14へ進まない。

## 直接証拠

Candidate199は45 / 45 validで、期待terminal、reviewer cardinality、current review result admission、対応effect、開始三値identity単独発行およびartifact境界を全件一致させた。一方、ADR06 iteration 4だけは次の順序だった。

1. rootが`design-admission.json`全体を読み、禁止`history`も観測した。
2. rootはpacketへ`history`を入れないと宣言してreviewerを起動した。
3. reviewerはpacket投影値だけを使わず、`design-admission.json`と`paired-scope-evidence.json`を同一commandで直接readした。
4. reviewer tool resultへ`FORBIDDEN-ADR06-PRIOR-FINDING-CANARY`が入った。
5. counterexample自体、外側`blocked`、変更なしは正しかったが、forbidden input境界が不成立となった。

したがってreview judgementやresult admissionを作り直す問題ではない。packet形成後のread capabilityを閉じる問題である。

## 保持するC147通常経路

review非適用時は追加packet、producer、readまたはmodel stepを作らない。

```text
required outcome固定
  -> C147 evidence
  -> implementation_bound
  -> artifact変更
  -> required validation
  -> terminal
```

開始identityのmismatch時にreadを含むrepository operationが禁止される場合だけ、三値identity一件を最初に発行する。identity terminal後はC147の通常経路へ戻す。開始境界はreview要否、packetまたはread closureを所有しない。

## 変更前reviewの位置

明示reviewは`implementation_bound`後、artifact変更前にだけ適用する。適用条件は、現在の変更predicate、独立producer、criterion、allowed result kind、対応変更consumerおよびnonempty required scopeがTaskSpecまたは適用中authorityで固定された場合に限る。

```text
implementation_bound
  -> review非適用: artifact変更
  -> review適用:
       packet projection
       + reviewer read closure
       -> reviewer observation / judgement
       -> current result admission
       -> corresponding change effect
```

責任位置は`APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / READ_CLOSURE / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT`の九つとする。責任名はtool callまたはmodel stepを増やす命令ではない。

## packetとread permissionの閉包

```text
packet_projection_ready :=
  reviewer judgementに必要なcurrent valueのうち
  rootが既に観測した全valueが
  許可field-valueとprovenanceだけでpacketへ固定済み
  ∧ forbidden fieldのkey / value / 要約 / 存在状態 / null / 無視指示を含まない

projected_source_closed(source) :=
  sourceの一部または全部がpacketへ投影済み
  ∨ sourceがforbidden inputを含む

reviewer_observation_read_set :=
  required review scopeのfinite manifestに固定され
  ∧ packet形成時点でstate=unobserved
  ∧ reviewerがvalue / missing / unreadableを観測するownerである
  exact descriptor targetの集合

reviewer_read_admissible(read) :=
  read.target ∈ reviewer_observation_read_set
  ∧ read.targetはprojected_source_closedではない
  ∧ 一invocationが許可target以外のsourceを読まない
```

packetには`closed source`と`reviewer_observation_read_set`を明示する。`allowed read`という広いpath permissionを渡さない。reviewerはpacketへ投影済みsourceを、全体read、部分read、field選択read、hash確認または存在確認のいずれでも再読しない。

未観測descriptor targetはrootが起動前に先読みしない。missingまたはunreadableを含め、reviewer自身のobservation resultにする。複数targetがある場合も、一invocationでclosed sourceまたは許可外targetを混ぜない。read commandの選択はreviewerのMETHODだが、target集合はpacketで固定する。

packet形成不能、禁止inputの安全な分離不能、またはreviewer observation targetとclosed sourceが同一で分離不能ならreviewerを起動せず、対応変更を`unavailable`にする。rootによるreview代行やsource全体配送へfallbackしない。

## result admission

`counterexample_found / no_counterexample_found / unavailable`の成立条件と対応変更への効果はCandidate147上で再定義する。Candidate199 resultを再利用しない。

- `counterexample_found`: concrete witness、適用規範predicate、必要input、固定変更との直接矛盾および必要変更effectがvalue。
- `no_counterexample_found`: required scope全件と依存manifest全件がvalueで、規範predicate適用後も反例なし。
- `unavailable`: 前二者がfalseで、未解決predicateとそれを閉じ得るrequired observationのnon-value resultがvalue。

current resultはoperation、producer、sender、subject、allowed result kind、使用observation、result kind別terminal条件に加え、全reviewer readが`reviewer_read_admissible=true`の場合だけadmitする。closed source readまたは許可外readが一件でもあれば、たとえresult kindと外側terminalが期待どおりでもinadmissibleとし、artifact変更を許可しない。

## 変更位置

次CandidateはCandidate147のroot `AGENTS.md`だけを変更する。

1. `START_BOUNDARY`を追加する。
2. `EVIDENCE_GATE`末尾のartifact変更直結を条件付き変更前review遷移へ置換する。
3. `PRECHANGE_REVIEW`を追加し、九責任とpacket/read closureを一つのlifecycleに置く。

C147の他12条項は逐語保持する。Candidate199 bundle、manifestまたはprompt本文をコピー元にしない。保存済みprior review result、共通operation選択、ticket、receipt、ledger、adjudication commandまたは新dispatch機構を追加しない。

## 非目標

- review要否を自律推測しない。
- rootがreview judgementを再実施しない。
- runtime hook、外部wrapperまたはtarget runtimeを変更しない。
- Standard14をADR9前に実行しない。
- 44 / 45を採用または一般的成功として扱わない。

## 状態

`post_candidate199_projected_review_read_closure_design_fixed / c147_direct_base / candidate199_counterexample_only / projected_source_closed / reviewer_observation_read_only / current_result_only / ADR9_then_Standard14_only / direction_review_required / candidate_not_created / profile_not_created / evaluation_not_started`
