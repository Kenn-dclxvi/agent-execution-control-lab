# Candidate179 review evidence interface 設計

## 目的

一般設計の敵対的reviewで、reviewerが根拠の種類を自己申告して観測receiptを迂回する経路を閉じる。同時に、起動後にしか生まれない値を起動前入力へ要求せず、意味上同じreview resultを表現上の入れ子差だけで棄却しない。

Candidate179は、根拠の資格、取得、結果受理を一つの`review_evidence_interface_admissible` predicateの三段階として分離する。

1. 起動前には、既存入力から直接bindできる最小source entryだけを固定する。
2. 起動後の観測はCandidate177の取得境界を維持し、source entryごとの個別resultへ接続する。
3. reviewer resultはsource identityをinstance bindingで参照し、rootが実行記録またはpacketへ機械照合する。

## 作成前ゲート

1. 基準prompt setは`the-caption-3ce91a4-result-invalidation-locality-r1`（Candidate177）とする。Candidate178は初回targeted gateで停止した診断証拠であり、本文の直接親にはしない。
2. 基準状態の最短正常経路は、起動前manifestの各観測をreviewerが個別に取得し、対応するsuccess receiptを保持し、具体的反例が成立すれば残りの無関係な観測に依存せず`counterexample_found`を返す経路である。
3. 保存済み誤経路はCandidate177 ADR05 N=20で観測された。20件中8件は、起動後のcurrent runtime observationを`prior_fixed_enumeration`またはreceipt済みsourceとして自己申告し、必要な個別観測receiptを経ずに正しい終端へ到達した。
4. Candidate177はsource identityの排他的schemaを結果へ要求するが、source classを誰がいつ固定するかを閉じていない。このためreviewerが起動後の値へsource labelを付け替える判断点が残る。Candidate178はこの判断点を閉じようとして、producer、runtime snapshot、result identity、selector、matching receiptなど起動後に確定する値まで起動前入力へ要求し、同一入力のreview起動と結果受理を不安定にした。
5. 追加する一つのpredicateは`review_evidence_interface_admissible`である。sourceの入力形、取得result、review resultの間の許される写像を一つのinterfaceとして固定する。
6. このpredicateは、reviewerがsource classを変更する判断点と、rootが意味上十分なresultへ新しい証明objectを追加要求する判断点を消す。取得範囲はCandidate177の既存制御を変更しない。
7. 新たに増える判断点は、起動前source registryがfinite manifest全descriptorとsemantic packet全itemを過不足なく含むかという機械照合一件である。
8. 品質維持は変更しないADR9 r2で確認する。特に個別receipt経路、履歴canary非配送、全manifest成功、missing観測時の必須review起動を別々に監査する。試験case、fixture、oracle、rating contractおよび期待終端は変更しない。
9. reviewer未起動、許可範囲外の内容取得、receiptなし観測の採用、意味上十分なresultの表現差による棄却、rootによる反例意味の再判定、またはCandidate177の反例優先終端と局所失効の破壊を一件でも観測した場合は停止する。

## 一般predicate

### 1. 起動前source registry

`review_source_kind := observation | fixed_packet_item`とする。

source kindはsourceの起動前の所在から決まり、reviewer resultのfield、説明、取得方法または値から決めない。

`observation_source_entry := source identity / kind=observation / observation identity / target / success condition`とする。

`fixed_packet_source_entry := source identity / kind=fixed_packet_item / packet item locator / 元source locatorがある場合はそのlocator / exact valueまたは改変不能な構造化内容 / provenance receipt / 既存入力にある場合だけsnapshot applicability`とする。

独立したsource identity、finite manifest identityまたはpacket item identityが既存入力に存在すると仮定しない。source identityはrootが起動前に既存値から次のtupleとして決定的に構成する。

- observation: `kind=observation / review operation identity / observation identity`
- fixed packet item: `kind=fixed_packet_item / review operation identity / packet item locator`

`packet item`は内容の意味的断片ではなく、semantic projection constructorの一つの構文的output occurrenceとする。既存sourceの明示field occurrenceまたはarray element occurrenceは各一itemとする。item境界を持たない非構造化値は、許可されたprojection値全体を一itemとし、rootが内容を読んで追加分割または結合しない。複数item化は、既存入力に独立したfield / element occurrenceがある場合、またはreview起動前に既存TaskSpecかrepository authorityが固定した非意味的projection ruleの独立output slotがある場合だけ許す。

rootはこれらoutput occurrenceを一つのcanonical immutable sequenceへ置く。structured objectはfield pathのUTF-8 byte昇順、arrayはindex昇順、異なる許可sourceはsemantic packet constructorへbindされたsource occurrence順、非構造化値は一occurrenceとして扱う。同じfield内に既存の複数occurrenceがある場合は元source occurrence ordinalを使う。`packet item locator := review operation identity / packet role=semantic_packet / zero-based canonical item position`とし、同一sequence内で一意にする。元sourceに一意なfield pathがある場合はそのsource locatorもentryへ保持するが、locator identityの必須構成要素にしない。禁止内容を含む元source全体をpacketへ戻さない。

packet item locatorはrootが既に許可されたpacket構築の参照位置として決定的に生成できるimplementation identityであり、source value、authority role、snapshot applicability、receiptまたは意味を生成・補完しない。Candidate177の`semantic_projection_valid`を変更せず、locator constructionはCandidate179のregistry predicate内だけで行う。source identityは上記tuple自体であり、新しいauthority、意味valueまたはhashを生成しない。provenance receiptはregistry entryの由来証拠として保持するが、独立したreceipt identityの存在を仮定せずsource identityまたはdomain keyの構成要素にしない。

`required_observation_domain := 当該review operationのfinite evidence manifestにある全observation identityの閉集合`とする。全descriptorが対象boundaryまたは必須review scopeへ一意にbindされていることを別条件とし、未bind、重複bindまたはmanifest外entryが一件でもあればregistryを成立させない。

`required_fixed_packet_domain := semantic_projection_validを満たす起動前semantic packetにある全packet item locatorの閉集合`とする。rootはcontract、authority、design subjectまたはpremiseという意味roleを分類せず、packet内の全itemを起動前fixed itemとしてregistryへ写す。全itemが対象boundaryまたは必須review scopeへ一意にbindされていることを別条件とする。各itemをどの意味predicateのsupportへ使えるかはCandidate177のreviewer criterionが決め、source registry membershipはその意味判断を代行しない。

`review_source_registry_ready := review operation起動前に、required observation domainの全descriptorとrequired fixed packet domainの全itemが対象boundaryまたは必須review scopeへ一意にbind済み ∧ 各要素が対応kindのentryへ過不足・重複なく一対一に写される ∧ 全entryが既存TaskSpec、finite evidence manifest、適用中repository authorityまたはsemantic packet itemへ一意にbind済み ∧ source identityが重複しない ∧ 各entryが上記いずれか一方のshapeだけを持つ`とする。

起動前に要求できるfieldは、上記既存入力へ直接bindできるものだけとする。producer execution identityはCandidate177に従ってreview operationへ起動前bindするが、source entryごとには複製しない。runtime input snapshot identity、result identity、terminal status、success receipt、実測locator、実測値、取得command、selector、canonicalization、content matching receiptおよびreviewer terminal resultは起動後の値であり、source registryの成立条件にしない。TaskSpecがそれらを明示的に固定している場合も、既存値として保持できるだけで、欠落を補完したり一般必須fieldへ昇格したりしない。

`review_source_registry_ready=false`ならCandidate177の`review_operation_admission_closed=false`へbindし、review operationを作らず、既存の起動前`unavailable`で停止する。この停止は起動後のreviewer三終端には含めない。trueなら、起動後にsource entryを追加、削除、別kindへ変換または別manifest・packet itemへ付け替えない。

### 2. 既存取得境界への接続

Candidate179は新しい取得証明、selector contractまたは外部envelopeを追加しない。manifest observationの取得はCandidate177の`CONTEXT`、`semantic_projection_valid`、forbidden input、`result_aggregation_safe`およびindividual receipt規則をそのまま使う。

`observation_acquisition_result := review operation identity / bound producer execution identity / runtime input snapshot identity / acquisition result identity / source identity / observed status=success|missing|unreadable|failed / success時のexact valueまたは改変不能な構造化内容 / individual terminal status / individual receiptが実在する場合はそのreceipt`とする。実際に欠けたreceiptをnull fieldや補完値として生成せず、absentのまま保持する。これらはCandidate177が既に要求するreview operation、producer、runtime snapshotおよびevidence unitへのbindingを、起動前registryのsource identityへ接続した形であり、起動前fieldにはしない。

rootは各acquisition entryを意味判定なしで次の排他的な一状態へ分類する。

- `admissible_success`: `observation_source_admissible=true`
- `admissible_non_success`: identity / operation / producer / snapshot bindingとindividual terminal resultが成立し、observed statusが`missing|unreadable|failed`
- `inadmissible_acquisition`: `missing_individual_receipt | identity_mismatch | operation_or_producer_mismatch | snapshot_mismatch | nonterminal | value_result_mismatch | unsafe_aggregation`の一件以上に該当

`inadmissible_acquisition`のvalueまたはpartial outputをsupportへ昇格させず、実在するacquisition result identityと機械的理由だけを保持する。statusを書き換えず、欠けたreceiptを補完せず、新しい外部証明を要求しない。

上記三分類とassessment recordは、選択したassessment generationが入力として要求する各observationに個別terminal acquisition result identityが実在するreviewer resultへ適用する。必要範囲はgeneration kindごとに次のとおりとする。

- established generation: 実使用supportであるobservationだけ
- not-established complete generation: required observation domain全件
- not-established unavailable generation: required observation domain全件

選択generationの必要範囲で一件でも個別result identity自体が存在しない場合、reviewerは不存在entryまたはreceiptを生成せず、当該assessment recordを構成しない。rootはCandidate177の`TERMINAL`、`delegated_result_ready`およびreview result admissionに従い、当該reviewer resultを不受理としてoperation-level `unavailable`にする。この外側のadmission failureはreviewer三終端に含めず、single assessment carrierはadmissible reviewer terminal resultのcarrierに限定する。established generationで実使用supportではない未発行observationはabsence failureに含めず、Candidate177のconsumer-terminal規則で失効する。

取得command、selector構文、tool call数およびbatch方法はCandidate177と`METHOD`の範囲で選ぶ。allowed read外またはforbidden inputを含むreadを新たに許さない。取得範囲をrootの新しいadmission predicateにせず、外部executor、tool adapter、runtime hookまたはwrapper変更も要求しない。

`observation_source_admissible := acquisition resultのreview operation / producer / runtime snapshot / result / source identityが現在operationへ一致 ∧ source identityがregistry内のobservation entryへ一致 ∧ individual terminal status=success ∧ individual receiptあり ∧ valueが当該individual resultへ一致 ∧ Candidate177のsemantic projectionとforbidden input条件を満たす`とする。

rootまたはreviewerは、aggregate output、隣接child result、説明、同じartifactの別readまたはcurrent snapshotの既知値から、欠けたindividual receiptやvalueを補完しない。`missing / unreadable / failed`は当該sourceのnon-success terminal resultとして保持し、別sourceを失効させない。

registry membershipとevidence support eligibilityを分ける。全`fixed_packet_item`はpacket内valueをそのままregistryへ写し、repositoryから再取得しない。reviewerが直接readした値を`fixed_packet_item`へ昇格させない。全itemのentryにはpacket item locator、valueおよびprovenance receiptだけを必須とし、元source locatorとsnapshot applicabilityは既存packet fieldまたは既存authority relationから直接bindできる場合だけ保持する。

`fixed_packet_source_admissible := 実際にsupport referenceから引用されたfixed itemについて、packet item locator / value / provenance receiptがregistryと一致 ∧ provenance receiptがsourceとvalueの由来へ一致 ∧ Candidate177の当該counterexample pathがcurrent snapshot applicabilityを要求する場合だけ、registryに既存snapshot applicabilityがあり現在のreview runtime input snapshotへ直接適用可能`とする。provenance receipt単体へcurrent snapshot applicabilityを要求しない。pathが要求するapplicabilityを既存入力から直接bindできないfixed itemは反例supportとして引用せず、新しいevaluator、receiptまたはauthority chainで補わない。その欠落だけを`unavailable`理由にせず、引用されていないpacket context itemのapplicability欠落または失効は他sourceまたは`no_counterexample_found`を失効させない。

`fixed_registry_integrity_valid := required fixed packet domainの全itemについて、packet item locator / value / provenance receiptが起動前registryと現在packetで一致し、いずれも直接失効していない`とする。これはitemの意味roleまたはcurrent snapshot applicabilityを判定せず、review対象packetのidentityと内容が変わっていないことだけを機械照合する。

### 3. 最小review result

reviewerが返すterminal resultは後述の`counterexample_assessment_record`そのものとし、別のresult objectまたはprojectionを作らない。正規形を次の三つとする。

- `counterexample_found := assessment record identity / terminal / counterexample identity / boundary identity / counterexample path / contract basis binding / concrete instance / direct contradiction / design effect / support references / decision-premise時のboundary dependency basis binding`
- `no_counterexample_found := assessment record identity / terminal / covered boundary identities / covered review scope / covered observation source identities`
- `unavailable := assessment record identity / terminal / admissible non-success observation entry refs / inadmissible acquisition entry refs / invalidated fixed source refs`

`support_reference := source identity / observationの場合は同じassessment record内のacquisition result identity / reviewer result内でそのsource valueを使用するinstance binding identity`とする。

`instance_binding := binding identity / source identity / optional subvalue locator`とする。source全体を使う場合はsubvalue locatorを空にし、一部を使う場合だけsourceのtyped value内へ機械適用できる構造的locatorを置く。reviewer resultはsource valueを再serializationせず、concrete instance、direct contradictionおよびdesign effectからinstance bindingを参照する。rootはbindingからadmissible source objectまたはそのsubvalueを解決し、reviewerが複製した文字列表現との一致を要求しない。

`contract_basis_binding := Candidate177が要求するcontract basisを一件以上のinstance bindingへ結ぶ参照`とする。`boundary_dependency_basis_binding := decision-premise pathで、明示premise、具体instanceおよびdirect contradictionを、それぞれの根拠となるinstance bindingへ結ぶ参照`とする。basis本文、source valueまたはreceiptを再serializationしない。

`evidentiary_fact_expression`は、事実leafとして`instance_binding_ref`だけを持つ次の有限grammarとする。

- `ref(binding identity)`
- `tuple(ref+)`
- `not(expression)`
- `and(expression+)`
- `or(expression+)`
- `eq(ref, ref)`
- `neq(ref, ref)`
- `member(ref, ref)`
- `relates(relation binding ref, ref+)`

各operator名とarityは上記列挙を正本とし、別名、追加operator、literal operand、空argsまたは型外operandを許さない。`relation binding ref`は関係predicateを値として持つ起動前fixed packet itemのinstance bindingへ解決し、relation名または内容をinlineにしない。非事実定数として追加で許すのは、counterexample path tag、boundary identity、および`design effect category := target_set | general_condition | canonical_authority | ownership | stop | fallback`だけとする。source value、runtime値、contract clause、状態、consumerまたは成果物関係をinline literalとして置かない。

concrete instance、明示premise、contract basisおよびdirect contradictionはevidentiary fact expressionで表す。design effectはboundary identityとdesign effect categoryだけで表し、反例成立に使う新しい事実leafを導入しない。任意の説明文は補助説明として保持できるが、admission、stateまたはterminalの根拠に使わず、そこから事実値を抽出しない。

全support referenceとinstance bindingは非空で、binding identityがresult内で一意でなければならない。全evidentiary fact expressionの事実leafが同じassessment record内のinstance bindingへ過不足なく解決し、未bindの事実literalがなく、decision-premise pathではpremiseとboundary dependency basisも同じ閉包を満たす。意味fieldから到達しない孤立support、同一bindingの重複または一つのbinding identityによる別sourceの兼用を許さない。rootは式の意味を評価せず、leaf型、許可operator、参照解決および未bind literal不在だけを再帰的に機械照合する。

assessment recordは、generation inputに含む各`observation_acquisition_result`の完全形をroot可視のtop-level entryとして一度だけ保持する。support reference、covered observation、non-success集合はそのentry identityを参照し、source value、producer、snapshot、result identity、receiptまたはstatusを別のnested objectへ複製しない。fixed packet itemのvalueとprovenanceはrootが構築済みのsource registryを参照し、reviewer resultへ再掲しない。取得projection、canonicalization、matching receiptまたはpacket lineageを新たに要求しない。

`support_reference_admissible := source identityがregistry内に一意に存在 ∧ observationなら同じassessment record内に現在operation / producer / snapshotへbindされた完全形のadmissible acquisition result entryが一件ありsupport referenceのacquisition result identityへ一致し、fixed packet itemなら対応するpacket itemが存在 ∧ instance bindingがそのsource objectまたは機械的subvalue locatorへ解決可能`とする。source kindとvalueはregistryとrecord entryから得て、別の自己申告または再serializationを受理しない。fixed itemがcontract、authority、design subjectまたはpremiseのどの意味roleを持つかはCandidate177のreviewer predicateだけが判定する。

`counterexample_assessment_generation := 判定に使用した全source identity / observation acquisition result identity / individual receipt / runtime input snapshot / fixed item locator・value・provenance integrity / pathで使用したsnapshot applicability`とする。

assessment generationの入力閉包をterminal候補ごとに固定する。

- `established generation`: 具体的反例を成立させる実使用support全件を含む。無関係sourceは要求しない。
- `not-established complete generation`: observation input集合がrequired observation domain全体と一致し、各inputが同一operation / producer / runtime snapshotのadmissible acquisition resultとindividual receiptへ一対一にbindされ、fixed input集合がrequired fixed packet domain全体と一致して全itemのlocator / value / provenance integrityを同じgenerationへbindする。
- `not-established unavailable generation`: 全admissible success observation entry refs、全admissible non-success observation entry refs、全inadmissible acquisition entry refs、およびrequired fixed packet domain全体のlocator / value / provenance integrityを同じgenerationへbindする。statusとsource identityはentryから解決し別集合へ複製しない。admissible supportから具体的反例が成立する場合はこのgenerationを`not_established`にせず、established generationを優先する。

同じreview operationではassessment generationとimmutable assessment recordを一件だけ生成する。producerはgeneration入力と意味判定を別artifactにせず、一つの`counterexample_assessment_record`として同時に確定する。`assessment record identity := review operation identity / producer execution identity / runtime input snapshot identity / generation kind / generationに含むobservation result identity集合 / fixed item locator集合`というtupleとする。

`counterexample_assessment_record`はgeneration kindに対応する上記三正規形の一つであり、共通してassessment record identity、generation inputに含むobservation acquisition result entry全集合、fixed item locator集合およびconcrete counterexample stateを保持する。`counterexample_found`形はcounterexample identity、boundary identity、counterexample path、実使用support identity集合、instance binding集合、contract basis binding、path別basis binding、concrete instance、direct contradictionおよびdesign effectを明示fieldとして持つ。`no_counterexample_found`形はcovered boundary identities、covered review scopeおよびcovered observation source identity全集合を持つ。`unavailable`形はadmissible success observation entry refs、admissible non-success observation entry refs、inadmissible acquisition entry refsおよびinvalidated fixed source refsを持つ。observationのsource identity、statusおよび実在receiptは参照entryから解決し、record内の別fieldへ複製しない。

同じassessment record内で、入力集合、acquisition result entry、state、binding、意味resultおよびterminalを同時に確定する。別recordのentry、state、support、bindingまたは意味fieldを組み合わせない。reviewerのterminal resultはこのrecord自体であり、同じacquisition resultまたはreceiptを複製した別projectionを作らない。rootはrecord identity、entry schema、集合および参照一致だけを照合し、意味判定を再実行しない。

producerは終端前に、現在admissibleなsupport集合についてCandidate177のnormativeまたはdecision-premise counterexample predicateを実行し、`concrete_counterexample_state := established | not_established`をcounterexample assessment generationへbindして一度だけ確定する。generation内のsupport、result、receipt、snapshotまたはfixed integrityがroot受理前に直接失効した場合、当該stateとassessment recordを失効し、古いstateまたはrecord identityを三終端へ使用しない。

同じreview operation内では意味predicateを再実行せず、二件目のassessment recordを作らない。generation失効後はrootが意味判定またはresultを再生成せず、当該review operationだけをoperation-level `unavailable`にする。再reviewが必要な場合は、新しいreview operation identityとproducer bindingで起動前registryから構成し直す。この停止は別source、別resultまたは別operationへ伝播させない。

`counterexample_result_admissible := terminal resultが一つのestablished counterexample assessment recordそのもの ∧ concrete_counterexample_state=established ∧ counterexample identity / support / instance binding / basis binding / concrete instance / direct contradiction / design effectが同record内generation inputと過不足なく一致 ∧ support referenceが一件以上あり全件admissible ∧ support / binding identityが一意 ∧ concrete instance / contract basis / direct contradictionがevidentiary fact expressionで全事実leafを使用bindingへ過不足なく解決し未bind事実literalなし ∧ design effectがboundary identityと許可categoryだけを持つ ∧ path=decision_premiseならboundary dependency basis bindingが存在して明示premise / concrete instance / direct contradictionを対応bindingへ結ぶ ∧ 孤立または重複supportなし ∧ reviewer terminal resultとsender bindingが成立`とする。

`no_counterexample_result_admissible := terminal resultが一つのnot-established complete assessment recordそのもの ∧ concrete_counterexample_state=not_established ∧ covered observation source identitiesが同recordのgeneration inputから射影したobservation source identity集合と一致し、その集合がrequired observation domain全体と一致 ∧ generation内fixed input集合がrequired fixed packet domain全体と一致 ∧ 全対象boundaryと必須review scopeが過不足なく一致 ∧ required observation domainの各identityに、現在operation / producer / runtime snapshotへbindされたobservation_source_admissible=trueのacquisition resultが過不足・重複なく一件あり、各resultがindividual receiptへ一対一に結び付く ∧ fixed_registry_integrity_valid=true ∧ reviewer terminal resultとsender bindingが成立`とする。起動前packet contextの全itemをreviewer resultへ再列挙したり、反例supportとして引用していないfixed itemのcurrent snapshot applicabilityを証明したりすることは要求しない。

`unavailable_result_admissible := terminal resultが一つのnot-established unavailable assessment recordそのもの ∧ concrete_counterexample_state=not_established ∧ generation内observation acquisition entry refsがadmissible success / admissible non-success / inadmissible acquisitionの排他的な和でrequired observation domain全体へ一対一に解決 ∧ generation内fixed inputがintegrity-valid refsとinvalidated fixed refsの排他的な和でrequired fixed packet domain全体へ一致 ∧ admissible non-success / inadmissible acquisition / invalidated fixedのいずれかが一件以上存在 ∧ terminalの三種unavailable refsが同recordの対応refs全集合へ過不足なく一致 ∧ 各admissible non-success entryが現在operation / producer / snapshotへbindされstatus=missing|unreadable|failed ∧ 各inadmissible acquisition entryが列挙済み機械的理由へ一致 ∧ 各invalidated fixed refが当該itemのpacket item locator / value / provenanceの直接失効へ一致 ∧ reviewer terminal resultとsender bindingが成立`とする。observationのsource identity、status、receipt有無またはfixed item statusを別fieldへ再掲しない。snapshot applicabilityの欠落または失効だけをunavailable fixed sourceへ分類しない。

rootはidentity、集合、statusおよびinstance bindingの解決可能性だけを照合し、必要前提、規範意味、直接矛盾、具体的反例またはdesign effectを再判定しない。必要な意味fieldが欠ける場合は不受理にするが、同じ意味を別の入れ子へ複製することは要求しない。

`review_evidence_interface_admissible := review_source_registry_ready ∧ 全使用sourceがkind別の取得規則を満たす ∧ reviewer terminal resultが上記いずれか一つの正規形と受理条件を満たす`とする。

## 失効と終端

- observation sourceはsource entry、現在のreview operation / producer / runtime snapshot、individual acquisition resultおよびreceiptへ依存する。
- fixed packet itemのregistry membershipはsource entry、packet item locator、valueおよびprovenance receiptへ依存する。実際に引用されたsupport eligibilityだけが、pathで必要なsnapshot applicabilityと現在review runtime input snapshotへ追加依存する。
- support referenceは参照したsourceとinstance bindingへ依存する。concrete counterexample stateはcounterexample assessment generation全体へ依存する。
- `counterexample_found`は実際に使用したsupportだけへ依存し、無関係sourceのmissing、追加または失敗で失効しない。
- `no_counterexample_found`はrequired observation domain全体と全observation sourceの正常終端、およびrequired fixed packet domain全体のlocator / value / provenance integrityへ依存する。manifest observationの追加、削除、置換、一件のnon-success、またはfixed itemのlocator / value / provenanceの直接失効で失効する。未引用fixed packet context itemのcurrent snapshot applicabilityには依存しない。
- sourceまたはreceiptの直接失効は、そのsourceを使うresultとcounterexample assessment generationだけへCandidate177の`result_invalidation_scope`で伝播する。失効したgenerationとrecordを不受理にして当該review operationを`unavailable`にするが、別source、別resultまたは別operationへ広げない。

三終端は排他的にする。`concrete_counterexample_state=established`なら`counterexample_found`だけを返す。`not_established`かつ全required sourceがsuccessなら`no_counterexample_found`だけを返し、`not_established`かつ一件以上のrequired sourceがnon-successなら`unavailable`だけを返す。admissibleな`counterexample_found`はCandidate177と同じく反例優先で終端し、無関係sourceのnon-successより優先する。

## 既存制御との接続

- Candidate177を直接親とし、`DESIGN_ADMISSION`内の`manifest_observation / prior_fixed_enumeration`結果自己申告schemaを、本設計の起動前registryと最小support referenceへ置き換える。
- Candidate177のreview要否、review permission、producer binding、semantic packet、normative / decision-premise counterexample、反例優先終端、safe aggregation、individual receiptおよびresult invalidation localityを保持する。
- fixed packet itemのauthority roleとapplicabilityは既存TaskSpec、repository authorityまたはsemantic packetが既に持つものだけを保持し、新しいauthorization chain、semantic projection、matching receiptまたはapplicability evaluatorをCandidate179内で作らない。
- `CONTEXT`のallowed read、forbidden inputおよびsemantic projectionを変更しない。packet内で判定可能なfixed packet itemをallowed readへ重複追加しない。
- `ROOT`を維持し、rootはreview criterionを代行せず、reviewerが返さなかった意味resultを再構成しない。

## 具体例

finite manifestが`OBS-CONSUMER-CONTRACTS`についてtarget=`consumer_contracts`、success condition=`field is readable`だけを固定している場合、rootは`observation / review operation identity / OBS-CONSUMER-CONTRACTS`というtupleをsource identityにして起動前registryを作れる。独立したmanifest identityは不要であり、producer、snapshot、result identity、selectorおよびreceiptはまだ存在しなくてよい。

reviewerは起動後にCandidate177のallowed readとforbidden inputを守る取得方法を選び、成功時はreview operation、producer、snapshot、result、source identity、value、individual statusおよびreceiptを実行記録へ保持する。Candidate179はこれとは別の取得証明objectを要求しない。

reviewerが反例へその値を使う場合、結果にはsource identityを持つinstance bindingだけを記す。rootはbindingから実行記録のtyped valueを参照する。reviewerが同じ値を`fixed_packet_item`と呼んでもregistryのkindは変わらず、現在operationのreceiptなしではadmitされない。一方、reviewerが値、receipt、snapshot、projectionまたはmatching receiptを独自の入れ子へ再掲しなくても、それだけを理由に正しい反例を棄却しない。

## 非目標

- Candidate178のsource schema、authority chain、semantic projection schemaまたは多重receipt objectの流用
- 特定case、fixture、target名、command、selector構文または期待終端への分岐
- 一観測一tool call、全sourceの逐次取得またはexact commandの固定
- review要否、反例の意味条件、permission、producer identityまたは一般設計の変更
- rootによる意味review、reviewer resultの補完またはrepository再読込
- 評価case、fixture、oracle、rating contract、既存result、Target本体、releaseまたはprojectionの変更

## 実装前停止条件

- 既存TaskSpecまたはsemantic packetにないfieldを起動前必須にする。
- source kindをreviewerの結果または説明から決める。
- Candidate177のforbidden inputまたはsemantic projection条件を緩和する。
- sourceごとのindividual resultとreceiptを保持できない。
- rootが意味判定を再実行しないとresultを受理できない。
- reviewer resultへ同じ値、identityまたはreceiptの重複serializationを要求する。
- Candidate177の反例優先終端、safe aggregationまたは局所失効を壊す。
- 情報封鎖した敵対的reviewで具体的反例が成立する。

## 状態

- design_identity: `candidate179-review-evidence-interface-r26`
- design: `complete`
- adversarial_review: `no_counterexample_found_r26`
- implementation: `complete`
- evaluation: `adr9_r2_n5_quality_failed_mechanism_failed_stopped`
- adoption: `not_decided`
