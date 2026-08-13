# Candidate215 packet source region closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundle作成前の設計記録である。Candidate214を親にせず、Candidate147へpacket construction receiptとsource region conflictを追加する。Candidate214は保存resultとtraceだけを反証入力にする。

## 結論

Candidate215で閉じるのは、packetへ実際に使ったregionを別selectorまたは包含regionとして再読する辺である。同時に、Candidate214が誤って閉じた同一container内の未投影・非重複regionへの必要readを回復する。

```text
packetへ使用したsource region
  -> 同一 / 祖先 / 子孫 / 重複regionをreviewerが再read

同じcontainer内の未投影・非重複region
  -/-> container一致だけで一律禁止
```

source名、field名、case名または命題の意味対応は使わない。receiptとrequested targetに固定されたcontainer identityとregion identityの構造関係だけでpermissionを決める。

## 直接baseと保存trace

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。

Candidate214 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 41 / 4`。
- Candidate213に残ったpacket投影元source再read6回は0回になった。
- root reviewer-owned target prereadは1回から0回になった。
- ADR07とADR09の必要paired observationは各5 / 5で維持した。
- ADR03 iteration 3、ADR05 iteration 1と4、ADR06 iteration 2では、同じfile内の未投影inventory regionまで閉じ、期待`blocked`に対して`unavailable`となった。
- 3件は必要inventory regionを読めず、別containerのmissing paired targetを代替観測した。1件はreadなしで停止した。

Candidate214の成功時tool順や判断順は継承しない。成立した境界と失敗したpermission edgeだけを使う。

## 保存traceで観測した誤経路

Candidate214のconflictは次の論理だった。

```text
target.container ∈ closed_container_set
  -> regionが非重複でもconflict
  -> current inventory membershipを観測不能
  -> counterexample_foundをbind不能
  -> unavailable
```

packetへ投影したregionと、必要なinventory / contract regionは同じfile内だが構造的に非重複だった。container全体の禁止は不要readだけでなく必要readも到達不能にした。

## Promptが制御を置く正しい層である理由

rootはpacket itemを作る時点で、入力resultに固定されたrepository containerとselector / region identityを保持できる。reviewerはmanifest targetからrequested container / region identityを選ぶ。

両regionの同一、祖先、子孫、重複、非重複は内容の意味を判断せず照合できる。regionが一方でも固定されない場合は、非重複を証明できないためcontainer単位の保守的閉鎖へfallbackする。この制御はpromptのevidence permission境界で成立し、executor変更を要求しない。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、rootがadmission済みinputからpacketを構築し、実際に使ったsource regionをreceiptへ固定し、reviewerがpacketだけでterminal supportを得るか、未確定命題を直接bindできる非重複regionだけを観測してterminal resultを返す経路である。

### 2. 保存traceへbindした具体的誤経路

- Candidate214で4 / 45 runが期待`blocked`から`unavailable`へ退行した。
- 4件とも具体的反例のcurrent inventory membershipが未確定だった。
- 必要regionはpacket sourceと同じcontainer内だがpacketへ投影されていなかった。
- container全体の閉鎖により必要regionへ到達できなかった。

### 3. 既存境界で防げない理由

Candidate147にはprechange review region境界がない。Candidate214のexact container membershipは、regionの非重複をpermissionへ反映しない。TaskSpecのallowed readだけでは、投影済みregionの不要再読と未投影regionの必要readを分けられない。

### 4. 変更するpredicateと責務境界

```text
packet_construction_receipt(item) :=
  packet item identity
  / literal admitted value
  / input result identity
  / repository source container identity if repository-backed
  / source region identity if structurally fixed
  / provenance

review_read_conflicts(target) :=
  同じcontainerのreceiptが存在
  and (
    receipt.regionまたはtarget.regionが未固定
    or receipt.regionとtarget.regionが同一 / 祖先 / 子孫 / 重複
  )

review_evidence_consumer_ready(observation) :=
  producer nonterminal
  and review_read_conflicts=false
  and terminal support未成立
  and requested resultが現在未確定の具体的命題をbind可能
  and requested resultの異なる値が残るallowed dispositionを分け得る
```

責務境界は次のとおりとする。

- receiptは実際に構築したpacket itemだけへbindする。
- input resultがcanonical selector / regionを固定していれば、そのregion identityを省略またはcontainerへ拡張しない。
- source regionを推測しない。固定不能なpacket itemはcontainer fallbackへbindする。
- target regionが固定されないwhole-container readは、同じcontainerのreceipt regionを包含するためconflictとする。
- 同じcontainerでも双方のregionが固定され非重複なら、container一致だけでは禁止しない。
- 非重複regionもdisposition-changing consumerが成立する場合だけreadできる。
- manifest membership、allowed readまたは将来の候補からreceiptを作らない。
- packet constructionのために新規repository evidenceを開かない。
- producer result admissionと対応変更effectは別責任として維持する。

### 5. 消す判断点と到達可能辺

container一律閉鎖をregion conflictへ置換し、同じfileという理由だけで必要regionを禁止する判断点を消す。

region overlap閉鎖は、packet投影元を別selector、親selector、子selectorまたは部分抽出として取り直す辺を残さない。

region未知fallbackは、region identity欠落を非重複と推測してcontainer内readを開く辺を閉じる。この三点は同じ構造identity permissionの完全な分岐であり、分離すると必要readの過剰閉鎖または不要readの再開が残る。

### 6. 新たに増える判断点、参照、例外

追加する判断は、同一container内で双方のregionが固定されているか、そのregionが重なるかの二点である。

意味、scope ownership、期待terminal、case固有pathによる例外は追加しない。非重複regionを一律許可せず、既存のterminal disposition effect predicateを維持する。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- Candidate214の4件で、必要な同一container内・非重複regionを観測し`counterexample_found`へ到達可能にする。
- packet投影元region再readは0件を維持する。
- root prereadは0件を維持する。
- ADR07 / ADR09の必要paired observationを各5 / 5で維持する。
- tool順、判断順またはmodel step順は固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- packet投影元regionと同一・祖先・子孫・重複するreviewer readが一件でもある。
- Candidate214で誤停止した経路に同じ必要region遮断が一件でも残る。
- region未知の同一container readが一件でも許可される。
- root prereadが一件でもある。
- ADR07 / ADR09の必要paired observationまたは期待terminalが一件でも欠ける。
- reviewer cardinality、result admissionまたはeffectが一件でも一致しない。

必要routeと不要routeのpermission分離が目的なのでzero-toleranceとする。有効な低品質runを自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- source名やregion名から意味を推定しない。
- 成功runのtool順または判断順を規定しない。
- fixed regionがあるreceiptをcontainer全体へ拡張しない。
- non-overlapを証明できない場合だけcontainer fallbackを使う。
- 未投影・非重複regionもterminal effectがある場合だけ開く。

## 現時点の判断

作成前gateの全項目を固定し、方向監査を通過したためCandidate147直接baseのbundleを作成した。効果は未評価であり、ADR9 r2 N=5の事前固定gateで判定する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate214 ADR9結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate214機序監査](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
