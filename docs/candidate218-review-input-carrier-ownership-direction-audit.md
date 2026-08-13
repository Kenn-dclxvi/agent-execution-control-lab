# Candidate218 review input carrier ownership 方向監査

## 状態

- `direction_passed_at_creation`
- `candidate_creation_allowed`
- `candidate_created`
- `ADR9_r2_N5_completed`
- `direction_assumption_refuted_by_evaluation`
- `stopped`

## 監査対象

[Candidate218作成前設計](candidate218-review-input-carrier-ownership-design.md)が、C217で観測したfixed input / packet carrier conflictを、必要なroot routing inputまたはreviewer direct observationを失わず閉じられるかを確認した。

## 直接観測できる契約

ADR9 r2のTaskSpecはrepository contentを読む前に次を明示する。

- reviewの要否とpermissionを含むoperation contract
- model-visible fixed inputのcomponent集合
- reviewer packetへ配送してよい情報の限定列挙
- rootがreviewを代行または補完しないこと
- 許可read pathとfinite manifest
- completion、blocked、unavailableの外部terminal条件

したがって、あるvalueがroot routing専用か、reviewerへpacket配送できるか、packet配送できずreviewer direct observationへ残るかは、current valueや期待resultを見ずに判定できる。

## C217反例への適用

C217は「TaskSpec-declared fixed inputでadmission済みならpacket」とした。しかしADR9 r2ではfixed inputの一部だけがpacket許可項目であり、別の一部はreview propositionへ必要でもpacketへ配送できなかった。またreview permissionなど、rootがroutingに必要だがreviewer judgementへ渡す必要のないcontrol inputも同じcontainerにあった。

C218はこれを三つのownerへ分ける。

| TaskSpec上の用途 | owner | current valueの消費 |
|---|---|---|
| review applicability、permission、packet / read contractだけをbind | root control | rootだけ。packet payloadまたはreview judgementへ流用しない |
| required review propositionへ必要かつpacket配送可 | packet carried | rootがexact projectionをadmitしpacketへ配送 |
| required review propositionへ必要、packet配送不可、direct read可 | reviewer observation | rootはcurrent valueを消費せずreviewerだけが観測 |
| 必須だが上記carrierなし | unavailable | reviewer resultを補完せず停止 |

この分類はcomponent名の意味推定ではなく、TaskSpecが各用途を明示した関係から決まる。

## mixed-owner container監査

ownerを分けてもrootがcontainer全体を読むと、reviewer-owned current valueまでmodel-visible resultへ入り、C217と同じ重複が再発する。このため次を同じ変更軸に含める必要がある。

- root evidence resultは、含む全projectionがroot controlまたはpacket carriedの場合だけadmitする。
- root-owned exact projectionをTaskSpecから直接固定できる場合、そのprojectionだけを取得する。
- exact projectionを分離できない場合、whole-container fallbackでownerを広げず該当inputを`unavailable`にする。
- reviewer observationはrootのread permission集合から除き、review producerのterminal-effect consumerへだけ残す。

owner分類だけを追加してmixed result admissionを残すと、rootが全値を先に取得する辺を閉じられない。mixed result admissionだけを閉じてowner分類を持たないと、必要valueをpacketとobservationのどちらへ残すかが再びrunごとに揺れる。二つは分離不能である。

## 正常経路と反例監査

| 状態 | 許可する経路 | 閉じる経路 |
|---|---|---|
| review不要 | root routingだけで終了 | reviewer / review observation発行 |
| permission denied | root control resultで停止 | packet構築、reviewer起動、direct observation |
| packetだけで命題が閉じる | root-owned projectionをpacket化 | packet source再読、reviewer-owned値の先読み |
| packet外の必要値がdirect read可 | reviewerがexact projectionを観測 | root admission、packetへの禁止配送 |
| packet外の必要値がmissing / unreadable | reviewer resultで`unavailable` | rootによる補完、別ownerへの再割当て |
| root-owned projectionが分離不能 | 対応inputを`unavailable` | mixed container全体のadmission |
| reviewer resultがterminal | 対応kindとeffectだけをadmit | root再判定、別kind専用の未発行read |

### root-controlをpacketへ誤配送しない

review operationのpermissionやallowed readをrootが知る必要はあるが、それだけでreviewer packet payloadにはならない。C218はroot-controlをpacket-carriedと分けるため、C217の「admission済みならすべてpacket」という過剰配送を再導入しない。

### reviewer-owned値をrootが先読みしない

TaskSpecがpacket配送を許可しないrequired proposition operandは、rootにとって「model-visibleだから読んでよいcurrent value」ではない。rootはそのvalue identityと許可関係だけを保持し、current contentはreview producerへ残す。

### 必要routeを意味対応で作らない

direct observationは、required propositionへ必要で、packet配送不可、producer direct read可という三関係がすべてTaskSpecからbindできる場合だけ開く。field名、scope名、case名、期待terminal、value equalityまたはmanifest membershipだけでは開かない。

### 成功手順を規定しない

設計はrootとreviewerのtool順を定めない。owner別の消費可能projection集合を排他的にするため、順序に依存せずowner外のvalueをadmitできない。

## 判断

作成前設計の発火条件はTaskSpecの明示契約からcurrent value取得前に判定できる。root-control input、packet-carried input、reviewer-observation inputを分け、mixed-owner repository resultをroot admissionから除くことで、C217のcarrier conflictと二重消費を同じ原因境界で閉じる。

blocking counterexampleは見つからなかった。Candidate147を直接baseとし、root `AGENTS.md`だけへ`REVIEW_INPUT_OWNERSHIP`を追加するCandidate218 bundleの作成を許可する。効果は未評価であり、ADR9 r2 N=5の固定gateで判定する。

## 評価後の再判定

ADR9 r2 N=5により、この方向監査の「mixed-owner repository resultをroot admissionから除けば、rootはreviewer-owned current valueを消費できない」という前提が反証された。ADR03からADR06の20 / 20 runで、一般`EVIDENCE_GATE`からdesign container readが発行され、reviewer-owned値を含むresultがroot modelへ返った。後から非admissionを要求する規則は、invocation発行とresult deliveryの経路を閉じていなかった。

作成時点の監査結果とCandidate作成許可は履歴として保持するが、評価後の次案根拠としては不通過とする。次の方向監査では、consumer ownerとexact projectionが一般repository evidence invocationの発行条件を直接制限し、owner境界を越えるresultになり得るinvocationを未発行にできるかを確認する必要がある。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- C217の`REVIEW_INPUT_CLOSURE`本文を継承しない。
- ownerはTaskSpecの明示用途、packet permission、direct observation permissionからだけ固定する。
- root-controlをpacket payloadまたはreview judgementへ流用しない。
- reviewer-owned current valueをrootがadmitしない。
- mixed-owner whole-container resultをroot review inputへadmitしない。
- case / field / scope対応、期待disposition、成功runのread順を追加しない。

## 参照

- [Candidate218作成前設計](candidate218-review-input-carrier-ownership-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
