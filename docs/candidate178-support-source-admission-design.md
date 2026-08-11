# Candidate178 support source contract 設計

## 目的

一般設計の敵対的reviewで、reviewerが根拠の出所を自己申告で変更し、本来必要な観測receiptまたはauthority bindingを迂回する経路を閉じる。

Candidate178は一predicateへの追加ではなく、次の4要素が協調する一つの一般契約とする。

1. 根拠資格を起動前のsource manifestへ固定する。
2. packet配送でも元の根拠資格を保存する。
3. 全counterexample pathへ同じsource admissionを適用する。
4. sourceまたは配送の直接失効だけを依存resultへ伝播する。

## 基準と観測事象

1. 直接親は`the-caption-3ce91a4-result-invalidation-locality-r1`（Candidate177）とする。
2. Candidate177のADR05 N=20は20 / 20 Score 4だったが、12件だけがmanifest observationの個別success receiptを用いた。7件はcurrent runtime snapshotのinventoryを`prior_fixed_enumeration`として申告し、1件は対応receiptのないmanifest observationを申告した。
3. Candidate177が固定したsafe aggregation、個別receipt、反例優先終端、result invalidation localityは保持する。
4. 問題はrepository readの有無ではない。正しいreceipt付きpacket itemは再読込せず使える。問題は、reviewerのsource kind申告だけで根拠資格を変更できることである。

## 既存信頼境界

Candidate178は新しい署名体系、authorization chainまたはauthority発行権限を作らない。sourceの信頼起点は、review operationより前に既存契約が閉じた次の二つだけとする。

- `TaskSpec authority receipt`: 利用者またはsystemから受領したTaskSpecが、当該review criterionで使える固定contract / authority itemのidentity、値またはcontent identity、適用範囲を明示している。
- `applicable repository authority receipt`: targetへ適用中のrepository instructionまたはTaskSpecが直接指名したrepository authorityについて、authority role、artifact identity、content identity、locator、値またはhash、適用範囲をbindした成功済み個別receiptがある。

`authority_binding_closed := 上記いずれかのreceiptがreview operationとgeneral design identityへ起動前に一意にbind済み`とする。

`authority_binding_kind := task_spec_item_binding | repository_artifact_binding`とする。

`task_spec_item_reference := authority binding kind=task_spec_item_binding / TaskSpec receipt identity / authority item identity / exact valueまたはcontent identity / applicability scope / provenance`とする。

`repository_artifact_reference := authority binding kind=repository_artifact_binding / repository authority receipt identity / artifact identity / content identity / selected locator / exact valueまたはcanonical hash / applicability scope / provenance`とする。

`authority_selected_reference`はauthority binding kindに対応する上記既存形一つだけとする。TaskSpec itemへrepository locatorまたは別個のcontent identityを要求せず、repository artifactへTaskSpec item identityを要求しない。一方のfieldを他方のidentityや値から導出・兼用・補完しない。

`applicability_evaluation_contract := applicability condition identity / machine-readable condition expression / deterministic evaluator identity・version / typed operator semantics / 全condition operandとrequired observed fact descriptor identity・field locator・expected valueの過不足・重複ない対応`とする。

`applicability_evaluation_receipt := evaluation receipt identity / evaluation contract identity / evaluation operationのindividual terminal success statusとsuccess receipt / 各operandに対応するobserved fact support identity・exact valueまたはhash / 各operand result / final result=true|false / provenance`とする。

`authority_applicability_state := applicable | not_applicable | unavailable`とする。

unconditional authorityは`applicable`とする。conditional authorityは、全required observed fact supportがadmissibleでevaluation operationがindividual terminal successとなり、bind済みevaluatorの再計算がreceiptのfinal resultへ一致した場合、`true`なら`applicable`、`false`なら`not_applicable`とする。required receiptの欠落、nonterminal / non-successまたは再計算不一致だけを`unavailable`とする。

`authority_semantic_projection := semantic item identity / authority selected reference identity / review criterionが参照するexact clause・valueまたは改変不能な構造化内容 / source locatorが既存referenceにある場合はそのlocator / canonicalization identity・version / content matching receipt identity / authority selected referenceのexact value・content identityまたはcanonical hashとの機械的一致receipt / authority applicability mode / conditionalの場合はrequired applicability observed fact descriptor identityの過不足・重複ない集合 / applicability mapping receipt identity / 明示applicability条件と当該descriptor集合の機械的一致receipt / conditionalの場合はapplicability evaluation contractとevaluation receipt identity / provenance`とする。

`authority_semantic_projection_ready := authority binding closed=true ∧ semantic projectionがreview operation起動前にpacket itemへ固定済み ∧ projection内容と既存authority selected referenceのexact valueが一致、または同じcanonicalizationで再計算したcontent identity/hashが一致 ∧ applicability mode / required descriptor identity集合 / 明示条件との機械的一致receiptが存在し、unconditionalなら集合が空、conditionalなら集合とevaluation contractが過不足・重複なく一致 ∧ rootは内容・mode・identity集合・評価contractの構造一致だけを照合し条項の意味を判定していない`とする。既存receiptがcontent identity/hashだけを持ち、対応するexact clause/value/structured contentと一致receiptを許可範囲で構築できない場合、または明示applicability条件をdescriptor identity集合と決定的evaluation contractへ機械的にbindできない場合はsource資格を偽装せず、review起動前に`unavailable`とする。

名称、説明、packetへの格納、current snapshotの値、reviewer/rootの解釈、一般的repository慣行、または単なるread成功からauthority roleを生成しない。`authority_binding_closed=false`のsourceは先行authorityとして使わない。必要な根拠が他に無ければreview resultは`unavailable`であり、Candidate178内でauthority chainを探索または補完しない。

## 1. Source manifest contract

`support_source_kind := observed_fact | prebound_authority`とする。

`observed_fact_descriptor := descriptor identity / source kind=observed_fact / finite evidence manifest identity / observation identity / target / success condition / producer identity / result identity requirement / runtime input snapshot identity / 許可result domain / deterministic selector / provenance requirement`とする。

selectorはmachine-readableな式と評価規則へ起動前に固定し、許可domain上で一意なfield locator一件を返す。観測によって初めて分かるlocatorと値は起動前に要求しない。0件、複数件、domain外または意味判断を必要とするselector resultは不受理にする。

`authority_applicability_mode := unconditional | conditional`とする。

`prebound_authority_descriptor := descriptor identity / source kind=prebound_authority / finite evidence manifest identity / authority binding kind / authority selected referenceの完全な写しまたは改変不能なidentity参照 / authority semantic projection identity / authority applicability mode / conditionalの場合はrequired applicability observed fact descriptor identityの過不足・重複ない集合 / provenance requirement`とする。

prebound authorityはauthority binding receiptが実際に閉じたreference形をそのままdescriptorへ保存する。repository artifactのlocator/valueはreceiptに既に存在し、TaskSpec itemはitem identity/valueまたはcontent identityで閉じる。authority semantic projectionの明示applicability条件から起動前にmodeとrequired descriptor identity集合をbindする。条件を機械的にdescriptor集合へbindできなければreview起動前に`unavailable`とし、rootが意味解釈で集合を生成しない。conditionalな各事実は別の`observed_fact_descriptor`と個別receiptへbindし、authority descriptorの自己申告でtrueにしない。

review operationが利用できる全descriptorとfinite evidence manifest membershipは起動前に固定する。reviewer、rootまたは後続resultは、観測後にsource kind、descriptor、selector、authority role、success condition、producer、snapshotまたはmanifest membershipを生成・変更・補完しない。

## 2. Support receipt contract

`observed_fact_receipt := support identity / descriptor identity / observation evidence unit identityの全要素 / producer result identity / individual terminal success status / individual success receipt / selectorが返したfield locator / exact valueまたはdescriptor固定方式によるcanonical hash / runtime input snapshot identity / provenance`とする。

`observed_fact_semantic_value := semantic value identity / observed fact descriptor identity / selectorが返したfield locator / review criterionが参照できるexact valueまたは改変不能な構造化内容 / canonicalization identity・version / observed resultのselected field exact valueまたはcanonical hashとのcontent matching receipt identity / provenance`とする。

`observed_fact_semantic_value_ready := semantic valueがreviewerへ配送済み ∧ locatorと内容がindividual resultのselected fieldへ機械的一致し、hashを使う場合は同じcanonicalizationで再計算したhashがreceiptへ一致 ∧ rootは内容一致だけを照合し意味判定していない`とする。hashのみで意味内容を配送できない場合は`unavailable`とし、再読込またはroot補完へfallbackしない。

`observed_fact_admissible := descriptorが同じreview operationのfinite evidence manifestへ起動前にbind済み ∧ observation identity / target / success condition / producer / result / snapshotがdescriptor、evidence unit、individual resultへ一対一に一致 ∧ individual terminal success receiptが存在 ∧ selectorが許可domain上でlocator一件だけを返す ∧ receiptのlocatorと値またはhashがindividual resultの同じfieldへ一致 ∧ observed_fact_semantic_value_ready=true ∧ provenanceが一致`とする。

wrapperまたはaggregate全体のstatus、partial output、隣接child、producer/rootの説明は個別success receiptを代替しない。aggregate由来ではCandidate177の`result_aggregation_safe=true`と、当該fieldを生成したindividual identity / status / receiptを必要とする。

`prebound_authority_receipt := support identity / descriptor identity / authority candidate packet identity / authority binding kind / authority selected referenceの完全な写しまたは改変不能なidentity参照 / authority semantic projectionの完全な写しまたは改変不能なidentity参照 / authority applicability mode / required applicability observed fact descriptor identity集合 / 対応する全observed fact support identity / conditionalの場合はapplicability evaluation receipt / provenance`とする。

`prebound_authority_resolution_complete := descriptorが当該review operationのfinite evidence manifestへ起動前に一意にbind済みでmanifest identityが一致 ∧ authority_candidate_packet_admissible=true ∧ authority_binding_closed=true ∧ authority_semantic_projection_ready=true ∧ descriptor、candidate packet、既存authority binding receipt、semantic projection、support receiptが同じauthority binding kindのauthority selected referenceとsemantic itemへ一対一に一致 ∧ 他binding kindのfieldを混在・導出・兼用していない ∧ applicability modeとrequired descriptor identity集合がdescriptor / candidate packet / semantic projection / receiptで一致 ∧ unconditionalならrequired集合 / support集合 / evaluation receiptが空 ∧ conditionalならrequired descriptor集合とobserved fact supportのdescriptor identity集合が一対一に一致して全supportがobserved_fact_admissible=true ∧ evaluation receiptが全operandを対応supportのexact valueへbind ∧ evaluation operationがindividual terminal success ∧ bind済みevaluatorが各operand結果とfinal resultを再計算してreceipt記録値へ一致 ∧ 欠落・重複・余分なapplicability supportなし`とする。これはapplicabilityの終端値を含まない共有完全性predicateである。

`prebound_authority_admissible := prebound_authority_resolution_complete=true ∧ (applicability mode=unconditional ∨ (conditional ∧ 再計算final result=true)) ∧ authority applicability state=applicable`とする。

`prebound_authority_not_applicable := applicability mode=conditional ∧ prebound_authority_resolution_complete=true ∧ 再計算final result=false ∧ authority applicability state=not_applicable`とする。これはevidentiary supportを成立させず、`unavailable`でもない。

finite evidence manifestのprebound authority descriptorは、`prebound_authority_admissible=true`のsupport、`prebound_authority_not_applicable=true`のclosure receipt、または`unavailable`のいずれか一つへ終端する。全manifest observationがsuccess receiptと意味判定用semantic value配送を持ち、全authority descriptorがadmissible supportまたはnot-applicable closureへ終端した場合、not-applicable authorityをsupportへ数えず`no_counterexample_found`のmanifest closureを満たせる。

current snapshotのinventory、探索結果、観測値、意味投影または要約は、packetへ含まれること、固定形式であること、`contract`または`authority`と命名されることだけでは`prebound_authority`にならない。

`support_source_admissible := source kindに対応するdescriptorとreceiptを排他的に持ち、対応するsource predicateがtrue`とする。

## 3. Packet projection contract

`authority_candidate_packet_descriptor := candidate packet identity / review operation identity / finite evidence manifest identity / packet item identity / prebound authority descriptor identity / authority binding kind / authority selected reference / authority semantic projection / applicability mode / required observed fact descriptor identity集合 / conditionalの場合はapplicability evaluation contract / candidate packet evidence unit identity / provenance requirement`とする。

`authority_candidate_packet_receipt := candidate packet identity / packet item identity / descriptorで固定済みauthority binding・selected reference・semantic projection・applicability mode・required descriptor集合・evaluation contractの改変不能な写しまたはidentity参照 / candidate packet evidence unit identity / provenance`とする。

`authority_candidate_packet_admissible := authority binding closed=true ∧ authority semantic projection ready=true ∧ candidate descriptorがreview operation起動前に同じfinite evidence manifestへbind済み ∧ descriptor / packet item / receiptがauthority内容、mode、required descriptor集合、evaluation contract、identity、provenanceを一対一に保存 ∧ 起動後のobserved result / evaluation result / final support receiptを成功済みとして含まない`とする。

candidate packetはreviewerがconditional observationを行うための固定入力であり、`support_source_admissible`または`counterexample_source_admission_ready`を単独では満たさない。reviewerは起動後、起動前に固定済みのobservation / support / evaluation identityだけを使って個別observed fact receipt、applicability evaluation receipt、prebound authority receiptを完成する。source kind、manifest membership、required descriptor集合、selector、authority内容またはevaluation contractを起動後に変更しない。

`packet_projection_common_descriptor := projection identity / review operation identity / packet identity / packet item identity / source descriptor identity / source support receipt identity / original source kind / projection evidence unit identity / provenance requirement`とする。

`observed_fact_projection_descriptor := packet projection common descriptor / original source kind=observed_fact / observed fact semantic value identity / projection locator / exact valueまたはcanonical hash / original runtime input snapshot identity`とする。

`prebound_authority_projection_descriptor := packet projection common descriptor / original source kind=prebound_authority / authority binding kind / authority selected referenceの完全な写しまたは改変不能なidentity参照 / authority semantic projectionの完全な写しまたは改変不能なidentity参照 / authority applicability mode / required applicability observed fact descriptor identity集合 / 対応support identity集合 / conditionalの場合はapplicability evaluation receipt identity`とする。

`packet_projection_descriptor`はoriginal source kindに対応する上記descriptor一つだけとする。

`observed_fact_projection_receipt := projection identity / packet identity / packet item identity / original observed fact receiptの改変不能な写しまたはidentity参照 / observed fact semantic valueとcontent matching receiptの改変不能な写しまたはidentity参照 / projection locator / exact valueまたはhash / original snapshot / projection evidence unit identity / provenance`とする。

`prebound_authority_projection_receipt := projection identity / packet identity / packet item identity / original prebound authority receiptの改変不能な写しまたはidentity参照 / authority binding kind / authority selected reference / authority semantic projection / authority applicability mode / required descriptor identity集合 / 対応support identity集合 / conditionalの場合はapplicability evaluation receipt / projection evidence unit identity / provenance`とする。unconditionalなら両集合とevaluation receiptを空として明示し、projection固有runtime snapshotを要求・生成しない。conditionalの各snapshotは対応するobserved fact receipt内だけに保持する。

`packet_projection_receipt`はoriginal source kindに対応する上記receipt一つだけとする。

`packet_projection_admissible := original sourceがsupport_source_admissible=true ∧ original source descriptorのfinite manifest membershipがprojection descriptorのreview operation identityと同じoperationへbind済み ∧ projection descriptorがreview operation起動前に固定済み ∧ observed factではdescriptor、packet item、receiptがsource descriptor / source receipt / source kind / observed fact semantic value / content matching receipt / locator / valueまたはhash / snapshot / provenanceを一対一に保存 ∧ prebound authorityではdescriptor、packet item、receiptがsource descriptor / source receipt / source kind / authority binding kind / authority selected reference / authority semantic projection / conditional applicability support identity集合 / provenanceを一対一に保存 ∧ 他source kindのfieldを混在・生成・補完しない`とする。

packet projectionは既にadmissibleなsupportの配送方法でありsource kindではない。未完成conditional authorityの起動前配送にはauthority candidate packetを使う。rootはadmissibleなsource receiptからpacket itemとprojection receiptを構築できるが、source kind、authority role、source content、review criterion、必要前提、直接否定、具体的反例またはdesign effectを生成しない。packet内projectionまたはcandidate packetで判定可能ならreviewerへ同じsourceのrepository再読込を要求しない。

reviewerが自ら発行したobserved fact resultは元receiptを直接参照でき、不要なpacket projection receiptを要求しない。

## 4. 全counterexample path共通のresult admission

`review_subject_reference := review subject identity / general design identity / boundary ledger identity / review criterionが参照するexact semantic valueまたはimmutable content identity / semantic packet identity / packet item identity / provenance`とする。

`review_subject_reference_valid := Candidate177のsemantic_projection_valid=trueのpacketへ起動前に固定済み ∧ design / ledger / semantic valueまたはcontent identity / packet item / provenanceがreview operation descriptorとreviewer resultへ一対一に一致`とする。これはreview対象の対応を示す非authority referenceであり、外部事実、規範authority、observed factまたはprebound authorityを成立させない。

`counterexample_source_admission_ready := normative / decision-premiseその他のpathを問わず、具体的外部clause、instance、入力、状態、consumerまたは失敗経路を証明する全evidentiary supportが、一意なsupport identity / 起動前source descriptor / class別source receipt / 意味判定用exact valueまたは構造化内容 / support_source_admissible=trueを持ち、reviewer resultが主張する全具体値が対応semantic valueへ機械的一致し、完成済みsupportをpacket projectionで配送した場合だけpacket_projection_admissible=trueを持つ`とする。固定一般設計、境界台帳、その明示premise、design treatmentおよびdesign effectはevidentiary sourceに含めずreview subjectとして扱う。authority candidate packetから同じreview operation内で完成したconditional supportは、authority_candidate_packet_admissible=trueとprebound_authority_resolution_complete=trueで閉じ、完成後の追加packet projectionを要求しない。

全counterexample pathは`counterexample_source_admission_ready=true ∧ review_subject_reference_valid=true`を必要とする。path名、contract basis種別または意味分類を変えてsource admissionを迂回しない。normative pathの外部contract/authority clauseと具体的instance、decision-premise pathの全fact supportはsource admissionを通り、固定design / ledgerとのpremise・treatment・effect対応はreview subject referenceを通る。

rootはmanifest membership、identity、source kind、selector result、value/hash、status、receipt、provenance、snapshot、applicability support、projection lineageおよびreview subject reference対応だけを機械照合する。必要前提、規範predicateの意味、直接否定、具体的反例またはdesign effectを再判定・補完しない。

一件でもdescriptor、receipt、identity、source class、value、snapshot、provenanceまたはprojectionが不一致なら当該supportを採用しない。必要supportを許可範囲で得られなければ`unavailable`として現designをadmitしない。admissibleな具体的反例が成立した場合はCandidate177の反例優先終端を維持する。

## 5. 失効contract

`support_dependency_identity := evidence_unit_dependency | artifact_or_receipt_dependency`とする。

`support_dependency_directly_invalidated(result, dependency) := (dependency kind=evidence_unit_dependency ∧ dependency identityがCandidate177のresult_invalidation_scope(result)に含まれる) ∨ (dependency kind=artifact_or_receipt_dependency ∧ resultが当該artifact / semantic item / packet item / receipt identity自体を直接変更または失効させる)`とする。

`source_manifest_membership_dependency := review operation identity / finite evidence manifest identity / source descriptor identity / descriptor membership relation identityを一つのartifact_or_receipt_dependencyとして固定`とする。membership relationの直接変更・失効は当該sourceだけを失効させ、同じmanifestの別descriptorへ伝播させない。

`finite_manifest_closure_dependency := review operation identity / finite evidence manifest identity / 起動前に固定した全descriptor identityの過不足・重複ない集合 / descriptor集合closure identityを一つのartifact_or_receipt_dependencyとして固定`とする。descriptorの追加・削除・置換はclosureを失効させる。

`authority_dependency_identity := authority selected referenceに既に含まれるauthority binding receipt identityをartifact_or_receipt_dependencyとして固定 ∪ 当該既存receiptがCandidate177形式のevidence unit identityを明示している場合だけそのidentityをevidence_unit_dependencyとして固定`とする。receipt identityから未記載のevidence unitを導出せず、evidence unit欠落を空dependencyへ読み替えない。

`authority_selected_content_dependency := (authority binding kind=task_spec_item_bindingならTaskSpec identity / authority item identity / bound exact valueまたはcontent identity) | (authority binding kind=repository_artifact_bindingならartifact identity / selected locator / bound content identityまたはcanonical hash)`を一つのartifact_or_receipt_dependencyとして固定する。resultがこの選択済みitem/valueまたはartifact locator/contentを直接変更・失効させる場合だけ当該dependencyを失効させ、同じartifactの無関係なlocator変更へ拡張しない。

`evidence_dependency(observed_fact_support) := {source manifest membership dependency, observed fact receiptのobservation evidence unit identityをevidence_unit_dependencyとして固定, observed fact descriptor identity / observed fact receipt identity / observed fact semantic value identity / content matching receipt identityをartifact_or_receipt_dependencyとして固定}`とする。

`evidence_dependency(prebound_authority_resolution) := {source manifest membership dependency, authority dependency identity, authority selected content dependency, prebound authority descriptor identity / prebound authority receipt identity / authority candidate packet descriptor・item・receipt identity / authority semantic item identity / content matching receipt identity / applicability mapping receipt identity / conditionalの場合はapplicability evaluation contract・receipt identityをartifact_or_receipt_dependencyとして固定, candidate packet evidence unit identityが明示済みならevidence_unit_dependencyとして固定, conditional applicabilityに使う全observed fact supportのevidence dependency}`とする。

`evidence_dependency(prebound_authority_support) := evidence_dependency(prebound_authority_resolution)`とする。

`evidence_dependency(prebound_authority_not_applicable_closure) := evidence_dependency(prebound_authority_resolution)`とする。いずれかのdependencyが直接失効した後は、同じdescriptorについて完全なfalse evaluation closureが再成立するまで`unavailable`とする。

`evidence_dependency(packet_projected_support) := original source supportのevidence dependency ∪ {projection evidence unit identityが明示済みならevidence_unit_dependencyとして固定, packet projection descriptor identity / packet item identity / projection receipt identityをartifact_or_receipt_dependencyとして固定}`とする。

`review_terminal_dependency := review operation terminal result identity / individual terminal status and success receipt identity / sender binding identityをartifact_or_receipt_dependencyとして固定 ∪ terminal resultがCandidate177形式のevidence unit identityを明示する場合だけevidence_unit_dependencyとして固定`とする。

`evidence_dependency(review_subject_reference) := {review subject reference identity, general design identity, boundary ledger identity, exact semantic valueまたはimmutable content identity, semantic packet identity, subject packet item identity, provenance receipt identityを各々artifact_or_receipt_dependencyとして固定 ∪ review subjectがCandidate177形式のevidence unit identityを明示する場合だけevidence_unit_dependencyとして固定}`とする。

`evidence_dependency(counterexample_result) := 全evidentiary supportのevidence dependency ∪ review terminal dependency ∪ evidence_dependency(review_subject_reference)`とする。

`evidence_dependency(no_counterexample_result) := finite manifest closure dependency ∪ 全manifest observation support / applicable authority supportのevidence dependency ∪ 全not-applicable authorityのprebound_authority_not_applicable_closure dependency ∪ review subject reference dependency ∪ review terminal dependency`とする。

finite manifest closure dependencyは全descriptorの閉包を必要とする`no_counterexample_found`だけへ適用する。admissibleな具体的反例は無関係descriptorの追加・欠落で失効させず、Candidate177の反例優先終端を維持する。

support dependencyの一件以上について`support_dependency_directly_invalidated(result, dependency)=true`の場合だけ、そのsupportと依存predicateを失効させる。projection dependencyの失効を元sourceまたは別projectionへ伝播させず、元source dependencyの失効はそのsourceから作られたprojectionへ伝播させる。無関係なfailure、別source、別snapshotまたは別supportへ伝播させない。

## 境界台帳

| 境界 | 閉包根拠 | 設計上の扱い |
|---|---|---|
| source kind | 起動前source descriptor | reviewer申告では変更しない |
| authority role | TaskSpecまたは適用中repository authorityの既存receipt | Candidate178内で生成・探索しない |
| observed fact | 個別producer resultとsuccess receipt | aggregate外形や説明で代替しない |
| conditional applicability | 別のobserved fact support | authority receiptの自己申告でtrueにしない |
| packet delivery | original source receiptとprojection receipt | source kindを保存し、再読込を不要にする |
| counterexample path | 共通source admission | normative等への分類変更で迂回しない |
| root/reviewer責任 | 資格照合と意味判定の分離 | rootは反例意味を再判定しない |
| invalidation | source / projection evidence dependency | 直接依存範囲だけを失効する |

## 敵対的review対象

1. current inventoryをprebound authorityと申告して観測receiptを迂回できない。
2. receiptのないmanifest observationを成功supportにできない。
3. 正しいobserved factをpacketで配送し、再読込なしで採用できる。
4. authority binding receiptにないclause、instanceまたはvalueを自己申告できない。
5. conditional authorityをcurrent snapshotへ適用する事実をauthority receipt自身で補完できない。
6. aggregate success/failureまたはpartial outputで個別receiptを代替できない。
7. selectorが0件または複数件を返すときroot/reviewerが意味で一件を選べない。
8. normative、decision-premiseその他へpathを変えてsource admissionを迂回できない。
9. packet itemまたはprojection receiptだけが失効した場合、そのprojection利用supportだけが失効する。
10. 元source receiptが失効した場合、そのsourceを使う直接・packet supportが失効する。
11. authority bindingが既存信頼境界で閉じていない場合、authorization chainを新設せず`unavailable`になる。
12. TaskSpec item bindingへrepository locator/content fieldを要求せず、repository artifact bindingとの間でfieldを推論・兼用しない。
13. 無条件prebound authorityのpacket projectionへ存在しないruntime snapshotを要求せず、conditional snapshotは対応observed fact receiptだけから保存する。
14. 既存authority receiptにないevidence unit identityを要求・導出せず、binding receipt identity自体を失効dependencyとして保持する。
15. authority bindingがcontent identity/hashだけで閉じていても意味内容なしにreviewを起動せず、既存referenceと一致するsemantic projectionがなければ`unavailable`とする。
16. conditional applicabilityの必要観測集合をrootが意味推論せず、起動前descriptor identity集合とsupport集合を一対一に照合する。
17. semantic projection自体がapplicability mode、required descriptor集合、明示条件との機械的一致receiptを保持する。
18. semantic projection、content一致receiptまたはapplicability mapping receiptの直接失効を当該authority supportと派生packetへ局所的に伝播する。
19. conditional applicabilityは必要観測の存在だけで成立させず、各exact valueをbind済みevaluatorで再計算してfinal result=trueを要求する。
20. evidence unitとartifact/receipt identityを型付きdependencyとして区別し、どちらの直接失効も同じsupportだけへ伝播する。
21. binding receiptが不変でも選択済みTaskSpec item/valueまたはrepository artifact locator/contentが直接変われば当該authority supportを失効する。
22. prebound authorityも当該review operationの起動前finite manifest membershipを必須にし、packetが別manifest由来sourceを配送できない。
23. conditional authorityは起動前candidate packetと起動後completion receiptを分け、未観測resultを補完せず固定済みidentityだけから最終supportを完成する。
24. source / candidate / projectionのdescriptorとclass別receipt自体の直接失効を、当該supportと派生supportへ局所的に伝播する。
25. 固定一般設計と境界台帳をauthorityへ分類せずreview subject referenceで照合し、そのitem失効を当該counterexample resultだけへ伝播する。
26. conditional evaluationの正常なfalseを`not_applicable`として閉じ、supportには使わずno-counterexample manifest closureへ含める。
27. not-applicable closureもapplicable supportと同じauthority resolution dependencyを保持し、一部失効後に古いfalse closureを再利用しない。
28. applicability終端値を含まないresolution-complete predicateから、applicableとnot-applicableを排他的に派生する。
29. sourceのfinite manifest membership relation自体をdependencyにし、その直接失効を当該sourceへ局所伝播する。
30. authority candidate packetから起動後完成したsupportへ、存在しない完成済みsupport projectionを追加要求しない。
31. reviewer terminal result / success receipt / sender bindingの直接失効を当該review resultだけへ伝播する。
32. counterexample / no-counterexampleの双方が同じreview subject reference dependencyを使う。
33. packet参照だけでなく元general design / ledger / semantic content / provenanceの直接失効もreview resultへ局所伝播する。
34. Candidate177の旧source schemaを新schemaへ明示置換し、無条件authorityへ存在しないsnapshot applicabilityを二重要求しない。
35. no-counterexample resultだけがfinite manifest全descriptor集合closureへ依存し、descriptor追加・削除・置換で旧closureを失効する。
36. observed factも意味判定用exact contentとmatching receiptを必須にし、hash-onlyで内容を配送できなければ`unavailable`とする。

## 既存制御との接続

- `DESIGN_ADMISSION`の全counterexample pathに共通するsource-bearing support受入schemaを本契約で置き換える。Candidate177の`manifest_observation`はCandidate178の`observed_fact` descriptor / receipt / admissionへ、`prior_fixed_enumeration`は`prebound_authority` descriptor / receipt / admissionへ機械的に対応させる。旧schemaとの二重要求はしない。
- 無条件`prebound_authority`へ旧`snapshot applicability` fieldを要求または生成しない。conditional authorityのcurrent applicabilityはrequired observed fact supportとevaluation receiptだけで閉じる。この対応をdecision-premiseだけでなくnormativeその他の全terminal pathへ共通適用する。
- 上記source schema置換以外では、normative / decision-premiseの必要前提、直接矛盾、具体的反例、design effectという意味predicateを変更しない。
- Candidate177の有限evidence manifest、semantic projection、producer binding、反例優先終端、safe aggregation、result invalidation localityを保持する。
- `semantic_projection_valid`の「packet内projectionで判定可能なsourceをallowed readへ重複追加しない」を維持する。
- `OWNER_ROLE`と`ROOT`を維持し、rootの機械照合をreview criterionの再実行へ拡張しない。
- `general_design_admissible`と`counterexample_found / no_counterexample_found / unavailable`の意味を変更しない。

## 非目標

- 一predicateだけへの集約
- 新しい署名、認証またはauthorization chain
- 一観測一tool call、全source再読込または逐次実行の強制
- 反例の意味条件、review要否、permissionまたはproducer identityの変更
- 特定case、fixture、manifest target、commandまたは期待終端への分岐
- 評価case、rating contract、既存result、Target本体、releaseまたはprojectionの変更

## 実装前停止条件

- source資格とpacket配送を分離できない。
- reviewer申告だけでsource kindまたはauthority roleを変更できる。
- rootの意味再判定または正規packetの再読込を必要とする。
- Candidate177のsafe aggregationまたは局所失効を壊す。
- 既存信頼境界が閉じていないのにCandidate178内で新しいauthority chainを必要とする。
- 敵対的reviewで具体的反例が成立する。

## 状態

- design_identity: `candidate178-support-source-contract-restart-r26`
- design: `complete`
- adversarial_review: `no_counterexample_found`
- implementation: `complete`
- evaluation: `ADR9 r2 N=5 quality_failed / mechanism_failed / stopped`
- adoption: `not_decided`
