# Candidate213 packet provenance review closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundleを作る前の設計記録である。Candidate212を親にせず、Candidate147へreview packetのsource閉鎖境界を加える。

## 結論

Candidate213で閉じるのは、reviewerへsemantic valueを投影したrepository sourceを、同じreviewerが「packetでは命題が未確定」と再分類して読み直せる経路である。

packet値の意味とrepository field名を対応させない。reviewer起動前に、packetを構成するために使用したsource identityの集合をそのまま`review_packet_closed_source_set`へ固定し、その集合へのreviewer readを無条件に禁止する。

## 直接baseと保存traceの扱い

直接baseはCandidate147の次の本文とする。

- `../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt`

Candidate210、Candidate211、Candidate212は直接baseではない。保存resultとtraceだけを反例または正常経路の証拠として使用する。

- Candidate212は45 / 45 Score 4、review result admission / effect 30 / 30で、外側の品質経路を維持した。
- packet-counterexample 20件ではreadなしが9件、11件が合計17回のrepository readを発行した。
- 17回のうち15回はpacket投影元sourceの再read、2回はpaired-scope sourceのreadだった。
- ADR03のreadなしrunはpacketの`consumer-d`をcurrent memberとしてterminal supportへbindした。
- 同じcaseのreadありrunは、同じpacketからcurrent membershipを未確定へ戻し、投影元inventoryを読み直した。
- ADR04は5 / 5でpacketだけから`counterexample_found`を返し、repository readは0件だった。
- ADR07とADR09はpaired-scope observation自体を各5 / 5で必要とした。

Candidate212の本文を継承せず、品質を維持したresult admission / effect責任と、失敗した再分類経路を設計入力として扱う。

## 保存traceで観測した誤経路

Candidate212 ADR03の失敗runは次の判断を行った。

```text
packetにconsumer-dのcontract値あり
  -> current inventory instanceかは未確定と再分類
  -> packet投影元のinventory sourceをread
  -> consumer-dの所属を再取得
  -> packetだけで成立していた同じcounterexample_foundを返す
```

ADR05では5 / 5でpacket投影元を読み直し、inventory、consumer contracts、場合によってpaired-scopeまで取得した。全件のterminal resultは`counterexample_found`であり、投影元readの異なる結果は最終kindを変えなかった。

閉じる辺は次である。

```text
packet semantic valueのsource identity
  -> reviewer repository read targetとして再選択
```

この辺は、packet値がどの命題を意味するかとは独立している。sourceがpacket構築に使用されたという実行時の直接観測だけで閉じられる。

## Promptが制御を置く正しい層である理由

rootはreviewer packetを構築する時点で、どのTaskSpec inputまたはrepository sourceからsemantic valueを投影したかを観測できる。reviewerもpacketに固定されたsource identity集合を受け取れる。

read発行前にtarget identityが閉鎖集合へ属するかは、fieldの意味、case identity、scope名または期待resultを推定せず判定できる。したがってpromptでpermissionを閉じられる。executor、tool adapterまたはtarget runtimeの変更は不要である。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setは`the-caption-3ce91a4-result-effect-scope-r1`とする。

最短正常経路は、TaskSpecが独立reviewを要求する場合に、rootが許可済みsemantic valueとそのprovenanceからpacketを一度構築し、reviewerがpacketと未投影の必要観測だけでterminal resultを返し、rootが対応変更へ局所的にeffectを適用する経路である。

### 2. 保存traceへbindした具体的誤経路

- ADR03でpacket投影元inventoryを3回再読した。
- ADR05でpacket投影元inventory / consumer contractsを9回再読した。
- ADR06でpacket投影元を3回再読した。
- ADR07 / ADR09でも、必要なpaired observationに加えてpacket投影元を7回再読した。

同じ再読機序はCandidate212全体で22回、packet-counterexample内で15回観測した。

### 3. 既存境界で防げない理由

Candidate212はpacket valueをcurrent evidenceとして扱い、同じfactのdirect sourceが存在するだけでは`unobserved`へ戻さないとした。しかし「同じfact」かどうかをreviewerが意味判断できたため、packetのcontract値とcurrent inventory membershipを別命題へ分け、source再readを合法化できた。

source identityの閉鎖はfact同一性を判断しない。packet構築に使用済みのsourceであることだけでreviewer permissionを否定する。

### 4. 変更するpredicateと責務境界

Candidate213で追加する分離不能な境界は次の一組である。

```text
review_packet_source_ready :=
  reviewer起動前
  and packetへsemantic valueを供給した全TaskSpec input / repository source identityが固定済み

review_packet_closed_source_set :=
  packetへsemantic valueを供給したrepository source identityのexact集合

review_source_read_forbidden(target) :=
  target identity ∈ review_packet_closed_source_set

review_evidence_consumer_ready(observation) :=
  review producerがnonterminal
  and observation.target ∉ review_packet_closed_source_set
  and packetまたはadmission済み観測でterminal kindがまだsupportされていない
  and requested resultの異なる値が残るallowed dispositionを分け得る
```

責務境界は次のとおりとする。

- rootはpacket構築時にsource identity集合を固定し、reviewerへ渡す。
- source identity集合の欠落時はreviewerを起動せず、集合を推測または拡張しない。
- reviewerは閉鎖sourceを、別命題、直接確認、provenance確認、より強い証拠または念のためという理由で読めない。
- 未投影sourceは、terminal resultを変え得る未確定観測のtargetである場合だけreadできる。
- packetにterminal supportが成立した後は、未投影sourceのreadも失効する。
- producer resultのadmissionと対応変更へのeffectは、Candidate212で全件成立した責務を維持する。

### 5. 各変更が消す判断点と到達可能辺

`review_packet_source_ready`は、reviewer起動後にpacketのprovenance sourceを再構成する判断を消す。

`review_packet_closed_source_set`と`review_source_read_forbidden`は、packet valueとrequested propositionが同じfactかを判断してsource readを許可する辺を消す。

`review_evidence_consumer_ready`は、未投影sourceへの必要readを保持しながら、packet terminal support成立後のpaired readを閉じる。

三つは同じpacket input closureの生成、permission、残存read consumerであり、別Candidateへ分けると、閉鎖集合を作っても消費されない状態、またはread predicateが参照する集合がない状態になるため分離しない。

### 6. 新たに増える判断点、参照、例外

新しい意味判断は追加しない。増える直接照合は、read target identityが固定済みclosed source setへ含まれるかの一件である。

新しいcase分類、field-to-proposition対応、scope-to-source対応、tool順または成功runの判断順は追加しない。閉鎖sourceへの例外は置かない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectをreview-required 30 / 30で一致

### 8. 想定する実行routeの変化

- packet投影元source再readは22回から0回になる。
- ADR03からADR06のpacket-counterexample repository readは0 / 20になる。
- ADR07 / ADR09の未投影paired-scope observationは各5 / 5で維持する。
- root preread、reviewer数、required command、result admissionおよびeffectは変更しない。
- tool順またはmodel step順は固定しない。

### 9. 停止条件

次のいずれか一件で停止する。

- validが45 / 45でない。
- Score 4が45 / 45でない。
- reviewerがpacket投影元sourceを一件でもreadする。
- ADR03からADR06でrepository readが一件でも発行される。
- ADR07 / ADR09で必要paired-scope observationまたは期待terminalが一件でも欠ける。
- closed source集合の欠落、reviewerによる再構成または拡張が一件でもある。
- reviewer cardinality、review result admissionまたはeffectが一件でも一致しない。

zero-toleranceとする理由は、対象が平均的なread削減ではなく、packet構築済みsourceへのreviewer permissionの閉鎖だからである。一件の再readは、同じ再分類辺が到達可能なままであることを示す。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- packet valueの意味からproposition名を作らない。
- 成功runのtool順または判断順を規定しない。
- closed source集合をpacket構築時のsource identityだけから固定する。
- 未投影の必要source経路を閉じない。

## 現時点の判断

作成前gateの全項目は固定できた。変更対象は、Candidate212で22回観測したpacket source再read permissionへ限定され、source identity membershipというmodel-visible値から直接判定できる。

次に方向監査で、packet-counterexample、必要paired success、必要paired non-value、permission deniedおよびreview不要の正常経路を確認する。通過した場合だけCandidate147直接baseのbundleを作成する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate212 ADR9結果](../evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5_2026-08-13.md)
- [Candidate212機序監査](../evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
