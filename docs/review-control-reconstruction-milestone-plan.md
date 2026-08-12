# review制御再構成マイルストーン計画

> **位置づけ**: 現行frontier／Candidate193 ADR9 r2品質・発行遷移機序不通過／M1原因分析再開

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

`reopened / candidate193_quality_and_dispatch_failures_bound / causal_analysis_in_progress`

成果物は[`review制御再構成の因果分析`](review-control-reconstruction-causal-analysis.md)とする。ADR01〜ADR09を5種類のterminal別証明責務へ全件分類し、過去Candidateの狙い・実結果・反復原因、C147の13条項の保持・改訂・分割・統合後削除候補、およびM2へ渡す未解決predicateと必要観測を固定した。

Candidate192の失敗を追加分析し、consumer・dependencyの判定自体ではなく、ready集合の論理判定と同一model responseからの実発行を別責務として解釈できたことを原因へbindした。C192からはconsumer、dependency、個別result contract、真正dependency非越境および50 / 50の品質維持を保持し、独立した抽象`DISPATCH_ADMISSION`とその挙動拘束仮定は継承しなかった。その時点ではCandidate191を直接基盤としてC147の`DECISION_BOUNDARY`をresult effectと発行遷移へ分割したが、この発行遷移部分は後続Candidate193の反例により撤回対象となった。

Candidate193の結果からは、ADR9全9ケースの開始identityと後続readが真正dependencyを持つ訂正済み判定、consumer／dependencyの判定軸、個別result contract、compound command禁止、43件で維持したreview・artifact・command境界、およびADR05・ADR06の保存反例を残す。同じ新基準ではCandidate191の越境36 / 45に対しCandidate193は28 / 45であり、正しい分離を9件から17件へ増やしたため、`DISPATCH_TRANSITION`全体を無作用として捨てない。ただし一意拘束には失敗しているため、各primitive、独立条項化および次Candidateの親は保留する。捨てるのは、自己terminal宣言だけで現在responseのtool-call選択を一意に強制できるという十分性仮定である。M1ではC147の`DECISION_BOUNDARY`の優先関係と2件のcertificate dependencyを再分析し、M2、次Candidateおよび追加評価は開始しない。

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

`historical_design / sufficiency_counterexample_found / primitives_pending / M1_reanalysis_required / candidate_not_created`

成果物は[`review制御再構成の責務設計`](review-control-reconstruction-responsibility-design.md)とする。operation specificationからouter terminalまでの既存10責務を保持し、共通execution coreへ`DISPATCH_TRANSITION`を加えた11責務とした。review適用可否・要否・実行permission、packet形成と観測state、review judgementと保存result admission、dependencyとinvalidation、発行遷移およびartifact変更許可を別々のownerへ固定した。

既存10責務とCandidate191の成立経路は保持した。再開範囲は発行遷移だけであり、`dispatch_frontier`の固定、同一model responseからの個別tool call全件発行、全result受領まで判断を戻さないclosureを`dispatch_transition_terminal`という分離不能な一つの挙動遷移へ配置した。C192への条項追加、review責務の再設計、新しいresult kindまたは評価系列の追加は行っていない。

このM2設計は「最大集合」を廃し、consumerを持つ発行候補から未解決predecessorを除いた`dispatch_frontier`を、現在model responseの全tool-call identityへ一対一bindした。しかしCandidate193評価で真正dependency越境を28 / 45件観測し、一意拘束には不足すると判明した。同じ基準のCandidate191より越境は8件少ないため部分効果は保留し、成立済み設計としても全棄却としても次へ渡さない。

## M3: 設計方向の敵対的レビュー

### 目的

設計を成立不能にする一般的な具体的反例を確認する。表現改善、網羅性の追加または試験で判定可能な不確実性だけを理由に設計を循環させない。

### 完了条件

- 未解決のblocking counterexampleがない。
- 設計のtarget、permission、methodまたはstop conditionを変える指摘が残っていない。
- 残余リスクが試験predicateと対象ケースへ対応している。
- reviewの反復で当初の設計軸を増やしていない。

### 現在状態

`complete / dispatch_transition_direction_review_passed`

成果物は[`review制御再構成の方向レビュー`](review-control-reconstruction-direction-review.md)とする。M2初稿へ具体的反例5件が成立したためM2へ戻り、review契約非適用、aggregate result contract、terminal後の新operation identity、finite relationのmachine-bound照合、保存result admissionと新規review permissionの分離を同じ10責務内で修正した。修正版8条件の再確認では未解決blocking counterexampleが0件となり、残余リスクをADR9とStandard14のmechanism predicateへ対応させた。

この完了はCandidate191までの責務設計に対する履歴である。M2で発行遷移を再設計した後は、consumerなし空集合、真正dependency、個別result contract、およびready集合の一部発行というC192由来の4反例だけを確認する。完全性確認や別系列の追加は行わない。

再開M3では、consumerなし空frontier、readを変える／変えないidentity result、同時発行上限、個別resultの一部失敗、cell ID付きnonterminal result、frontierの部分発行およびcompound command代用を確認した。いずれも同じ`DISPATCH_TRANSITION`内で一意に停止または発行でき、未解決blocking counterexampleは0件だった。成果物は[`方向レビュー`](review-control-reconstruction-direction-review.md)のCandidate192後追記を正本とする。

## M4: Candidate実装

### 目的

固定した設計をprompt bundleへ実装する。C147への追記だけに限定せず、必要な分割、統合、置換および削除を行う。

### 完了条件

- 設計predicateと実装箇所が一対一または明示された合成関係で対応する。
- 各責務の正本が一つで、旧定義との競合がない。
- bundle identity、manifest、構造試験および実装一致監査が成功する。
- Candidate、評価、採用、releaseおよびprojectionの状態が分離されている。

### 現在状態

`candidate192_stopped_historical / candidate193_evaluated_stopped / M1_reopened`

Candidate188は静的再監査で停止した。Candidate189はcurrent resultへ保存result用`result_use_permission`を誤適用した一件で停止し、Candidate190でcurrent/prior admissionを分離した。Candidate190はM5とM6を通過したが、M7 Standard14の8 runでcriterion ownerを独立review operationへ昇格し、不要producerを起動したため停止した。この反例により、C147の`OWNER_ROLE`を統合後削除した分類を撤回し、独立責務として復元する。

修正版の成果物は[`Candidate191 explicit review operation applicability実装監査`](candidate191-explicit-review-operation-applicability-implementation-audit.md)と、prompt bundle `the-caption-3ce91a4-explicit-review-operation-applicability-r1`とする。Candidate190を直接親とする単一修正で、reviewを必要な独立operationとして直接名指しした場合だけreview controlを適用し、owner、`non_machine_risk`、静的確認または独立確認の語列だけではoperation、producer、spawnおよびreview resultを作らない。限定Standard14では修正対象3ケースを通過した。ADR9 r2も30 / 30 Score 4となり、初回機序監査が報告した83件は後続再監査でcollector誤検出と確定したため、Candidate191のM5は訂正後に通過した。

後続のコスト機序再判定で、Candidate191はStandard14の9ケース、45 run中44件で変更前stepを一つ増やし、A01ではconsumerのない開始identity観測も発行したと確認した。Candidate192はCandidate191を直接親とし、`DISPATCH_ADMISSION`だけを追加する。evidence資格、result効果、review責務を変えず、requested resultのconsumerと相互dependencyから発行集合を決める。成果物は[`Candidate192 consumer-bound co-issuance実装監査`](candidate192-consumer-bound-coissuance-implementation-audit.md)と、prompt bundle `the-caption-3ce91a4-consumer-bound-coissuance-r1`とする。

Candidate192の対象Standard14評価は50 / 50 validかつScore 4だったが、A01 consumerなし開始identityが2 / 5、退行8ケースのidentity/read共同発行が1 / 40に留まった。定義した発行資格が実際のmodel stepを拘束しなかったためCandidate192を停止し、M1へ戻る。次Candidateの実装は、新原因に対する設計と方向を変える具体的反例の確認が終わるまで開始しない。

限定M2・M3完了後、Candidate193 `the-caption-3ce91a4-frontier-bound-dispatch-transition-r1`をCandidate191の直接childとして作成した。C192本文は継承せず、`DISPATCH_TRANSITION`だけを追加し、`RESULT_EFFECT`から発行所有を移した。成果物は[`Candidate193 frontier-bound dispatch transition実装監査`](candidate193-frontier-bound-dispatch-transition-implementation-audit.md)とする。後続M5で品質・発行遷移機序の不一致を観測したためCandidate193は停止済みである。

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

`candidate189_failed_and_stopped / candidate190_targeted_m5_passed / candidate191_full_M5_passed / candidate191_M6_passed / candidate193_quality_failed_mechanism_failed_stopped`

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

`M1_reopened_for_candidate193_quality_and_dispatch_failures / candidate193_M5_valid_45_score4_43_score1_2 / candidate193_dispatch_dependency_crossing_28 / candidate193_stopped / candidate193_M6_not_started / candidate193_Standard14_not_started / M2_dispatch_transition_redesign_historical / M3_dispatch_transition_direction_review_historical / OWNER_ROLE_restore_retained / candidate188_stopped / candidate189_evaluated_stopped / candidate190_targeted_m5_passed / candidate190_M6_passed_historical / candidate190_M7_quality_passed_mechanism_failed / candidate191_full_M5_passed / candidate191_M6_passed / candidate191_N50_not_issued / candidate191_M7_quality_passed_mechanism_failed_reassessed / candidate192_targeted_standard14_quality_passed_mechanism_failed / candidate192_remaining_standard14_not_issued / candidate192_ADR9_not_issued / M9_not_ready / adoption_not_decided / release_not_created / projection_not_performed`
