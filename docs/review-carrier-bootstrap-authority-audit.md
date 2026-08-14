# review carrier bootstrap authority 監査

## 状態

- `analysis_completed`
- `candidate214_delivery_boundary_reinterpreted`
- `candidate221_failure_route_preserved`
- `candidate222_prompt_only_axis_evaluated_failed`
- `cumulative_route_ledger_fixed`
- `current_fixed_input_carrier_not_demonstrated`
- `next_candidate_not_created`

## 結論

必要なreviewを成立させるうえで、次に閉じるべき辺はreviewerのread判断ではなく、rootによる最初のsource取得である。

Candidate214は、packet構築後にreviewerがpacket投影元を別selector、部分抽出または別commandで再取得する経路を閉じ、別containerの必要なpaired observationを残した。一方、保存rolloutをdelivery境界で再監査すると、全45 root runがreview開始前に`evaluation-fixture/design-admission.json`全体を取得していた。ADR03からADR06のreview対象20 / 20 runでも、rootへ返ったresultはpacket配送禁止の`consumer_inventory`と`consumer_contracts`を含んでいた。

したがって、Candidate214の一次resultにあるroot preread 0件は、当時固定した消費・admission境界での歴史的判定として保持するが、rootへのwhole-source deliveryが実行不能だったことを意味しない。Candidate214から保持できるのは、packet構築後のreviewer側再read閉鎖と、別containerの必要観測を残した局所境界である。rootへの初回mixed-owner deliveryは未解決だった。

Candidate221は、この初回source取得へproducer別集合を追加したが、whole containerを`root_operation_set`へ含める自己分類を残した。このため同じ20 / 20 runでroot whole-source deliveryが続いた。

Candidate222は将来root operation用viewをpre-review authorityから削除し、root viewをpacket許可値だけへ閉じるprompt-only案を固定ADR9 r2で試した。しかしroot whole-source deliveryとmixed-owner admissionはpacket case 20 / 20に残り、必要なreviewer direct observationも12 / 20だった。view定義だけではwhole-source invocationを発行不能にできず、必要reviewの完遂も29 / 30に留まった。

この結果で、Candidate221の失敗を`root_operation_set`へ再分類したことだけで説明する仮説は棄却された。Candidate222はその集合を削除しても45 / 45 runでrootが最初にwhole design containerを取得したため、残る辺はさらに上流にある。

```text
rootがreviewer packetのliteral値を構築する責任を持つ
  -> literal値はdesign-admission.json内にだけ存在する
  -> 同じcontainerにreviewer direct observation値も共存する
  -> rootのrepository readはprojectionとwhole-container出力の両方を実行できる
  -> prompt上のview定義だけではwhole-container出力の実行能力を除去できない
```

したがってC222から得た知見は、「observation viewという名称が弱かった」ことではない。現在の固定入力では、packet構築に必要なliteral carrierと、rootへのwhole-container出力を不可能にする境界が別々のauthorityとして存在していない、という構造上の不足を特定したことである。次の検討はこの不足を解消できる既存のprompt内境界を探す作業へ接続し、同じcontainerへ新しい分類名や禁止文を足す作業へは戻さない。

## C214からC222までの累積閉鎖台帳

各Candidateを次Candidateの親として連結するのではなく、成立した局所境界、棄却した仮説、残った辺を連結する。

| 証拠 | 保持する局所境界 | 棄却した案または仮説 | 次へ残った辺 |
|---|---|---|---|
| C214 | packet構築後のreviewerによる同一container再readを0件にし、別containerの必要観測を残した | source container全体を閉じれば必要reviewも維持できる | root初回deliveryと、同一container内のreviewer必要値carrier |
| C215–C217 | packet配送値とdirect observation値を区別する必要性を特定した | 必要性判断、投影状態、operand、model-visible性だけでread permissionを閉じる | source取得前に外部authorityへbindされたrecipient別carrier |
| C218–C220 | 不要reviewer起動、manifest外read、canary配送の局所観測を分離した | ownership、ticket、work item、observable output labelでwhole-source readを閉じる | target帰属をモデルに選ばせない実行可能なoutput境界 |
| C221 | packet、reviewer、root用集合を同時に置くとwhole containerをroot用へ再分類できることを確認した | `root_operation_set`を含むproducer別集合で安全なprojectionを作れる | 将来root operationと独立したpre-review carrier |
| C222 | 将来root operation用viewを削除しても、root whole-source deliveryが20 / 20に残ることを確認した | C221の主因が`root_operation_set`であり、その削除で閉じる | packet literal取得そのものとwhole-container出力能力の結合 |

この台帳により、C222の不通過は次の設計へ二つの拘束を残す。

1. `root_operation_set`、observation view、owner、ticketまたは必要性の別名を追加して再試行しない。
2. rootがpacketを構築する正常経路と、reviewer-owned値をrootへ返さない安全境界を同時に証明する。片方だけを満たす案はCandidateへしない。

## 監査対象と境界

この監査の目的はADR9を通す条件を作ることではない。実際のprechange review operationについて、必要なreviewerが判定に必要なcurrent valueを受け取り、rootがその値を先にまたは共同outputとして受け取らない合法routeが、現在のmodel-visible inputから構成できるかを確認することである。

使用した証拠は次のとおりである。

- Candidate214の登録result、品質監査、機序監査およびseal済みexecution archiveに対応するroot / reviewer rollout。
- Candidate221の登録result、source-authority機序監査および対応rollout。
- ADR9 r2全9ケースのmodel-visible TaskSpecと、fixtureが作る`design-admission.json`の構造。
- `docs/prompt-control-design-principles.md`のpermission / dependency closureとcarrier原則。

過去resultのscore、statusまたは当時固定したaudit predicateは変更しない。この文書は、後続のsource-delivery境界から行った現在解釈である。

## C214で実際に成立していた情報経路

C214のrootは、開始identityと`design-admission.json`全体を取得し、そのadmission済みresultからreviewer packetを構築した。packet itemに使ったsource container identityを`review_closed_container_set`へ入れたため、reviewerは同じfileのどのregionにも再到達できなかった。

```text
TaskSpecがdesign-admission.jsonをmodel-visible fixed inputとして指定
  -> C147 EVIDENCE_GATEがtarget artifactの変更前readを許可
  -> rootがdesign-admission.json全体を受領
  -> packet許可値だけをreviewer packetへ投影
  -> packet source container全体をreviewerへ閉鎖
```

この構造により、次は成立した。

- reviewerによるpacket投影元source再readは0回。
- projected source、mixed sourceおよびmanifest外sourceのreviewer readは0回。
- ADR07とADR09では、別containerのpaired targetだけを各5 / 5 runで直接観測できた。
- 必要reviewerの起動、成果物境界、required commandおよびforbidden canary境界は全件一致した。

一方、同じ構造により、同一container内のpacket非配送値には合法carrierがなかった。

| review命題 | 必要なcurrent value | C214での状態 |
|---|---|---|
| current inventoryの一員へsame-treatment contractが適用されるか | `consumer_inventory` membershipと対応contract | rootはwhole source resultとして受領済みだがpacket配送は禁止。reviewer direct readもcontainer closureで禁止 |
| external consumerがowner-local設計の反例になるか | `consumer_inventory`と`consumer_contracts` | 同上 |
| semantic selectionから欠けたinstanceがcurrent inventoryへ属するか | `consumer_inventory` membership | 同上 |

ADR03の1 run、ADR05の2 run、ADR06の1 runでは、独立reviewerは起動したが上記命題を確定できず、必要な`counterexample_found`ではなく`unavailable`で終端した。これはreviewerの判断精度ではなく、必要値を届けるcarrierが存在しなかった失敗である。

## C221でも残った辺

Candidate221は`packet_projection_set`、`reviewer_observation_set`および`root_operation_set`を導入した。しかし、集合へのtarget帰属をsource取得前の外部authorityへ固定せず、モデルがwhole containerをroot operationのtargetへ含められた。

```text
root operationにはtarget artifactのcurrent contentが必要
  -> whole design containerをroot_operation_setへ含める
  -> rootがwhole-source resultを受領
  -> reviewer-owned current valueもrootへ配送
```

この経路は、packet構築目的、routing、将来のartifact変更またはvalidationを理由にroot readを開く限り残る。受領後の非admission、packet非配送または無視では修復できない。

## C222で棄却した説明と残った辺

Candidate222はC221のpre-review authorityから`root_operation_set`を削除し、rootのviewをTaskSpecがpacket配送を許可した値へ限定した。それでも45 / 45 runで最初のreadはwhole design containerとなり、ADR03からADR06の20 / 20 runでrootがinventory / contractsを含むmixed-owner outputを受領した。明示的なprojection commandへ狭まった3 / 20 runもinventory / contractsを含んだ。

この結果から、次を分けて扱う。

- 棄却済み: 将来のartifact変更やvalidation用集合がroot whole-source readを再開する唯一の原因である。
- 観測済み: rootはreview開始前にpacketのliteral値を取得する必要があり、その値は同じdesign container内にしかない。
- 未閉鎖: promptがrecipient別viewを定義しても、repository readのrequestとobservable outputをそのviewへ強制的に閉じる実行境界は生じなかった。
- 維持必須: この辺を閉じるためにrootのcontainer readを一律禁止すると、C214と同様に必要reviewのcarrierを失う。

したがって、次の調査対象はread後の分類やreviewerの判断ではなく、source外から利用できるpacket literal carrier、またはsource取得時点でwhole outputを構成不能にする既存authorityの有無である。

## model-visible inputに存在する手がかり

ADR9 r2のTaskSpecとfixtureには、必要routeを表現するための構造identity自体は存在する。

- TaskSpecは`design-admission.json`内のreview contract、review applicabilityに必要なfieldおよびpacket配送可能なvalue classをsource read前に名前で示す。
- `review_contract.finite_evidence_manifest`はreviewer observationのexact pathまたはJSON pointerを持つ。
- ADR03、ADR05およびADR06の必要値は、`#/consumer_inventory`と`#/consumer_contracts`へ固定されている。
- packet配送値、reviewer直接観測値、`history` / `untrusted_prior_result`およびpost-review artifact値は、fixture上で互いに別のstructural regionにある。

このため、安全なprojectionを返すreadと、reviewerが必要値だけを直接受け取るreadは、repository構造上は表現できる。しかし、現在のTaskSpecはrootへ返せるexact output projectionを独立したcarrier manifestとして固定していない。packet permissionのvalue class、review applicabilityのoperand、finite manifest targetからroot projectionを組み立てる部分には、依然としてmodel-side classificationが残る。

## 合法routeの充足監査

### 1. rootがwhole sourceを受領してpacketで一部だけ運ぶ

不成立。rootはpacket非配送のreviewer-owned値とforbidden valueをすでに受領する。受領後の選別ではdelivery境界を閉じられない。

### 2. rootが安全なexact projectionだけを受領し、reviewerがmanifest targetを直接観測する

必要な正常routeの形としては成立する。

```text
source取得前に固定されたroot projection identity
  -> rootにはreview applicability operand / packet許可値 / manifest descriptorだけを返す

source取得前または安全なdescriptor resultで固定されたreviewer target identity
  -> reviewerには未投影の必要current valueだけを返す
```

しかし、現行固定入力からこのrouteを強制できることは実証されていない。Candidate222は将来root operation用viewをreview terminal前のauthorityから削除したが、whole-source outputを45 / 45 runで止められなかった。TaskSpecが示すfield名とmanifest targetはprojectionを記述する材料にはなるが、rootが受け取るliteral projectionをsource外で供給せず、whole-source requestを実行不能にもしない。したがって「構造上表現できる」ことを「promptだけで閉鎖済み」と扱わない。

### 3. reviewerがsource全体を取得して必要値を選ぶ

不成立。packet投影済み値、root-owned値およびforbidden valueをreviewerへ配送するため、C214で閉じた再取得経路を開く。

### 4. 別のpacket constructorがwhole sourceを取得してprojectionだけをrootへ返す

現行入力では未成立。TaskSpecはそのproducer identity、source authorityおよびrootへ返せるobservable outputを固定していない。promptが新しいproducerやoutput contractを自己生成するだけでは、必要carrierのauthorityにならない。

### 5. 安全なcarrierを固定できないため`unavailable`にする

安全停止としては成立するが、repository内に必要値がありpermissionもallowedなreviewを完遂する目的を満たさない。C214の4 runをこのrouteへ固定する案は解決ではない。

## 次の設計軸

次の候補は、reviewer readの必要性判断ではなく`source bootstrap projection`を扱う。

必要な境界は次のとおりである。

1. prechange review sourceへの最初のrepository evidence invocationから適用する。packet構築後に閉じても遅い。
2. rootへ返せるoutputは、source read前に既存TaskSpecがpacket配送を直接許可したreview applicability operand、packet配送値およびmanifest descriptorだけとする。将来root operation用valueをpre-review viewへ含めない。
3. whole container、ancestor region、複数recipient用valueを含む共同outputおよび除外を証明できないoutputは、目的に関係なくrootへ発行しない。
4. packet非配送のmanifest targetはbind済みreview producerだけが直接観測し、そのinvocation outputはpacket投影値、root-owned値およびforbidden valueを含まない。
5. post-reviewのartifact変更・validationも、将来必要になるという理由でpre-review root authorityを開かない。各operationが発行可能になった時点でも、root outputはexact operation targetへ閉じ、reviewer-owned regionを含むwhole sourceへ戻らない。
6. field名やcase対応をpromptへ埋めず、既存TaskSpecのpacket permissionとmanifest targetをrecipient別viewとして消費する。現行入力で一意に閉じられないことが実測された場合は、その事実をprompt制御の未解決として保持し、試験入力を変更して補わない。

carrierの成立判定では、少なくとも次をsource read前のmodel-visible inputまたはpromptが固定したrecipient別viewへbindする必要がある。

- exact source regionまたはstructural target
- sourceを取得できるproducer
- resultを受領できるproducer
- packetへ運べるvalue identity
- observable outputが含んではならないregion
- target missing / unreadable時のresult kind

これはADR9の期待terminalやcase固有fieldをCandidateへ埋め込む案ではない。実際のreview operationに必要な情報配送契約を固定する案である。Candidate222ではTaskSpec、schema、case、fixtureおよびoracleを変更しない。

## 次へ接続するcarrier実在監査

次Candidateの文面を考える前に、変更しないADR9 r2のmodel-visible inputについて次の順で監査する。

1. sourceを読む前にrootへ見えているauthorityを全件列挙する。
2. 各authorityについて、packetに必要なfield名だけでなくliteral値まで供給できるかを確認する。
3. literal値を供給できる場合は、そのresultがreviewer direct observation値、forbidden値またはcontainer ancestorを含み得ないかを確認する。
4. rootの安全性を満たしたまま、ADR03、ADR05、ADR06およびpaired caseでreviewerが必要値を取得できるかを確認する。
5. 全必要値に一つ以上の合法routeがあり、かつwhole-source routeがモデルの判断に関係なく実行不能な場合だけCandidate設計へ進む。

現在の固定入力を照合した結果は次のとおりである。

| source取得前の入力 | field / target identity | packet用literal値 | whole outputを閉じるauthority | 判定 |
|---|---:|---:|---:|---|
| TaskSpecの`design_and_authority_input` | あり | なし | なし | field名の手がかりに限る |
| TaskSpecの`review_operation_contract` | あり | なし | なし | 配送可能classを示すが値を運ばない |
| `review_contract.finite_evidence_manifest` | source内 | source read後にだけ取得可能 | なし | reviewer target descriptorとしては使える |
| `design-admission.json` | あり | あり | なし | 必要値と複数recipient値が同居する |
| 別containerのpaired target | exact targetあり | reviewerが直接取得可能 | container分離あり | C214で成立した経路として保持 |

この監査時点では、同一`design-admission.json`内のpacket用literal値をsource外からrootへ運ぶcarrierも、rootのread outputをrecipient別projectionへ強制するauthorityも見つかっていない。これはprompt-only全般の不可能性を主張するものではないが、C222と同じ固定入力・同じread surfaceに分類名や禁止文を追加するだけのCandidateを作る根拠はない。

次の調査で新しい既存authorityが見つからない場合は、欠けている値と辺をこの表へ追加して`candidate_not_created`を維持する。見つかった場合だけ、そのauthorityが安全性、必要reviewの完遂、recipient排他性、全必要値の充足、whole-source routeの実行不能性を同時に満たすかを設計gateで確認する。試験、TaskSpec、case、fixtureまたはoracleは変更しない。

## Candidate223で確認したscope別carrier

利用者の明示指示により、既存入力にsource外carrierがないことを未解決のまま止めず、TaskSpec r13とcase r4へ`review-scope-carrier-contract/v2`を追加してCandidate223を評価した。fixtureの意味、oracle、期待terminal、rating、runtime、permissionおよびexecutor条件は維持し、missing evidenceは追加していない。

45件の保存traceは次を示した。

- root exact projection: 45 / 45。
- root whole-container、reviewer-owned projection、unproven projection: 各0件。
- ADR03からADR06でpaired scope read: 0件。
- ADR07とADR09でdesign-container read: 0件。
- review不要時のreviewer read: 0件。
- 必要reviewer起動: 28 / 30。

これにより、source外のscope別exact carrierはC214の正常carrier欠落とroot bootstrap whole-source deliveryを同時に閉じられることを支持した。全scope共通target和集合は不要であり、scope外readをpermission段階で閉じられる。

一方、TaskSpec r13は`SCOPE-CONTRACT`へ、source内finite evidence manifestに存在しない新設identity`OBS-BOUNDARY-LEDGER`を割り当てた。ADR06の2件はこの不一致を検出し、reviewerを起動せず`unavailable`へ安全停止した。他の43件が不一致を無視して進んだことは成功根拠にしない。

次へ持ち越す辺は配送permissionではなく、source外scope-to-observation対応とsource内manifestの全域整合性である。次案ではsource内manifestに存在するobservation identityだけをrequired scopeへbindする。boundary ledgerのliteral値はpacket-carried supporting valueとして保持し、新しいobservation identityを作らない。この整合性を全caseで静的に証明できない案は`candidate_not_created`とする。

## 累積更新規則

今後の分析またはCandidate評価は、その場の成否だけを書かず、この文書の台帳へ次を同じ変更で追記する。

- 今回検証した一つの因果仮説。
- 保存traceがその仮説を支持または反証した具体的経路。
- 今後使わない案の範囲。
- 次へ持ち越すpermission / dependency edge。
- 必要reviewの正常carrierに与えた影響。

この5項目へ接続できない追加promptは、試験を行う手がかりを増やさないためCandidateへしない。

## Candidate作成判断

評価入力を変更せず、promptだけを変数とするCandidate222を作成して評価した。

作成時は、Candidate221のpre-review authorityへpacket projection、reviewer observationに加えて`root_operation_set`を置いたことがwhole-source再分類を許した主因だと仮定した。Candidate222ではroot projection targetをTaskSpecへ追加せず、review terminal前のroot source viewをpacket配送許可値だけへ閉じ、将来root operation用viewをreview terminal後まで存在させなかった。

このprompt-only境界は実行時に強制できなかった。ADR9 r2のcase、fixture、TaskSpec、oracleおよび実行条件を変更せず、Candidate222だけを新規実行した結果、delivery境界と必要review完遂の双方が不通過だった。また、`root_operation_set`を削除しても同じwhole-source deliveryが残ったため、作成時の主因仮説も棄却した。

現在は、上のcarrier実在監査で確認した不足を解く新しい既存authorityが見つかるまで、次Candidateを作成しない。Candidate222へ条件を追加せず、同じread surfaceに分類名や禁止文を重ねない。次Candidateへ進めるのは、whole-source invocationをprompt準拠で構成不能にしながら、必要reviewの正常carrierを残せる別構造を既存入力から証明できた場合だけである。

### 後続更新

上の判断後、利用者は既存authorityがない場合にsource外carrierを評価入力へ追加して試験することを明示した。このauthority拡張をTaskSpec r13として固定し、Candidate223を作成・評価した。結果は上の「Candidate223で確認したscope別carrier」のとおりであり、C222と同じread surfaceへの禁止文追加ではない。Candidate223は必要review欠落2件で停止し、次Candidateはまだ作成していない。

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate214経路閉鎖の再制御方針](candidate214-route-closure-recontrol-direction.md)
- [Candidate214 ADR9 r2 N=5結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate214機序監査](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate221 source authority closure原因分析](candidate221-source-authority-closure-causal-analysis.md)
- [Candidate221 ADR9 r2 N=5結果](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate221機序監査](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate222設計](candidate222-review-source-observation-view-design.md)
- [Candidate222 ADR9 r2 N=5結果](../evaluations/results/candidate222-review-source-observation-view-adr9-r2-n5_2026-08-14.md)
- [Candidate223設計](candidate223-review-scope-exact-carrier-design.md)
- [Candidate223 ADR9 r4 N=5結果](../evaluations/results/candidate223-review-scope-exact-carrier-adr9-r4-n5_2026-08-14.md)
