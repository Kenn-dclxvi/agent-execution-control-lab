# Candidate194停止後のreview制御M2再設計

> **位置づけ**: C147直接基盤のM2成果物／Candidate194の4原因を正の実行契約へ変換／次Candidate未作成／新規run 0件

## 結論

Candidate194の失敗は、24責任の名称不足ではなく、責任間で受け渡すresultとready条件が操作可能な形になっていなかったことにある。M2ではCandidate194へ条項を追記せず、C147から次の4つの実行票を再構成する。

1. operationとpredecessorを結ぶ`operation ticket`
2. method invocationとrequested result成立を分ける`method receipt`
3. finite closureを正のfield集合で立証する`finite closure certificate`
4. reviewerの実観測resultを機械的対応のまま保持する`observation ledger`

発行制御は、C192の`DISPATCH_ADMISSION`やC193の`DISPATCH_TRANSITION`のようなtask全体の抽象gateへ戻さない。各tool invocationは一つのoperation ticketへbindし、そのticketの全predecessor edgeが充足した場合だけ現在responseへ出せる。ready集合の判定と実発行を別の自由記述へ分けず、現在responseのtool-call identity集合そのものをticket集合へ照合する。

C147の安全停止、単一producer、root非代行、情報封鎖、局所失効、validation closureは保持する。Candidate194で成立した危険変更0件、canary配送0件、真正command exit欠落0件も保持条件とする。

## 設計境界

この文書で行うことは、M1で確定した4原因を一般的な制御契約へ変換することである。行わないことは次のとおりである。

- Candidate194本文またはdescriptorの変更
- Candidate195その他の次Candidate identityの作成
- case、fixture、oracle、rating contractまたはprofileの変更
- repository外executor、tool adapter、runtime hookによる強制
- 評価run、M6、Standard14、採用、releaseまたはprojection

直接入力はC147原文、[Candidate194 M5原因分析](candidate194-m5-causal-analysis.md)、Candidate194の保存済み45件およびmodel-visible Standard14・ADR9 TaskSpecとする。C191からC193は反例と部分効果の診断証拠であり、prompt本文または直接親として使わない。

## 4つの実行票

### 1. operation ticket

各未発行operationへ次を実行前に固定する。

| field | 内容 |
|---|---|
| `operation_identity` | 他operationと共有しないidentity |
| `operation_class` | read、review、change、validation、clarification等の発行class |
| `producer_identity` | rootまたはTaskSpec明示の独立producer |
| `predicate_identity` | operationが判定する一つのpredicate |
| `requested_result_contract` | producerが返すresult kind、必要fieldおよびpass condition |
| `permission_source` | operationとmethodを許可するTaskSpecまたは適用authority |
| `incoming_edges` | 先行result identity、受入stateおよび失効atom |
| `conflict_keys` | 同時変更、同一producer、同一mutable target等、同時発行を禁止するresource identity |
| `terminal_contract` | operation固有のterminal result。外側terminalは含めない |

一つのpredecessor edgeは、次をすべて満たした場合だけ`edge_satisfied=true`となる。

```text
edge_satisfied :=
  actual_result.operation_identity == predecessor_operation_identity
  ∧ actual_result.contract_identity == predecessor_result_contract
  ∧ actual_result.terminal = true
  ∧ actual_result.state ∈ accepted_states
  ∧ result_still_valid = true
```

predecessor edgeは`satisfied | rejected | pending`の三状態を持つ。predecessor resultがterminalかつvalidで、受入stateなら`satisfied`、TaskSpec明示の停止stateなら`rejected`、result未受領、nonterminalまたは失効済みなら`pending`とする。

一つでも`rejected` edgeを持つ未発行ticketは、producer resultを捏造せず、control stateを`suppressed_by_predecessor`としてterminalにする。これはpredicateのsuccess、failureまたは`unavailable`ではなく、そのoperationがTaskSpec上の発行対象から外れたことだけを表す。`pending` edgeを持つticketはnonterminalかつ発行禁止である。

predecessor resultがconsumer発行前に失効した場合はedgeを`pending`へ戻す。consumer invocation中に失効した場合は受領したconsumer resultをadmitしない。consumer terminal後にdependency atomが変わった場合はterminal operationを再開せず旧resultを失効し、TaskSpecが許す場合だけ新operation identity、ticket、producer bindingおよびedgeを作る。

`operation_ready`は次で定義する。

```text
operation_ready :=
  operation_ticket_ready
  ∧ producer_bound
  ∧ permission_allowed
  ∧ every incoming edge is satisfied
  ∧ control state is active
  ∧ operation is nonterminal
  ∧ no invocation for the same operation is nonterminal
```

先行resultが同じmodel responseの別tool callとして予定されていても、そのresultはまだ実在しないためedgeを充足しない。したがって、そのresponse内の後続tool call、同じcustom wrapper内のcall、shell compound commandの後半へ後続operationを入れてはならない。

TaskSpecが限定停止を明示した場合は、停止対象classだけへedgeを作る。停止がreadを変えない場合、read ticketにedgeはなく、identity ticketと同時にreadyになれる。無限定停止なら全後続operationへedgeを作る。これによりStandard14の共同発行可能経路とADR9のidentity単独先行を、case名ではなくedgeの有無から導出する。

### 2. method receipt

methodはoperationでもevidenceでもなく、同じoperationのrequested resultを得るための実行手段である。各method attemptは次のいずれかを返す。

| state | 意味 | 効果 |
|---|---|---|
| `binds_requested_result` | result contractの全required fieldを真正な値へbindした | predicate判定へ渡す |
| `does_not_bind_requested_result` | invocationはterminalかつ成功したが、required fieldが不足 | operationをnonterminalのまま保ち、別methodを選ぶ |
| `invocation_failed` | methodがresultを返せなかった | permission内の別methodを選ぶ。必要ならRECOVERYへ渡す |
| `method_prohibited` | TaskSpecまたはauthorityがmethodを明示禁止 | 実行せず停止する。回避しない |

`does_not_bind_requested_result`を`missing evidence`、permission denial、predicate failureまたは外側`unavailable`へ昇格しない。methodの再選択は同じoperation、同じpredicate、同じrequested result contract内で行い、新しいrepository evidence operationを作らない。

別methodは、すでにmodel-visibleなTaskSpec、適用instruction、利用可能toolとmethod inventoryから選ぶ。選択のためだけにrepository readを追加しない。`method_eligible := permission内 ∧ 明示禁止なし ∧ methodの既知output schemaがrequested result contractの全required fieldを返し得る`とする。全fieldを原理的に返せないmethodを試行候補にしない。eligibleなmethodが複数ある場合は実行前に有限なcandidate setと固定順序へbindし、未試行methodがある間はoperationをterminalにしない。明示methodが一つに固定されている場合、そのmethodのterminal failureはTaskSpecのterminal contractに従う。

ADR9の開始identityではrequested resultを`HEAD / HEAD^ / HEAD^^`の三値tupleとする。既知output schemaがHEADしか持たない`git status`はこのoperationのeligible methodではない。もし選択時には全fieldを返し得ると判断したmethodが実resultでは一部fieldしか返さなかった場合だけ`does_not_bind_requested_result`とし、固定candidate setの次methodへ進む。現在HEADが得られたことだけでidentity operationまたは依頼全体を`unavailable`にしない。

### 3. finite closure certificate

独立reviewの要否より先に、現在のimplementation predicateが先行authorityへ有限かつ直接一致するかを正のcertificateで判定する。

`finite_closure_certificate_ready=true`には次の全fieldを要求する。

1. `authority_identity`: 現在design operationより前に固定された一意なauthority
2. `complete_target_set`: authorityが全targetを明示列挙し、完全集合であると直接固定
3. `complete_effect_map`: 各targetのend stateまたはtransformを全件固定
4. `complete_relation_set`: artifact間relationを全件固定
5. `preservation_constraints`: 非変更fieldと保持constraintを全件固定
6. `implementation_exact_match`: 現在変更predicateが上記target、effect、relation、constraintと過不足なく一致
7. `exhaustive_validation_coverage`: 固定集合全件を検証できる既存predicateがある
8. `no_open_selection`: 追加探索、fallback、normalization、選択または除外が不要

一fieldでも`non-value`または不一致ならcertificateは成立しない。rootは「一般にnon-machine riskがある」「review contractが存在する」「複数artifactである」という語列からcertificateを否定しない。逆に、open authorityや探索依存を現在inventoryの有限性だけで閉包しない。

review controlが適用され、certificateが成立すれば`review_requirement=not_required`、成立しなければ`required`とする。review control自体が非適用の通常operationまたはprimary review taskでは`not_applicable`とする。

### 4. observation ledger

review packet作成時に、各観測を次のidentityへ固定する。

```text
observation_spec :=
  observation_identity
  + target_identity
  + predicate_identity
  + producer_identity
  + invocation_result_contract_identity
  + allowed terminal states
```

観測tool resultを受領した時点で、自由文のreview judgementより先にledger atomを作る。

```text
ledger_atom :=
  observation_identity
  + machine_returned_invocation_identity
  + result_contract_identity
  + structured exit status
  + terminal state
  + value or non-value payload
```

個別tool callではmachine-returned identityをそのまま使う。複数観測を一つのcustom wrapperから同時発行する場合は、発行前に`observation_batch_identity`とwrapper result contractを固定する。wrapperは同じbatch identity、`observation_identity -> individual result`の一対一mapping、各individual resultのexit statusとpayload、およびmapping全体から機械生成した`ledger_receipt_identity`を一つのterminal resultとして返さなければならない。atom identityは`ledger_receipt_identity + observation_identity`とし、内部chunk identityまたはwrapper表示順をreviewerが手作業で付け替えない。

wrapper全体のexit 0、別atomの成功、reviewerの「観測済み」という宣言からatomを`value`へ昇格しない。mapping欠落、重複key、別targetのpayloadまたはresult contract不一致は、そのatomだけを`terminal_failure`にする。

`REVIEW_JUDGEMENT`は固定ledgerだけを消費する。`counterexample_found`はcertificateが実際に使うvalue atomだけへ依存する。`no_counterexample_found`は固定manifest全atomがauthenticなvalueの場合だけ成立する。reviewer final resultはledgerを自由文で再構成せず、`observation_batch_identity`、`ledger_receipt_identity`、消費したobservation identity集合、result kindおよびcertificateだけを返す。rootは同じbatch identityへbindされたproducer resultとの一致だけを機械照合し、内部chunk identityを再構成しない。

## 発行とterminalの一意な所有

### issuance

現在responseへtool callを一件でも出す前に、全nonterminal operation ticketについて`operation_ready`を判定する。発行対象はready ticketだけであり、実tool-call identityを各ticketへ一対一bindする。

次を禁止する。

- incoming edgeが未充足のticketを、predecessor tool callと同じresponseへ入れる
- 異なるoperationを一つのshell compound commandへまとめる
- readyで相互非依存なticketの一部だけを便宜的に次responseへ送る
- 一つのtool callを複数operationのresultとして使う。ただし事前固定した個別result contract付きwrapperは除く
- nonterminal cell IDがある間にwait以外のoperationを発行する

`tickets_independent := predecessor relationなし ∧ conflict_keys共通要素なし ∧ 一方のresultが他方のtarget / permission / method / stop condition / result contract / 発行可否を変えない`とする。相互非依存なready ticketは同じmodel responseから個別tool callとして全件発行する。readyでもconflict keyが重なるticketは同時発行せず、TaskSpec順、なければticket identityの固定順で一件だけ発行し、result受領後に次ticketのedgeとvalidityを再判定する。同時発行上限が固定されている場合もticket identityの固定順で上限分を発行する。発行後は当該集合の全resultがterminalになるまで新しい判断を行わない。

### operation terminal

operationは、requested result contractを満たすbind済みproducer resultがあり、そのresult stateがoperation固有terminal contractへ一致する場合だけterminalになる。

`method receipt=does_not_bind_requested_result`、未充足edge、未発行review、ledger atom identity不一致、validation途中はoperation terminalではない。review resultの`unavailable`はreview operationのterminalになり得るが、開始identity methodの不適合をreview unavailableへ変換しない。

### outer terminal

依頼全体は、TaskSpecがrequiredとしたactive operationがterminalで、conditional operationがterminal resultを持つか`suppressed_by_predecessor`であり、pending edgeがなく、各result kindを外側terminal contractへbindできる場合だけterminalになる。

- `completion_ready`: 必要changeとvalidationのsuccess resultが全件存在
- `blocked`: admissibleなcounterexample certificateが存在
- `unavailable`: 必要reviewのadmissible `unavailable`、permission denial、packet unavailable等、TaskSpecが定めた不足resultが存在
- `clarification_required`: 別clarification operationのterminal resultがTaskSpecのsingle outcomeになる

最終文字列が期待と一致するだけでは、欠けたrequired operation resultを補完しない。ADR09でreviewを起動せずrootが`unavailable`と述べても、review operationのresultが欠けているためouter terminal contractは未充足である。

## 再構成する責任

責任数は設計目標にせず、上記4実行票のownerを重複させない結果として次の27責任へ再配置する。

1. `TASK_SPEC`
2. `OPERATION_TICKET`
3. `PREDECESSOR_EDGE`
4. `PRODUCER_BINDING`
5. `PRODUCER_RESULT`
6. `OWNER_ROLE`
7. `ROOT`
8. `WORKER_CONTEXT`
9. `METHOD_SELECTION`
10. `METHOD_RESULT`
11. `RECOVERY`
12. `EVIDENCE_ADMISSION`
13. `ISSUANCE`
14. `IMPLEMENTATION_BINDING`
15. `FINITE_CLOSURE_CERTIFICATE`
16. `REVIEW_REQUIREMENT`
17. `PRIOR_REVIEW_RESULT_ADMISSION`
18. `REVIEW_EXECUTION_PERMISSION`
19. `REVIEW_PACKET`
20. `OBSERVATION_LEDGER`
21. `REVIEW_JUDGEMENT`
22. `CURRENT_REVIEW_RESULT_ADMISSION`
23. `CHANGE_ADMISSION`
24. `VALIDATION_PLAN`
25. `VALIDATION_CLOSURE`
26. `OPERATION_TERMINAL`
27. `OUTER_TERMINAL`

`OPERATION_TICKET`はoperationの正本、`PREDECESSOR_EDGE`はresult dependencyと局所失効の正本、`ISSUANCE`は現在responseのtool-call集合の正本とする。`METHOD_RESULT`だけがmethod attemptを同じoperation内で継続させ、`EVIDENCE_ADMISSION`は新しい観測targetを持つrepository evidence operationだけを扱う。finite closureの成立は`FINITE_CLOSURE_CERTIFICATE`だけが所有し、reviewerの観測真正性は`OBSERVATION_LEDGER`だけが所有する。

## Candidate194の24責任からの移行

| Candidate194責任 | 扱い | M2移行先 |
|---|---|---|
| `OPERATION_SPEC` | 分割 | `TASK_SPEC`、`OPERATION_TICKET` |
| `RESULT_DEPENDENCY` | 置換 | `PREDECESSOR_EDGE` |
| `DECISION_BOUNDARY` | 置換 | edgeに基づく`ISSUANCE`。抽象frontierは作らない |
| `METHOD` | 分割 | `METHOD_SELECTION`、`METHOD_RESULT` |
| `EVIDENCE_ADMISSION` | 縮小 | 新しい観測targetのoperation admissionだけを所有 |
| `IMPLEMENTATION_BINDING` | 保持・限定 | target、effect、relation、constraintの一変更predicate形成 |
| `REVIEW_REQUIREMENT` | 分割 | `FINITE_CLOSURE_CERTIFICATE`、`REVIEW_REQUIREMENT` |
| `OBSERVATION_RESULT` | 置換 | tool result受領時に作る`OBSERVATION_LEDGER` |
| `REVIEW_JUDGEMENT` | 改訂 | ledger receiptだけを入力にする |
| `CURRENT_REVIEW_RESULT_ADMISSION` | 保持 | rootはidentityとcertificateを機械照合し、意味を補完しない |
| producer、owner、root、context | 保持 | C147の単一producerとroot非代行を維持 |
| prior result、permission、packet、change | 保持 | result class、permission、情報封鎖、安全停止を維持 |
| validation、terminal | 保持・強化 | method不適合と未充足edgeをterminalから除外 |

Candidate194のprompt本文は履歴artifactとして変更しない。次Candidateを作る場合もCandidate194を親にせず、C147からこの移行表を実装する。

## 一般経路への適用

### ADR9型の無限定開始停止

1. `start_identity` ticketだけがincoming edgeなしでreadyになる。
2. `design_read`、review、change、validationの全ticketは、`start_identity=matched`だけを受け入れるedgeを持つ。
3. 最初のresponseにはidentity tool callだけを発行する。
4. methodがHEAD tupleをbindしなければ同じidentity operation内でmethodを再選択する。
5. matched resultを受領した後に初めてdesign readをreadyにする。

### Standard14型の限定停止

drift resultがchangeとrequired validationだけを禁止し、read target、permission、methodを変えない場合、read ticketにはidentity edgeを作らない。identity ticketとread ticketは同時にreadyとなり、同じresponseから個別発行する。drift result受領前のchange ticketにはedgeがあるため発行しない。

### finite closure

先行authorityが全target、effect、relation、constraintを閉じ、現在implementation predicateが直接一致する場合、finite closure certificateを形成し、独立reviewなしでchange admissionへ進む。review contractやnon-machine riskの語列だけでreviewを追加しない。

### open boundary review

finite closure certificateが不成立で、TaskSpecが独立review operation、criterion、allowed result kind、consumerおよびindependenceを固定している場合だけreviewをrequiredにする。packetとobservation specを起動前に固定し、reviewerはledger receiptからjudgementを作る。

### 観測identity不一致

一atomのmappingが欠けた場合、そのatomは`terminal_failure`となる。counterexample certificateがそのatomを使わなければ成立済みcounterexampleは保持できる。`no_counterexample_found`が全manifestを必要とする場合は成立せず、reviewerは`unavailable`を返す。rootは誤った`no_counterexample_found`を引き続き拒否する。

## M2完了判定

4原因はそれぞれ、別の正本とresult contractへbindされた。

| M1原因 | M2の正本 | 競合owner |
|---|---|---|
| 開始dependency越境 | `PREDECESSOR_EDGE`と`ISSUANCE` | なし |
| method早期terminal化 | `METHOD_RESULT` | なし |
| finite closure誤分類 | `FINITE_CLOSURE_CERTIFICATE` | なし |
| 観測identity誤対応 | `OBSERVATION_LEDGER` | なし |

各terminalはCandidate名や期待terminalを参照せず、operation ticket、edge、method receipt、certificate、ledgerおよびproducer resultから導出できる。evidence発行、method再選択、観測真正性、dependency、失効、operation terminalおよびouter terminalも別ownerへ分かれている。

M2は`complete_after_candidate194`とする。後続の[M3方向review](post-candidate194-review-control-m3-direction-review.md)では初稿へ4件のblocking counterexampleが成立したため、`suppressed_by_predecessor`、`conflict_keys`、method eligibilityおよびmachine-generated ledger receiptを本書へ反映した。修正版22状態の再確認では未解決blocking counterexampleが0件となった。次に許可されるのはM4の新Candidate prompt artifact実装であり、profile作成および評価slot発行はまだ許可しない。

`M2_complete_after_candidate194 / c147_direct_parent_retained / operation_ticket_fixed / predecessor_edge_fixed / method_receipt_fixed / finite_closure_certificate_fixed / observation_ledger_fixed / responsibilities_27 / M3_passed_after_revision / candidate_not_created / evaluation_not_started`
