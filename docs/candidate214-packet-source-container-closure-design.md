# Candidate214 packet source container closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundleを作る前の設計記録である。Candidate200、Candidate202またはCandidate213を親にせず、Candidate147へpacket construction receiptとsource container包含閉鎖を加える。

## 結論

Candidate214で閉じるのは次の二つの到達可能辺である。

```text
packet source container
  -> 同じcontainerのfield / JSON pointer / 部分抽出を別target identityとしてreviewerがread

finite manifestに存在する未投影source
  -> packet construction sourceへ昇格してrootがreviewer起動前にread
```

packetの値、field名、scope名またはcase名を意味対応させない。packet itemを実際に構築した時点のsource container identityだけをconstruction receiptへ固定し、reviewer read targetのcontainerが一致するか、regionが同一・子孫・祖先または重複する場合にpermissionを否定する。

manifest membershipはpacket construction sourceを作らない。rootが既にadmission済みのTaskSpec inputまたはrepository resultから実際にpacket itemを作った場合だけreceiptを作る。packet作成のための新規repository readは開かない。

## 直接baseと保存traceの扱い

直接baseはCandidate147の次の本文とする。

- `../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt`

Candidate200、Candidate202、Candidate213は保存resultとtraceだけを設計入力にする。

- Candidate200は起動したreviewer 16 / 16でclosed source read 0、mixed read 0を達成したが、required reviewer欠落14 / 30、Score 4は30 / 45だった。
- Candidate202はreviewer cardinality、routing、projection receipt acknowledgement、result admission / effectを各30 / 30または45 / 45で成立させたが、packet反例20件のうち9件で不要な別source readを残した。
- Candidate213はpacket反例readなしを9 / 20から17 / 20へ増やし、投影元source再readを22回から6回へ減らしたが、同じrepository fileのfield targetを別identityとして6回読んだ。
- Candidate213 ADR06の1件では、rootが未投影のmissing paired sourceをpacket readinessの必須sourceへ昇格してreviewerを起動しなかった。
- Candidate213 ADR07の1件では、reviewerが必要paired sourceの代わりにpacket投影元inventoryを再読し、rootがresultをadmitせず停止した。

Candidate200 / Candidate202のprompt本文、routing table、projection-first順序またはcase固有対応は継承しない。

## 保存traceで観測した誤経路

### container fragment escape

Candidate213 ADR05の2 runでは、reviewerはclosed sourceを再読しないと宣言しながら、packetへ値を供給したrepository fileのinventory fieldとcontract fieldを別々の`jq` invocationで読んだ。ADR06とADR07でも同じfile内のinventory fieldを一件ずつ読んだ。

```text
closed source identity = repository file
  -> requested target identity = file内field
  -> exact identityが異なると再解釈
  -> fieldだけをread
```

source containerの構造的包含を見れば、値の意味を判断せず全件をconflictへbindできる。

### manifest-to-packet promotion

Candidate213 ADR06の1 runでは、rootがpacket値を供給していないpaired sourceを、finite manifestに存在するためpacket readinessに必要と解釈した。missingを観測してreviewerを起動せず、期待`blocked`を`unavailable`へ退行させた。

```text
manifest targetあり
  -> packet construction sourceと再分類
  -> rootが起動前read
  -> missing
  -> reviewer非起動
```

packet construction receiptを実際にpacket itemを作ったoperationへだけbindすれば、この昇格は成立しない。

## Promptが制御を置く正しい層である理由

rootはpacket itemを構築する時点で、使用したadmission済みinput resultと、そのrepository container identityを観測できる。reviewerもread発行前にtarget container identityを選んでいる。

必要な照合は文字列または構造identityの同一・包含・重複であり、fieldの意味、期待resultまたはscope ownershipを推定しない。したがってpromptのpermission境界で制御できる。

container identityまたはregion relationをmodel-visibleに固定できない場合は、promptで強制できないためCandidateを作らない。この設計ではTaskSpec-fixed manifest targetとrootが実行済みresultから保持するrepository path / selectorを使用し、executor変更を要求しない。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setは`the-caption-3ce91a4-result-effect-scope-r1`とする。

最短正常経路は、rootが既にadmission済みのTaskSpec inputとrepository resultからreview packetを構築し、各packet itemへconstruction receiptを付け、reviewerがpacketとclosed containerに重ならない必要観測だけからterminal resultを返す経路である。

### 2. 保存traceへbindした具体的誤経路

- Candidate213でpacket投影元sourceのfield readが6回残った。
- packet反例20 runのうち3 runが合計5回のrepository readを発行した。
- Candidate213 ADR06の1 runでrootが未投影paired sourceを起動前にreadし、reviewerを欠落させた。
- Candidate213 ADR07の1 runで必要paired sourceをpacket投影元inventoryで代替した。

### 3. 既存境界で防げない理由

Candidate213は`target identity ∈ review_packet_closed_source_set`というexact membershipを使った。repository fileとそのfield / JSON pointerを異なるtarget identityへ分ける余地があり、container内readを禁止できなかった。

また`packetへsemantic valueを供給した全TaskSpec input identityとrepository source identity`というtotalityは、実際にpacket itemを供給していないmanifest targetまでsource identityへ昇格できた。

### 4. 変更するpredicateと責務境界

```text
packet_construction_receipt(item) :=
  packet item identity
  / literal admitted value
  / input result identity
  / repository source container identity if repository-backed
  / source region identity if fixed
  / provenance

review_closed_container_set :=
  packet_construction_receiptに現れるrepository source container identityのexact集合

review_read_conflicts(target) :=
  target.container identity ∈ review_closed_container_set
  or target.regionとreceipt.source regionが同一 / 子孫 / 祖先 / 重複

review_evidence_consumer_ready(observation) :=
  review producerがnonterminal
  and review_read_conflicts(observation.target)=false
  and terminal support未成立
  and requested resultが未確定命題をbind可能
  and requested resultの異なる値が残るallowed dispositionを分け得る
```

責務境界は次のとおりとする。

- packet construction自体はrepository evidence consumerを開かない。
- receiptは実際に作成したpacket itemへだけ一件作り、manifest membership、allowed readまたは将来必要かもしれない値から作らない。
- repository-backed itemのcontainer identityが欠けるpacketは配送しない。
- rootはreviewerが直接観測する未投影targetをpacket receipt作成のためにreadしない。
- reviewerはclosed containerのfield選択、JSON pointer、hash、存在確認、部分抽出または別commandを発行できない。
- closed containerと許可targetを同一invocationへ混ぜた場合はinvocation全体をinadmissibleにする。
- closed containerに重ならない未投影sourceは、disposition-changing consumerがある場合だけreadできる。
- producer result admissionと対応変更へのeffectは別責任として維持する。

### 5. 各変更が消す判断点と到達可能辺

construction receipt限定は、manifest targetをpacket sourceへ昇格する判断点を消す。

container / region conflictは、fileとfieldを別命題または別target identityとして再分類し、closed sourceの一部だけを読む辺を消す。

consumer predicateは、必要な未投影paired sourceを保持しながら、packet terminal support成立後の追加readを閉じる。

receipt生成、container閉鎖、残存read consumerは同一の入力permission構造であり、別Candidateへ分けるとsource totalityの過剰停止またはfragment escapeのどちらかが残るため分離しない。

### 6. 新たに増える判断点、参照、例外

増える直接照合は、packet itemのsource container identityと、read targetのcontainer / region relationだけである。sourceの意味、field-to-proposition対応、scope-to-source対応または期待terminal分類は追加しない。

closed containerへの例外は置かない。packet constructionのための新規readも例外にしない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectをreview-required 30 / 30で一致

### 8. 想定する実行routeの変化

- Candidate213で残ったpacket投影元source再read 6回を0回にする。
- ADR03からADR06のpacket-counterexample repository readを0 / 20にする。
- rootのreviewer-owned target prereadを0 / 30にする。
- ADR07 / ADR09のclosed containerと重ならない必要paired observationを各5 / 5で保持する。
- tool順、判断順またはmodel step順は固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validが45 / 45でない。
- Score 4が45 / 45でない。
- reviewerがclosed source containerまたはその一部を一件でもreadする。
- ADR03からADR06でrepository readが一件でも発行される。
- rootがreviewer-owned未投影targetを一件でも起動前にreadする。
- ADR07 / ADR09で必要paired observationまたは期待terminalが一件でも欠ける。
- packet receiptが実際のpacket item以外から作られる、またはrepository-backed itemのcontainer identityが欠ける。
- reviewer cardinality、review result admissionまたはeffectが一件でも一致しない。

対象はpermissionの到達不能化であり、同じfragment escapeまたはmanifest promotionが一件でも残れば境界未成立なのでzero-toleranceとする。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- source名またはfield名から意味を推定しない。
- 成功runのtool順または判断順を規定しない。
- construction receiptを実際に作ったpacket itemへだけbindする。
- source containerとread targetの構造関係だけでpermissionを閉じる。
- 未投影の必要source経路を閉じない。

## 現時点の判断

作成前gateの全項目は固定できた。Candidate213の失敗6 readとroot preread 1件へ、model-visibleなcontainer / region relationとconstruction receipt限定を直接適用できる。

次に方向監査で、packet-counterexample、必要paired success、必要paired non-value、permission deniedおよびreview不要の正常経路を確認する。通過した場合だけCandidate147直接baseのbundleを作成する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate200 ADR9結果](../evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate202 ADR9結果](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5_2026-08-13.md)
- [Candidate213 ADR9結果](../evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
