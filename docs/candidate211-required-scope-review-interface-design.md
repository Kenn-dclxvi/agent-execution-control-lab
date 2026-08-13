# Candidate211 必須scope消費review入出力境界 設計

## 状態

- `creation_gate_fixed`
- `candidate_not_created`
- `evaluation_not_started`
- direct base: `Candidate147`

この文書はCandidate bundleを作る前の設計記録である。Candidate211の本文、profile、評価slotはまだ作成しない。

## 目的

Candidate210で残った失敗を、reviewerの判断手順を増やすのではなく、失敗時に使われた入出力経路を到達不能にして閉じる。

閉じる対象は次の二つである。

1. manifestに含まれるという理由だけで、TaskSpecの必須review scopeを充足しないsourceまでrepository readへ進める入力経路
2. reviewの内部判定名や自由記述を、外部のterminal resultとして受理できる出力経路

Candidate211は、この二つを一つのreview入出力境界として再構成する。入力側では、reviewerへ渡す前にpacket projectionと直接観測の担当scopeを固定し、直接読めるtargetを閉集合にする。出力側では、外部へ返せるterminal resultをexact enumへ限定する。

## 直接baseと持ち込まないもの

直接baseは次のCandidate147本文だけとする。

- `../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt`

Candidate175、Candidate179、Candidate210は直接baseではない。そこから本文や状態機械を継承せず、次の観測だけを設計根拠として使う。

- Candidate175: packetから判定可能なsourceをreviewerの直接readへ重複追加しない境界は、ADR9で成立した。
- Candidate179: manifest全体を必要観測領域として扱うと、reviewerの判定責任が広がり、成立するreviewまで`unavailable`へ落ち得る。
- Candidate210: 品質は45/45で通過した一方、repository readが9/20のpacket-counterexample caseで発生し、review result admissionも3/30で不一致だった。

したがって、Candidate196以降の多値状態、receipt、evidence domain、certificate deficit、四状態frontierは持ち込まない。

## Candidate210で実際に残った失敗経路

Candidate210のADR9 N=5では、45/45 valid、45/45 Score 4だったが、mechanismは12/45で失敗した。

### 入力側

packetだけでcounterexampleを判定できる20件のうち9件でrepository readが発行された。

- 7件は、必須review scopeに`SCOPE-PAIRED`を含まないcaseで`OBS-PAIRED-SCOPE`を読んだ。
- 2件は、packetへprojection済みのinventoryまたはconsumer contractをsourceから再読した。

Candidate210は、descriptorがmanifestにあり、まだpacket値へbindされていなければ、`unobserved_direct`としてread frontierへ残した。この許可辺が、counterexampleをすでに判定できる場合にも到達可能だった。

### 出力側

review result 30件のうち3件で、外部result admissionが一致しなかった。

- 1件は`counterexample_found`をexact terminal kindとして返さず、終了時の説明にだけ含めた。
- 2件は外部の`unavailable`ではなく、内部名の`review_unavailable`を返した。

これはreview内容の誤りではなく、内部判定から外部terminal resultへ出る経路が閉じていなかった失敗である。

## 現行TaskSpecだけでは閉じない理由

ADR9のTaskSpecは、必須review scopeと観測manifestを別々に固定している。manifest membershipは、各descriptorが今回の必須scopeを直接充足することまでは意味しない。

また、packetへprojectionされた観測と同じsourceがmanifestにも残る場合、source targetを明示的に除外しなければ再readできる。

出力についても、意味上同じ説明を要求するだけでは、exact external result kindと内部状態名の区別を強制できない。

したがって、Candidate側で新しい事実を推測するのではなく、TaskSpecで固定済みの必須scope、packet projection、manifest descriptor、external dispositionを、dispatch前の一つのinterfaceへbindする必要がある。

## Candidate作成前の検討gate

### 1. base promptの最短正常経路

Candidate147の最短正常経路は、operationごとのrequired outcomeを固定し、producerを一つにbindし、必要なpredicateだけを観測し、terminal resultのeffectを未発行operationへ限定して進む経路である。

Candidate211ではこの通常経路を維持する。prechange reviewがTaskSpecで明示されたoperationだけ、artifact変更の直前に独立reviewを挿入する。

### 2. 失敗を許した既存辺

Candidate210で閉じるべき辺は次の三つである。

```text
manifest membership
  -> reviewer direct read

packet-projected observation
  -> same source direct reread

internal judgement name or free-form prose
  -> admitted external terminal result
```

### 3. 変更するpredicate

Candidate211で追加または変更するpredicateは次に限定する。

- prechange reviewの適用対象であること
- packet projectionが各必須review scopeを充足しているか
- manifest descriptorが、未充足の必須review scopeへ直接かつ一意にbindするか
- requested repository targetがdispatch前に固定した`review_allowed_read_set`へ属するか
- reviewerのterminal outputがexternal `disposition` enumと一致するか

成功時のtool順、判断順、model stepは新しい義務へ転記しない。

### 4. 除去する到達可能辺

入力側は次の閉集合で制御する。

```text
scope_evidence_binding(descriptor, required_scope) :=
  descriptorとrequired_scopeがTaskSpecで固定済み
  and descriptorのobservation identity / target / success conditionが
      required_scopeを直接充足する観測を明示する
  and 同じ観測を消費し得る別のrequired_scopeがない

review_allowed_read_set := {
  target(descriptor)
  | required_scopeはTaskSpec-required
  and required_scopeはpacket projectionで未充足
  and scope_evidence_binding(descriptor, required_scope)
}
```

追加制約は次のとおりとする。

- packet projectionに使ったsource targetは、同じreviewの`review_allowed_read_set`へ入れない。
- manifestにあるだけのdescriptorは許可しない。
- reviewerは集合へtargetを追加、置換、再分類しない。
- bindingが直接かつ一意に確定しない場合は、集合を広げずpacketを`unavailable`にする。
- target名の類似だけではbindingを作らない。

この規則により、`SCOPE-PAIRED`が必須でないcaseの`OBS-PAIRED-SCOPE`はread集合から外れる。一方、`SCOPE-PAIRED`が必須でpacketから未充足のcaseでは、同descriptorを直接観測として残せる。

出力側は次のexact interfaceで制御する。

```json
{"disposition":"counterexample_found"}
{"disposition":"no_counterexample_found"}
{"disposition":"unavailable"}
```

- external terminal resultはこの三値だけを受理する。
- 内部predicate名、説明文、別名は`disposition`を代替しない。
- `counterexample_found`は、bind済みscopeから反例が成立した時点でterminalにできる。
- `no_counterexample_found`は、全必須scopeがpacket projectionまたは許可済み直接観測で充足した場合だけterminalにできる。
- 必須scopeが許可済み入力から確定できない場合は`unavailable`にする。

### 5. 新しく必要になる判断

新しい判断は、dispatch前の`scope_evidence_binding`だけである。reviewer自身に「次に何を読めばよいか」を選ばせない。

このbindingはCandidate211の中心仮説であり、まだ評価済みではない。ADR9 TaskSpecの明示情報から直接かつ一意に作れないcaseがあれば、Candidate本文を作って評価で補うのではなく、作成gateを再度停止する。

### 6. 期待する正常経路

```text
prechange review applicabilityを固定
  -> required scopesとpacket projectionをbind
  -> 未充足scopeだけを直接観測descriptorへ一意bind
  -> review_allowed_read_setを閉じる
  -> 独立reviewerへpacketをdispatch
  -> exact external dispositionをadmit
  -> no_counterexample_foundだけartifact変更を開く
```

この経路は、新しいreceiptや中間状態を増やさない。reviewerへ渡る入力集合と、reviewerから戻る外部result集合を狭める。

## C147からの再構成方針

Candidate bundleを作る場合も、Candidate147本文へ最小差分で再構成する。

1. Candidate147の`EVIDENCE_GATE`末尾で、明示的なprechange reviewが適用されるoperationだけ、artifact変更の前にreviewへ遷移させる。
2. `PRECHANGE_REVIEW`は、適用条件、packet、producer、閉じたread集合、判定、exact external output、result admission、result effectを一つのlifecycleとして持つ。
3. `no_counterexample_found`がadmitされた場合だけartifact変更を開く。
4. `counterexample_found`と`unavailable`は、そのoperationのartifact変更だけを閉じる。
5. Candidate147の通常経路、開始identity、validation、method、result-effect controlは保持する。

Candidate199またはCandidate210を親として差分追加しない。

## ADR9での評価gate

Candidate211を作成できた場合、最初の評価はADR9 N=5だけとする。Standard14、N=20、release、projectionへ同時に進まない。

品質gate:

- 45/45 valid
- 45/45 Score 4

mechanism gate:

- packet-counterexample 20件のrepository read: 0
- packet projection元sourceの再read: 0
- `review_allowed_read_set`外targetのread: 0
- paired-scope直接観測が必要なADR07: 5/5で当該targetを読み、`no_counterexample_found`
- paired-scope観測が欠けるADR09: 5/5で外部`unavailable`
- review result admission: 30/30一致
- external `disposition`: 30/30 exact match
- root preread、closed-source delivery、mixed delivery、forbidden input delivery: 0

いずれか一件でも外れた場合は`quality_failed`または`mechanism_failed`として停止する。同じ設計のrepair rerun、N=20、Standard14へは進まない。

## 現時点の判断

Candidate211の作成前設計は固定する。ただし、これは効果の証明ではない。

次に行うべきことは、ADR9の固定済み入力だけから全caseの`scope_evidence_binding`を直接かつ一意に構成できるかを、Candidate本文作成前に確認することである。構成できればCandidate147からbundleを作る。構成できなければ、その曖昧さを新しい状態名やreviewer判断で補わず、Candidate作成を停止する。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate175 review operation admission closure設計](candidate175-review-operation-admission-closure-design.md)
- [Candidate175 ADR9 / Standard14 N=5結果](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)
- [Candidate179 ADR9 N=5結果](../evaluations/results/candidate179-review-evidence-interface-adr9-r2-n5_2026-08-11.md)
- [Candidate210作成前設計](candidate210-review-evidence-state-closure-design.md)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
