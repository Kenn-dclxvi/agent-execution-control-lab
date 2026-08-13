# Candidate196停止後のC147局所review応用設計

> **状態**: `design_fixed / c147_execution_core_retained / local_review_connections_3 / obligation_states_4 / known_cases_23_classified / direction_review_required`

## 結論

Candidate194からCandidate196までの不通過を受け、C147の13条項を24〜30責任へ再構成する方向を停止する。次の方向は、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の既存execution coreを変更せず、独立review契約が適用される変更predicateだけへ次の三接続を局所追加する。

1. `REVIEW_OBLIGATION`
2. `REVIEW_RESULT_ADMISSION`
3. `REVIEW_RESULT_EFFECT`

operation ticket、predecessor edge schema、method receipt、observation ledger、materialized predispatch adjudication、result-kind別control command、conflict keyおよびdispatch frontierは追加しない。Candidate196を修正元または親にせず、次Candidateを作る場合もC147を直接基盤とする。

本設計はCandidate artifact、profile、case、rating contractまたは評価slotを作成しない。一般反例reviewを通過するまでCandidate実装を許可しない。

## 設計入力と証拠境界

直接入力は次に限定する。

- C147の13条項原文
- Candidate194、Candidate195、Candidate196の保存済みADR9 r2各45 runと原因証拠
- ADR9 r2全9ケースのmodel-visible TaskSpecと固定oracle境界
- Standard14全14ケースのmodel-visible TaskSpec
- Candidate173、Candidate175、Candidate191で成立したreview経路と後続で確認した機構反例

private oracle、case identity、期待terminalおよび過去findingをprompt入力へ追加しない。保存済み結果は設計反例と試験設計にだけ使う。

## C194からC196で否定された共通方向

三CandidateはすべてC147を直接基盤にしたが、review問題を解くために実行制御全体を再構成した。

| Candidate | 構成 | ADR9 Score 4 | 機構失敗runまたは主要不一致 |
|---|---|---:|---|
| Candidate194 | 24責任 | 40 / 45 | 15 / 45 |
| Candidate195 | 27責任とoperation ticket | 43 / 45 | 9 / 45 |
| Candidate196 | 30責任とmaterialized receipt | 36 / 45 | receipt・result-kind経路を含む36 run |

責任、ticketおよびreceiptを増やしても、発行主体と制御を解釈する主体が同じmodelであるため、論理上のready、receiptおよび実tool-callを一意に対応させられなかった。Candidate196では制御手続き自体が新しい失敗源となった。

したがって本設計では、review以外にも適用される共通dispatch、method、validationおよびterminalを作り直さない。

## 保持するC147 execution core

| C147条項 | 本設計での役割 | 扱い |
|---|---|---|
| `SPEC` | required outcome、operation、permission、constraintの事前binding | 変更しない |
| `PRODUCER` | 一operation一producer、明示時だけ独立producerをbind | 変更しない |
| `TERMINAL` | producer terminal resultなしのoperation terminal化禁止 | 変更しない |
| `CONTEXT` | reviewer packetのallowed readとforbidden input | 変更しない |
| `EVIDENCE_GATE` | 未観測predicateを変えられる観測だけを発行 | 変更しない |
| `OWNER_ROLE` | owner語列だけでproducerを作らない | 変更しない |
| `ROOT` | rootによるreviewer result再生成を禁止 | 変更しない |
| `INDEPENDENCE` | review operationへ固有predicateとproducerをbind | 変更しない |
| `DECISION_BOUNDARY` | review resultの効果を対応する未発行変更へ限定 | 変更しない |
| `VALIDATION_CLOSURE` | required validationの個別resultと早期停止 | 変更しない |
| `VALIDATION_PLAN` | 変更後だけvalidation票を発行 | 変更しない |
| `METHOD` | method不適合をpermission denialやouter terminalへ昇格しない | 変更しない |
| `RECOVERY` | review判断の再生成をenvironment recoveryに含めない | 変更しない |

review追加接続は開始identityのdispatch、repository evidence全体、artifact変更methodまたはvalidation planを所有しない。

## 二段階のresult構造

### 第1段階: rootのreview obligation

rootはTaskSpecと適用中authorityから次の一状態を形成する。

```text
review_obligation := not_applicable | not_required | required | denied
```

| 状態 | 意味 |
|---|---|
| `not_applicable` | 独立review operation、subject、allowed result kindまたはconsumerが直接固定されていない |
| `not_required` | review契約は適用されるが、契約が直接定める有限な免除条件へ一致する |
| `required` | 独立review resultが対応変更のadmission前提で、実行permissionがある |
| `denied` | review resultは必要だがcurrent reviewの実行permissionがない |

`not_applicable`はoperation resultとしてmaterializeしない。review obligation operation、review packet、producer、invocationおよびreview resultを作らず、C147の既存経路へ進む。

`not_required`と`denied`はrootが所有するobligation resultであり、reviewer resultではない。closure success、implementation binding、owner語列、`non_machine_risk`またはtask名の`review`だけでは`not_required`を成立させない。

### 第2段階: required reviewの独立result

`review_obligation=required`の場合だけ、C147の`PRODUCER`、`CONTEXT`、`OWNER_ROLE`および`ROOT`を使って独立review operationを起動する。reviewerが返せるterminal resultは次の三種類だけとする。

```text
review_result := counterexample_found | no_counterexample_found | unavailable
```

rootはこの意味判断を再実行または補完しない。

## REVIEW_OBLIGATION

### 適用条件

review制御は、TaskSpecまたは適用中authorityが次を直接固定した場合だけ適用する。

```text
review_control_applicable :=
  independent review operationが直接固定済み
  ∧ review subjectがC147の変更predicateへbind済み
  ∧ allowed review result kindが固定済み
  ∧ review resultを消費するchange admissionまたはstop judgementが固定済み
```

criterion owner、`non_machine_risk`、静的確認、独立確認、reviewというtask名または一般的安全性だけでは適用しない。

### obligationの優先順

1. `review_control_applicable=false`なら`not_applicable`としてreview制御を開始しない。
2. review契約が有限な直接一致を明示的な免除条件として固定し、その全対象、effect、relationおよび保持constraintがC147のimplementation choiceと一致する場合だけ`not_required`にする。
3. 免除条件が成立せずreview resultが必要で、permissionがある場合は`required`にする。
4. review resultが必要だがpermissionがない場合は`denied`にする。

closure evidenceが完全であることは、required reviewerが`no_counterexample_found`を判断できる条件にはなり得るが、review免除条件にはしない。

## REVIEW_RESULT_ADMISSION

### current resultとprior result

- current resultは、bind済みreview operation、producer identity、sender identity、execution permission、allowed result kindおよびsubject identityが一致する場合だけadmitする。
- saved prior resultはcurrent resultとして扱わない。TaskSpecが利用を許可し、現在条件とresult dependencyが一致する場合だけadmitできる。
- rootの説明、進捗、異Sender message、worker起動またはwaitをreview resultとしてadmitしない。

### result kindの意味境界

```text
counterexample_found :=
  固定review subjectへ適用される具体的witnessが
  許可済み観測値から一般設計predicateを直接反証する

no_counterexample_found :=
  固定review scopeの全必要観測がvalueで
  どのwitnessもcounterexampleを成立させない

unavailable :=
  counterexampleを推測できず
  no_counterexample_foundを閉じるために必要な観測がnon-valueである
```

一件の真正なcounterexampleが成立した後、そのcertificateが消費しないmissing、別witnessのnon-valueまたは未来全域の未確認を理由に`unavailable`へ変更しない。反対に、witness applicabilityまたは規範predicate自体がnon-valueならcounterexampleを推測しない。

## REVIEW_RESULT_EFFECT

admit済みresultだけを、C147がすでにbindした変更predicateへ接続する。

| obligationまたはreview result | 効果 |
|---|---|
| `not_applicable` | review resultを作らずC147の既存経路を維持 |
| `not_required` | reviewerを起動せずC147のchange admissionへ進む |
| `denied` | reviewerを起動せず対応変更を禁止し、外側admissionが`unavailable`を形成 |
| `counterexample_found` | 対応変更を禁止し、外側admissionが`blocked`を形成 |
| `no_counterexample_found` | 対応変更のadmissionを開く |
| `unavailable` | 対応変更を禁止し、外側admissionが`unavailable`を形成 |
| required result未受領または不受入 | review operationをnonterminalのまま保持し、変更も外側terminalも形成しない |

停止効果をtask全体へ伝播させない。対象変更をpayloadから分離するとrequired outcome、artifact間relation、保持constraintまたは実行可能性を壊す場合は、C147のimplementation choice全体を失効し、新しいchoiceはC147の変更前gateから別identityで作る。

## 開始identityとdispatchの非干渉

本設計はC147の`DECISION_BOUNDARY`を置換しない。

- ADR9は開始identity不一致時の停止が無限定なので、identity result受領前にobligation用read、review read、artifact変更またはvalidationを発行しない。
- Standard14で停止対象がartifact変更またはrequired commandに限定され、read targetとpermissionがidentity resultで変わらない場合は、C147どおりidentityと許可済みreadを同じmodel stepから発行できる。
- review条項は新しいdispatch operation、receipt、edgeまたはstepを追加しない。

三値identityを満たさないmethod resultはC147の`METHOD`に従って同じpredicate内で継続し、review `denied`、review `unavailable`またはouter terminalへ昇格しない。

## 既知23ケースの分類

### obligation

| 状態 | ケース | 件数 |
|---|---|---:|
| `not_applicable` | Standard14全14ケース | 14 |
| `not_required` | ADR01、ADR02 | 2 |
| `required` | ADR03〜ADR07、ADR09 | 6 |
| `denied` | ADR08 | 1 |
| 未分類 | なし | 0 |

### required review result

| result | ケース | 件数 |
|---|---|---:|
| `counterexample_found` | ADR03〜ADR06 | 4 |
| `no_counterexample_found` | ADR07 | 1 |
| `unavailable` | ADR09 | 1 |
| 未分類 | なし | 0 |

この分類はcase IDをprompt分岐へ使用することを許可しない。実装と試験ではmodel-visibleなreview契約、finite direct match、permission、witness applicability、規範predicate、観測stateおよびconsumerから同じ状態を導出する。

## 既知反例への対応

| 既知反例 | 対応境界 |
|---|---|
| owner語列から不要reviewerを起動 | `review_control_applicable=false` |
| task自体がreviewなので別reviewerを起動 | 独立review operationとconsumerの直接固定を要求 |
| closure successからrequired reviewを省略 | closureを免除条件にしない |
| prior resultをcurrent resultとして使用 | current/prior admissionを分離 |
| permission denial時にreviewerを起動 | `denied`はreview operationを作らない |
| rootがreviewerの`unavailable`を補完 | obligation resultとreviewer resultを分離し、C147 `ROOT`を維持 |
| counterexampleを無関係なmissingで失効 | certificate局所性 |
| review resultをtask全体へ伝播 | C147 `DECISION_BOUNDARY` |
| review追加によりidentity/readを逐次化 | dispatch非干渉 |

## 実装前停止条件

次のいずれかが一般反例reviewで成立した場合は、本設計を修正するか方向を停止し、Candidateを作らない。

- 四obligation状態または三review resultで分類できない状態がある。
- `not_applicable`判定に追加tool、review operationまたはmodel stepが必要になる。
- review契約のないStandard14経路へproducer、read、terminalまたはresult effectが漏れる。
- rootがreviewerの意味resultを再生成しないとouter terminalを形成できない。
- review result effectをC147の既存変更predicateへ局所bindできない。
- 正しいreview経路のために共通dispatch、method、validationまたはterminal体系の再構成が必要になる。

## 現在状態

設計上、Standard14 14ケースとADR9 9ケースの計23ケースは未分類0件である。これはprompt挙動、品質、機構、採用、releaseまたはprojectionの成立を意味しない。

次に許可する作業は、この設計をcase名に依存しない一般状態で確認する方向reviewだけである。Candidate、profile、評価slot、releaseおよびprojectionはまだ作成しない。

`post_candidate196_local_review_design_fixed / c147_13_clauses_retained / local_connections_3 / obligation_states_4 / reviewer_result_kinds_3 / known_cases_23_classified / unclassified_0 / candidate_not_created / evaluation_not_started`
