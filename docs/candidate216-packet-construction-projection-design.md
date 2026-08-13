# Candidate216 packet construction projection 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundle作成前の設計記録である。Candidate215を親にせず、Candidate147へpacket construction時の構造projection receiptを追加する。Candidate215は保存resultとtraceだけを反証入力にする。

## 結論

Candidate216で閉じるのは、repository readのselectorがcontainer全体だった場合に、packetへ実際に選んだ部分regionがreceiptへ残らず、review permissionがrunごとに揺れる辺である。

```text
admission済み構造object
  -> packet itemへliteralに選択したstructural projection
  -> construction時にexact source regionをreceiptへ固定

repository read時のselectorなし
  -/-> packet source region不明と即断
```

field名、case名、命題名または値の意味対応は使わない。受領済み構造object内の位置と、packet itemへ実際に採用したliteral data dependencyだけを使う。

## 直接baseと保存trace

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。

Candidate215 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 41 / 4`。
- packet投影regionの重複またはwhole-container readとroot先読みは各0件だった。
- 同じcontainer内の必要非重複region readは13回、9 runで成立した。
- ADR03の1件とADR05の2件は必要regionへ到達せず、期待`blocked`から`unavailable`へ外れた。
- ADR07の1件はpaired targetを観測したが、packetにないinventory / contractへ到達できず期待`completion_ready`から`unavailable`へ外れた。
- ADR07 / ADR09では不要な非重複region readが7回、4 runに残った。
- 実runのrootは`design-admission.json`全体をadmitした後、その構造objectの一部をpacketへ選んだ。元のread resultにcanonical selectorがないため、Candidate215の`source_region_structurally_fixed`はconstruction時の選択をreceiptへ固定できなかった。

Candidate215の成功時tool順、判断順またはread順は継承しない。成立した非重複region routeと、projection identityが欠けてpermissionが揺れた反例だけを使う。

## Promptが制御を置く正しい層である理由

rootはpacket itemを構築する主体であり、admission済み入力objectのどの構造部分をliteral itemへ採用したかを、その構築時点で直接保持できる。repository toolがselectorを返したかとは独立している。

このprojectionは、入力objectのcanonical path、選択範囲、配列要素または部分木として表せる。複数originの結合、意味変換、要約または出所不明で一意なpathを固定できない場合だけcontainer fallbackへ戻す。runtime hookやexecutor変更は必要なく、prompt内のpacket construction責務とreview read permissionの境界で制御できる。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、rootがadmission済みinputからpacket itemを構築する同じ操作でliteral data dependencyのexact structural regionをreceiptへ固定し、reviewerがpacketだけでterminal supportを得るか、投影regionと重ならずterminal dispositionを直接分けるregionだけを観測してterminal resultを返す経路である。

### 2. 保存traceへbindした具体的誤経路

Candidate215では元のrepository readがcontainer全体だったため、packet construction時に選んだ部分regionがreceiptへ一貫して固定されなかった。その結果、同じ条件で必要regionを読むroute、必要regionを閉じるroute、paired targetへ逸れるroute、不要regionまで読むrouteが併存した。品質4件、機序9件が事前gateから外れた。

### 3. 既存境界で防げない理由

Candidate147にはpacket source closureがない。Candidate215の保存traceで使った境界はinput result自身がcanonical selectorを直接bindすることを要求し、container全体のresultからpacket itemを選ぶconstruction operationをsource region identityの生成点として扱わない。TaskSpecのallowed readやmanifestだけでは、実際にpacketへ採用した部分を確定できない。

### 4. 変更するpredicateと責務境界

```text
packet_projection_region(item, admitted_input) :=
  item構築時にliteral data dependencyとして選択した
  admitted_input内のexact structural path / range / subtree集合

packet_construction_receipt(item) :=
  packet item identity
  / literal admitted value
  / input result identity
  / repository source container identity
  / packet_projection_region if uniquely materialized
  / provenance

review_read_conflicts(target) :=
  同じcontainerのreceiptが存在
  and (
    receipt projectionまたはtarget regionが未固定
    or 両regionが同一 / 祖先 / 子孫 / 重複
  )
```

責務境界は次のとおりとする。

- projection receiptはpacket itemを構築する同じoperationでだけ生成する。
- source read時のselectorがなくても、admission済み構造objectからliteralに選択したpathが一意ならmaterializeする。
- value equality、field名、意味、別sourceの類似値または後続推測からprojectionを作らない。
- 複数origin、要約、変換または一意でない出所はregionを推測せずcontainer fallbackへbindする。
- 一意なprojectionを固定した後に省略またはcontainer全体へ拡張しない。
- target regionとの構造的重なりだけをconflictにし、固定非重複regionは既存のdisposition-effect consumerが成立する場合だけ許可する。
- packet constructionのために新規repository evidenceを開かず、manifest targetを先読みしない。
- producer result admissionと対応変更effectは別責任として維持する。

### 5. 消す判断点と到達可能辺

この置換は、source tool resultにselectorがないという理由だけでcontainer fallbackへ進む判断点を消す。packet構築時の実際のprojectionをreceiptへ固定するため、同じ入力からreceipt粒度がrunごとに揺れる辺を閉じる。

同時に、projectionと重なる再readは閉じ、固定非重複regionをcontainer一致だけで禁止しない。projection materialization、曖昧時fallback、overlap conflictは一つのprovenance permission分岐であり、分離すると不要read再開または必要read遮断のどちらかが残る。

### 6. 新たに増える判断点、参照、例外

追加する判断は、packet itemのliteral data dependencyがadmission済み構造object内の一意なregionへ投影可能かどうかだけである。一意なら固定し、不明ならfallbackする。意味分類、case固有例外、期待terminal、tool順は追加しない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- ADR03からADR06ではpacket projectionと非重複の必要inventory / contract regionだけを到達可能にする。
- packet projectionと重なるreadおよびwhole-container readは0件を維持する。
- ADR07 / ADR09ではpaired targetだけの必要routeを各5 / 5へ戻し、不要なdesign-container region readを0件にする。
- root prereadを0件に維持する。
- tool順、判断順、model step順または具体的selectorを固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- packet projectionと同一・祖先・子孫・重複するreadまたはwhole-container readが一件でもある。
- ADR03からADR06で必要な非重複regionが遮断され期待terminalから外れるrunが一件でもある。
- ADR07 / ADR09でpaired target以外のrepository regionを読むrunが一件でもある。
- 曖昧なprojectionを意味またはvalue equalityから推測したreceiptが一件でもある。
- root preread、reviewer cardinality、result admissionまたはeffectが一件でも不一致になる。

必要routeと不要routeの構造分離が目的なのでzero-toleranceとする。有効な低品質runを除外または自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- 成功runのtool順、read順または判断順を規定しない。
- construction時のliteral structural dependencyだけをprojection identityにする。
- 一意でないprojectionを推測せずcontainer fallbackへ戻す。
- 固定後のprojectionをcontainer全体へ拡張しない。
- 非重複regionもterminal dispositionを分ける場合だけ開く。

## 現時点の判断

作成前gateの全項目を固定し、方向監査を通過したためCandidate147直接baseのbundleを作成した。効果は未評価であり、ADR9 r2 N=5の事前固定gateで判定する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate215 ADR9結果](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate215機序監査](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
