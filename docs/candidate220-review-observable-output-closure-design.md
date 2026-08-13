# Candidate220 review observable output closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

## 結論

Candidate220で閉じるのは、repository sourceの利用目的を一つのconsumerへ説明できれば、tool resultがそのconsumerに不要なvalueまで返してもよいとする辺である。

```text
source availability
  != consumer admission
  != observable tool output closure

発行可能 :=
  tool resultとしてmodelへ返り得る全valueが、
  一つのnonterminal predicateのproducerへ許可され、
  そのpredicateを分け得る
```

Candidate219のticket概念は継承しない。Candidate147を直接baseとし、artifact変更前reviewに関係するrepository invocationの「目的」ではなく、toolから各producerへ実際に配送され得るobservable outputを発行境界にする。

## 保存traceから固定する反証

Candidate219 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 41 / 4`。
- ADR03からADR06の20 / 20 runでrootがdesign container全体またはreviewer用valueを含むprojectionを取得した。
- rootは最初のreadを「model-visibleな固定入力からreview必要条件、permission、packet readinessを確認する」と説明し、start identityと同一stepでwhole-container outputを受領した。
- 13 / 20 runでreviewerも同じcurrent valueを直接観測した。
- review obligationが空のADR01 / ADR02で9 / 10 runにreviewerを起動した。
- ADR03 / ADR04 / ADR06の4 runは必要reviewer observationまたはterminal supportを失い、期待`blocked`に対して`unavailable`となった。
- ADR09のpaired-only routeは4 / 5、paired caseのdesign projection再readは4回で、observable outputを限定する合法route自体は到達可能だった。

成功時のcommand、selector、read順または判断順は継承しない。source availabilityをresult admissionと同一視できたこと、abstract ticketが実際のtool output shapeへ接続されなかったこと、および一般review命題が空work itemでもreviewerを開いたことだけを使う。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、TaskSpec literalだけからreview permission、独立producer identity、packet permissionとrequired predicate instanceを固定し、packetで未充足かつ独立producerにしかbindできないpredicate instanceが残る場合だけreviewerを起動することである。rootとreviewerのrepository invocationは、それぞれのmodel-visible resultへ配送され得る全valueが同producerの未観測predicateへ閉じる場合だけ発行する。

### 2. 保存traceへbindした具体的誤経路

Candidate219のrootは「design sourceはmodel-visibleな固定入力」というTaskSpec記述から、container全体をroot routing用inputと扱った。Candidate本文はconsumer-bound projectionを要求したが、rootはrequestの目的全体をrouting predicateへ結びつけ、command stdoutにreviewer用current valueが含まれる事実を別に判定しなかった。

別経路では、required scope instanceが空でもtask-levelのdesign admission命題をnonemptyなreview propositionと解釈し、reviewerを起動した。

### 3. 既存境界で防げない理由

Candidate147の`EVIDENCE_GATE`はrequested resultがpredicate stateをbind可能かを問うが、同じresultに不要valueが同梱されることを禁止しない。Candidate219はticketへrequested result projectionを加えたが、source、commandの目的、observable resultの全valueを分離せず、model自身の「このreadはrouting用」という分類でwhole outputをadmitできた。

`review_required := nonempty proposition`も、predicate instance集合と一般review目的を区別しなかった。

### 4. 置換するpredicateと責務境界

```text
review_work_item :=
  TaskSpecが独立producerのresultをrequiredとするpredicate instance
  ∧ state=unobserved
  ∧ TaskSpec literalまたはpacketだけではbind不能
  ∧ allowed direct observationの異なるvalueがallowed terminalを分け得る

observable_output_closed(invocation) :=
  invocationのtool resultとしてproducer modelへ配送され得る全valueが
  同producerのbind済みnonterminal predicate instanceへ許可され、
  少なくとも一つのstateをbind可能
```

責務境界は次のとおりとする。

- sourceがfixed、model-visible、allowed pathまたはread permittedであることは、observable output admissionを意味しない。
- invocationの内部processがcontainerをparseしても、modelへ返るresultが閉じていればよい。特定tool、selectorまたはcommandを固定しない。
- observable resultがwhole container、別producer用value、別predicate用valueまたはforbidden inputを含み得る場合は発行しない。受領後に無視、非admission、要約またはpacket非配送として補わない。
- rootはpacket配送可valueをobservable outputへ限定できる場合だけ取得できる。
- reviewerは同reviewerの未観測work itemを分け得るfinite observationだけを取得できる。packetで充足済みのvalueを再取得しない。
- `review_work_item`集合が空ならreviewerを起動しない。review contract、一般review目的、permission、manifestまたはallowed readの存在をwork itemにしない。
- 同producerの複数work itemへ必要なvalueだけを一つのresultで共同取得するrouteを保持する。
- terminal support成立後は同producerの残りwork itemを失効し、別terminalだけのmissingを伝播しない。
- observable outputを限定できないがrequired work itemが残る場合は、whole-output fallbackを使わず対応reviewを`unavailable`にする。

### 5. 消す判断点と到達可能辺

requestを発行した後でresult内valueのconsumerを分類する判断点を消す。source availabilityやrequest目的からwhole outputをadmitする辺、root resultからreviewer用valueを後で除外する辺、rootとreviewerが同じvalueを二重消費する辺を閉じる。

reviewer startを残存work item集合へ接続するため、一般review目的だけからproducerを起動する辺も閉じる。

### 6. 新たに増える判断点、参照、例外

増える判断は、invocationのobservable resultに含まれ得るvalue集合が一つのproducerの未観測predicate集合へ閉じているかだけである。source内部の全field ownership、case対応表または命名規則は増やさない。

同producerに必要な複数valueの共同outputは許可する。sourceが同じであることだけを理由にcontainer全体を返す例外は置かない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- ADR01 / ADR02のreviewer起動を0 / 10にする。
- ADR03からADR06のroot mixed-owner observable resultを0 / 20にする。
- ADR03からADR06の必要reviewer observationと期待terminalを20 / 20にする。
- ADR07 / ADR09はpaired targetだけのreviewer routeを各5 / 5にする。
- packet-carried projection再read、forbidden output、manifest外readを各0件にする。

tool call数、特定commandまたはmodel step数はgateにしない。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- rootのobservable resultへreviewer用またはforbidden valueが一件でも返る。
- 同じcurrent valueをrootとreviewerが二重消費するrunが一件でもある。
- empty work itemまたはpermission deniedでreviewerを起動するrunが一件でもある。
- ADR03からADR06の期待terminalが20 / 20でない。
- ADR07 / ADR09でpaired target以外のreviewer observable resultを受領するrunが一件でもある。
- terminal support後のmissingがresultを変えるrunが一件でもある。
- reviewer cardinality、result admission / effect、artifact boundary、required commandまたはforbidden inputが一件でも不一致になる。

有効な低品質runを除外または自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- Candidate219の`REVIEW_EVIDENCE_ADMISSION`を継承しない。
- case、field、scope、observation、期待terminalまたは具体的selectorを記載しない。
- source availabilityとobservable result admissionを分離する。
- reviewer startを残存`review_work_item`集合のnonempty性へbindする。
- requestの目的ではなくmodelへ返る全valueを発行前に閉じる。
- 成功時のtool順、read順、判断順またはpacket文面を規定しない。

## 現時点の判断

作成前gateの9項目と方向監査を固定し、blocking counterexampleがないことを確認した。Candidate147直接baseのCandidate220 bundleを作成した。評価はまだ開始していない。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate219 ADR9結果](../evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5_2026-08-14.md)
- [Candidate219機序監査](../evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
