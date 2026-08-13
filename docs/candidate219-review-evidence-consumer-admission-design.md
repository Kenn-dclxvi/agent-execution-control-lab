# Candidate219 review evidence consumer admission 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundle作成前に固定した設計記録である。Candidate218を親にせず、Candidate147の一般`EVIDENCE_GATE`とartifact変更前reviewの接続を、一つのconsumer-bound evidence admissionとして再構成した。Candidate218は保存resultとtraceだけを反証入力にした。

## 結論

Candidate219で閉じるのは、review inputのownerを宣言した後も、一般`EVIDENCE_GATE`からowner境界を越えるrepository resultをrootまたはreviewerへ返せる辺である。

```text
未確定predicate
  -> consumer execution identity
  -> 欠けている観測値
  -> そのpredicateだけをbindするrequested result projection
  -> 許可source

上の実行票が揃う場合だけevidence invocationを発行
  -> result envelopeがconsumer外projectionを含み得るなら未発行
  -> consumer terminal時に残りを失効
```

case名、field名、scope名、期待terminal、具体的selectorまたは成功runのread順は使わない。TaskSpecが直接固定するreview obligation、packet permission、finite observation target、producer identityと、現在未確定のpredicate dependencyだけを使う。

## 直接baseと保存trace

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。

Candidate218 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 43 / 2`。
- ADR03からADR06の20 / 20 runで、rootがreviewer-owned current valueを含むrepository resultを取得した。
- 19 / 20 runでreviewerも同じ値を直接観測し、同一値の二重消費になった。
- reviewer finalから、packet配送禁止値のpacket deliveryを2 runで直接確認した。
- review不要なADR01 / ADR02でreviewerを7 run起動した。
- ADR07 / ADR09のpaired targetだけのrouteは2 / 5、1 / 5で、packet-carried design projectionのreviewer再readが17回だった。
- ADR04の2 runは具体的反例候補を構成できた後も、別scope observationのmissingを`unavailable`へ伝播した。

Candidate218の成功時tool順、selector、packet文面または判断順は継承しない。owner外projectionを含むinvocationがprompt上合法だったこと、空のreview obligationでもreviewer起動が合法だったこと、およびterminal support後も別kind用missingが結果を変えられたことだけを使う。

## Promptが制御を置く正しい層である理由

modelは各repository invocationの発行前に、TaskSpec、現在のpredicate state、producer identity、requested sourceおよび取得しようとするresult projectionを観測できる。したがって、consumer外の値を返し得るrequestを発行しないこと、空のreview obligationでproducerを起動しないこと、terminal support後の未発行requestを失効することはpromptで制御できる。

tool adapterが返却後に出力を削ることや外部wrapperでprojectionを強制する必要はない。model自身がconsumer-bound result shapeを持つcommandまたはread methodだけを選べる。exact projectionを表現できない場合はwhole-container fallbackを使わず、そのevidence requestを`unavailable`にする。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、まずrootがdesign admissionのroutingとpacket構築に必要なprojectionだけを取得することである。TaskSpec-fixed review obligationが空ならreview operationを作らず通常のartifact変更へ進む。obligationがありpermissionが許可されている場合だけ、packetで供給できない必要値を独立review producerがfinite allowed sourceから観測し、一つのterminal resultを返す。

### 2. 保存traceへbindした具体的誤経路

C218ではownerを四分類したが、rootはその分類前後に一般`EVIDENCE_GATE`の`target artifact`許可からcontainer全体を読めた。resultがroot modelへ返った後で「admitしない」と宣言しても、reviewer-owned current valueはすでにroot consumerへ流入していた。その後reviewerのdirect observationまたはpacket deliveryが重なった。

別経路では、required review obligationが空でもreview contractの存在だけでreviewerを起動した。また具体的反例がsupportされた後も、別dispositionだけに必要なmissing observationを全体の`unavailable`へ伝播した。

### 3. 既存境界で防げない理由

Candidate147の`EVIDENCE_GATE`はconsumer readinessを要求するが、requested resultのprojection境界とconsumer execution identityを一つの発行票へbindしない。`target artifact`または明示read-only pathであれば、未確定predicateに不要な値を同じresult envelopeへ含められる。

Candidate218はresult受領後のownership admissionを追加したが、invocation発行前のresult shapeを制限しなかった。reviewer起動条件も独立review contractの存在と、nonemptyなrequired review obligationを分離しなかった。

### 4. 置換するpredicateと責務境界

```text
review_required :=
  TaskSpec-fixed required review propositionまたはscope obligationがnonempty

review_evidence_ticket :=
  consumer execution identity
  + nonterminal required predicate
  + currently missing observation identity
  + requested result projection
  + allowed source identity

consumer_projection_closed(ticket) :=
  requested result envelopeの全value projectionが
  同ticketのpredicateをbindするためにconsumerへ許可済み
```

責務境界は次のとおりとする。

- review contract、permissionまたはmanifestが存在するだけでは`review_required=true`にしない。
- root用ticketはreview applicability、permission、packet permission、subject identity、packet-carried valueまたは通常実装predicateをbindするprojectionだけを許可する。
- packet配送禁止でreview propositionへ必要なcurrent valueはroot ticketへ入れず、bind済みreview producerのticketへだけ残す。
- reviewer用ticketは、現在未確定のrequired review propositionをbindし、残るallowed dispositionを分け得るfinite allowed observationだけを許可する。
- result envelopeが別consumer、別predicateまたはforbidden inputのprojectionを含み得るinvocationは発行しない。受領後の非admissionで補わない。
- 一つのinvocationが同じconsumerの複数predicateへ必要なprojectionだけを返すことは許可する。tool順、1 fieldずつのreadまたは具体的selectorを義務化しない。
- concrete `counterexample_found`、完全な`no_counterexample_found`または根拠ある`unavailable`のいずれかがsupportされた時点でreview consumerをterminalにし、別kindだけに必要な未発行ticketを失効する。
- missing / unreadable resultは、その観測値に依存するpredicateだけをunresolvedまたはunsatisfiedにし、すでにsupportされた別terminal kindを失効しない。
- ticket作成、projection確認、locator探索または一般的安全確認だけを目的に追加evidenceを発行しない。

### 5. 消す判断点と到達可能辺

この置換は、container resultを受領した後で各値のownerを振り分ける判断点を消す。invocation発行前にconsumerとresult projectionを一体化するため、rootへreviewer-owned値が流入する辺、同じ値を二consumerが消費する辺、packet配送禁止値をroot取得からpacketへ流す辺を閉じる。

同じ発行票がreviewer startと追加observationにも適用されるため、空obligationからreviewerを起動する辺と、terminal support後に別kind用missingを全体へ伝播する辺も消える。これらは「consumerへ未確定predicateをbindするresultだけを発行する」という同じ原因境界であり、別々の手順追加ではない。

### 6. 新たに増える判断点、参照、例外

増える判断は、requested result envelopeの全projectionが一つのconsumerの未確定predicate集合へ閉じているかだけである。C218の四つのowner stateとresult受領後の再分類は持ち込まない。

exact projectionを表現できない場合の`unavailable`は増えるが、whole-container fallbackでowner外値を読む例外は置かない。同じconsumerに必要な複数projectionの共同取得は保持する。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- ADR01 / ADR02のreviewer起動を0 / 10にする。
- ADR03からADR06のroot mixed-owner resultと二重消費を各0 / 20にする。
- ADR03からADR06の必要reviewer observationと期待terminalを20 / 20にする。
- ADR07 / ADR09はpaired targetだけのreviewer routeを各5 / 5にする。
- ADR04では具体的反例support後の別kind用missing伝播を0件にする。
- manifest外read、forbidden canary delivery、packet禁止値配送を各0件にする。

tool call数やmodel step数そのものを品質gateにしない。owner外read、二重消費、不要reviewerとterminal後readの減少に対応する方向だけを診断する。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- rootへreviewer-onlyまたはforbidden projectionを含むresultが一件でも返る。
- 同じcurrent valueをrootとreviewerが二重消費するrunが一件でもある。
- packet配送禁止値をpacketへ含めるrunが一件でもある。
- review obligationが空またはpermission deniedのときreviewerを起動するrunが一件でもある。
- required reviewer observationを失い、ADR03からADR06の期待terminalが20 / 20でなくなる。
- ADR07 / ADR09でpaired target以外のreviewer repository projectionを読むrunが一件でもある。
- terminal kindがsupportされた後、別kindだけに必要なmissing observationがresultを変えるrunが一件でもある。
- reviewer cardinality、result admission / effect、artifact boundary、required commandまたはforbidden inputが一件でも不一致になる。

owner外current valueの流入は受領後に取り消せず、独立producer境界と禁止配送を同時に破るためzero-toleranceとする。有効な低品質runを除外または自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- Candidate218の`REVIEW_INPUT_OWNERSHIP`を継承しない。
- case identity、固定path、field / scope / observation identityまたは期待dispositionを記載しない。
- 成功runのtool順、read順、具体的selectorまたはpacket文面を規定しない。
- review obligationのnonempty性をreviewer起動の必要条件にする。
- every evidence invocationをconsumer、未確定predicate、missing observation、requested result projection、allowed sourceへbindする。
- consumer外projectionを含み得るinvocationを発行前に閉じる。
- terminal support後の別kind専用ticketを失効する。

## 現時点の判断

作成前gateの9項目と方向監査を固定し、blocking counterexampleがないことを確認した。Candidate147直接baseのCandidate219 bundleを作成した。評価はまだ開始していない。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
- [Candidate218機序監査](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
