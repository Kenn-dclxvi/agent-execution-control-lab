# Candidate198停止後のC147構造化変更前review設計

> **状態**: `design_fixed / c147_direct_base / chronological_boundary_structure / start_scope_local / c191_responsibility_structure_only / c175_admission_connection_only / review_before_change / direction_review_required / candidate_not_created`

## 結論

次の方向は、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接基盤とし、通常operationの選択と発行順序をC147の既存制御へ戻した上で、TaskSpecまたは適用中repository authorityが独立review operationを直接要求する場合だけ、固定済み変更predicateの直前へreviewを一件接続する。

Candidate191は直接親または実行機構として使わず、review責任を`適用 / 実行準備 / packet / judgement / result admission / change effect`へ分けた構造だけを設計確認に使う。Candidate175も直接親にせず、review operation仕様、専用producer binding、allow-list semantic projectionを一つのadmissionへ閉じた成立経路だけを接続根拠に使う。

責任を分けることとmodel stepを分けることを同一視しない。review内部の責任名は状態所有者を示すだけであり、それ自体はtool発行、producer起動、result待機または別model stepを作らない。実際に先行resultを待つのは、そのresultが後続operationの必要性、target、permission、methodまたはstop conditionを変え得る場合だけとする。

Candidate198の`selected_operations`、包含最小集合、候補の再選択および`REVIEW_SELECTION`は継承しない。次Candidateを作る場合もC147の直接childとし、開始時だけに作用する`START_BOUNDARY`と、変更直前だけに作用する`PRECHANGE_REVIEW`を順序上の別位置へ置く。C147の`EVIDENCE_GATE`にある`implementation_bound`からartifact変更への遷移だけを条件付きreview接続へ置換する。本設計の方向reviewが完了するまではprompt bundle、profile、case、評価slotまたはreleaseを作成しない。

## 設計入力と証拠境界

本設計の直接入力は次へ限定する。

- C147の13条項原文
- Candidate175のADR9 r2全9ケースN=5およびStandard14全14ケースN=5の保存結果
- Candidate191のroot `AGENTS.md`責任構造、ADR9 r2全9ケースN=5、Standard14全14ケースN=5およびStandard14コスト機序再判定
- Candidate198のADR9 r2全9ケース45 run、訂正品質監査および訂正機構監査
- ADR9 r2とStandard14のmodel-visible TaskSpecおよび固定fixture

Candidate175のN=5成功を一般的な完全性証明にしない。Candidate191の責任名、operation分解、保存result再利用経路または実行順序を継承しない。Candidate198の静的方向review通過を実挙動の成立証拠にしない。private oracle、case ID、期待terminal、過去findingおよび採点用commandをprompt判断へ入れない。

## Candidate198で否定された方向

Candidate198はC147の`SPEC`と`DECISION_BOUNDARY`を置換し、通常operationとreviewを同じ候補集合から選んだ。ADR9 r2では開始identity単独先行がCandidate197の4 / 45から35 / 45へ改善した一方、reviewer cardinalityは32 / 45、current review result admissionは27 / 45、result effectは26 / 45、品質は26 / 45 Score 4に留まった。

これは次を示す。

1. review必要性を論理的に分類できても、汎用候補集合への包含だけではproducerの実起動を一意に拘束できない。
2. 開始identity、repository read、review、変更およびvalidationを同じ最小集合へ入れると、一経路の改善が別経路の欠落を生み得る。
3. 全operationへ共通する抽象選択を新設するより、C147の通常経路を保持し、reviewを対応変更へ直接接続する必要がある。

したがって、次設計では「現在必要な全operationを一つの集合から選ぶ」責任を追加しない。開始時のTaskSpec stop scopeだけを`START_BOUNDARY`が所有し、そのterminal後の通常operationはC147の`SPEC`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`および`METHOD`が引き続き所有する。`EVIDENCE_GATE`もevidence admissionと`implementation_bound`の成立までは維持し、そのterminal resultからartifact変更へ進む一接続だけを置換する。

## 開始境界をreviewから分離する

C197ではC147の通常発行をそのまま使った結果、ADR9 r2で最初の実repository operationを三値identityだけに限定できたrunは4 / 45だった。C198は全operationの候補選択へ開始identityを含めて35 / 45まで改善したが、review起動とresult接続を同じ選択へ入れたため別の退行を生んだ。

次設計では全operation選択を継承せず、TaskSpecが明示する開始identityとdrift時stop scopeだけを一つの`START_BOUNDARY`へ固定する。

```text
start_boundary_applicable :=
  TaskSpecが開始identity predicateと
  mismatch時に禁止するoperation classを直接固定

start_identity_ready :=
  start_boundary_applicable
  ∧ required identity value集合が固定済み
  ∧ result consumerが固定済み
  ∧ selected methodがrequired identity value全件を返し得る

initial_issue_set :=
  start identity operation
  + mismatch時にも禁止されず
    identity resultで必要性、target、permission、methodまたはstop conditionが変わらない
    現在必要なoperation
```

TaskSpecがmismatch時にrepository readを含む全repository operationを禁止する場合、`initial_issue_set`はstart identity一件だけとする。mismatch時にartifact変更とrequired commandだけを禁止し、固定済みreadを禁止しない場合は、C147の`DECISION_BOUNDARY`に従いidentityとそのreadを同じmodel stepから発行する。

required resultが`HEAD / HEAD^ / HEAD^^`の三値なら、三値を原理的に返せないmethodを選ばない。全required valueを返し得るmethodが実行結果では一部しか返さなかった場合は、その結果だけでouter taskを`unavailable`にせず、C147の`METHOD`に従って同じidentity predicateへ継続する。method選択のためのrepository read、ticket、receiptまたは別model stepを追加しない。

`START_BOUNDARY`は最初の実repository operation集合だけを所有し、review要否、review producer、変更、validationまたはtask全体のoperation選択を所有しない。開始identityのterminal result受領後はC147の通常経路へ戻り、review lifecycleは`implementation_bound`まで開始しない。

## 保持する通常経路

reviewが適用されない通常経路は次とする。

```text
required outcome固定
  -> C147に従う必要evidence
  -> implementation_bound
  -> artifact変更
  -> required validation
  -> terminal
```

この経路へreview要否を調べるためのread、producer、packet、result、状態確認または追加model stepを入れない。criterion owner、`non_machine_risk`、task名に含まれるreview語、一般的安全性または有用性からreviewを補完しない。

C147の`DECISION_BOUNDARY`を通常operationの発行順序の正本として逐語維持する。開始identity resultが許可済みreadの必要性、targetまたはpermissionを変えない場合は同じmodel stepから発行できる。TaskSpecがidentity mismatch時にread自体を禁止する場合はidentityだけを先行させる。review責任の追加を、この判断より上位の共通dispatch規則にしない。

## reviewを置く位置

reviewは`implementation_bound=true`となり、実行可能な一つの変更predicate、保持constraint、対象artifactおよび成果物間relationが固定された後、最初のartifact変更の直前へ置く。

```text
required outcome固定
  -> 必要evidence
  -> implementation_bound
  -> [明示reviewが適用される場合だけ PRECHANGE_REVIEW]
  -> artifact変更
  -> required validation
```

開始時点には置かない。具体的なsubjectがない状態でreviewerへ探索または設計補完をさせない。artifact変更後にも置かない。review結果が変更を否定し得るのに、先に変更して再作業を作らない。validationへも統合しない。reviewは変更前subjectの反例判断、validationは変更済みartifactの要求充足確認として別predicateを維持する。

C147原文の`EVIDENCE_GATE`は、`implementation_bound=true`となったresultを変更前evidence operationのterminal resultにした後、未発行evidenceを失効して「次にartifact変更を発行する」と定める。この最後の遷移を次へ置換する。

```text
prechange_transition :=
  artifact_change
    if implementation_bound
       ∧ explicit_prechange_review_fixed=false
  prechange_review
    if implementation_bound
       ∧ explicit_prechange_review_fixed=true
       ∧ prechange_review_ready
  unavailable
    if implementation_bound
       ∧ explicit_prechange_review_fixed=true
       ∧ prechange_review_ready=false
```

`prechange_review`のadmissible resultが`no_counterexample_found`の場合だけ、同じ変更predicateをartifact変更へ開く。`counterexample_found`または`unavailable`では開かない。この置換はevidence operationを再開せず、`implementation_bound`を失効させず、review対象外の通常変更経路へ追加operationを作らない。

## 責任構造と実行境界の分離

次Candidateのpromptではreviewを一つの`PRECHANGE_REVIEW` lifecycleへまとめ、その内部を次の八責任へ分ける。

| 責任 | 所有する判断 | 所有しないもの |
|---|---|---|
| `APPLICABILITY` | 明示review contractが現在の変更subjectへ適用されるか | owner語列からの推測、producer起動 |
| `EXECUTION_PERMISSION` | current reviewを新規実行してよいか | review要否、保存resultの利用許可、tool failure |
| `OPERATION_READY` | operation identity、producer、criterion、scopeが固定済みか | permissionの補完、observation成功、review result |
| `PACKET` | 許可fieldだけのpacketを形成できるか | review judgement、禁止sourceの配送 |
| `OBSERVATION` | 固定descriptorのvalue、missing、unreadableまたはterminal failure | root推測、別observationによる補完 |
| `JUDGEMENT` | reviewerが三つのallowed result kindの一つを形成する | rootによる代行、change admission |
| `RESULT_ADMISSION` | producer、sender、subject、result kind、使用観測が一致するか | judgementの再実施、別subjectへの転用 |
| `CHANGE_EFFECT` | admitted resultが対応変更を許可または停止するか | task全体、無関係operation、validationへの効果伝播 |

八責任は説明と状態所有の境界であり、八operation、八tool callまたは八model stepを意味しない。次を明示的不変条件とする。

```text
responsibility_separation != dispatch_dependency

dispatch_dependency(a, b) :=
  a.resultがbの必要性、target、permission、methodまたはstop conditionを変え得る
```

同一producer内で既に固定済みの値を分類するだけの責任間にmodel returnを入れない。tool resultまたは独立producer resultがなければ次のpredicateを判定できない場合だけ待つ。

## 適用条件

reviewを適用する条件は、C191で成立した正の適用境界へ限定する。

```text
explicit_prechange_review_fixed :=
  TaskSpecまたは適用中repository authorityが
    現在のimplementation_boundな変更predicateをreview subjectとして直接固定
  ∧ 独立producer execution identityを固定
  ∧ review criterionを固定
  ∧ allowed result kindを固定
  ∧ review result consumerを対応変更へ固定
  ∧ required review scope identityを一件以上固定
```

`explicit_prechange_review_fixed=false`なら、review lifecycle全体を`not_applicable`として通常のC147変更経路へ進む。欠けたfieldをrootが推測または一般的慣行で補完しない。review taskという名称、criterion owner、risk owner、静的確認、独立確認または成果確認だけではtrueにしない。

同じTaskSpecがrequired review scopeを空集合として直接固定する場合も`not_applicable`とし、reviewerを起動しない。保存済みreview resultの再利用は、後続の別変更軸とする。本設計の初回Candidateではcurrent review resultだけを扱い、prior result admissionを追加しない。

## 変更直前reviewの起動閉包

適用されたreviewは、汎用候補集合へ入れず、対応変更の未充足先行predicateとして一件だけ形成する。

```text
prechange_review_ready :=
  implementation_bound
  ∧ explicit_prechange_review_fixed
  ∧ review execution permission=allowed
  ∧ review operation identityが一意
  ∧ producer execution identityが一意
  ∧ criterion、allowed result kind、consumer、required scopeが固定済み
  ∧ allow-list packetを形成可能
```

`prechange_review_ready=true`なら、C147の`PRODUCER`、`CONTEXT`、`OWNER_ROLE`および`ROOT`に従い、一つのreview operationを指定producerへ一回だけ配送する。reviewerの観測対象がmissingまたはunreadableでも、descriptorとallowed readが固定済みならoperation readinessをfalseにしない。観測結果としてreviewerが扱う。

permission denied、producer identity不定、scope不定、packet形成不能または禁止情報を安全に分離不能な場合はreviewerを起動せず、対応変更を許可せず`unavailable`とする。rootや別producerへのfallbackを行わない。

packetは許可されたfield-valueとprovenanceだけから新規構築する。禁止fieldは実値だけでなく、key、空値、null、要約、存在状態または無視指示も含めない。禁止fieldを含むsource全体を配送しない。packet内projectionで判定可能なsourceをreviewerへ重複readさせない。

## judgement、result admission、変更効果

reviewerが返せるresult kindは、TaskSpecが固定した有限集合に限る。ADR9 r2では`counterexample_found / no_counterexample_found / unavailable`である。rootはreviewerの意味判断を再実行せず、次の機械的対応だけを確認する。

result kindごとのterminal条件を混ぜない。

```text
counterexample_result_ready :=
  concrete witnessがvalue
  ∧ witnessへ適用する規範predicateと必要入力がvalue
  ∧ 固定済み変更predicateとの直接矛盾が成立
  ∧ 解消には現在の変更predicate、permission、methodまたはstop conditionの変更が必要

no_counterexample_result_ready :=
  required review scope全件を判定済み
  ∧ resultが依存するfinite manifest observation全件がvalue
  ∧ 規範predicate適用後もcounterexampleなし

unavailable_result_ready :=
  counterexample_result_ready=false
  ∧ no_counterexample_result_ready=false
  ∧ 未解決predicateが固定済み
  ∧ そのpredicateを閉じ得るrequired observationのnon-value resultが固定済み
```

`counterexample_result_ready=true`なら、certificateと無関係なmanifest observationのmissingまたは未発行を理由に失効させない。`no_counterexample_result_ready`はrequired scopeまたは必要manifestを一件でも省略して成立させない。一般的不確実性、将来反例の可能性またはreviewerの自信不足だけで`unavailable`を成立させない。

```text
current_review_result_admissible :=
  review operation identity一致
  ∧ producerとsender identity一致
  ∧ subject identity一致
  ∧ result kindがallowed
  ∧ resultが使用した観測へbind可能
  ∧ result kindに対応する上記terminal条件が成立
  ∧ forbidden input不使用
```

admissible resultの効果は対応変更だけへ固定する。

| result | 対応変更への効果 | 外側terminal |
|---|---|---|
| `no_counterexample_found` | 変更前review predicateをsatisfiedにし、他のC147 gateが全件成立した場合だけ変更を許可 | 変更とrequired validation後に判定 |
| `counterexample_found` | 現在の変更predicateを許可しない | 現subjectを`blocked` |
| `unavailable` | 現在の変更predicateを許可しない | 現subjectを`unavailable` |
| result欠落またはinadmissible | 変更を許可せず、rootが補完しない | producerまたはsessionがnonterminalならoperationもnonterminal。producer terminal後にC147のidentity・sender・result binding条件を満たせなければ`unavailable` |

`counterexample_found`後に同一subjectをその場で修正してreviewを再開しない。別案を試す場合は、新しい変更predicateとreview subject identityを形成し、C147の変更前evidence境界から別operationとして始める。review resultは開始identity、無関係なread、別artifactの独立変更、完了済みresultまたはtask全体へ伝播させない。

## C147、C175、C191からの採用境界

| source | 採用するもの | 採用しないもの |
|---|---|---|
| C147 | 通常operation、result effect、evidence、producer、terminal、validation、method、recovery | 訂正済みADR9機序を成功証明として扱うこと |
| C175 | operation readinessと観測結果の分離、専用producer、allow-list packet、permission-before-dispatch | C173由来の自律的review要否、prompt本文、直接親関係 |
| C191 | review責任の分離、owner非権限化、明示review applicability | 外側operation分解、観測atom体系、prior result再利用、逐次実行、prompt本文、直接親関係 |
| C198 | 開始identity単独化の部分効果とreview接続失敗の反例 | `selected_operations`、包含最小集合、候補再選択、`REVIEW_SELECTION` |

この採用境界により、失敗Candidateの機構を親として持ち込まず、成立した責任と具体的反例だけをC147上の新しい一接続へ使う。

## 次Candidateで変更する位置

次Candidateを作る場合のprompt差分は、次の三位置に限定する。

1. `START_BOUNDARY`を一条項追加し、TaskSpec明示の開始identity、stop scope、required result valueおよび最初の実repository operation集合だけを所有させる。
2. C147の`EVIDENCE_GATE`末尾にある`implementation_bound`からartifact変更への無条件遷移を、上記`prechange_transition`へ置換する。
3. `PRECHANGE_REVIEW`を一条項追加し、内部に`APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT`の八責任を置く。

C147の`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`および`RECOVERY`は逐語保持する。`EVIDENCE_GATE`も上記遷移以外は逐語保持する。

三位置は「責任位置を実行順序へ直接対応させ、無関係な責任を一つのoperation選択へ混ぜない」という一つの構造変更である。`START_BOUNDARY`を分けることで開始stop scopeをreview選択から独立させる。`PRECHANGE_REVIEW`だけを追加すると、C147の既存遷移がreview前のartifact変更を許す。遷移だけを置換すると、review applicability、producer、packet、result admissionおよび変更効果の所有者がない。したがって同じCandidateで扱う。

## ADR9 r2とStandard14で確認する経路

最初の評価系列はADR9 r2全9ケース各N=5とする。全45件で品質Score 4、開始identity dependency、reviewer cardinality、packet情報封鎖、current result admission、result kind、artifact変更境界およびrequired commandを確認する。一件でも品質または機構が不通過なら保存して停止し、Standard14へ進まない。

ADR9通過後だけStandard14全14ケース各N=5を実行する。Standard14では追加reviewer 0件を必須とし、C147が成立させた開始identityと許可済みreadの共同発行を退行させない。品質全70件、command protocol、artifact境界、model step、all-agent tokenおよびelapsedを確認する。別の評価系列は追加しない。

KPIは品質、all-agent tokenおよびelapsedの三つを保存する。ただしtokenまたはelapsedの改善をreview起動、result admission、情報封鎖またはdependency成立の代用にしない。

## 次Candidate作成前の方向review

方向reviewでは少なくとも次をcase名に依存しない一般状態で確認する。

1. review非適用の変更はC147通常経路だけで完了できる。
2. mismatch時にreadも禁止する開始contractではidentityだけを最初に発行する。
3. mismatch時にreadを禁止しない開始contractではidentityと必要readを共同発行する。
4. required identity valueを返せないmethodを開始methodにしない。
5. 明示review contractがある変更だけ、`implementation_bound`後にreviewが一件起動する。
6. review責任を分けても、tool result dependencyのない責任間にmodel returnを作らない。
7. permission deniedではreviewerも変更も発行しない。
8. missing observationをoperation readiness不足へ変換しない。
9. allow-list packetを作れない場合にrootが補完または代行しない。
10. `counterexample_found`が対応変更だけを止め、無関係なmissingで失効しない。
11. `no_counterexample_found`がrequired scopeと必要manifestの全件valueを要求する。
12. `unavailable`が固定された未解決predicateとnon-value observationへbindする。
13. `no_counterexample_found`だけではC147の他の変更gateやvalidationを省略しない。
14. result欠落またはinadmissible時に変更へ進まない。
15. review resultをtask全体または別operationへ伝播させない。
16. `EVIDENCE_GATE`の置換がreview非適用時の直接artifact変更を維持する。
17. `EVIDENCE_GATE`の置換がreview適用時のreview前artifact変更を禁止する。
18. prior result、ticket、receipt、ledger、共通dispatch機構または追加評価系列なしで成立する。

一件でも一般反例が残る場合はCandidateを作らず、本設計を改訂する。方向review通過後だけ、C147の直接childとしてpromptを構築し、構造・identity・非変更targetを静的検証する。

## 非目標

- C175、C191またはC198を直接親にすること
- 全operationの最小集合または全タスクの最短経路を新しい共通schemaで表すこと
- 保存済みreview resultの再利用
- reviewをartifact変更後またはvalidation内へ置くこと
- review要否をowner、risk、task名または一般的有用性から推測すること
- runtime、executor、CLI、tool adapterまたは外部wrapperを変更すること
- 新しいcase、rating contract、releaseまたはtarget本体へのprojection

## 現在状態

`post_candidate198_structured_prechange_review_design_fixed / c147_direct_base / chronological_boundary_structure / start_boundary_one_clause_added / evidence_gate_transition_replaced / prechange_review_one_clause_added / other_twelve_c147_clauses_preserved / review_after_implementation_bound_before_change / c191_responsibility_structure_only / c175_admission_connection_only / responsibility_not_dispatch_dependency / current_result_only / ADR9_then_Standard14_only / direction_review_required / candidate_not_created / evaluation_not_started / release_not_created / projection_not_performed`
