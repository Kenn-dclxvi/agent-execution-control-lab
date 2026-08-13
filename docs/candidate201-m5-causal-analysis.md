# Candidate201 M5 ADR9 r2 N=5原因分析

> **状態**: `analysis_complete / mechanism_failure_runs_26_classified / unknown_cause_0 / c147_direct_base_retained / M2_reopen_ready`

## 結論

Candidate201の機構不通過26 runは、重なりを含む四つの直接原因へ全件分類できる。原因不明は0件である。

1. required reviewer欠落15件は、review入力manifestに存在しないowner指定を`input_partition_ready`の必須入力にし、同時にrootによるowner決定を禁止したため、review前に`unavailable`へ停止した。
2. reviewer起動済み8件は、rootが投影した五つのobservation identityをreviewer finalから直接bindできず、`projection_complete`が未観測のままになった。これは投影不足が観測された8件ではなく、投影を証明する機械可読receiptがない8件である。
3. 3件は、TaskSpecが不一致時の停止を要求しているのに、三値開始identityとdesign readを同じ最初のrepository operationへ入れた。
4. ADR04 iteration 1の1件は、成立可能な具体的反例より、反例certificateが消費しないpaired-scopeのmissingを優先して`unavailable`を返した。

Candidate175は同じ互換条件のADR9 r2 N=5で45 / 45 Score 4、required reviewer 30 / 30を成立させた成功対照である。差は、C175がreview operation仕様、専用producer binding、semantic projection、missing targetのreviewer観測およびresult-kind優先順を一つのadmission closureへ結び、ownerラベルを追加の起動前必須入力にしなかった点にある。Candidate201はread閉鎖を強化した一方、ownerを決めるauthorityを失い、安全条件を満たすほどreviewerを起動できなくなった。

ただしC175を次Candidateの親にはしない。C175はCandidate173のchildであり、現在のC147直接基盤規律とは異なる。またC175監査はCandidate201で追加した開始identity単独発行とprojection completenessを評価していない。C175から持ち越せるのは、保存済み成功traceとadmission closureの成立条件だけである。

## 証拠境界

分析対象は[Candidate201結果](../evaluations/results/candidate201-review-input-partition-adr9-r2-n5_2026-08-13.md)、[品質監査r2](../evaluations/results/candidate201-review-input-partition-adr9-r2-n5-quality-audit-r2.json)、[機構監査r9](../evaluations/results/candidate201-review-input-partition-adr9-r2-n5-mechanism-audit-r9.json)、登録result `ba6c59a08d8744c08600207791c3b34f`および保存済みroot / reviewer traceである。

C175との比較には[Candidate175結果](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)、[ADR9監査r1](../evaluations/results/candidate175-review-operation-admission-closure-adr9-r2-n5-audit-r1.json)、登録result `eba0a4bc1d0e4391afa631462b8daccb`および保存済みADR9 r2 cycleを用いた。両登録resultのcompatibility keyは`1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`で一致する。

固定済みcase、fixture、private oracle、rating contract、Candidate201 bundleおよび保存済みresultは変更しない。追加run、Standard14、新Candidate、releaseおよびprojectionは作成しない。

## C175との結果比較

| 観測 | Candidate175 | Candidate201 | C201 - C175 |
| --- | ---: | ---: | ---: |
| valid run | 45 / 45 | 45 / 45 | 0 |
| Score 4 | 45 / 45 | 30 / 45 | -15 |
| required reviewer起動 | 30 / 30 | 15 / 30 | -15 |
| forbidden canary配送 | 0 | 0 | 0 |
| quality中央値 | 100.000 | 83.333 | -16.667 |
| all-agent token中央値 | 1,123,616 | 974,488 | -149,128（-13.27%） |
| elapsed中央値 | 733.368秒 | 511.902秒 | -221.467秒（-30.20%） |

C201のtokenとelapsedが小さい主因は、必須reviewerを15件起動せず、うちADR07の2件では後続変更とrequired commandにも進まなかったことである。したがって、このcost差は有効な効率改善ではない。品質・機構gateを満たしたC175と、必要operationを省略したC201の実行量差であり、winner、採用またはrelease判断へ使わない。

C175のStandard14は70 / 70 Score 4だった。Candidate201はADR9で停止したためStandard14を開始しておらず、Standard14間のKPI比較は存在しない。

## 26 runの分類

| 直接原因 | run数 | case内訳 | C201で最初に崩れたpredicate |
| --- | ---: | --- | --- |
| owner authority欠落によるreview前停止 | 15 | ADR03=4、ADR04=2、ADR05=3、ADR06=3、ADR07=2、ADR09=1 | `input_partition_ready` |
| projection receiptの観測不能 | 8 | ADR03=1、ADR05=2、ADR07=2、ADR09=3 | `projection_complete=unobserved` |
| 開始identityとreadの共同発行 | 3 | ADR02=2、ADR05=1 | `initial_identity_only` |
| counterexampleより無関係なmissingを優先 | 1 | ADR04=1 | `current_review_result_admissible` |

ADR05 iteration 4はprojection未観測と開始identity違反の両方に属するため、表の単純合計は27になる。重複を除くと機構不通過26 run全件となる。

required command機構不一致2件はADR07 iterations 2、5であり、いずれもreviewer未起動のため変更とadmit後commandへ進めなかった結果である。review result effect不一致15件も、reviewer未起動14件とwrong result 1件の下流結果である。別の第五原因として数えない。

## 原因1: owner authorityを起動前必須入力にした

### 全15件の観測

| case | iterations | rootの停止理由 |
| --- | --- | --- |
| ADR03 | 1、2、3、5 | owner、source identity、consumer predicate等がmanifestへ固定されず、補完禁止のためpartition不能 |
| ADR04 | 4、5 | `root_projection` / `reviewer_observation` ownerが未固定 |
| ADR05 | 2、3、5 | owner未固定、または同じ`design-admission.json`をprojected sourceとreviewer observation sourceにできない |
| ADR06 | 2、4、5 | owner未固定、またはprojected source閉鎖とinventory直接観測が衝突 |
| ADR07 | 2、5 | owner、source identity、consumer predicate、forbidden statusが未固定 |
| ADR09 | 4 | owner未固定 |

15件すべてでrootは、reviewが必要でpermissionが`allowed`であることまでは確定した。その後、case入力の`finite_evidence_manifest`にC201固有のowner fieldがないこと、または同一sourceを二つの役割へ安全に分けられないことを理由に`input_partition_ready=false`とし、reviewerを起動しなかった。

### C175との差

C175の`DESIGN_ADMISSION`は、有限manifestのdescriptor、各observation identity・target・success condition、allowed readおよびforbidden inputが固定されれば`review_operation_spec_ready`を成立させる。rootが許可field-valueだけのsemantic projectionを構成し、descriptor固定済みtargetのmissing / unreadableはreviewerが観測する。manifest entryごとのowner labelをTaskSpec側へ要求しない。

実traceでもC175はADR03〜ADR07・ADR09の30 / 30で同じtask identity `adversarial_design_review`を一件ずつ起動した。対してC201は、`REVIEW_INPUT_PARTITION`で全entryのownerを要求しながら、source種類、読みやすさ、現在値または利便性からのowner決定を禁止した。case入力にowner authorityがないため、同じmodel-visible入力から起動と停止の両方が生じた。

直接原因はread閉鎖そのものではない。C201の起動済み15件ではexact read set 15 / 15、closed source read、mixed read、root先読みおよびcanary配送はすべて0だった。失敗は、安全な分割が成立した後ではなく、分割を決めるauthorityを固定しないまま完全分割をpreconditionにしたことにある。

## 原因2: projection completenessを証明するreceiptがない

projection未観測8件は次のrunである。

| case | iteration | run ID | review result |
| --- | ---: | --- | --- |
| ADR03 | 4 | `233108e65bc3453381f40d4d1d3984a7` | `counterexample_found` |
| ADR05 | 1 | `4bcbeadd24054c2f8f219bdabfd17439` | `counterexample_found` |
| ADR05 | 4 | `2b019ac60cbf45c2ba4e517994091174` | `counterexample_found` |
| ADR07 | 3 | `17d2cb64be0644948b5bef67933e4c01` | `no_counterexample_found` |
| ADR07 | 4 | `0dd89084cfed405c8a9672a9bade9ae8` | `no_counterexample_found` |
| ADR09 | 1 | `1ac2658927ad405a8fbc62e92ddda59f` | `unavailable` |
| ADR09 | 2 | `011d9efa65c34323bc4746bc938b1743` | `unavailable` |
| ADR09 | 3 | `a7f46c71d25f4d179bf8e63c49704791` | `unavailable` |

r9監査は、reviewer finalが五つのroot-projected observation identityをすべてbindした場合だけ`projection_complete`を直接観測する。8件では最終判断に必要な一部だけが記述され、spawn packetの値・provenance・consumer predicate一対一対応をtraceから再構成できなかった。

したがって8件を`projection_incomplete=false`へ補完しない。一方、C201本文は`projection_complete`をroot内部predicateとして宣言するだけで、後から照合可能なpacket receiptまたはreview resultへの全identity再bindをterminal条件にしていない。この観測可能性不足が固定mechanism gateを閉じられない直接原因である。

C175監査にはこのpredicateがないため、C175のreviewer 30 / 30をprojection completeness 30 / 30と遡及判定しない。C175はdispatchとqualityの成功対照であり、この観測predicateの比較対照ではない。

## 原因3: 開始境界が実tool発行を拘束しない

ADR02 iterations 4、5とADR05 iteration 4では、最初のtool callが三値identity確認だけでなく、`AGENTS.md`または`design-admission.json`のreadを同じinvocationへ含めた。C201の`START_BOUNDARY`と固定評価設計は、不一致ならrepository operation全体を停止する今回のTaskSpecでは三値identity一件だけを先に発行すると定める。それでも三件で共同発行できたため、論理predicateが現在responseのtool選択を構造的に拘束していない。

C175 traceにもidentityと固定入力を同時に読む経路があり、当時の監査は開始identity単独発行を固定mechanism predicateにしていない。したがってC175をこの三件の成功対照には使わない。この原因はC201のinput partition効果ではなく、C147直接再構成で追加した開始境界の独立退行として保持する。

## 原因4: result-kindの優先関係が実判定を拘束しない

ADR04 iteration 1 `abb458034a5044648811a112a46dc34d`では、projected observationsだけで`consumer-d`、適用規範および固定設計との矛盾を形成できた。しかしreviewerは、`OBS-PAIRED-SCOPE`がmissingで全scopeを閉じられないことを優先し、期待`counterexample_found`ではなく`unavailable`を返した。

C201本文には「counterexampleを無関係なmissingで失効させない」とあるが、具体的反例certificateが消費するobservation集合と、`unavailable`が待つ先行predicateを独立terminal resultへしていない。このためreviewerはpaired-scopeをcounterexampleの必要入力へ拡張できた。

C175の`DESIGN_ADMISSION`は、許可済み成功観測から`concrete_counterexample_established`を先に判定し、成立すれば後続または別manifest項目のmissingで失効させないと一つのadmission closure内に直接固定する。C175のADR04 5 / 5は`blocked`だった。この成立traceは保持するが、C175本文を親として継承はしない。

## 成立した境界

Candidate201を無作用とはしない。次は保存する。

- 45 / 45 runがvalidで、excluded attemptとexternal failureは0件だった。
- reviewerを起動した15件ではexact read setが15 / 15一致した。
- closed source read、mixed read、rootによるreviewer-owned target先読み、forbidden canary配送はすべて0件だった。
- review不要のADR01・ADR02とpermission否定のADR08では不要reviewer起動が0件だった。
- 7 / 15では五つのprojected observation identityをreviewer finalから直接bindできた。

これらはread境界の部分効果であり、Candidate201を親、成功Candidate、採用候補またはrelease候補にする証拠ではない。

## M2へ渡す未解決predicate

- review入力の取得責任を、case入力に存在しないowner labelへ依存せず、TaskSpecの明示的packet field、有限manifest target、allowed readおよびforbidden inputから一意に閉じられること。
- owner決定を実行者の利便性へ委ねず、同じmodel-visible入力からreview起動と停止の両方を許さないこと。
- root projectionのobservation identity、value、source identity、provenanceおよびconsumer predicateを、後続監査が直接bindできるterminal receiptへ残すこと。
- 具体的反例certificateの必要observation集合を固定し、集合外missingが成立済みcounterexampleを失効できないこと。
- 開始identity result受領前に後続readを同じtool callまたはmodel responseへ入れられないこと。
- projected source閉鎖、reviewer exact read、mixed read禁止、root先読み禁止およびforbidden input非配送を維持すること。

M2ではC147を直接基盤とする。C175、C200およびC201は、成立trace、反例、責任境界および必要観測としてだけ参照する。新Candidate、profile、評価slot、releaseおよびprojectionは作成しない。

## 再開判断

M1は`mechanism_failure_runs_26_classified / unknown_cause_0`として完了する。次に許可するのは、上の未解決predicateをC147の責任へ戻すM2再設計だけである。

`candidate201_M1_analysis_complete / mechanism_failure_runs_26_classified / owner_authority_missing_15 / projection_receipt_unobserved_8 / initial_identity_boundary_violation_3 / judgement_priority_violation_1 / overlap_1 / unknown_cause_0 / c175_success_control_limited / c147_direct_base_retained / candidate201_not_parent / M2_reopen_ready / new_candidate_not_created / new_evaluation_not_started`
