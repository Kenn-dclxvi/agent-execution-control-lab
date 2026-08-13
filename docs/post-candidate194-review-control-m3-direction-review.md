# Candidate194停止後のreview制御M3方向review

> **位置づけ**: M2再設計に対するroot producerの方向review／具体的反例だけを対象／独立producerなし／新規run 0件

## 結論

[M2初稿](post-candidate194-review-control-m2-redesign.md)には、target、methodまたはstop conditionを変えるblocking counterexampleが4件あった。いずれもM2へ戻して同じ4実行票の内部を修正した。

1. predecessorが停止stateを返すと、後続ticketが永遠にnonterminalになる
2. 同じmutable targetを持つready ticketを同時発行できる
3. requested resultの全fieldを原理的に返せないmethodを候補にできる
4. wrapper内部chunk identityをreviewerが再構成する限り、観測identity誤対応が再発する

修正版では、`suppressed_by_predecessor`、`conflict_keys`、method output schemaによるeligibility、`observation_batch_identity / ledger_receipt_identity`を追加した。22状態の再確認で未解決blocking counterexampleは0件となった。

M3は`passed_after_revision`とする。これは設計方向の成立を示すだけであり、prompt artifactの実装一致、挙動拘束、評価成功、採用、releaseまたはprojectionを意味しない。次に許可されるのは、C147を直接親としてM2修正版を新しいCandidate artifactへ実装するM4だけである。Candidate identity、文面、profileおよび評価slotはまだ作成していない。

## review contract

| 項目 | 固定値 |
|---|---|
| operation identity | `post-candidate194-review-control-m3-direction-review` |
| producer | root |
| criterion | M2の4実行票を一般入力で成立不能にし、target、permission、methodまたはstop conditionの変更を必要とする具体的反例があるか |
| pass condition | 確認状態が修正版27責任から一意に導出でき、未解決blocking counterexampleが0件 |
| allowed input | C147原文、Candidate194 M1原因分析、M2再設計、保存済みCandidate194 trace、model-visible Standard14・ADR9 TaskSpec、既存方向reviewの具体的反例 |
| forbidden input | private oracleの追加入力化、Candidate194のその場修正、新しいcase・rating・評価系列、repository外runtime変更 |
| independent producer | TaskSpecが要求していないため起動しない |

reviewは表現改善、一般的な完全性要求、prompt量、条項数または将来の全入力列挙を目的にしない。具体的状態が誤った発行、producer、result、変更またはterminalを許す場合だけblocking counterexampleとする。

## 初稿で成立したblocking counterexample

### M3-01: rejected predecessorによるterminal deadlock

初稿の`operation_ready`は全incoming edgeの`satisfied`を要求した。しかし開始identityが`mismatch`を返した場合、後続readのedgeは永遠にsatisfiedにならず、後続operationもouter taskもnonterminalのまま残る。

これは安全に発行しないことだけでは解けない。TaskSpecが「不一致なら停止」としたconditional operationを、未発行のままrequired operationとして残さないcontrol terminalが必要である。

修正ではedgeを`satisfied | rejected | pending`へ分け、停止stateを返したedgeのconsumerを`suppressed_by_predecessor`にする。このstateはproducer resultを代行せず、conditional operationが発行対象外になったことだけを表す。outer terminalはactive operationのterminal resultとsuppressed conditional operationを区別して集約する。

### M3-02: readyだが競合するchangeの同時発行

predecessor relationがない二つのchange ticketが同じartifactまたは同じproducerを消費する場合、初稿の「相互非依存なready ticketを全件発行」だけでは、両者を独立と誤判定して同じresponseから発行できた。

修正ではticketへ`conflict_keys`を追加し、同一mutable target、同一producerの分離不能operation、共有validation subject等を同時発行禁止にした。independenceはpredecessor不在だけでなく、conflict key不一致と相互result effectなしを全件要求する。競合ticketは固定順で一件ずつ発行し、各result後に残りのvalidityを再判定する。

### M3-03: result contractを満たせないmethod候補

初稿は`git status`がHEADだけを返した後に別methodを選べるため、Candidate194の早期`unavailable`を防げた。しかし、HEAD三値tupleを原理的に返せないmethodを最初から候補にでき、candidate setの作り方次第では不適合methodを反復できた。

修正では、methodの既知output schemaがrequested result contractの全required fieldを返し得ることをeligibility条件にした。ADR9開始identityではHEADしか返さない`git status`は候補外である。全fieldを返し得るeligible methodが実際には一部fieldしか返さなかった場合だけ`does_not_bind_requested_result`を使う。candidate setと順序は最初のattempt前に有限固定する。

### M3-04: wrapper内部identityの再転記

初稿はatom identityを`wrapper result identity + observation_identity`としたが、wrapper result identity自体がreviewerから安定して参照できなければ、Candidate194の誤chunk転記を別形式で繰り返す。

修正では発行前に`observation_batch_identity`を固定し、wrapper result contractへ同じbatch identity、観測key別の個別result、structured exit、payloadおよびmapping全体から機械生成する`ledger_receipt_identity`を要求した。reviewer final resultはbatch identity、ledger receipt identity、消費observation identityとcertificateだけを返し、内部chunk identityを再構成しない。

## 修正版の状態確認

| # | 具体的状態 | 修正版からの導出 | 判定 |
|---:|---|---|---|
| 1 | required outcome未固定で開始identityにconsumerなし | 実装ticketをactiveにせず、別clarification ticketだけを発行 | 反例不成立 |
| 2 | driftがchangeだけを禁止しreadを変えない | read ticketにidentity edgeを作らず同時発行 | 反例不成立 |
| 3 | driftが全後続operationを禁止 | 全後続ticketへmatched edgeを作りidentityだけを先行 | 反例不成立 |
| 4 | identityがmismatch | 後続ticketを`suppressed_by_predecessor`にし、発行せずouter stopへ集約 | 反例不成立 |
| 5 | method schemaがrequired fieldの一部しか返せない | `method_eligible=false`で試行しない | 反例不成立 |
| 6 | eligible methodの実resultだけがfield不足 | `does_not_bind_requested_result`で同じoperationを継続 | 反例不成立 |
| 7 | eligible methodが環境理由でfailed | permission denialへ変換せず、固定candidate setの次methodまたはRECOVERYへ進む | 反例不成立 |
| 8 | 相互非依存な二つのread ticket | conflict keyなし、相互effectなしなら同一responseから個別発行 | 反例不成立 |
| 9 | 同じmutable artifactへの二つのchange ticket | conflict key一致により固定順で逐次発行 | 反例不成立 |
| 10 | predecessorとconsumerを一つのcompound commandへ入れる | consumer edge未充足のため同一response・wrapper・shell後半へ入れられない | 反例不成立 |
| 11 | 依頼自体がroot producerのprimary review | 独立review controlは`not_applicable` | 反例不成立 |
| 12 | authorityがtarget、effect、relation、constraintを直接閉じる | finite closure certificate成立、独立reviewなし | 反例不成立 |
| 13 | authorityがopenで追加探索が必要 | certificate不成立、明示review contractがあれば`required` | 反例不成立 |
| 14 | review execution permission denied | packet、producer、spawnを作らず外側admissionへpermission resultを渡す | 反例不成立 |
| 15 | packet targetは固定済みだが現在missingの可能性あり | packetはready、reviewerが観測してledger atomを`missing`にする | 反例不成立 |
| 16 | observation batchの全atomがvalue | machine-generated ledger receiptから`no_counterexample_found`を形成可能 | 反例不成立 |
| 17 | counterexampleに不要な一atomだけmapping欠落 | 欠落atomだけterminal failure。成立済みcounterexample certificateを失効させない | 反例不成立 |
| 18 | no-counterexampleに必要な一atomがmapping欠落 | 全manifest value条件を満たさずreview resultは`unavailable` | 反例不成立 |
| 19 | reviewer finalのledger receipt identityが不一致 | rootは意味を補完せずcurrent resultを拒否 | 反例不成立 |
| 20 | admissibleなsaved prior resultがある | prior result専用permissionとvalidityを確認し、新規review permissionを追加要求しない | 反例不成立 |
| 21 | 発行済みticketがcell ID付きnonterminal resultを返す | 同じcell IDへのwait以外を発行しない | 反例不成立 |
| 22 | change後のrequired validation | validation ticketの全result受領までoperationとouter taskをterminalにしない | 反例不成立 |

## result invalidationの再確認

predecessor resultがconsumer発行前に失効した場合、edgeは`pending`へ戻りconsumerを発行しない。consumer invocation中にpredecessor resultが失効した場合、そのconsumer resultはcurrent ticketへadmitしない。consumerがterminalになった後にdependency atomが変わった場合、terminal operationを再開せず旧resultを失効し、TaskSpecが許す場合だけ新operation identity、ticket、producer bindingおよびedgeを作る。

この規則はM2の`PREDECESSOR_EDGE`へ追記対象とする。失効を同一operationの暗黙rerun、root補完または全taskの一括失効へ変換しない。

## 残余リスクと次の検証predicate

M3で反例なしとしたことはpromptが挙動を一意に実行する証拠ではない。実装後の評価では少なくとも次を独立した機構predicateにする。

- unsatisfied predecessor edgeを越えたtool call 0件
- same-response、custom wrapper、compound command内のpredecessor越境0件
- method schema不適合候補の実行0件
- `does_not_bind_requested_result`から外側terminalへの直接昇格0件
- finite closure certificate成立時の不要review 0件
- open boundaryで必要なreview未起動0件
- observation batchとledger receiptの一意対応100%
- ledger atom mapping欠落からのunsafe `no_counterexample_found` 0件
- conflict key一致ticketの同時発行0件
- suppressed ticketをproducer success／failureとして数えるrun 0件
- dangerous artifact change 0件
- forbidden canary delivery 0件

これらは既存quality oracleを置換しない。case、fixture、rating contractも変更せず、prompt identity以外の互換条件を固定した比較前receiptが`ready`になった場合だけrunを発行する。

## M3完了判定

初稿のblocking counterexample 4件はM2内で修正され、修正版22状態に未解決blocking counterexampleはない。新しいoperation class、producer role、review result kind、評価caseまたはruntime機構は追加していない。

次に許可されるのは、C147を直接親とし、修正版27責任を一つの新Candidate prompt artifactへ実装するM4である。Candidate194の本文を変更せず、Candidate191からC193またはCandidate194を親にしない。実装後も静的検証と評価準備を別gateにする。

`M3_passed_after_revision / initial_blocking_counterexamples_4 / unresolved_blocking_counterexamples_0 / reviewed_states_22 / c147_direct_parent_retained / next_candidate_not_created / profile_not_created / evaluation_not_started`
