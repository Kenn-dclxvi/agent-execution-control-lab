# Candidate218 review input carrier ownership 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `ADR9_r2_N5_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- direct base: `Candidate147`

この文書はCandidate bundle作成前の設計記録である。Candidate217を親にせず、Candidate147へreview inputの合法carrierとconsumer ownershipを固定する一つの境界を追加する。Candidate217は保存resultとtraceだけを反証入力にする。

## 結論

Candidate218で閉じるのは、TaskSpecが一つのcontainerをmodel-visible fixed inputとしたことを、そのcontainer内の全current valueをrootがadmitしてよいpermissionへ拡張する辺である。

```text
TaskSpec-declared review input use
  -> root controlだけに必要
  -> reviewer packetへ配送可能
  -> reviewerが直接観測可能
  -> どのcarrierにも合法的にbind不能

各value identityを一つのconsumer ownerへ固定
  -> rootはroot-owned projectionだけを消費
  -> reviewer-owned projectionを含むcontainer全体はroot resultへadmitしない
```

case名、field名、期待terminal、値の意味類似または成功runのread順は使わない。TaskSpecが宣言したreview operation contract、packetの許可範囲、direct read permission、required review propositionとのpredicate dependencyだけを使う。

## 直接baseと保存trace

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。

Candidate217 ADR9 r2 N=5では次を観測した。

- 45 / 45 valid、Score `4 / 1 = 40 / 5`。
- ADR03からADR06の20 runすべてで、reviewerが必要とし得る値はmodel-visible fixed inputだったが、reviewer packetの許可項目には含まれなかった。
- rootは20 / 20 runでその値を含む構造container全体を先に読み、current valueをadmitした。
- C217はadmission済みoperandをpacketへ必須化し、reviewer-owned observationへ戻すことも禁止したため、合法carrierを失った。
- 5 runはreviewerを起動せず期待`blocked`から`unavailable`へ停止し、15 runはcarrier conflictを残したままreviewerを起動した。
- root admission後のreviewer再readは12回、7 runだった。
- ADR07はpaired targetだけのrouteが5 / 5、ADR09は4 / 5まで改善した。

Candidate217の成功時tool順、判断順、selectorまたはpacket文面は継承しない。固定入力とpacket permissionが一致しない反例、およびrootのwhole-container admissionがowner分離を失効させた事実だけを使う。

## Promptが制御を置く正しい層である理由

TaskSpecはrepository evidenceより前から、reviewの要否とpermission、model-visible fixed input、reviewer packetへ渡してよい情報、許可read範囲、rootによるreview代行禁止を明示する。したがって、各input valueをどのconsumerが使えるかはcurrent valueを読む前に契約から判定できる。

rootが構造containerを読むmethodもpromptのrepository evidence permission内で選べる。root-owned projectionとreviewer-owned projectionが同じcontainerにある場合、root-owned部分だけを選択するか、分離できなければresultをadmitしない境界はpromptで制御できる。executor、tool adapter、runtime hookまたは評価case変更は必要ない。

## Candidate作成前の検討gate

### 1. 基準prompt setと最短正常経路

基準prompt setはCandidate147とする。

最短正常経路は、TaskSpecからreview input useをconsumer別に分割し、rootがreview applicability、permissionおよびpacket構築に必要なroot-owned projectionだけをadmitする経路である。packetへ配送できないreview proposition operandはreviewer-ownedのまま保持し、reviewerが許可されたexact projectionを必要時だけ観測する。どちらのconsumerにも合法的にbindできない必須値だけを`unavailable`へ結ぶ。

### 2. 保存traceへbindした具体的誤経路

C217ではTaskSpecがcontainer内の複数値をmodel-visible fixed inputとしたことから、rootがcontainer全体を読み込んだ。その後、reviewerが必要とするがpacketへ配送できない値を、packetへ入れる、reviewerに再読させる、供給不能として停止するという三経路が併存した。前二経路はownershipが重複し、後者は必要な合法direct observationを失った。

### 3. 既存境界で防げない理由

Candidate147はreview inputのconsumer ownershipを持たない。C217はcurrent valueのadmission後にpacketかobservationかを決めたため、packet permissionより先にrootがreviewer-owned値を消費する経路を防げなかった。`model-visible`、read permissionおよびcontainer identityだけでは、rootが消費してよいprojectionとreviewerへ残すprojectionを分けない。

### 4. 変更するpredicateと責務境界

```text
review_input_use(value_identity) :=
  root_control
  | packet_carried
  | reviewer_observation
  | unavailable

root_control :=
  review applicability / permission / packet contract / allowed readをbindするが
  review propositionの真偽をproducerに代わってbindしないTaskSpec input

packet_carried :=
  reviewerのrequired propositionへ必要
  and TaskSpecがpacket配送を許可

reviewer_observation :=
  reviewerのrequired propositionへ必要
  and packet配送は許可されない
  and TaskSpecがproducerによるdirect observationを許可

root_review_input_admissible(result) :=
  resultの全value projectionがroot_controlまたはpacket_carried
```

責務境界は次のとおりとする。

- value identityはTaskSpecが直接要求するinput component、packet contract、allowed readとrequired propositionのdependencyから固定する。case、field、scope、targetの名称を意味対応させて生成しない。
- 一つのvalue identityへexactly one `review_input_use`を固定する。
- `root_control`はreview operationのroutingだけに使用し、review judgementまたはpacket payloadへ流用しない。
- `packet_carried`だけをrootがcurrent valueとしてadmitし、literal valueとprovenanceをpacket receiptへbindする。
- `reviewer_observation`はrootのrepository evidence consumerへ入れず、review producerだけが既存のterminal-effect gateで直接観測できる。
- 同一repository resultがroot-ownedとreviewer-ownedの両projectionを含む場合、そのresult全体をroot review inputへadmitしない。TaskSpecから直接固定できるroot-owned exact projectionだけを取得できる場合に限り、そのprojection resultをadmitする。
- projectionの分離不能、missing、unreadableまたはcarrier permission欠落は、該当必須inputだけを`unavailable`へbindする。whole-container fallbackでownershipを広げない。
- packet construction、ownership確認またはlocator探索のための追加repository evidenceを開かない。
- reviewer起動、terminal support、producer result admission、対応変更effectは同じPRECHANGE_REVIEW境界で維持する。

### 5. 消す判断点と到達可能辺

この置換は、model-visible containerをrootが一括admitした後にcarrierを選ぶ判断点を消す。current valueを取得する前にconsumer ownerが固定されるため、reviewer-owned valueをroot admissionへ混ぜる辺と、rootが読んだことを理由に必要direct observationを閉じる辺を同時に除く。

これは「rootが先に特定selectorを読み、reviewerが後から別selectorを読む」という順序の義務化ではない。rootとreviewerの各consumerが発行できるvalue projection集合を排他的にし、どちらが先に実行されてもowner外のvalueを消費できないようにする。

### 6. 新たに増える判断点、参照、例外

追加する判断は、TaskSpecが一つのvalueをroot routing、packet delivery、reviewer direct observationのどれへ許可したか、および一つのrepository resultがowner境界を越えるprojectionを含むかである。case固有表、期待terminal、値の内容、成功traceのtool順またはfield対応は増やさない。

### 7. 品質維持を確認するcaseとscore分布

初回評価はADR9 r2全9ケース、各N=5とする。

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、artifact境界、reviewer cardinality、required command、forbidden inputを全件一致
- review result admission / effectを全件一致

### 8. 想定する実行routeの変化

- ADR03からADR06ではrootによるmixed-owner whole-container admissionを0件にし、reviewer-owned direct observationを必要な20 / 20 runで保持する。
- 同じcurrent valueをrootとreviewerが二重消費するrunを0件にする。
- ADR07 / ADR09ではpacket-carried inputとreviewer-owned paired observationを分離し、paired targetだけのrouteを各5 / 5にする。
- review不要またはpermission deniedではreviewer-owned observationを発行しない。
- packet重複read、mixed source、manifest外read、forbidden canaryを各0件に維持する。

### 9. 停止条件

次のいずれか一件で停止する。

- validまたはScore 4が45 / 45でない。
- rootがreviewer-owned valueを含むrepository resultをreview inputへadmitするrunが一件でもある。
- 同じvalue identityをrootとreviewerが二重消費するrunが一件でもある。
- packetへ配送禁止のvalueをpacketへ含めるrunが一件でもある。
- 必要なreviewer-owned direct observationをroot admission済みとして閉じ、期待terminalから外れるrunが一件でもある。
- ADR03からADR06の期待terminalが20 / 20でない。
- ADR07 / ADR09でpaired target以外のreviewer-owned repository projectionを読むrunが一件でもある。
- reviewer cardinality、result admission、result effect、artifact boundaryまたはforbidden inputが一件でも不一致になる。

consumer ownershipの重複と必要routeの欠落を同じ境界で判定するためzero-toleranceとする。有効な低品質runを除外または自動再実行しない。

## Candidate本文へ持ち込む拘束

- Candidate147以外のprompt本文を親にしない。
- case identity、固定path、field identity、scope identityまたは期待dispositionを記載しない。
- 成功runのtool順、read順または判断順を規定しない。
- TaskSpecのpacket permissionとdirect observation permissionからconsumer ownerをcurrent value取得前に固定する。
- root-control、packet-carried、reviewer-observation、unavailableを排他的にする。
- rootはreviewer-owned projectionを含むresultをreview inputへadmitしない。
- mixed-owner containerをwhole-container fallbackでrootへ広げない。
- reviewer-owned valueはreview producerだけが既存のterminal-effect gateで観測する。

## 評価後の判断

ADR9 r2 N=5は45 / 45 valid、Score `4 / 1 = 43 / 2`だった。ADR03からADR06の20 / 20 runでrootがreviewer-owned値を含むcontainer resultを取得し、19件ではreviewerも同じ値を直接観測した。ownershipを排他的に宣言しても、一般のrepository evidence発行許可がrootのmixed-owner readを開いたままだった。

ADR07 / ADR09のpaired-only routeも2 / 5、1 / 5にとどまり、review不要時のreviewer起動が7件あった。したがってC218は`quality_failed / mechanism_failed / stopped`とし、repair rerun、ADR9 N=20、Standard14、採用、releaseおよびprojectionへ進めない。次の設計ではownershipを結果受領後のadmission規則ではなく、consumer別のevidence invocation発行可能集合へ接続する必要がある。

## 参照

- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate217機序監査](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
