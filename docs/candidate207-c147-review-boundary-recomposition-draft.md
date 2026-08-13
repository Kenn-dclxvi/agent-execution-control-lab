# Candidate207 C147 review境界再構成 本文案・作成前監査

## 状態

- 直接基盤: `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）
- 比較対象: Candidate147
- C173〜C206の用途: 保存済み誤経路と成立機序の診断証拠だけ
- 現在段階: `sentence_disposition_complete / input_ownership_complete / draft_complete / pretrace_falsification_passed_after_revision`
- Candidate bundle: `not_created`
- evaluation: `not_started`

この文書は、[C207再構成・検証計画](candidate207-c147-review-boundary-recomposition-plan.md)の実施順1〜3を完了する。後続の実施順4では初回本文案に一件のblocking counterexampleを確認し、`projected_counterexample_established(packet)`をdirect-read eligibilityへ接続して解消した。事前反証の正本は[`candidate207-c147-review-boundary-recomposition-direction-review.md`](candidate207-c147-review-boundary-recomposition-direction-review.md)とする。

## 1. C147からC206へ追加された全文の処分

識別子はC206 root `AGENTS.md`の変更箇所を句点単位で分けたものである。`P`は`PRODUCER`、`O`は`OWNER_ROLE`、`E`は`EVIDENCE_GATE`、`D`は`DESIGN_ADMISSION`を表す。C147と同一の文は表へ入れず、追加または置換された文を全件扱う。

処分は次の四値へ限定する。

- `C147維持`: C147の既存文ですでに境界が成立するため追加しない。
- `局所置換`: 保存済み誤経路を閉じる値だけをC147の既存制御群へ接続する。
- `review固有境界`: C147に存在せず、ADR9のmodel-visible入力と保存結果が必要性を示すpredicateだけを追加する。
- `除外`: 手順、別最適化軸、未観測の完全化または既存制御の重複なのでC207へ入れない。

### `PRODUCER / OWNER_ROLE / EVIDENCE_GATE`

| ID | C206追加・置換文 | 処分 | C207での扱い |
| --- | --- | --- | --- |
| P1 | `explicit_producer_execution_required`を、TaskSpec内のproducer identityの直接・一意bindingで定義する | `局所置換` | operation applicabilityとpermissionが明示される場合、そのbind済み値も要求する`producer_execution_required(operation)`へ変換する |
| P2 | 特定field名またはschemaを要求しない | `C147維持` | C147は既に特定schemaを要求せず「TaskSpecが明示」としているため追加しない |
| P3 | identityを指定しないcriterion、owner、risk、pass condition、役割語だけではproducerを選ばない | `C147維持` | C147 `PRODUCER / OWNER_ROLE`のowner語列非権限化を維持し、重ねない |
| O1 | `explicit_producer_execution_required=true`の場合だけworkerを起動する | `局所置換` | P1の`producer_execution_required(operation)=true`を既存`OWNER_ROLE`が消費する形にする |
| E1 | `admitted_evidence_current`の定義 | `除外` | C206固有の再取得最適化軸でありreview再構成と分ける |
| E2 | current identityを再利用し同一repository invocationを発行しない | `除外` | 発行回数を直接固定する実行制御で、C147比の費用対効果が不通過 |
| E3 | currentはavailabilityでありpredicate satisfactionではない | `除外` | E1を採用しないため定義補足も持ち込まない |
| E4 | permissionだけではcurrentにせず、値変更後は再観測できる | `除外` | E1系列の例外・再観測手順であり初回C207の因果軸外 |

### `DESIGN_ADMISSION`

| ID | C206追加文の役割 | 処分 | C207での扱い |
| --- | --- | --- | --- |
| D01 | `design_contract_ready`と`general_design_ready`を一つの開始条件へ定義 | `除外` | C147 `SPEC`と`implementation_bound`を別lifecycle内で再定義するため追加しない |
| D02 | contract未readyならSPECへ戻り確認する | `C147維持` | C147 `SPEC`が未固定required outcomeだけをclarificationにする |
| D03 | general design未readyならreviewを起動せず`unavailable`にする | `除外` | review要否とは別の一般設計完全性分類を新設しない。判定に必要なTaskSpec入力欠落だけをreview requirementの`unavailable`にする |
| D04 | artifact変更前にgeneral design identityと全boundary decisionを台帳へ固定 | `除外` | ADR9はdesign identityとboundary ledgerをmodel-visible入力として既に固定する。台帳構築operationを作らない |
| D05 | 各境界へ7種のfieldを結び付ける | `除外` | supplied boundary recordを読むための入力schemaを、prompt内の構築手順へ変えない |
| D06 | `boundary_requires_adversarial_review` | `review固有境界` | supplied boundary record上のreview必要predicateとして残す。台帳構築は要求しない |
| D07 | 全境界を分類して`not_required / required / unavailable`を決める | `局所置換` | TaskSpecが判定対象として固定したboundary record集合に対する一つのrequirement stateへ変換し、分類operationや逐次処理を作らない |
| D08 | `review_permission_allowed` | `局所置換` | 新しいpermission lifecycleを作らず、P1のproducer発行条件と既存`implementation_bound`のdependencyでTaskSpec permissionを直接消費する |
| D09 | review operation identityを構成し、専用producer bindingを検証する | `局所置換` | operation identityはC147 `INDEPENDENCE`、producer identityは`PRODUCER`へ渡す。構成順を固定しない |
| D10 | `bound_task_identity`は専用identityだがowner語列から生成しない | `C147維持` | C147の直接producer指定とowner非権限化で成立する。P1が条件付き指定のapplicabilityだけを補う |
| D11 | `review_operation_spec_ready`へidentity、scope、manifest、read、forbidden inputを集約 | `局所置換` | TaskSpec-supplied packet membershipは`CONTEXT`へ渡し、manifest targetの存在・read成功は開始条件にしない |
| D12 | semantic projectionを新規構築し、forbidden inputと重複readを排除 | `局所置換` | packetの許可membershipと禁止membershipだけを`CONTEXT`へ接続する。新規構築やread順は要求しない |
| D13 | 空/nullによる禁止field配送を禁じ、rootのcriterion/observation生成を禁じる | `局所置換` | 禁止情報の非配送は`CONTEXT`、root非代行は既存`ROOT`で保持する |
| D14 | producer、spec、projectionを`review_operation_admission_closed`へ集約 | `除外` | C147既存群のpredicateを一つの別owner gateへ再集約しない |
| D15 | permissionまたはpacket不足ならoperation作成前に`unavailable`とする | `局所置換` | permission否定はproducerを発行せず変更を閉じる。TaskSpec-required packet descriptor欠落だけを`unavailable`にし、target missingはreviewer観測へ残す |
| D16 | admission closed後だけ一review operationを作りpacketを配送 | `除外` | producer発行資格はP1、cardinalityはC147 `PRODUCER`、packetは`CONTEXT`が所有する。文章順のworkflowを追加しない |
| D17 | 固定済みtargetのmissing/unreadableをreview非起動理由にしない | `局所置換` | descriptorと観測値の所有権分離として`CONTEXT / TERMINAL`へ残す |
| D18 | rootはreview criterionを代行しない | `C147維持` | C147 `ROOT`は非producer operationのpredicate実行・result再生成を禁止済み |
| D19 | `concrete_counterexample_established` | `review固有境界` | `counterexample_found`のterminal certificateとして`TERMINAL`へ接続する |
| D20 | open可能性、名称、より強い設計だけでは具体的反例にしない | `review固有境界` | D19のfalse-positive境界として`TERMINAL`へ残す |
| D21 | 反例を先に判定し、成立後は別manifest不足で失効させない | `局所置換` | 「先に」という手順を削除し、一つの有効witnessでterminalになったresultを無関係なmissingで失効させない境界だけを残す |
| D22 | 反例不成立後にmissingなら`unavailable`、全成功なら`no_counterexample_found` | `局所置換` | 判定順を削除し、三result kindの排他的なterminal条件として`TERMINAL`へ置く |
| D23 | result kindごとにidentity、evidence、manifest完全性を照合 | `review固有境界` | C147 `delegated_result_ready`へreview固有certificateを加える。`counterexample_found`へ全manifest成功を要求しない |
| D24 | 禁止入力、identity、receipt不足をrootが補完しない | `C147維持` | C147 `ROOT / OWNER_ROLE`の非代行と真正Sender条件を維持する |
| D25 | `general_design_admissible`だけが`implementation_bound`とartifact変更を開く | `局所置換` | review requirementとadmissible terminal resultを既存`implementation_bound`の追加dependencyへ直接渡す |
| D26 | 新design identityで台帳とreviewをやり直す | `除外` | revision loopをpromptへ追加しない。bind済みresultの局所失効はC147の既存境界を使う |

この処分で、C206から残るのは「明示producerの条件付きapplicability」「review要否」「review packet membership」「review observation consumer」「三terminal certificate」「変更許可へのresult effect」である。いずれも新しいreview lifecycleを所有せず、C147の既存制御群へ値を渡す。

## 2. 入力所有権

### 所有権表

| 値 | 所有者・供給元 | C207で許す作用 | 禁止する補完 |
| --- | --- | --- | --- |
| required outcome、変更前review要件、artifact変更前禁止 | TaskSpec | `SPEC`と`implementation_bound`のconstraint | promptが一般的review要件を作ること |
| design identity、general design semantic | TaskSpec model-visible fixed input | review operation/resultを対象designへbind | rootまたはreviewerが同一identity内でdesignを改訂すること |
| 判定対象boundary record集合と各recordの`design_relies_on_boundary / closure_source / closure authority / validation coverage / counterexample effect` | TaskSpec model-visible fixed input | `REVIEW_BOUNDARY`のrequirement stateをbind | promptが台帳を探索・構築・拡張すること |
| repository authority、必要時のboundary normative contract | TaskSpec model-visible fixed inputまたはTaskSpecが許可したrepository authority | direct closureと具体的反例のnormative basis | 名称やopen可能性から未観測関係を推測すること |
| review permission | TaskSpec review contract | producer発行可否と変更許可を制約 | capability、一般read許可、owner語列からpermissionを作ること |
| producer execution identity | TaskSpec review contract | requirement=`required`かつpermission=`allowed`の場合だけreview operationへbind | criterion、owner、`review`等の役割語からidentityを生成すること |
| allowed dispositions、required review scope、manifest descriptors、allowed read、forbidden input | TaskSpec review contract | `CONTEXT` packet membershipとresult certificateの有限scope | targetの存在・read成功をpacket readinessへ含めること |
| semantic projection | rootがTaskSpec-supplied値とprovenanceからpacketへ投影 | 許可membershipだけを独立producerへ配送 | 実装、期待結果、history、untrusted prior result、rootの予想反例、forbidden source全体を配送すること |
| manifest targetの実在、可読性、観測値、success condition充足 | bind済みreview producer | `EVIDENCE_GATE`がconsumerを持つ場合だけ観測し、review terminal certificateへbind | rootが先読みまたは代行し、missingをpacket不備へ変えること |
| `counterexample_found / no_counterexample_found / unavailable` | bind済みreview producerのterminal result | `TERMINAL / OWNER_ROLE / implementation_bound`が真正性とresult effectを消費 | root宣言、異Sender、進行記述でresultを補完すること |
| operation identity、producer binding、evidence consumer state、result effect scope、implementation choice | C147既存制御群 | review固有値を既存lifecycleへ接続 | review clauseが別のoperation lifecycleとして再所有すること |

### descriptorとobservation valueの境界

ADR9でTaskSpecが開始前に固定するのは、observation identity、target、expected readable state、success conditionを含むmanifest descriptorである。targetの現在値、実在、可読性またはsuccess receiptはreviewer-owned observationであり、producer起動前のpacket inputではない。

したがって、ADR09のpaired-scope target missingは`review packet incomplete`ではない。reviewerを起動し、残るallowed dispositionを決めるために必要なnamed observationが取得不能であることを`unavailable`へbindする。反対に、ADR03〜ADR06でsemantic projectionだけから有効な具体的反例certificateが成立した場合、別manifest targetを読むconsumerはなくなる。

## 3. ADR9九ケースのmodel-visible状態表

private oracleの値をpromptへ持ち込まず、各trial inputとseedがmodel-visibleに固定する値だけから導出する。

| case | supplied boundary state | requirement | permission | producer | admissible review terminal | outer terminal | C207が閉じる誤経路 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADR01 | repository authorityが単一membershipを直接closure、validation exhaustive、effect implementation-local | `not_required` | allowed | 0 | 不要 | `completion_ready` | review contract内のtask identityだけによる不要review |
| ADR02 | repository authorityが有限集合とrelationを直接closure、validation exhaustive、effect implementation-local | `not_required` | allowed | 0 | 不要 | `completion_ready` | 有限closure済みrelationへの不要review |
| ADR03 | autonomous exploration、authority open、validation non-exhaustive、effect general-design-change | `required` | allowed | 1 | `counterexample_found` | `blocked` | review省略、open可能性だけの推測、certificate成立後の不要read |
| ADR04 | membershipは直接closureだがstop applicabilityはautonomous/open/non-exhaustive/general-design-change | `required` | allowed | 1 | `counterexample_found` | `blocked` | 一つのclosed boundaryから別のopen boundaryまで閉じたとする誤分類 |
| ADR05 | ownershipがautonomous/open/non-exhaustive/general-design-change | `required` | allowed | 1 | `counterexample_found` | `blocked` | owner局所判断による自己免除と、無関係missingによる反例失効 |
| ADR06 | semantic membershipがautonomous/open/non-exhaustive/general-design-change、forbidden historyあり | `required` | allowed | 1 | `counterexample_found` | `blocked` | history/canary配送と、projectionで閉じた後のsource全体再読 |
| ADR07 | paired open boundary、全manifest target readable | `required` | allowed | 1 | `no_counterexample_found` | `completion_ready` | 一件witness用条件と全scope成功条件の混同、正しいreview resultの汚染扱い |
| ADR08 | 二つのautonomous/open boundary | `required` | denied | 0 | review resultなし | `unavailable` | permission否定後のreview起動、artifact変更またはroot代行 |
| ADR09 | ADR07と同じrequirementだがpaired-scope observation targetがmissing | `required` | allowed | 1 | `unavailable` | `unavailable` | target missingをpacket不備としてreviewer起動前に停止すること |

期待review cardinalityは、ADR01、ADR02、ADR08が各run 0、ADR03〜ADR07とADR09が各run 1である。これはworker数一般をKPIにするものではなく、TaskSpecが明示した独立review operationのapplicabilityとpermissionを検証する機序値である。

## 4. C207 root制御本文案

本文案はC147全文を直接基盤とし、次の差分だけを適用する。ここにないC147条項と文はbyte単位で変更しない。この差分定義により、Candidate bundleを作らずにC207本文を一意に再構成できる。

### 4.1 `PRODUCER`第3文の置換

C147の次の文を置換する。

> TaskSpecが独立したproducer executionを明示した場合だけ、その指定identityをproducer role identityへbindする。

本文案:

> `producer_execution_required(operation) := TaskSpecがそのoperationのterminal resultとproducer execution identityを明示し、そのidentityを対応operation identityへ直接かつ一意にbind可能 ∧ TaskSpecまたはbind済みresultがそのoperationのapplicabilityまたはpermissionを明示する場合はそれぞれtrueまたはallowedへbind済み`とし、trueの場合だけ指定identityをproducer role identityへbindする。

既存の「criterion owner語列だけでproducerを選ばない」とproducer変更時の失効はそのまま残す。

### 4.2 `OWNER_ROLE`第2文の置換

C147の次の文を置換する。

> TaskSpecが独立したproducer executionを明示した場合だけ、起動前にそのexecution identityをtask identityとしてproducerへbindし、predicate前に対応workerを起動する。

本文案:

> `producer_execution_required(operation)=true`の場合だけ、起動前にそのexecution identityをtask identityとしてproducerへbindし、predicate前に対応workerを起動する。

`delegated_result_ready`、Sender照合、root補完禁止および別operationのresult非失効は変更しない。

### 4.3 `CONTEXT`末尾への追加

本文案:

> TaskSpecがartifact変更前の独立reviewを明示した場合、review packetはTaskSpecがreview inputとして許可したsemantic valueとprovenanceだけを含み、実装、期待result、history、untrusted prior result、rootの予想resultおよびforbidden inputのkey / value / 要約 / 存在状態を含めず、forbidden inputを含むsource artifactまたはread result全体も含めない。TaskSpecがobservation identity / target / expected state / success conditionをmanifest descriptorとして固定済みなら、targetの現在値 / 実在 / 可読性 / success receiptはreviewer-owned observationであり、packet readinessまたはproducer起動条件にしない。

これはpacket membershipと観測所有権だけを定める。packetの作成順、read順または配送roundは定めない。

### 4.4 `TERMINAL`末尾への追加

本文案:

> artifact変更前の独立reviewでは、`projected_counterexample_established(packet) := packet内のTaskSpec-allowedなmodel-visible valueとprovenanceだけでreview operation / design / boundary / contract basis / 具体的instance / 固定designとの直接矛盾 / designを変えるeffectがbind済み`、`counterexample_found := bind済みproducer resultがprojected_counterexample_established=trueまたは許可済みobservationによる同じcertificateへbind済み`、`no_counterexample_found := bind済みproducer resultがTaskSpec-fixedな全review scopeと全manifest descriptorのsuccess receiptへ過不足・重複なくbind済み`、`review_unavailable := bind済みproducer resultが残るallowed dispositionを決めるため必須のnamed observationのmissing / unreadable / non-valueへbind済み`とする。open可能性、名称、より強いdesignの存在だけでは`projected_counterexample_established`または`counterexample_found`にせず、有効な`counterexample_found`は別scopeのmissing / unreadable / non-successによって失効させない。この三resultのいずれか一つが真正なbind済みproducer terminal resultとして成立した場合だけreview operationをterminalにする。

三result kindのpredicateを定義するが、判定順またはread順は定めない。

### 4.5 `EVIDENCE_GATE`への二つの局所変更

`evidence_consumer_ready`の定義直後へ次を追加する。

> `review_observation_consumer_ready(observation) := prechange_review_requirement_state=required ∧ bind済みreview producerがnonterminal ∧ projected_counterexample_established(packet)=false ∧ observationがTaskSpec-fixed manifest descriptorへbind済み ∧ requested resultが未解決のallowed review dispositionをbind可能 ∧ 同じrequired factをbindするmodel-visible inputまたはadmission済みresultがない`とし、reviewerのrepository evidence invocationもtrueの場合だけ発行する。

既存`implementation_bound`定義の末尾へ次のdependencyを加える。

> `∧ TaskSpecがartifact変更前review contractを明示した場合は(prechange_review_requirement_state=not_required ∨ bind済みreview terminal result=no_counterexample_found)`

これにより、`counterexample_found`は現designのartifact変更を開かず、`review_unavailable`またはpermission否定も変更許可を作らない。既存のconsumer terminal後の未発行evidence失効と局所invalidationは変更しない。

### 4.6 `INDEPENDENCE`後への`REVIEW_BOUNDARY`追加

本文案:

> - REVIEW_BOUNDARY: TaskSpecがartifact変更前の独立review contractと判定対象boundary record集合を固定した場合、`prechange_review_required(boundary) := general designがrequired outcome充足の前提としてboundaryへ依存 ∧ closure_source=autonomous_exploration ∧ TaskSpecまたは先行repository authorityによるdirect closureなし ∧ required validation coverage=non_exhaustive ∧ counterexampleがrequired validationを通過可能 ∧ counterexample effectがgeneral design change`とする。`prechange_review_requirement_state := supplied集合の一件以上でprechange_review_required=trueならrequired | supplied集合の全design dependencyがdirect authority closure / exhaustive required validation / implementation-local counterexample effectへbind済みならnot_required | TaskSpec-requiredなsupplied valueのmissing / non-value / conflictによりいずれもbind不能ならunavailable`とする。permission、producer identity、criterion owner、変更規模またはreview capabilityだけでは`required`を成立させない。このstateは既存`PRODUCER / CONTEXT / EVIDENCE_GATE / TERMINAL / implementation_bound`が消費するpredicate resultであり、独立operation、tool invocationまたはmodel-step barrierを作らない。

配置はC147の`INDEPENDENCE`直後、`DECISION_BOUNDARY`直前とする。review operation自体の独立identityは既存`INDEPENDENCE`、そのresultが後続へ与える効果は既存`DECISION_BOUNDARY`が所有する。

## 5. 追加文監査

| 追加・置換 | 消す保存済み誤経路・判断点 | 接続先 | 新たに増える判断点 | 手順化判定 |
| --- | --- | --- | --- | --- |
| `producer_execution_required` | ADR01/02の不要review、ADR08 permission否定後review、owner語列のproducer昇格 | `PRODUCER / OWNER_ROLE` | 明示producer operationについてapplicabilityとpermissionを一度bind | 境界。順序・toolなし |
| review packet membership | ADR06 forbidden canary配送、forbidden source全体再読、root予想の流入 | `CONTEXT / ROOT` | 許可membershipと禁止membership | 境界。packet作成recipeなし |
| descriptor / observation ownership | ADR09 reviewer起動前停止 | `CONTEXT / TERMINAL` | descriptor readinessと観測resultを分ける一判断 | 境界。target確認を起動前手順にしない |
| 三review terminal | 具体的反例のmissingによる失効、ADR07 valid result汚染、過剰`unavailable` | `TERMINAL / OWNER_ROLE` | result kindごとの必要evidence | 境界。優先順を定めない |
| `projected_counterexample_established`と`review_observation_consumer_ready` | projected certificate成立前のpaired-scope先読み | `TERMINAL / EVIDENCE_GATE` | packetだけでcertificateが成立するか、requested observationが残るresultを変えるか | 境界。先行operation、receipt、read回数・順序を定めない |
| review dependency付き`implementation_bound` | review未完了、counterexample、permission否定後のartifact変更 | `EVIDENCE_GATE`内の既存変更許可 | review適用時だけadmissible terminalを一件確認 | result effect。別change lifecycleなし |
| `REVIEW_BOUNDARY` | C147のreview要否不安定、closed boundaryの不要review、open boundaryのreview省略 | `PRODUCER`以下の既存群 | supplied boundary集合からrequirement stateを一度bind | predicate。operation / tool / stepを作らない |

### 手順化禁止の監査結果

- 台帳の作成・拡張: なし。TaskSpec-supplied集合だけを読む。
- 「全件分類してから次へ進む」operation: なし。requirement stateはproducer発行資格が消費するpredicate resultである。
- packet作成・配送workflow: なし。membershipとownershipだけを定める。
- 「counterexampleを先に判定し、その後read」: なし。packet上のcertificate成立をdirect-read eligibilityの否定条件として同じpredicateへ入れ、先行operationまたはreceiptを作らない。
- revision loop: なし。
- review責務によるmodel-step分割: なし。C147 `DECISION_BOUNDARY`を変更しない。
- 同一evidence再取得禁止: なし。`admitted_evidence_current`を含めない。

したがって本文案の静的判定は`draft_boundary_connected / procedural_review_lifecycle_not_included / pretrace_falsification_passed_after_revision`である。これは評価run上の機序通過を意味しない。

## 6. 今回の停止位置

C207再構成計画の実施順1〜3は完了した。後続の実施順4も別記録で完了し、Candidate bundle作成前のblocking counterexampleは0件となった。Candidate bundle、評価profileおよび評価runはこの文書自体では作成しない。

## 一次参照

- [C207再構成・検証計画](candidate207-c147-review-boundary-recomposition-plan.md)
- [C206 review制御コスト・記述構造分析](candidate206-review-control-cost-representation-analysis.md)
- [C147制御群の重複・最適性監査](c147-control-group-overlap-optimality-audit.md)
- [prompt制御設計原則](prompt-control-design-principles.md)
- [ADR9 r2 set](../evaluations/sets/the-caption-preimplementation-adversarial-design-review-r2/README.md)
- [C147 ADR9 r2 N=50](../evaluations/results/candidate147-result-effect-scope-adr9-r2-n50_2026-08-10.md)
- [C173 ADR9 r2 N=50](../evaluations/results/candidate173-concrete-counterexample-adjudication-adr9-r2-n50_2026-08-10.md)
- [C175 ADR9・Standard14 N=5](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)
- [C191 Standard14 cost機序再判定](../evaluations/results/candidate191-standard14-cost-mechanism-reassessment-r1.json)
