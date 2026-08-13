# review制御再構成マイルストーン計画

> **位置づけ**: 現行frontier／Candidate203 ADR9 r2 N=5品質通過・機構不通過・停止・C147直接基盤維持

## ゴール

Candidate147までに得た有効な不変条件を保持しながら、operation、predicate、evidence、producer、result、dependency、invalidation、terminalおよびartifact変更許可の定義を一貫した制御構造へ再構成する。

ゴールはCandidate176、Candidate187または他の既存Candidateの再現ではない。ADR9 r2の各ケースについて、model-visibleな契約と入力から期待terminalを導出し、正しいproducer、観測、resultおよび局所効果の経路で成立させる。加えて、Standard14で既存の実行制御を退行させない。

Candidate147の本文、条項数、配置または語列は保持条件にしない。必要であれば既存条項を分割、統合、置換または削除する。条項数、プロンプト量、判断点および実行コストは、制御成立後に測定する結果であり、設計前の制限にしない。

## 完了条件

1. ADR9 r2の全対象runがvalidかつScore `4`となる。
2. 各terminalが、期待するproducer、evidence、resultおよびdependency経路で成立する。
3. 未観測receiptの昇格、root代行、禁止情報配送、無関係なresultによる失効および危険なartifact変更が0件となる。
4. 過去の低頻度失敗に対応する高リスクケースの拡張試験を通過する。
5. Standard14互換試験で品質と既存機序を退行させない。
6. 保存済み基準resultとprompt identity以外の互換条件が一致し、比較前receiptが`ready`となる。
7. 評価、採用、releaseおよびprojectionを別ゲートとして保持する。

## 共通原則

- C147、C176または他Candidateを正解として固定しない。既存Candidateは成功経路、失敗経路および設計仮定を識別する診断証拠として使う。
- C147で成立した挙動を保持対象とするが、C147の定義または文章を逐語維持しない。
- C176で成立したreview admission、情報封鎖、具体的反例およびterminal判断を参考にするが、C176で残った観測result境界の失敗も修正対象とする。
- review要否、evidence充足、review result、terminalおよびartifact変更許可を同じ状態へ縮約しない。
- 全入力の列挙または分類を、terminalごとのdependency証明の代用にしない。
- 設計レビューは方向を成立不能にする具体的反例の確認に限定する。完全性は互換試験で検証する。
- validな低品質runを再実行で置き換えない。
- 拡張試験は結論を変え得るケースだけを選び、適格な既存atomic runを再利用する。

## M1: 過去結果の因果分析

### 目的

過去Candidateが狙った制御、設計時に置いた仮定、実際の結果、成立した部分および誤っていた部分を、Candidate固有の表現ではなく制御境界へ変換する。

### 成果物

- ADR01〜ADR09のterminal別証明責務
- 過去Candidateの設計意図と実結果の対応
- 繰り返し発生した失敗原因
- C147の保持・改訂・分割・削除候補

### 完了条件

- ADR01〜ADR09の全失敗を、有限閉包、具体的反例、反例なし、判断依存入力不足またはpermission否定へ分類できる。
- 原因不明またはCandidate名だけで表した失敗を残さない。
- 設計へ渡す未解決predicateと必要観測を列挙できる。

### 現在状態

`complete_after_candidate195 / candidate195_mechanism_failures_9_classified / predispatch_adjudication_not_terminal_operation_8 / judgement_dependency_not_ticketed_1 / unknown_cause_0 / c147_direct_parent_retained / M2_reopen_ready`

成果物は[`review制御再構成の因果分析`](review-control-reconstruction-causal-analysis.md)とする。ADR01〜ADR09を5種類のterminal別証明責務へ全件分類し、過去Candidateの狙い・実結果・反復原因、C147の13条項の保持・改訂・分割・統合後削除候補、およびM2へ渡す未解決predicateと必要観測を固定した。

Candidate192の失敗を追加分析し、consumer・dependencyの判定自体ではなく、ready集合の論理判定と同一model responseからの実発行を別責務として解釈できたことを原因へbindした。C192からはconsumer、dependency、個別result contract、真正dependency非越境および50 / 50の品質維持を保持し、独立した抽象`DISPATCH_ADMISSION`とその挙動拘束仮定は継承しなかった。その時点ではCandidate191を直接基盤としてC147の`DECISION_BOUNDARY`をresult effectと発行遷移へ分割したが、この発行遷移部分は後続Candidate193の反例により撤回対象となった。

Candidate193の結果からは、ADR9全9ケースの開始identityと後続readが真正dependencyを持つ訂正済み判定、consumer／dependencyの判定軸、個別result contract、compound command禁止、43件で維持したreview・artifact・command境界、およびADR05・ADR06の保存反例を残す。同じ新基準ではCandidate191の越境36 / 45に対しCandidate193は28 / 45であり、正しい分離を9件から17件へ増やしたため、`DISPATCH_TRANSITION`全体を無作用として捨てない。ただし一意拘束には失敗しているため、各primitive、独立条項化および次Candidateの親は保留する。捨てるのは、自己terminal宣言だけで現在responseのtool-call選択を一意に強制できるという十分性仮定である。M1ではC147の`DECISION_BOUNDARY`の優先関係と2件のcertificate dependencyを再分析し、M2、次Candidateおよび追加評価は開始しない。

後続再分析では、Standard14とADR9のmodel-visible `trial-prompt-input.json`を全23ケース直接照合した。Standard14はconsumerなし1ケース、開始identityとreadを共同発行できる9ケース、開始identityを先に確定する4ケースへ分類し、ADR9は全9ケースで無限定停止によりidentity単独先行と確定した。C147を次案の直接基盤とし、C191〜C193は成立経路、consumer／dependencyの判断軸、部分効果、保存反例だけを設計証拠として使う。これによりM1の未解決predicateと開始経路はM2へ渡せる状態となった。現在の正本は[`Candidate194作成前設計`](candidate194-c147-direct-review-control-reconstruction-preimplementation-design.md)とする。

Candidate194のM5第1段階後にM1を再開し、15件の機構失敗を保存traceへ戻して再分類した。開始dependency越境7件、開始identity観測methodの早期terminal化6件、有限閉包誤分類1件、観測result identity誤対応1件で全件を説明でき、原因不明は0件となった。品質失敗5件は後二群ではなく、method群の4件と観測identity群の1件である。現在の再開M1正本は[`Candidate194 M5第1段階の原因分析`](candidate194-m5-causal-analysis.md)とし、次に許可されるのはC147を直接基盤とするM2再設計だけである。

Candidate195のM5後にもM1を再開し、9件を[原因分析](candidate195-m5-causal-analysis.md)へ戻した。開始identityに関する8件は、ready・method・発行集合の判定が独立terminal operationではなく、判定result受領前にtool callを発行できたことが原因である。ADR04の1件は、三result kindのcertificate dependencyをticketへ分けず、具体的反例に不要なmissing atomを`unavailable`へ伝播できたことが原因である。原因不明は0件となった。Candidate195を親にせず、C147を直接基盤とするM2だけを次に許可する。

## M2: 制御構造の再設計

### 目的

C147の13条項を保持・改訂・分割・削除へ分類し、operation、predicate、evidence、producer、result、dependency、invalidation、terminalおよびartifact変更許可を一貫した責務構造へ再配置する。

### 完了条件

- 一つの状態遷移を複数条項が競合して所有しない。
- 各terminalの必要条件をCandidate名、case IDまたは期待terminalの参照なしに導出できる。
- evidence発行条件、観測resultの真正性、dependency、result失効およびterminal形成が区別されている。
- 実行方法の自由が独立観測resultの統合許可を意味しない。
- 条項数、追加量または総量を理由に必要な制御を削らない。

### 現在状態

`complete_after_candidate194 / c147_direct_reconstruction / four_execution_tickets_fixed / 27_responsibilities_fixed / M3_reopen_ready`

成果物は[`review制御再構成の責務設計`](review-control-reconstruction-responsibility-design.md)とする。operation specificationからouter terminalまでの既存10責務を保持し、共通execution coreへ`DISPATCH_TRANSITION`を加えた11責務とした。review適用可否・要否・実行permission、packet形成と観測state、review judgementと保存result admission、dependencyとinvalidation、発行遷移およびartifact変更許可を別々のownerへ固定した。

既存10責務とCandidate191の成立経路は保持した。再開範囲は発行遷移だけであり、`dispatch_frontier`の固定、同一model responseからの個別tool call全件発行、全result受領まで判断を戻さないclosureを`dispatch_transition_terminal`という分離不能な一つの挙動遷移へ配置した。C192への条項追加、review責務の再設計、新しいresult kindまたは評価系列の追加は行っていない。

このM2設計は「最大集合」を廃し、consumerを持つ発行候補から未解決predecessorを除いた`dispatch_frontier`を、現在model responseの全tool-call identityへ一対一bindした。しかしCandidate193評価で真正dependency越境を28 / 45件観測し、一意拘束には不足すると判明した。同じ基準のCandidate191より越境は8件少ないため部分効果は保留し、成立済み設計としても全棄却としても次へ渡さない。

上記11責務設計はCandidate193までの履歴として保持する。現在のM2はC147を直接基盤とし、C147原文を保持・分割・移動・置換へ分類したうえで、共通execution core、独立review、validation、operation terminal、outer terminalを24責任へ再構成した。`dispatch_frontier`系の抽象機構は継承せず、実発行は`RESULT_DEPENDENCY`と`DECISION_BOUNDARY`へ戻す。review applicability、prior result、execution permission、packet、observation、judgement、current result、change admissionは別責任として維持する。設計本文、23ケース経路、二段階評価、停止条件は[`Candidate194作成前設計`](candidate194-c147-direct-review-control-reconstruction-preimplementation-design.md)を正本とする。

Candidate194停止後のM2では、24責任を固定数として維持せず、4原因を[`M2再設計`](post-candidate194-review-control-m2-redesign.md)へ戻した。開始dependencyは`operation ticket / predecessor edge / issuance`、method早期terminal化は`method receipt`、finite closure誤分類は正の`finite closure certificate`、観測identity誤対応はtool result受領時の`observation ledger`へbindした。責任数は結果として27となる。C192・C193型の抽象frontierは作らず、各tool invocationをreadyなticketへ一対一bindする。現在のM2は完了し、次に許可されるのは一般的な具体的反例だけを使うM3再reviewである。

## M3: 設計方向の敵対的レビュー

### 目的

設計を成立不能にする一般的な具体的反例を確認する。表現改善、網羅性の追加または試験で判定可能な不確実性だけを理由に設計を循環させない。

### 完了条件

- 未解決のblocking counterexampleがない。
- 設計のtarget、permission、methodまたはstop conditionを変える指摘が残っていない。
- 残余リスクが試験predicateと対象ケースへ対応している。
- reviewの反復で当初の設計軸を増やしていない。

### 現在状態

`passed_after_candidate194_M2_revision / initial_blocking_counterexamples_4 / reviewed_states_22 / unresolved_blocking_counterexamples_0 / M4_completed_as_candidate195`

成果物は[`review制御再構成の方向レビュー`](review-control-reconstruction-direction-review.md)とする。M2初稿へ具体的反例5件が成立したためM2へ戻り、review契約非適用、aggregate result contract、terminal後の新operation identity、finite relationのmachine-bound照合、保存result admissionと新規review permissionの分離を同じ10責務内で修正した。修正版8条件の再確認では未解決blocking counterexampleが0件となり、残余リスクをADR9とStandard14のmechanism predicateへ対応させた。

この完了はCandidate191までの責務設計に対する履歴である。M2で発行遷移を再設計した後は、consumerなし空集合、真正dependency、個別result contract、およびready集合の一部発行というC192由来の4反例だけを確認する。完全性確認や別系列の追加は行わない。

再開M3では、consumerなし空frontier、readを変える／変えないidentity result、同時発行上限、個別resultの一部失敗、cell ID付きnonterminal result、frontierの部分発行およびcompound command代用を確認した。いずれも同じ`DISPATCH_TRANSITION`内で一意に停止または発行でき、未解決blocking counterexampleは0件だった。成果物は[`方向レビュー`](review-control-reconstruction-direction-review.md)のCandidate192後追記を正本とする。

これらのM3完了はCandidate191からC193までの履歴であり、C147直接基盤の24責任設計を通過させたものではない。次に許可する作業は、24責任についてtarget、permission、method、stop conditionを変える具体的反例だけを確認するM3再reviewである。Candidate194実装、profile作成、slot発行はその完了前に開始しない。

C147直接基盤のM3再reviewでは、model-visibleな23ケース経路と既存M3反例を使い、clarification、限定・無限定停止、primary review、review非適用、finite relation、prior result、packet missing、aggregate failure、局所失効、coupled subject、部分発行、cell ID、compound commandを含む15状態を確認した。確認中の修正は既存24責任内へ反映し、未解決blocking counterexampleは0件となった。責任、schema、registry、producer role、result kind、評価系列は増やしていない。現在のM3正本は[`Candidate194作成前設計`](candidate194-c147-direct-review-control-reconstruction-preimplementation-design.md)の「M3方向review」とする。次に許可されるのはCandidate194 prompt artifactの作成だけであり、profile作成またはslot発行ではない。

このM3完了もCandidate194作成前の履歴である。Candidate194の実評価で4原因が成立し、後続M2が27責任へ変わったため、M3は再び未開始へ戻した。次に確認するのは、operation edge未充足時の同一response越境、method resultの`does_not_bind_requested_result`、finite closure certificateの正負、wrapper result contractによるobservation ledger、certificate別dependency、限定停止と無限定停止、primary review非適用、prior result、permission denial、cell IDおよびvalidation terminalである。M3通過前に次Candidateを作らない。

後続の[`M3方向review`](post-candidate194-review-control-m3-direction-review.md)では、M2初稿にrejected predecessorのterminal deadlock、競合changeの同時発行、result contractを満たせないmethod候補、wrapper内部identityの再転記という4件のblocking counterexampleを確認した。M2へ戻して`suppressed_by_predecessor`、`conflict_keys`、method output schemaによるeligibility、`observation_batch_identity / ledger_receipt_identity`を追加した。修正版22状態では未解決blocking counterexampleが0件となったためM3を通過する。次に許可されるのはC147を直接親とする新Candidate artifactのM4実装だけであり、Candidate identity、profileおよび評価slotはまだ作成していない。

## M4: Candidate実装

### 目的

固定した設計をprompt bundleへ実装する。C147への追記だけに限定せず、必要な分割、統合、置換および削除を行う。

### 完了条件

- 設計predicateと実装箇所が一対一または明示された合成関係で対応する。
- 各責務の正本が一つで、旧定義との競合がない。
- bundle identity、manifest、構造試験および実装一致監査が成功する。
- Candidate、評価、採用、releaseおよびprojectionの状態が分離されている。

### 現在状態

`candidate192_stopped_historical / candidate193_evaluated_stopped / candidate194_evaluated_stopped / candidate195_evaluated / candidate195_quality_failed / candidate195_mechanism_failed / candidate195_stopped`

Candidate188は静的再監査で停止した。Candidate189はcurrent resultへ保存result用`result_use_permission`を誤適用した一件で停止し、Candidate190でcurrent/prior admissionを分離した。Candidate190はM5とM6を通過したが、M7 Standard14の8 runでcriterion ownerを独立review operationへ昇格し、不要producerを起動したため停止した。この反例により、C147の`OWNER_ROLE`を統合後削除した分類を撤回し、独立責務として復元する。

修正版の成果物は[`Candidate191 explicit review operation applicability実装監査`](candidate191-explicit-review-operation-applicability-implementation-audit.md)と、prompt bundle `the-caption-3ce91a4-explicit-review-operation-applicability-r1`とする。Candidate190を直接親とする単一修正で、reviewを必要な独立operationとして直接名指しした場合だけreview controlを適用し、owner、`non_machine_risk`、静的確認または独立確認の語列だけではoperation、producer、spawnおよびreview resultを作らない。限定Standard14では修正対象3ケースを通過した。ADR9 r2も30 / 30 Score 4となり、初回機序監査が報告した83件は後続再監査でcollector誤検出と確定したため、Candidate191のM5は訂正後に通過した。

後続のコスト機序再判定で、Candidate191はStandard14の9ケース、45 run中44件で変更前stepを一つ増やし、A01ではconsumerのない開始identity観測も発行したと確認した。Candidate192はCandidate191を直接親とし、`DISPATCH_ADMISSION`だけを追加する。evidence資格、result効果、review責務を変えず、requested resultのconsumerと相互dependencyから発行集合を決める。成果物は[`Candidate192 consumer-bound co-issuance実装監査`](candidate192-consumer-bound-coissuance-implementation-audit.md)と、prompt bundle `the-caption-3ce91a4-consumer-bound-coissuance-r1`とする。

Candidate192の対象Standard14評価は50 / 50 validかつScore 4だったが、A01 consumerなし開始identityが2 / 5、退行8ケースのidentity/read共同発行が1 / 40に留まった。定義した発行資格が実際のmodel stepを拘束しなかったためCandidate192を停止し、M1へ戻る。次Candidateの実装は、新原因に対する設計と方向を変える具体的反例の確認が終わるまで開始しない。

限定M2・M3完了後、Candidate193 `the-caption-3ce91a4-frontier-bound-dispatch-transition-r1`をCandidate191の直接childとして作成した。C192本文は継承せず、`DISPATCH_TRANSITION`だけを追加し、`RESULT_EFFECT`から発行所有を移した。成果物は[`Candidate193 frontier-bound dispatch transition実装監査`](candidate193-frontier-bound-dispatch-transition-implementation-audit.md)とする。後続M5で品質・発行遷移機序の不一致を観測したためCandidate193は停止済みである。

M3完了時点ではCandidate194は未作成だった。作成時はC147を直接親とし、C191、C192、C193のprompt本文や抽象機構を継承しない条件を固定した。M3再reviewが完了し、[`Candidate194作成前設計`](candidate194-c147-direct-review-control-reconstruction-preimplementation-design.md)の開始条件を満たした後にだけ、別artifact単位として実装することを許可した。

上記条件の充足後、Candidate194 `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1`をC147の直接child full bundleとして作成した。変更targetはroot `AGENTS.md`だけで、設計の24責任を同名・同順の24 labelへ実装した。bundle verification、C147との非変更file identity照合、責任label照合および書式確認に通過した。M4完了時点の状態は`candidate_created / static_verification_passed / not_evaluated`だった。その後のM5第1段階で不通過となり、現在は`evaluated / quality_failed / mechanism_failed / stopped`である。成果物は[`Candidate194実装監査`](candidate194-c147-direct-review-control-reconstruction-implementation-audit.md)と[`Candidate194結果`](../evaluations/results/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5_2026-08-12.md)を正本とする。

Candidate194停止後のM1、M2、M3を完了し、Candidate195 `the-caption-3ce91a4-operation-ticketed-review-control-r1`をC147の直接child full bundleとして作成した。変更targetはroot `AGENTS.md`だけである。operation ticket、predecessor edge、method result、finite closure certificate、observation ledgerを含む27責任を実装し、M3で追加した`suppressed_by_predecessor`、`conflict_keys`、method output schema eligibility、`observation_batch_identity / ledger_receipt_identity`も反映した。bundle verification、C147との非変更file identity照合、27 label照合および書式確認に通過した。M4完了時点は`candidate_created / static_verification_passed / not_evaluated`だった。その後のM5で不通過となり、現在は`evaluated / quality_failed / mechanism_failed / stopped`である。成果物は[`Candidate195実装監査`](candidate195-operation-ticketed-review-control-implementation-audit.md)と[`Candidate195結果`](../evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5_2026-08-12.md)を正本とする。

Candidate195停止後のM1、M2、M3も完了し、Candidate196 `the-caption-3ce91a4-materialized-adjudication-control-r1`をC147の直接child full bundleとして作成した。変更targetはroot `AGENTS.md`だけである。repository tool発行前のready・method・edge・conflict判定をmachine-returned terminal receiptへ固定し、review result kindを固有dependencyと優先順を持つ三つのadjudication operationへ分けた30責任を実装した。bundle verification、C147との非変更file identity照合、30 label照合および書式確認に通過した。M4完了時点の状態は`candidate_created / static_verification_passed / not_evaluated`だった。その後のM5で不通過となり、現在は`evaluated / quality_failed / mechanism_failed / stopped`である。成果物は[`M2設計`](post-candidate195-review-control-m2-materialized-adjudication-design.md)、[`M3方向review`](post-candidate195-review-control-m3-direction-review.md)、[`Candidate196実装監査`](candidate196-materialized-adjudication-control-implementation-audit.md)および[`Candidate196結果`](../evaluations/results/candidate196-materialized-adjudication-control-adr9-r2-n5_2026-08-12.md)を正本とする。

その後、[`Candidate196評価設計`](candidate196-materialized-adjudication-control-adr9-r2-n5-evaluation-design.md)と[`実行準備監査`](candidate196-materialized-adjudication-control-adr9-r2-n5-execution-preparation-audit.md)で、実ADR9 r2全9ケースN=5、private oracle境界、materialized receiptと三result-kind判定の機構predicate、Candidate195登録resultへの互換参照、不足45件およびM=24を固定した。45件を発行した結果は45 / 45 valid、Score `4 / 1 = 36 / 9`だった。最初の実repository操作が三値identityだけだったのは33 / 45、receipt被覆は140 / 150 tool、method family一致は136 / 150 tool、result-kind経路一致は26 / 45 runだった。[Candidate196結果](../evaluations/results/candidate196-materialized-adjudication-control-adr9-r2-n5_2026-08-12.md)を`quality_failed / mechanism_failed / stopped`として保持し、M6とStandard14を開始しない。Candidate196を親にせずC147直接基盤を維持する。

Candidate196停止後は、責任、ticketおよびreceiptを増やす共通再構成方向を停止した。[`C147局所review応用設計`](post-candidate196-c147-local-review-application-design.md)ではC147の13条項を変更せず、独立review契約が適用される変更predicateだけへ`REVIEW_OBLIGATION`、`REVIEW_RESULT_ADMISSION`、`REVIEW_RESULT_EFFECT`の三接続を追加する。Standard14 14ケースとADR9 9ケースの計23ケースは四obligation状態と三review resultへ未分類0件で分類した。[`方向review`](post-candidate196-c147-local-review-direction-review.md)は一般16状態でblocking counterexample 0件を確認した。

方向review通過後、Candidate197 `the-caption-3ce91a4-local-review-application-r1`をC147の直接child full bundleとして作成した。C147の13条項は逐語保持し、root `AGENTS.md`末尾へ三接続だけを追加した。その他18 targetのmanifest entryはC147と同一であり、ticket、receipt、ledger、adjudication commandまたは新dispatch機構を持ち込んでいない。[`Candidate197実装監査`](candidate197-local-review-application-implementation-audit.md)を`candidate_created / static_verification_passed / not_evaluated`の正本とする。

続く[`Candidate197 ADR9 r2全9ケースN=5評価設計`](candidate197-local-review-application-adr9-r2-n5-evaluation-design.md)では、実model-visible trial input 9件とprivate oracle 9件を直接照合し、三局所接続、root/reviewer境界、certificate局所性、result effectおよびC147開始identity・validation保持をqualityとmechanismへ分離して固定した。[`実行準備監査`](candidate197-local-review-application-adr9-r2-n5-execution-preparation-audit.md)でCandidate196登録resultと保存Layer 1を互換参照へbindし、Candidate197の不足45件を発行した。結果は45 / 45 valid、Score `4 / 1 = 32 / 13`だった。reviewer cardinalityは29 / 45、review result admissionは21 / 45、result effectは33 / 45、最初の実repository操作が三値identityだけだったのは4 / 45である。[Candidate197結果](../evaluations/results/candidate197-local-review-application-adr9-r2-n5_2026-08-12.md)を`quality_failed / mechanism_failed / stopped`として保持し、Standard14を開始しない。Candidate197を親にせずC147直接基盤を維持する。

Candidate197停止後の[`C147最小operation選択設計`](post-candidate197-c147-minimal-operation-selection-design.md)では、全タスクの具体操作や真の最短経路を事前固定せず、各判断時点で現在成立し得るoperation候補を並べ、成果または次分岐をbindするための最小集合だけを選ぶ方向へ切り替えた。ターン数は固定せず、先行resultが未発行operationの必要性、target、permission、methodまたはstop conditionを変える場合だけ再選択する。reviewは明示required scope、consumer、current resultおよびpermissionから通常operationと同じ選択へ入れる。ADR9 9ケースとStandard14 14ケースは未分類0件で、方向reviewは一般18状態のblocking counterexample 0件を確認した。

方向review通過後、Candidate198 `the-caption-3ce91a4-minimal-operation-selection-r1`をC147の直接child full bundleとして作成した。C147の`SPEC`と`DECISION_BOUNDARY`だけを置換し、`REVIEW_SELECTION`一件を追加した。他の11条項とその他18 targetはC147と同一で、Candidate191からCandidate197までのprompt本文、ticket、receipt、ledger、adjudication command、dispatch機構およびTPOを継承していない。[`Candidate198実装監査`](candidate198-minimal-operation-selection-implementation-audit.md)を`candidate_created / static_verification_passed / not_evaluated`の正本とする。

続くCandidate198 ADR9 r2全9ケースN=5は45 / 45 valid、訂正後Score `4 / 1 = 26 / 19`だった。reviewer cardinalityは32 / 45、current result admissionは27 / 45、result effectは26 / 45、開始identity単独は35 / 45である。初回監査のterminalとresult kind parser誤分類はappend-only rating recoveryで訂正したが、不通過判断は変わらない。[Candidate198結果](../evaluations/results/candidate198-minimal-operation-selection-adr9-r2-n5_2026-08-13.md)を`quality_failed / mechanism_failed / stopped`として保持し、Standard14を開始しない。Candidate198を親にせずC147直接基盤を維持する。


M4とは別のアーティファクト単位で、[`Candidate195 ADR9 r2全9ケースN=5評価設計`](candidate195-operation-ticketed-review-control-adr9-r2-n5-evaluation-design.md)を作成した。9件のmodel-visible `trial-prompt-input.json`とprivate oracleを直接照合し、既存quality oracleを変更せず、Candidate194の4原因に対応する機構predicateを固定した。開始identity mismatch時の`suppressed_by_predecessor`と競合changeの`conflict_keys`は、この固定fixtureでは未観測になることも明示した。

続く[`Candidate195実行準備監査`](candidate195-operation-ticketed-review-control-adr9-r2-n5-execution-preparation-audit.md)では、Candidate194登録result `04c8b680e4884eafa39929e06a935035`と保存Layer 1を互換参照へbindした。Candidate195の空pool、不足45件、45 capsule、M=24およびglobal planを固定し、comparison preflightは`ready`となった。当時の状態は`authorized_45 / issued_0 / not_evaluated`である。後続の明示的実行判断で固定45件を発行し、M5結果へ遷移した。

## M5: ADR9 r2互換N=5

### 目的

保存済みADR9 r2基準resultとprompt identity以外の条件を一致させ、再構成した制御の品質と機序を確認する。中核定義を広く変更する場合は9ケースすべて、変更効果が限定できる場合はその効果境界と必要な対照ケースだけを選ぶ。

### 実行前条件

- 基準resultを一意にbindする。
- case、fixture、TaskSpec、oracle、rating、model、reasoning、runtime、permission、executorおよびLayer 1を機械照合する。
- comparison preflightが`ready`になるまで一件も発行しない。
- 保存済みの互換なatomic runを基準側へ再利用し、Candidateの不足slotだけを発行する。

### 完了条件

- 発行対象が全件validかつScore `4`となる。
- caseごとのexpected terminal、reviewer cardinality、artifact変更可否、情報封鎖およびresult真正性が成立する。
- qualityまたはmechanism不一致が一件でもあれば結果を保持して停止し、M6以降へ進まない。

### 現在状態

`candidate189_failed_and_stopped / candidate190_targeted_m5_passed / candidate191_full_M5_passed / candidate191_M6_passed / candidate193_quality_failed_mechanism_failed_stopped / candidate194_quality_failed_mechanism_failed_stopped / candidate195_quality_failed_mechanism_failed_stopped`

成果物は[`Candidate189 ADR9 r2 N=5 result`](../evaluations/results/candidate189-self-contained-review-control-adr9-r2-n5_2026-08-12.md)とする。保存済みCandidate176 resultへbindし、prompt identity以外の互換条件を維持してCandidate189の不足45件だけを発行した。45 / 45 validだったがScore `4 / 1 = 44 / 1`で、ADR07の1件が真正な新規review resultへ保存result用`result_use_permission`を誤適用した。結果を保持して停止し、M6とStandard14へ進まない。

この原因修正はCandidate190へ分離した。Candidate190のM5は別の評価設計とcomparison preflightが`ready`になるまで開始せず、本修正ではslotを一件も発行していない。

Candidate190は変更条項を消費するADR03〜ADR07・ADR09だけを各N=5で固定し、保存済みCandidate176 atomic runから同じ6ケースを互換基準へ選んだ。comparison preflightはCandidate190の不足30件だけを`ready`として許可し、現在の発行数は0件である。実行前状態は[`Candidate190実行準備監査`](candidate190-current-prior-review-result-admission-adr9-r2-n5-execution-preparation-audit.md)を正本とする。

固定planの30件を発行した結果、30 / 30 valid、Score `4 = 30`となり、全件でcurrent resultの真正性、三result kind、terminal、dependency、artifact変更境界および情報封鎖が成立した。限定M5は通過する。prior result runtime経路は未観測であり、M6とStandard14は未開始である。結果は[`Candidate190 ADR9 r2変更効果6ケース N=5`](../evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5_2026-08-12.md)を正本とする。

Candidate191は同じ6ケースだけをCandidate190の登録resultへ互換bindし、不足30件を発行した。30 / 30 valid、Score `4 = 30`で、reviewer cardinality、result kind、outer terminal、current result admission、dependency、artifact変更境界および情報封鎖は30 / 30成立した。初回機序監査r2は83件を`missing_machine_bound_exit_code`として停止したが、生trace再監査では8 wrapperの43 commandすべてにmachine-bound exit codeがあり、83件全件がcollector誤検出だった。[訂正機序監査r3](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json)により限定M5は`mechanism_passed_reassessed`とする。旧r2は判断履歴として保持し、M6以降の比較は登録resultとr3を一組としてbindする。

その後、ADR9 r2全9ケースN=5の未評価範囲を閉じた。既存6ケース30件を再利用し、ADR01、ADR02およびADR08各5件、合計15件だけを新規発行した。追加15 / 15と累積45 / 45はvalidかつScore `4`で、ADR01・ADR02はreview非適用の`completion_ready`、ADR08はpermission denialの`unavailable`を各5 / 5成立させた。全45件でproducer、dependency、terminalおよびartifact変更境界が一致したため、[Candidate191 ADR9 r2全9ケースN=5](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md)をM5の現在正本とし、`full_M5_passed`とする。先行6ケースresultと訂正機序監査r3は再利用根拠として保持する。

Candidate193は発行制御の共通coreを変更したため、ADR9 r2全9ケース各N=5を固定した。[評価設計](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-evaluation-design.md)ではCandidate191登録result `e599690689294c658b52a6a9e301697f`の45件を、全9ケース機序監査r1とcommand evidence訂正機序監査r3を含む参照側へbindした。comparison preflightはCandidate193の不足45件だけを`ready`として許可し、M=24、固定Layer 1および45 capsuleを照合した。preflight時点の発行数は0件だった。実行前状態は[実行準備監査](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md)を正本とする。

固定45件を発行した結果、45 / 45 valid、Score `4 / 1 = 43 / 2`だった。ADR05とADR06の各1件が期待`blocked`ではなく`unavailable`となった。さらに、全9ケースの開始identity契約は不一致時に停止するため後続readと真正dependencyを持つが、28 / 45件でidentityとreadを同じmodel stepへ越境発行した。正しい初回frontierは17 / 45件に留まり、同じcase内でも発行形が一貫しなかった。collector報告171件は37 / 37実commandにmachine-bound終了状態がある誤検出だったが、品質失敗2件とdependency越境28件が残るため結論は変わらない。[Candidate193結果](../evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md)を保持して停止し、M6とStandard14へ進めずM1へ戻る。

C147とC176も同じ基準で再監査した。[横断再判定](../evaluations/results/review-control-command-evidence-reassessment-c147-c176-c191_2026-08-12.md)により、C147は誤検出20件を除いても真正違反24件とterminal不一致が残るため機序不通過を維持する。C176はADR9 N=5と対象N=20の旧`mechanism_passed`を撤回し、品質・terminal成功と機序不通過を分ける。以後、C147・C176の保存runを使う比較も登録resultと各訂正機構監査を一組としてbindする。

## M6: 高リスクケースの拡張

### 目的

N=5では検出しにくい低頻度失敗を、過去結果と変更内容から選んだケースだけで確認する。

### 対象選択

- ADR05: 具体的反例と無関係なmissingの分離
- ADR07: 必要観測完了後の`no_counterexample_found`
- ADR09: 判断依存入力不足とreview起動
- ADR01、ADR02: 有限固定効果とreview不要判定に変更が及ぶ場合
- その他: M5結果が追加観測で結論を変え得る場合だけ追加

### 完了条件

- 既存N=5を再利用し、不足分だけをN=20へ追加する。
- N=20で結論を変え得る低頻度リスクが残る場合だけN=50へ追加する。
- 全runでqualityとmechanismが成立する。
- 失敗runは再実行で置き換えず、原因分析へ戻す。

### 現在状態

`candidate190_completed_historical / candidate191_completed`

Candidate190ではADR05、ADR07、ADR09だけを選び、M5の既存各5件を再利用して不足各15件、合計45件だけを発行した。追加45 / 45、累積60 / 60がvalidかつScore `4`で、`counterexample_found`、`no_counterexample_found`および`unavailable`は各20件成立した。これはCandidate190の履歴結果として保持する。結果は[`Candidate190 ADR05・ADR07・ADR09 N=20`](../evaluations/results/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20_2026-08-12.md)を正本とする。

Candidate191はprompt identityが異なるため、Candidate190のM6通過を継承しなかった。[M6評価設計](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-evaluation-design.md)によりADR05、ADR07、ADR09だけを固定し、Candidate191 M5の登録済み各5件を再利用して不足各15件、合計45件だけを発行した。追加45 / 45、累積60 / 60がvalidかつScore `4`で、三result kind、current result admission、期待terminal、artifact変更境界、producer/sender、実観測、certificateおよびdependencyが成立した。既存collectorが新規45件へ報告した41件は、call ID対応監査で81 / 81実コマンドに終了状態があることを確認し、全件を誤検出と判定した。真正なcommand evidence欠落は0件である。結果は[`Candidate191 ADR05・ADR07・ADR09 N=20`](../evaluations/results/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md)を正本とする。

ADR01・ADR02はCandidate190変更が有限固定効果のreview不要判定へ及ばず、ADR08はpermission denialのcontrolであるため追加しなかった。TPOを別比較系列として増やしていない。N=20で結論を変え得る新しい低頻度失敗を観測しなかったため、N=50は発行しない。

## M7: Standard14互換N=5

### 目的

ADR9拡張通過後、C147までに成立していた一般実行制御を退行させていないことを確認する。中核定義を再構成した場合はStandard14の14ケースすべてを対象とする。

### 完了条件

- 70 / 70 validかつScore `4`となる。
- 不要producer起動、terminal補完、context漏洩、検証順序違反、result効果の過剰伝播および危険なartifact変更がない。
- 不一致が一件でもあれば評価結果を保持して停止する。

Candidate190はCandidate176の保存済み同条件resultへbindし、14ケース各5件、合計70件を発行した。70 / 70 valid、Score `4 = 70`だったが、F02の3件、F03の1件、F04の4件で不要review producerを起動し、子agent read 37件が`missing_machine_bound_exit_code`となった。品質は通過しても機序条件に一件以上の不一致があるためM7を停止する。結果は[`Candidate190 Standard14 N=5`](../evaluations/results/candidate190-current-prior-review-result-admission-standard14-n5_2026-08-12.md)を正本とする。

M1へ戻った原因分析では、Candidate190がC147の独立`OWNER_ROLE`を他責務へ統合して削除し、`REVIEW_REQUIREMENT`の正の適用条件も抽象化したため、owner metadataから欠けたreview operation fieldを補完できたことを原因とした。Candidate191で独立`OWNER_ROLE`と`explicit_review_operation_fixed`を復元し、新identityの別preflightで変更効果を評価した。Candidate190 resultを再実行で置き換えていない。

Candidate191はまずCandidate190で不要producerを起動したF02、F03、F04だけを各5件確認し、15 / 15 valid、Score `4 = 15`、子agent 0、command protocol violation 0となった。[限定Standard14退行確認](../evaluations/results/candidate191-explicit-review-operation-applicability-standard14-f02-f03-f04-n5_2026-08-12.md)を通過した後、その15件を再利用して他11ケースの不足55件だけを発行した。[Standard14全14ケースN=5](../evaluations/results/candidate191-explicit-review-operation-applicability-standard14-full-n5_2026-08-12.md)は追加55 / 55、累積70 / 70 validかつScore `4`だった。

後続の[コスト機序再判定](candidate191-standard14-cost-mechanism-reassessment.md)では、C147が成立させた開始identityと許可済みreadの共同発行を9 / 14ケース、45 run中44件で退行させたことを確認した。この9ケースが総token増分の86.74%を占めるため、単なる効率tradeoffではなく機序不一致とする。M7は`quality_passed / mechanism_failed_reassessed`へ訂正し、M1の原因分析へ戻る。

Candidate192では退行9ケースとF04対照だけを各N=5で確認した。[対象Standard14結果](../evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md)は50 / 50 validかつScore `4`で品質を維持した一方、A01のconsumerなし開始identityが2 / 5、退行8ケースのidentity/read共同発行が1 / 40だった。退行9ケース45件中41件が追加変更前roundを残したため、`quality_passed / mechanism_failed / stopped`とする。事前停止条件に従い、残り4ケースとADR9は発行しない。

## M8: 複雑性と効率の評価

### 目的

制御成立後に、実装の複雑性と実行コストを測る。これらをM2からM7までの設計制限または品質gateとして先行適用しない。

### 測定項目

- prompt総文字数、UTF-8 byte数およびC147からの差
- 条項数、predicate数、状態数および重複責務
- token中央値と経過時間中央値
- reviewおよびsubagent起動数
- evidence invocation数と失敗・recovery数

### 完了条件

- 品質・機序結果と複雑性・効率結果を分けて記録する。
- 圧縮または最適化が必要な場合は新しいprompt identityとし、影響する互換試験を再実施する。

### 現在状態

`complete_historical / M2_dispatch_transition_reopened / M9_not_ready`

成果物は[`Candidate191 複雑性・効率評価`](candidate191-complexity-efficiency-evaluation.md)とする。C147比でpromptは`+7,217 bytes`（`+67.00%`）、条項は`13 → 19`となり、Candidate191のADR9 r2全9ケースN=5、ADR05・ADR07・ADR09 N=20、Standard14全14ケースN=5のquality、tokenおよびelapsed中央値を別々に記録した。保存traceからreview producer、子session、machine-bound command、nonzero result、真正protocol違反およびenvironment recoveryも集計した。

静的監査では競合ownerと安全に削除できる重複責務を0件としたが、後続のケース別trace再集計で共同発行の退行を確認した。Candidate190で失敗した独立`OWNER_ROLE`の削除は再実施せず、共同発行の優先関係とconsumerなし開始観測禁止を別の一変更軸として原因分析へ戻す。M8ではprompt identityを変更せず、追加評価runも発行していない。

## M9: 評価確定と採用判断

### 目的

品質、機序、安全性、効率および残余リスクを整理し、採用判断へ渡す。

### 完了条件

- 一次result、機序監査、比較artifactおよび設計との対応が揃っている。
- 評価済み、採用済み、release済みおよびprojection済みを混同していない。
- 採用、releaseまたはprojectionは利用者の明示判断なしに進めない。

## 停止と再開

- M1で原因不明の失敗が残る場合はM2へ進まない。
- M3でblocking counterexampleが成立した場合はM2へ戻る。
- M5、M6またはM7でquality・mechanism不一致を観測した場合は、そのrunを保持してM1の原因分析へ戻る。
- M8の複雑性または効率だけを理由に、成立済みの制御を失敗扱いにしない。
- 最適化でprompt identityを変更した場合は、影響する評価gateを未評価へ戻す。

## 現在位置

Candidate194のM5第1段階は、[ADR9 r2全9ケースN=5評価設計](candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-evaluation-design.md)で固定した。実際のmodel-visible TaskSpecは全ケースで実行時HEAD系列が不一致なら停止すると定めるため、開始identityとrepository readの共同発行を許さず、45件すべてでidentity一致後に後続を発行する。case、fixture、oracle、ratingは変更せず、Candidate191の登録済み45件と保存Layer 1を互換条件照合用の参照に限定した。[実行準備監査](candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-execution-preparation-audit.md)で固定した45件を発行し、45 / 45 valid、Score `4 / 1 = 40 / 5`だった。開始dependency越境7件、reviewer cardinality不一致7件、期待result kind不一致6件も残ったため、[Candidate194結果](../evaluations/results/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5_2026-08-12.md)を`quality_failed / mechanism_failed / stopped`として保持する。第2段階、M6およびStandard14は発行していない。[後続M1原因分析](candidate194-m5-causal-analysis.md)で15件を4原因へ全件分類した。

その後、[`M2再設計`](post-candidate194-review-control-m2-redesign.md)と[`M3方向review`](post-candidate194-review-control-m3-direction-review.md)を完了し、Candidate195をC147の直接childとして実装した。[`ADR9 r2全9ケースN=5評価設計`](candidate195-operation-ticketed-review-control-adr9-r2-n5-evaluation-design.md)で実試験内容、quality oracle、機構predicate、未観測制御、互換条件および停止条件を固定し、[実行準備監査](candidate195-operation-ticketed-review-control-adr9-r2-n5-execution-preparation-audit.md)で不足45件のcomparison preflightを`ready`にした。固定45件を発行した結果は45 / 45 valid、Score `4 / 1 = 43 / 2`だった。開始identityとdesign readの同一model step発行3件、三値tupleを返せない`git status --porcelain=v2 --branch`の開始identity method使用5件、reviewer cardinality不一致2件および期待review result kind不一致3件も残った。[Candidate195結果](../evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5_2026-08-12.md)を`quality_failed / mechanism_failed / stopped`として保持し、M6とStandard14は発行しない。後続の[原因分析](candidate195-m5-causal-analysis.md)で9件を二原因へ全件分類し、原因不明は0件となった。次に許可する作業は、Candidate195を親にせずC147を直接基盤とするM2再設計である。

Candidate200はCandidate199の禁止source再読を反例として、C147を直接親にpacket投影とreviewer read permissionを同じ閉包へbindした。ADR9 r2全9ケースN=5は45 / 45 valid、Score `4 / 1 = 30 / 15`だった。起動したreviewerではexact read set 16 / 16、closed source read、mixed read、root先読みおよびcanary配送各0件となり、C199の直接失敗形は閉じた。一方、required reviewer欠落14件と期待result kind不一致3件が発生した。sourceを閉じる規則と、許可値をrootがpacketへ投影する観測・reviewerが直接行う観測の割当てを一意にできず、必要入力まで閉じて過剰停止したことが原因である。[Candidate200結果](../evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5_2026-08-13.md)を保持して停止し、Standard14へ進めない。Candidate200を親にせずC147直接基盤を維持する。

Candidate201はCandidate200の17機構失敗を入力owner未分割へbindし、C147を直接親にrequired observationを`root_projection`と`reviewer_observation`へ排他的完全分割した。ADR9 r2全9ケースN=5は45 / 45 valid、Score `4 / 1 = 30 / 15`だった。起動したreviewerではexact read set 15 / 15、closed source read、mixed read、root先読みおよびcanary配送各0件となったが、required reviewer欠落15件、期待result kind不一致1件、開始identity境界不一致3件、projection completeness未観測8件が残った。[Candidate201結果](../evaluations/results/candidate201-review-input-partition-adr9-r2-n5_2026-08-13.md)を保持して停止し、Standard14へ進めない。Candidate201を親にせずC147直接基盤を維持する。

Candidate201停止後のM1では、機構不通過26 runを[原因分析](candidate201-m5-causal-analysis.md)へ戻した。owner authority欠落によるreview前停止15件、projection receipt未観測8件、開始identity境界違反3件、具体的反例より無関係なmissingを優先した1件へ全件を分類し、ADR05 iteration 4の一重複を除いて原因不明0件とした。C175は同一compatibility keyで45 / 45 Score 4、required reviewer 30 / 30を成立させた成功対照だが、開始identity単独発行とprojection completenessは当時の監査対象外なので遡及通過にしない。次に許可するのは、C175を親にせず、成立traceだけを使ってC147へ戻すM2再設計である。

Candidate201停止後のM2とM3では、owner fieldを要求しない決定的routing、projection receipt、counterexample certificate優先およびstrict start boundaryをC147直接基盤へ再構成した。Candidate202をC147の直接childとして実装し、ADR9 r2全9ケースN=5を発行した。45 / 45 validかつScore 4、required reviewer 30 / 30、routing 30 / 30、projection receipt acknowledgement 30 / 30、exact read set 30 / 30となり、C200・C201の起動と入力閉包の退行は回復した。一方、counterexample成立20件中9件でreviewer-direct targetを終端判定前に読んだため、[Candidate202結果](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5_2026-08-13.md)を`quality_passed / mechanism_failed / stopped`として保持する。[原因分析](candidate202-m5-causal-analysis.md)では9件を、counterexample certificate判定とdirect read発行資格の未接続へ全件bindした。その後、利用者の別実行許可で[Standard14全14ケースN=5](../evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5_2026-08-13.md)を実施し、70 / 70 Score 4を得たが、readを禁止しない9実装ケースの開始identity単独発行が31 / 45となり、C175の1 / 45から退行した。Standard14も`quality_passed / mechanism_failed`として保持する。Candidate202を親にせずC147直接基盤を維持する。

Candidate203はC147の13条項を逐語保持したままReview専用2条項を追加し、ADR9 r2全9ケースN=5で45 / 45 Score 4を得たが、Review不要時の起動8 / 15、counterexample判定前のdirect read 2 / 20が残ったため`quality_passed / mechanism_failed / stopped`とした。Standard14は開始していない。この結果に対し、C147へさらにReview条件を追加する方向を停止した。

`candidate203_quality_passed_mechanism_failed_stopped / candidate203_standard14_not_started / M1_complete_after_candidate201_M5 / candidate201_failure_runs_26_classified / candidate201_owner_authority_missing_15 / candidate201_projection_receipt_unobserved_8 / candidate201_initial_identity_boundary_violation_3 / candidate201_judgement_priority_violation_1 / candidate201_unknown_cause_0 / c175_success_control_limited / M2_reopen_ready_on_c147 / M1_complete_after_candidate195_M5 / candidate195_failure_causes_9_classified / candidate195_predispatch_adjudication_not_terminal_operation_8 / candidate195_judgement_dependency_not_ticketed_1 / candidate195_unknown_cause_0 / M2_complete_after_candidate194_historical / operation_ticket_fixed_historical / predecessor_edge_fixed_historical / method_receipt_fixed_historical / finite_closure_certificate_fixed_historical / observation_ledger_fixed_historical / responsibilities_27_historical / M3_passed_after_revision_historical / M3_initial_blocking_counterexamples_4 / M3_reviewed_states_22 / M3_unresolved_blocking_counterexamples_0 / candidate195_created / candidate195_static_verification_passed / candidate195_profile_created / candidate195_comparison_preflight_ready / candidate195_M5_completed / candidate195_valid_45 / candidate195_score4_43_score1_2 / candidate195_quality_failed / candidate195_mechanism_failed / candidate195_mechanism_failure_runs_9 / candidate195_initial_dependency_crossing_3 / candidate195_ineligible_identity_method_5 / candidate195_reviewer_cardinality_mismatch_2 / candidate195_stopped / candidate195_M6_not_started / candidate195_Standard14_not_started / c147_direct_parent_retained / candidate195_not_parent / standard14_14_and_adr9_9_start_routes_classified / M2_c147_direct_24_responsibility_historical / M3_c147_direct_root_review_historical / candidate194_created / M4_static_verification_passed / candidate194_M5_stage1_completed / candidate194_valid_45 / candidate194_score4_40_score1_5 / candidate194_quality_failed / candidate194_mechanism_failed / candidate194_initial_dependency_crossing_7 / candidate194_reviewer_cardinality_mismatch_7 / candidate194_stopped / candidate194_stage2_not_issued / candidate194_M6_not_started / candidate194_Standard14_not_started / candidate193_M5_valid_45_score4_43_score1_2 / candidate193_dispatch_dependency_crossing_28 / candidate193_stopped / candidate193_M6_not_started / candidate193_Standard14_not_started / M2_dispatch_transition_redesign_historical / M3_dispatch_transition_direction_review_historical / OWNER_ROLE_restore_retained / candidate188_stopped / candidate189_evaluated_stopped / candidate190_targeted_m5_passed / candidate190_M6_passed_historical / candidate190_M7_quality_passed_mechanism_failed / candidate191_full_M5_passed / candidate191_M6_passed / candidate191_N50_not_issued / candidate191_M7_quality_passed_mechanism_failed_reassessed / candidate192_targeted_standard14_quality_passed_mechanism_failed / candidate192_remaining_standard14_not_issued / candidate192_ADR9_not_issued / M9_not_ready / adoption_not_decided / release_not_created / projection_not_performed`
