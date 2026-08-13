# Candidate196停止後のC147局所review応用方向review

> **状態**: `direction_review_complete / reviewed_states_16 / blocking_counterexamples_0 / c147_direct_base_retained / candidate_implementation_not_started`

## 結論

[`C147局所review応用設計`](post-candidate196-c147-local-review-application-design.md)を、case identityや期待terminalを使わず、target、permission、method、stop conditionまたはproducerを変え得る16の一般状態で確認した。設計方向を成立不能にするblocking counterexampleは0件だった。

三接続は独立review契約が適用される変更predicateだけへ作用し、C147の共通dispatch、evidence、method、validationおよびterminalを再構成しない。`not_applicable`は追加operationを作らず、rootのobligation resultと独立reviewer resultも分離できる。

本reviewはCandidate実装、promptによる挙動拘束、評価通過、採用、releaseまたはprojectionを証明しない。次に許可されるのは、C147を直接親とし、三接続だけを追加する新Candidate artifactの設計・実装である。profileと評価slotは静的実装監査後の別gateとする。

## review contract

| 項目 | 固定値 |
|---|---|
| operation identity | `post-candidate196-c147-local-review-direction-review` |
| producer | root |
| criterion | 三接続を一般入力で成立不能にし、共通execution coreの再構成を必要とする具体的反例があるか |
| pass condition | 全確認状態をC147と三接続から導出でき、未解決blocking counterexampleが0件 |
| allowed input | C147原文、局所応用設計、model-visible ADR9・Standard14契約、保存済み原因証拠 |
| forbidden input | case identity分岐、private oracleのprompt入力化、Candidate196の局所修正、repository外runtime変更 |

TaskSpecは独立producerを要求していないため、本方向reviewにworkerを起動していない。完全性は将来試験へ委譲する。

## 16状態の確認

| # | 一般状態 | 導出 | 判定 |
|---:|---|---|---|
| 1 | review契約のない通常実装 | `review_control_applicable=false`で追加operationなし | 反例不成立 |
| 2 | ownerとnon-machine riskだけが存在 | owner語列は独立operation、result kind、consumerを固定しない | 反例不成立 |
| 3 | task自体がread-only review | task producerの成果であり、別の独立review契約ではない | 反例不成立 |
| 4 | review契約の有限な直接免除が全field一致 | obligation=`not_required`、reviewerなしでC147へ進む | 反例不成立 |
| 5 | closure completeだが独立reviewがrequired | obligation=`required`を維持し、closureはreviewer判断の入力にだけ使う | 反例不成立 |
| 6 | required reviewのpermission denial | obligation=`denied`、review operationとpacketを作らない | 反例不成立 |
| 7 | denied時に未信頼prior resultが存在 | prior admission条件を満たさず不受入、rootは意味resultを代行しない | 反例不成立 |
| 8 | current resultとsaved prior resultが同じresult kind | execution identityと利用permissionを分けてadmitする | 反例不成立 |
| 9 | 真正counterexampleと無関係なmissingが共存 | counterexample certificateのconsumer外missingはresultを失効しない | 反例不成立 |
| 10 | witness applicabilityがmissing | counterexampleを推測せずreview `unavailable` | 反例不成立 |
| 11 | counterexampleなし、closure必要値がmissing | `no_counterexample_found`へ昇格せずreview `unavailable` | 反例不成立 |
| 12 | 全scopeがvalueでcounterexampleなし | review `no_counterexample_found`をadmitし対応変更だけを開く | 反例不成立 |
| 13 | required reviewer resultが欠落または不受入 | operationはnonterminal、root補完・変更・outer terminalを禁止 | 反例不成立 |
| 14 | review停止対象と独立した未発行operation | C147の`DECISION_BOUNDARY`により停止効果を伝播しない | 反例不成立 |
| 15 | 無限定identity停止と後続review read | identity一致前は後続readを発行せず、review条項はdispatchを所有しない | 反例不成立 |
| 16 | 限定identity停止と独立read | C147どおり同時発行可能で、review条項は追加stepを作らない | 反例不成立 |

## 非blockingだが試験へ残す境界

次は設計上分類できるが、promptが安定して従うことは未確認である。

- `not_applicable`のStandard14全14ケースで追加reviewerと追加stepが本当に0件になるか。
- closure completeでもrequired reviewを省略しないか。
- finite direct matchでは不要reviewerを起動しないか。
- permission denialではreviewer、packet、prior result採用およびartifact変更が0件になるか。
- counterexample成立後にcertificate外missingを見て`unavailable`へ落とさないか。
- ADR9の無限定開始停止でidentity result前のrepository readを0件にできるか。
- Standard14の限定停止でC147のidentity/read共同発行を退行させないか。

これらを方向reviewのpassへ読み替えず、Candidate実装後のmechanism predicateとして固定する。

## Candidate実装へ渡す境界

新Candidateを作る場合は次を固定する。

- 直接親はCandidate147とする。
- C194、C195、C196のprompt本文、責任構造、ticket、receiptおよびadjudication commandを継承しない。
- C147の13条項本文は保持し、その後に三接続だけを追加する。
- review接続はroot `AGENTS.md`以外のbundle fileを変更しない。
- case identity、fixture名、期待terminal、private oracleおよび過去findingを含めない。
- `not_applicable`、`not_required`、`required`、`denied`と三review resultの意味を混ぜない。
- review追加条項へdispatch、method selection、validation planまたはouter terminalの一般所有を移さない。

静的監査では、C147非変更file identity、13条項保持、追加三label、禁止語彙・禁止機構の非導入およびbundle identityを確認する。

## 評価順序

Candidate実装後も直ちにADR9 45件へ進まない。変更効果を最小に確認するため、次の順序を別gateとして設計する。

1. ADR9全9ケース各N=5で四obligation状態、三review result、root/reviewer境界およびartifact effectを確認する。
2. ADR9通過後、Standard14全14ケース各N=5で`not_applicable`とC147経路非退行を確認する。

各段階でqualityまたはmechanism不一致が一件でもあれば保存して停止する。前段runを後段Candidateのresultとして置換せず、互換条件が一致する場合だけ同一Candidate内のatomic runを再利用する。

## 完了判定

16状態に未解決blocking counterexampleはない。C147の13条項を再分解せず、三つの局所接続だけで既知23ケースと一般状態を分類できる。

次に許可されるのは新Candidate artifactのM4実装だけである。Candidate identity、profile、評価slot、採用、releaseおよびprojectionはまだ作成・決定していない。

`post_candidate196_direction_review_complete / reviewed_states_16 / blocking_counterexamples_0 / local_review_connections_3 / c147_direct_base_retained / candidate_not_created / evaluation_not_started`
