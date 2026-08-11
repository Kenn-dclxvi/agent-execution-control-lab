# review decision record全域性設計

> 状態: `pre_candidate_design / adversarial_review_not_started / candidate_not_created`

## 結論

この設計はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基準とし、有限固定効果のreview不要判定と、reviewerが返す具体的反例・反例なし・利用不能の形成を、一つの`review_decision_record`の前後段として固定する。

追加する制御は`review_decision_record_totality`の一軸だけである。Candidate147が固定したoperation、producer、terminal result、`implementation_bound`、変更predicate、permissionおよび`result_effect_scope`の単位を変更しない。tool、file、schema、read順、review回数、worker数、runtimeまたは外部executorを固定しない。

本設計はCandidate bundleではない。情報封鎖した実装前敵対的reviewが`no_counterexample_found`で終端するまでCandidate番号、prompt bundle、profile、Target評価、採用、releaseまたはprojectionを作成しない。

## 設計対象

本設計は、authorityと変更predicateの効果が有限固定集合として完全一致する場合のreview不要判定と、reviewが必要な場合に非value入力を含む全許可入力の判断効果をterminal recordへ閉じる境界だけを扱う。評価case、過去resultまたは既存Candidateの挙動を設計本文の入力にしない。

## 基準と非継承

直接の基準はCandidate147だけとする。後続Candidateの本文、label、state名、coemission機構、registry、record schema、locator、完全coverage条件または未来集合の閉包条件は継承しない。Candidate147へ次の二つの観測可能な決定だけを追加する。

1. finite effect entry同士の全件対応を機械的な比較形へ固定する。
2. reviewerが受領した各input stateの判断効果を全件分類してterminal recordを形成する。

## 開始条件とsubject

開始条件はCandidate147の`implementation_bound=true`である。Candidate147が一つの実行可能な変更predicateとしてbindしたidentityを一つの`review_subject`とする。

- 一predicateが複数target、field、artifactまたは一つのartifact間relationを含んでも分割しない。
- Candidate147が複数predicateを個別bindした場合だけ複数subjectとする。
- read-only operation、validation、別required outcomeまたは未来の変更候補をsubjectへ加えない。

本境界は`implementation_bound`を補完、再探索または再証明しない。

## review decision recordの固定順序

各subjectについて次を一度だけ順にbindする。

1. `implementation_bound=true`を確認する。
2. subjectと変更predicateを固定する。
3. authorityと変更predicateの全change effectをfinite effect occurrence graphと0個以上のopen class effect componentへ重複・欠落なくpartitionし、component間relationと全保持constraintをsubject relation basisへbindする。
4. 全componentのcorrespondenceを合成し、subject correspondenceを`matched | unmatched | unbound`の一状態へbindする。
5. `matched`ならreviewを作らず変更predicateを個別にadmit可能とする。
6. `unmatched | unbound`なら、reviewとは別のadmission operationへproducerをbindし、permissionと独立review producerのbind可否を判定する。
7. admission operationが`admitted(review_producer_identity)`で終端した場合だけ、許可入力identity全集合を固定し、その全集合とdomainが一致するterminal input state mapをbindしてreviewを発行する。`not_admitted(cause_identity)`ならreview operationを作らず、対応subjectの未発行変更だけを止める。
8. reviewerは許可入力identity全集合とdomainが一致する全input effect classificationを含むterminal recordを一つ返す。
9. terminal recordの効果を対応subjectの未発行変更だけへ適用する。

後段のreview result、manifest可読性、現在target数、予定validationまたは具体的反例をsubject correspondenceへ逆流させない。

## subject effect partition

Candidate147が一つの変更predicateへbindした全change effect identityを、次のpartitionへ一度だけ割り当てる。保持constraintはcomponentへ所有させず、後述のsubject relation basisへ一度だけbindする。

`subject_effect_partition := (finite_effect_graph_or_empty, open_class_effect_components)`

`open_class_effect_components`は0個以上のcomponentからなる。各componentは一つのclass predicateへ届く効果を持つ。同じ変更predicateにfinite effectとopen class effectが併存しても一方を選ばず、双方を同じpartitionへ保持する。複数のopen class effectもcomponentを縮約せず個別に保持する。

`partition_coverage := complete | incomplete | unbound`

- `complete`: finite graphの全occurrenceと全open class componentのeffect identityの非重複和集合が、変更predicateへbind済みの全change effect identityと完全一致する。
- `incomplete`: 全identityがbind済みで、重複割当て、未割当てまたはpartition外の追加effectが一件以上ある。
- `unbound`: coverage比較に必要なidentityが`missing / unreadable / terminal failure`である。

authority側とimplementation側でそれぞれpartitionとcoverageをbindする。partitionはsubjectを分割せず、一つのsubject correspondenceを形成するための内部component表現である。

## 有限固定効果のoccurrence対応

有限効果では、TaskSpecまたは適用中authorityが直接固定した各atomic effectを、重複を縮約しないoccurrence nodeと、その適用順または依存順を表すedgeへ変換する。

`effect_occurrence := (occurrence_identity, target_binding, precondition_binding, transform_or_end_state_binding, occurrence_constraint_reference_set)`

`authority_effect_graph(subject) := (occurrence_multiset, order_or_dependency_edges)`

Candidate147の`implementation_bound`へbind済み変更predicateも同じ要素を持つgraphへ変換する。

`implementation_effect_graph(subject) := (occurrence_multiset, order_or_dependency_edges)`

`occurrence_multiset`は同じtarget、precondition、transformまたはend state、constraint参照を持つnodeが複数あっても、その個数と各`occurrence_identity`を保持する。集合へ縮約しない。順序が効果へ影響する場合は、その順序をedgeとして全件bindする。順序非依存が直接bind済みの場合だけ該当node間のedgeを要求しない。

各`binding`は`(identity, bound_value)`である。`occurrence_constraint_reference_set`は、subject relation basisに一度だけ保存されたconstraintのうち、`dependency_identity_set`が当該occurrenceを含むconstraint identityへの参照だけを保持する。constraintのbound valueをnodeへ複製しない。nodeとedgeは既にbind済みのidentityと値から作り、照合のための追加read、再探索、自然言語上の類似判定または未来target列挙を行わない。

preconditionはauthority側とimplementation側で独立に`present(precondition_binding) | absent`へbindする。一方で`absent`を観測しても他方へ伝播させない。双方`absent`の場合だけ一致し、片側が`present`で他方が`absent`、または双方`present`でidentityかbound valueが異なる場合は`unmatched`とする。preconditionの有無または値をbind不能な場合は`unbound`とする。

atomic effectのoccurrenceまたは必要な順序・依存identityがbind不能なら`matched`にしない。

変更predicateにsubject effect partitionの外へ届く選択規則、fallback、正規化または追加変換があるかを次へbindする。

`extra_effect_rule_state := absent | present | unbound`

`finite_component_matched(subject) := authorityとimplementationのfinite graphが双方empty ∨ (authority occurrence数 == implementation occurrence数 ∧ occurrence_identityによる一対一対応が全nodeで成立 ∧ 対応nodeのtarget_binding、precondition_binding、transformまたはend state binding、occurrence constraint reference集合が全件一致 ∧ 対応後のorder_or_dependency_edgesが全件一致)`

- 式が全件成立すればfinite componentは`matched`。
- 全比較値がbind済みで一項目以上が不一致ならfinite componentは`unmatched`。
- 比較に必要なidentityまたは値が`missing / unreadable / terminal failure`ならfinite componentは`unbound`。

target数、relationの存在、`design_relies_on_boundary`、予定validation、現在constraint成立またはreview permissionは式を変更しない。targetが複数でも一predicateなら一回のoccurrence graph照合だけを行う。

## open class effect

各open class componentへ届く変更は、次のbasisを一つにbindする。

`open_class_basis := (class_predicate_binding, definition_binding, version_binding, deterministic_transform_binding, component_constraint_reference_set)`

`component_constraint_reference_set`は後述のsubject relation basisに一度だけ保存されたconstraintのうち、dependency identity setが当該componentを含むconstraint identityへの参照である。constraintをcomponentへ複製して所有させない。

既存の許可済みmachine-boundなconstraint保持resultは、現在の`open_class_basis`と同じidentityおよびbound valueをdependencyとして持ち、そのcoverage predicateが「現在のclass predicateを満たす全instanceへ現在の決定的変換を適用しても、当該componentだけへ依存する全constraint bindingが保持される」ことへbindされ、かつterminal successである場合だけcomponent-localな全class coverageを持つ。複数componentへ依存するconstraintは後述のsubject relation resultだけで閉じる。sample、現在列挙済みinstance、部分集合または別versionの結果は全class coverageにしない。

`open_class_component_matched(component) := authorityとimplementationのcomponent identityおよびopen_class_basisが一致 ∧ result.basis == implementation.open_class_basis ∧ result.coverage_predicate_domain == current_class_predicate ∧ result.covered_transform == deterministic_transform_binding ∧ result.preserved_constraints == component-local constraint bindings ∧ result.terminal=success`

authorityとimplementationのopen class component数が一致し、component identityによる一対一対応が成立し、全対応componentでこの式が成立する場合だけopen class componentsを`matched`とする。双方0個の場合も`matched`とする。一componentでも具体的不一致なら`unmatched`、必要bindingが一件でもbind不能なら`unbound`とする。

未来instanceの列挙やreviewerによる一般的不確実性の解消は要求しない。全class coverageはinstance列挙ではなく、現在basisへbindされたmachine predicateのdomainで閉じる。basis、coverage domain、変換またはconstraintの具体的不一致は`unmatched`、必要binding、coverage predicateまたはmachine-bound resultのmissing等は`unbound`とする。

## subject relation basis

component内およびcomponent間の意味関係を、次へ一度だけbindする。

`constraint_dependency_binding := (constraint_identity, bound_value, dependency_identity_set, evaluation_stage_binding)`

`subject_relation_basis := (inter_component_order_or_dependency_edges, constraint_dependency_binding_set)`

`dependency_identity_set`は、一つのconstraintが依存するfinite occurrenceまたはopen class component identityを1個以上保持する。複数componentへ届く共有constraintも一bindingとして保持し、そのdependency setから各componentが参照する。`evaluation_stage_binding`はconstraintを判定する合成前後のstate identityを固定する。

`inter_component_order_or_dependency_edges`は、finite occurrenceとopen class component、または複数open class componentの間にbind済みの全順序・依存relationを保持する。非可換な変換の順序を省略しない。順序非依存が直接bind済みの組だけedgeを要求しない。

authorityとimplementationのsubject relation basisは、全edgeと全constraint dependency bindingについてidentity、bound value、dependency set、evaluation stageが全件一致する場合だけ`matched`とする。具体的不一致は`unmatched`、比較に必要な値のbind不能は`unbound`とする。

dependency setが複数componentを含み、そのいずれかがopen class componentであるconstraintには、現在の全dependent component basis、component間edge、constraint bindingおよびevaluation stageをdependencyに持つsubject relation resultを要求する。このresultは、dependent class predicateが許す全instance組合せへbindされた決定的な合成変換後もconstraintが保持されるmachine predicateを持ち、terminal successの場合だけ`matched`にできる。sample、部分的なcomponent組合せ、別順序、別versionまたはcomponent-local resultで代用しない。未来instanceの列挙は要求せず、現在dependency domainへbindされたmachine predicateで閉じる。

## subject correspondenceの合成

`subject_correspondence(subject) := matched iff authority.partition_coverage=complete ∧ implementation.partition_coverage=complete ∧ finite_component=matched ∧ open_class_components=matched ∧ subject_relation_basis=matched ∧ required_subject_relation_results=matched ∧ extra_effect_rule_state=absent`

- 全比較値がbind済みで、いずれかのpartitionが`incomplete`、finite component、open class components、subject relation basisまたはrequired subject relation resultが`unmatched`、またはextra ruleが`present`なら`unmatched`。
- coverage、component比較、relation、required resultまたはextra ruleの判定に必要な値が一件でもbind不能なら`unbound`。

finiteだけ、open classだけ、両者の混合、または複数open classのいずれでも同じ合成式を使う。一componentの`matched`をsubject全体の`matched`へ読み替えない。

## review要否とpacket形成

`review_requirement(subject) := not_required if subject_correspondence=matched else required`

`not_required`とreview admissionまたはreview operationは同じsubjectへ併存できない。`required`の場合だけreview admission operationを作る。admission operationはpredicate前に自身のproducerを一つbindし、permissionと独立review producerのbind可否を次のterminalへ閉じる。admission producer、implementation producer、review judgement producerは相互に異なるexecution identityでなければならない。同じexecution identityを二つ以上のroleへbindしない。

review admissionは、permission bindingと当該subjectへ許可された全input source authorityをbasisに、次のinput domain receiptを形成する。

`review_input_domain_receipt := (permission_basis_identity, allowed_input_source_basis_set, complete_input_identity_set, coverage_predicate_identity, coverage_result_dependency)`

`coverage_result_dependency`は、現在のpermission basisと全許可input sourceに対し、permission内でreviewへ渡せるinput identityを余剰・欠落なく列挙したterminal successへbindされなければならない。有限の直接列挙または現在basis全域を閉じるmachine-bound enumerator resultを許す。形成側が選んだ自己申告集合、sample、現在可読な入力だけ、別permission basisまたはnonterminal resultを完全性receiptにしない。

`review_admission_result := admitted(review_producer_identity, review_input_domain_receipt) | not_admitted(permission_denial_identity) | not_admitted(review_producer_binding_failure_identity) | not_admitted(input_domain_unbound_identity)`

admission operationのproducer terminal resultだけがこの状態を形成する。`not_admitted`の場合はreview operation、packet、classificationまたはreview terminalを作らない。rootがadmission producerでない場合は、このresultを補完しない。起動方法のfailedまたはunavailableをpermission denialへ読み替えない。

review発行前に、admission resultのinput domain receiptから、permission内で当該subjectの判断へ渡せる入力identity全集合を一つ固定する。

`allowed_review_input_identity_set(subject) := {input_identity}`

各許可入力identityへ次の一状態をbindする。

`review_input_state(input) := value(identity,value) | missing(identity) | unreadable(identity) | terminal_failure(identity,result)`

`review_input_state_map.domain`はinput domain receiptの`complete_input_identity_set`および`allowed_review_input_identity_set`と完全一致しなければならない。余剰または欠落identityが一件でもあればpacketを発行しない。`missing / unreadable / terminal_failure`であること自体はpacketを未完成にしない。packet identityにはinput domain receipt、`allowed_review_input_identity_set`とstate mapを含める。packetはTaskSpec、適用中authority、Candidate147が許可したrepository evidence、implementation choice、subject、保持constraint、review criterion、全許可入力identityと各terminal state、および下記terminal recordの形成条件だけを含む。

評価case、fixture、oracle、rating、過去finding、旧Candidate、期待terminal、修正案または会話履歴を含めない。

`admitted`にbindされた、admission producerおよびimplementation producerの双方と異なる独立producerだけをreview operationのproducerとする。producer identityを後から変更せず、同じreview judgementを別producerへ再割当てしない。packetの`allowed_review_input_identity_set`はadmission resultへbindされた`complete_input_identity_set`とidentityおよび全要素が完全一致しなければならない。

## input effect classification

reviewerはpacket identityへbindされた`allowed_review_input_identity_set`の全identityについて、次の一分類をterminal前にbindする。

`input_effect_class(input) := counterexample_support | outcome_sensitive | irrelevant`

各classificationはlabelだけでなく次のrecordを持つ。

`input_effect_class_record := (input_identity, review_input_state, class, classification_predicate_identity, classification_result_dependency)`

- `counterexample_support`: そのinput stateまたはvalueが、bind済みの具体的反例を直接成立させる。classification predicateとresult dependencyはcounterexample recordの同じsupport atomおよびdirect conflictへbindする。
- `outcome_sensitive`: そのinputが別の許可値なら、同じsubjectについて具体的反例の成立または不成立が変わり得る。classification predicateとresult dependencyは、原因input identity、terminalを変え得る許可値またはstateのidentity、および具体的反例predicateへbindする。
- `irrelevant`: packetに固定されたsubject、authority、保持constraintおよび反例predicateに対し、当該inputの全許可値またはstateでterminal judgementが不変であることを直接bindする。classification predicateは当該inputの現在の許可値domainとsubject basis全体を持ち、classification result dependencyはその全domainで同じterminal identityになることをbindした受領済みterminal successでなければならない。sample、現在stateだけ、一般的推測またはreviewerのlabelだけで代用しない。

`input_effect_class_map.domain`はinput domain receiptの`complete_input_identity_set`およびpacketの`allowed_review_input_identity_set`と完全一致しなければならない。一inputへ複数分類をbindしない。classification predicateまたはresult dependencyを省略しない。現在のsubject、input domainまたはreview input stateとbasisが一致しないresultを使わない。`missing / unreadable / terminal_failure`を値が存在しないことだけで`irrelevant`にしない。open domainまたは未来instance未列挙だけを`outcome_sensitive`にしない。

具体的反例が成立済みで、そのmissing等が反例の成立条件を変えない場合は`irrelevant`とし、成立済み反例を失効させない。missing等の値によって未選択instance、処遇または直接矛盾が成立し得る場合は`outcome_sensitive`とする。

## terminal recordの三状態

reviewerは次の排他的terminalを一つ返す。

### `counterexample_found`

次の全要素を一つのrecordへbindした場合だけ成立する。

`counterexample_record := (witness_input_or_state, subject_output_or_treatment, violated_predicate_identity, direct_conflict, counterexample_support_set)`

`packet_support_atom_set := {TaskSpec binding, subject binding, authority binding, implementation choice binding, 保持constraint binding, (input_identity, review_input_state(input))}`

- witnessは`packet_support_atom_set`に属する一つ以上のbind済みidentityと値またはterminal stateである。packet外の入力または状態をwitnessにしない。
- treatmentはsubjectがそのwitnessへ与える出力または処遇である。
- violated predicateはTaskSpec、authorityまたは保持constraintのidentityである。
- direct conflictはtreatmentとviolated predicateの直接矛盾である。
- support setはwitnessとdirect conflictを直接成立させる`packet_support_atom_set`の全atomを保持する。`input_effect_class=counterexample_support`の全inputは`(input_identity, review_input_state(input))`として必ず含める。`value`はbind済み値を含むstate全体を、`missing / unreadable / terminal_failure`はそのterminal state全体を記録し、非value stateを値へ変換しない。許可入力集合が空でも、packetへbind済みのTaskSpec、subject、authority、implementation choiceまたは保持constraintが直接矛盾を成立させる場合は、それらのatomから非空support setを形成する。

`counterexample_support_set`は非空であり、witness dependencyを全件含み、`packet_support_atom_set`の部分集合でなければならない。terminal recordは`record_dependency_identity_set`を持ち、その集合はpacket identityへbind済みのTaskSpec、subject、authority、implementation choice、保持constraintおよび`counterexample_support_set`のidentityだけからなり、packet外identityを含まない。全許可入力のclassificationは`counterexample_support | irrelevant`のいずれかで、`outcome_sensitive`は0件でなければならない。値により反例成立が変わるinputが残る場合は`counterexample_found`ではなく、下記`unavailable`へ閉じる。

一要素でもbind不能なら`counterexample_found`を返さない。rootは欠落要素を補完しない。

### `no_counterexample_found`

次を全件満たす場合だけ成立する。

- `review_input_domain_receipt.complete_input_identity_set == review_input_state_map.domain == input_effect_class_map.domain == allowed_review_input_identity_set`である。
- 許可入力全集合に属する全value入力について具体的反例が成立しない。
- 許可入力全集合の全input identityに`input_effect_class`がbind済みである。
- `missing / unreadable / terminal_failure`を含む全非value入力が`irrelevant`である。
- `outcome_sensitive`が0件である。

反例不存在の未来全域証明、input domainの完全列挙または一般的不確実性の解消を要求しない。

### `unavailable`

次のいずれかをbindした場合に成立する。

- 一つ以上のinputが`outcome_sensitive`であり、原因input identityと、その値により成立または不成立が変わり得る具体的反例predicateをbindした。
- counterexample recordの必須要素を受領済みinputだけでは対応づけられず、`missing_counterexample_field_identity`、`missing_dependency_identity`、およびその欠落により形成不能になる`counterexample_found`のterminal identityを全件bindした。
- 一つ以上のinputについてclassification predicateまたはclassification result dependencyが`missing / unreadable / terminal_failure`であり、原因input identity、欠落dependency identity、形成不能になるclassification、およびその欠落により形成不能になる`counterexample_found | no_counterexample_found`のterminal identityをbindした。

open domain、未来instance未列挙、一般的不確実性、review回数または探索未完了だけでは`unavailable`にしない。

## rootの受入境界

rootは全terminalに共通してproducer identity、terminal性、subject identity、packetへbind済みinput domain receiptのbasisとterminal success、`complete_input_identity_set`、`allowed_review_input_identity_set`、state map domain、classification map domainの完全一致、全`input_effect_class_record`のpredicate identityとresult dependency、当該terminal固有の必須field identityおよびresult dependencyだけを確認する。さらにterminal identityごとに次だけを確認する。

- `counterexample_found`: 非空support setが`packet_support_atom_set`の部分集合でwitness dependencyを全件含むこと、`outcome_sensitive=0`、`record_dependency_identity_set`がTaskSpecとimplementation choiceを含むpacket identity basisの部分集合であること。
- `no_counterexample_found`: 全非value入力が`irrelevant`、`outcome_sensitive=0`である。非空support setを要求しない。
- `unavailable`: 上記`unavailable`形成理由の原因identityとdependencyが存在する。counterexample field欠落の場合は欠落field、欠落dependency、形成不能terminal identityが全件存在する。classification根拠欠落の場合は原因input、欠落dependency、形成不能classificationとterminal identityが全件存在する。`outcome_sensitive`を原因とする場合は1件以上を許し、非空support setまたは`outcome_sensitive=0`を要求しない。

これらの確認は意味判断ではなく、bind済みidentity、domainおよびterminal固有fieldの機械的coverage確認である。rootは反例の意味、分類の正しさ、missingの関連性または反例なしの十分性を再判定、補完、比較または再採点しない。

recordがterminal形成条件を満たさない場合、そのreview operationはadmissibleなterminal resultを持たず、nonterminalのまま保持する。rootは`unavailable`を含むterminal resultへ変換せず、進行報告、集約結果またはfinal responseで補完しない。同じjudgementを別producerまたはrootへ再割当てしない。`unavailable`は、bind済みproducer自身が上記形成条件を満たすrecordとして返した場合だけreview terminalになる。

## result効果と失効

- `matched / not_required`は対応subjectだけを個別にadmit可能にする。
- review admissionの`not_admitted`は対応subjectを含む未発行artifact変更だけを停止する。
- `counterexample_found`は対応subjectを含む未発行artifact変更だけを停止する。
- `no_counterexample_found`は対応subjectだけを個別にadmit可能にする。
- `unavailable`は対応subjectを含む未発行artifact変更だけを停止する。

別subject、read-only operation、別required outcomeまたはtask全体へ効果を伝播させない。停止subjectを除くとrequired outcome、artifact間relation、実行可能性または保持constraintを満たせない場合は、Candidate147の当該implementation choiceだけを失効する。

subject correspondence recordはauthority / implementationそれぞれのpartition coverage、全occurrence node、component内外の全orderまたはdependency edge、全open class componentの`open_class_basis`とcoverage predicate、全constraint dependency binding、required subject relation result、extra rule stateをbasisへbindする。review recordはinput domain receipt、`allowed_review_input_identity_set`、全input state、全classification predicateとresult dependency、terminal recordのfieldとdependencyをbasisへbindする。次operation前にbasis一致を確認し、不一致の場合だけ旧resultを失効して変更後basisへ同じpredicateの新producerをbindする。basisが一致するresultを再取得、表現差、support外入力または無関係resultだけで失効させない。

## 正常経路

### 有限固定効果

authorityとimplementationのoccurrence graphがoccurrence identityで一対一対応し、各nodeのtarget、precondition、transformまたはend state、constraint参照、重複数およびorderまたはdependency edgeが一致し、参照先の全constraint dependency bindingもsubject relation basisで一致し、extra ruleがなければ、一回の照合で`matched / not_required`となる。manifest、packetまたはreviewerを読まずにartifact変更へ進む。

### missingを含む具体的反例

packetのmissingをterminal input stateとしてreviewerへ渡す。現在valueだけで具体的反例recordが完成し、missingがその成立を変えない場合、missingを`irrelevant`、必要valueを`counterexample_support`へbindして`counterexample_found`を保持する。

### 判断に関係するmissing

missingの値によって未選択instanceまたは直接矛盾が成立し得る場合、そのinputを`outcome_sensitive`へ分類し、原因identityと具体的反例predicateを持つ`unavailable`を返す。`no_counterexample_found`を返さない。

### permission denial

reviewが必要でもpermissionがdeniedなら、review admission operationのbind済みproducerが原因identityを持つ`not_admitted`を返す。review producer、review operationまたはreview terminalを作らず、当該subjectを含む未発行変更だけを止める。

## 禁止する変換

1. target数、relation、`design_relies_on_boundary`または予定validationだけで有限固定効果をreviewへ送る。
2. occurrenceの重複を集合へ縮約する、orderまたはdependency edgeを捨てる、または自然言語上の類似、現在値、一部一致で`matched`にする。
3. finite effectとopen class effectの一方だけ、または複数open class componentの一部だけの`matched`をsubject全体へ適用する。
4. component間の順序・依存edgeを捨てる、または共有constraintを一componentへ局所化、複製所有もしくはcomponent-local resultだけで閉じる。
5. missing等をpacket readiness failureにする。
6. 許可入力全集合とstate mapまたはclassification mapのdomainが一致しないpacketまたはterminalをadmitする。
7. input domain completeness receiptを自己申告集合、sample、現在可読入力または別permission basisで形成する。
8. classification predicateとresult dependencyなしに分類labelをadmitする、またはmissing等を値がないことだけで`irrelevant`にする。
9. `outcome_sensitive`があるまま`no_counterexample_found`をadmitする。
10. packet外witness、空support setまたは`outcome_sensitive`を残した`counterexample_found`をadmitする。
11. counterexample recordの欠落要素をrootが補完する。
12. 不完全なproducer recordをrootが`unavailable`その他のterminalへ変換する。
13. permission denialまたはreview producer bind不能をreview terminalの`unavailable`へ変換する。
14. support外missingで成立済み反例を失効する。
15. open domainまたは未来instance未列挙だけで`unavailable`にする。
16. 一subjectのresultを別subject、read-only operation、別required outcomeまたはtask全体へ伝播する。
17. tool、file、schema、read順、review回数、worker数または外部runtime変更を解決条件にする。

## Candidate作成前gate

独立した情報封鎖review producerへ、次だけを渡す。

- Candidate147原文
- `docs/prompt-control-design-principles.md`
- 本設計本文

Candidate185本文、評価case、fixture、oracle、rating、raw trace、過去review finding、期待terminal、修正案および会話履歴は渡さない。

review criterionは次のとおりとする。

- 一つのreview subjectがCandidate147の一つの`implementation_bound`変更predicateと一致するか。
- subject effect partition、component間relation、共有constraintと合成式が、finite、open class、両者の混合および複数open classを重複・欠落なく全域的に扱うか。
- occurrence identityによる一対一対応とsubject relation basisがtarget、precondition、transformまたはend state、constraintのidentityとbind済み値の意味差を取りこぼさないか。
- fixed effect fast pathがmanifestやreviewerを要求しないか。
- open class fast pathが現在basisの全classを覆うmachine-bound保持resultを要求するか。
- permission basisにbindされたinput domain completeness receiptを要求し、`missing / unreadable / terminal_failure`を含む許可入力全集合とstate map、classification mapのdomain一致を強制するか。
- `counterexample_found`が許可入力0件の場合を含め、packet内witness、subject treatment、violated predicate、direct conflict、非value stateを表現可能な非空packet support setを全件bindし、packet外dependencyと`outcome_sensitive`を残さないか。
- 全classificationへpredicate identityとresult dependencyを要求し、`no_counterexample_found`がoutcome-sensitiveな非value inputを根拠なく`irrelevant`にできないか。
- `unavailable`が具体的な反例predicate、counterexample fieldまたはclassification根拠の欠落dependencyと、その欠落で形成不能になるterminal identityを要求し、一般的不確実性を許さないか。
- implementation、review admission、review judgementのproducer execution identityを相互に分離し、terminal別root受入条件、root補完禁止、重複review禁止および別producer再割当て禁止を保つか。
- Candidate147のoperation identity、permission、producer、terminalおよびresult effect境界を変更していないか。
- tool、file、schema、read順、review回数、worker数または外部runtimeを固定していないか。

一件でも一般反例が成立した場合は設計を修正し、別identityの独立producerで全criterionを再reviewする。全criterionが`no_counterexample_found`となるまでCandidateを作成しない。

## 状態境界

この文書はCandidate147へ追加可能な制御境界を設計したものであり、Candidate、評価結果、採用、releaseまたはprojectionではない。
