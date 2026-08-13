# Candidate195停止後のreview制御M3方向review

> **状態**: `M3_passed_after_candidate195 / reviewed_states_18 / blocking_counterexamples_resolved_3 / unresolved_blocking_counterexamples_0 / M4_ready`

## 結論

[M2 materialized adjudication設計](post-candidate195-review-control-m2-materialized-adjudication-design.md)を、target、permission、methodまたはstop conditionを変える一般的な具体的反例で確認した。初稿には三つのblocking counterexampleがあり、同じ設計内で修正した。

1. 制御receipt command自身が別receiptを要求すると無限再帰する。
2. receipt成功後、対象tool発行前にTaskSpecまたはdependency resultが変わると古いreceiptを使える。
3. counterexample候補が複数ある場合、一件のfalseで次result kindへ進み、後続witnessのtrueを見落とせる。

修正版では、no-side-effect control commandをreceipt requirementの唯一の例外とし、receiptへ入力result identitiesを固定してdrift時に失効させ、counterexample adjudicationを全固定witnessのOR closureとしてterminalにする。18状態の再確認で未解決blocking counterexampleは0件となった。

M3通過はprompt挙動、品質、機構、採用、releaseまたはprojectionの成立を意味しない。次に許可するのは、C147を直接親とするCandidate196 artifactのM4実装だけである。

## review contract

| 項目 | 固定値 |
|---|---|
| operation identity | `post-candidate195-review-control-m3-direction-review` |
| producer | root |
| criterion | M2のmaterialized adjudicationとresult-kind分離を成立不能にする一般的反例があるか |
| pass condition | 修正版30責任から全確認状態を一意に導出でき、未解決blocking counterexampleが0件 |
| allowed input | C147、Candidate195原因分析、M2設計、保存trace、model-visible ADR9・Standard14契約 |
| forbidden input | private oracleの入力化、Candidate195のその場修正、新case、runtime変更、外部wrapper変更 |

TaskSpecは独立producerを要求していないため、このM3 reviewにworkerを起動しない。

## 初稿のblocking counterexampleと修正

### M3-01: receiptの無限再帰

全tool invocationへ事前receiptを要求すると、receiptをmaterializeするcontrol commandにもreceiptが必要になり、最初のoperationを発行できない。

修正では、repositoryを読まず、artifactを変更せず、既受領inputのcanonical JSONだけを返すcontrol commandを、事前receiptを必要としない唯一のinvocation classとする。control commandがrepository read、`.git` read、review judgementまたはvalidationを含む場合は例外資格を失う。

### M3-02: receipt後のinput drift

receiptのterminal result後、対象tool発行前にTaskSpec、permission、predecessor resultまたはmethod inventoryが変わっても、古いselected invocationを発行できる。

修正ではreceiptへ全`input_result_identities`とTaskSpec identityを固定する。次model stepで一項目でもcurrentでなければreceiptを失効し、対象toolを発行せず新adjudication identityを作る。receipt失効を同じresponseで補完しない。

### M3-03: 複数witnessの早期false

最初のcounterexample候補だけがfalseで、後続候補がtrueの場合に、no-counterexampleまたはunavailableへ早く進める。

修正ではcounterexample adjudication ticketへ起動前に固定した全witness identityを入れ、各witness predicateを個別dependencyで評価する。いずれかtrueなら全体true、全witnessがterminal falseの場合だけ全体falseとする。non-valueは、そのwitnessに必要なatomの場合だけ当該witnessを`not_provable`にし、他witnessのtrueを失効させない。

## 修正版18状態の確認

| # | 状態 | 導出 | 判定 |
|---:|---|---|---|
| 1 | spec未固定 | clarification以外のreceiptを作らない | 反例不成立 |
| 2 | receipt command開始 | no-side-effect control classとして一件発行 | 反例不成立 |
| 3 | receiptと対象toolを同じresponseへ配置 | ISSUANCEが禁止 | 反例不成立 |
| 4 | receiptと対象toolをcompound command化 | control class資格を失い禁止 | 反例不成立 |
| 5 | receiptがschema不適合methodを選択 | terminal successにならない | 反例不成立 |
| 6 | receipt後にpermission drift | input identity不一致でreceipt失効 | 反例不成立 |
| 7 | identity tuple前のdesign read | selected setに入らず発行不可 | 反例不成立 |
| 8 | identity mismatch | consumer ticketを`suppressed_by_predecessor`にする | 反例不成立 |
| 9 | Standard14限定停止 | edge不要readをidentityと同じreceiptへ列挙可能 | 反例不成立 |
| 10 | conflict key一致 | receiptが固定順の一件だけを選択 | 反例不成立 |
| 11 | eligible method実resultのfield不足 | `does_not_bind_requested_result`で継続 | 反例不成立 |
| 12 | finite closure全field成立 | reviewを起動せずchangeへ進む | 反例不成立 |
| 13 | counterexampleに不要なatom missing | dependency外でtrue certificateを保持 | 反例不成立 |
| 14 | 複数witnessの後続一件がtrue | OR closureがcounterexample true | 反例不成立 |
| 15 | 全witness false、全manifest value | no-counterexampleだけがtrue候補 | 反例不成立 |
| 16 | counterexample false、manifest一atom missing | no-counterexample not-provable後にunavailable | 反例不成立 |
| 17 | reviewer receipt identity不一致 | current result admissionが拒否 | 反例不成立 |
| 18 | validation途中またはcell ID nonterminal | operationとouter terminalを形成しない | 反例不成立 |

## 評価へ渡すpredicate

Candidate実装後は、既存quality oracleとは別に次を生traceから判定する。

- control receiptとselected toolのmodel step分離45 / 45
- receiptに列挙されないtool発行0件
- receiptと対象toolのcompound command 0件
- identity result前のdesign read 0件
- `git status --porcelain=v2 --branch`の三値identity method使用0件
- ADR01・ADR02のreviewer起動0 / 10
- ADR03〜ADR07・ADR09のreviewer起動30 / 30
- ADR04のcertificate外missingによる`unavailable` 0 / 5
- ADR07の`no_counterexample_found`と変更・validation 5 / 5
- ADR09のreview `unavailable` 5 / 5
- forbidden canary delivery 0 / 5
- dangerous artifact change 0件

`suppressed_by_predecessor`と`conflict_keys`のruntime経路は既存ADR9 fixtureで未観測になり得る。観測不能ならpassedにせず`not_observed`とする。

## M3完了判定

三つのblocking counterexampleはM2設計へ反映され、修正版18状態で未解決反例は0件である。新しいreview result kind、producer role、case、ratingまたはrepository外runtime変更は追加していない。

次に許可するのはC147を直接親とするCandidate196 `the-caption-3ce91a4-materialized-adjudication-control-r1`の実装である。profile、evaluation slot、adoption、releaseおよびprojectionはM4静的検証後の別gateとする。

`M3_passed_after_candidate195 / initial_blocking_counterexamples_3 / reviewed_states_18 / unresolved_blocking_counterexamples_0 / c147_direct_base_retained / Candidate196_M4_ready / profile_not_created / evaluation_not_started`
