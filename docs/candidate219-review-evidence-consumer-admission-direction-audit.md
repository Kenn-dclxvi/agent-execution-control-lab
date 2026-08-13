# Candidate219 review evidence consumer admission 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `direction_assumption_refuted_by_evaluation`

## 監査対象

[Candidate219作成前設計](candidate219-review-evidence-consumer-admission-design.md)が、C218で残ったmixed-owner root result、二重消費、不要reviewer、packet projection再読およびterminal support後のmissing伝播を、成功手順やcase対応へ変えず閉じられるかを確認した。

## 直接観測できる入力

- TaskSpec-fixed required review propositionまたはscope obligationのempty / nonempty
- review permission、bound producer identity、packet permission、direct observation permission
- current required predicate stateとmissing observation identity
- finite observation targetとsuccess condition
- invocation前にmodelが選ぶrequested result projection
- producer terminal resultとsupportされたdisposition

case名、field名、scope名、期待terminal、value equality、具体的selectorまたは成功runのread順は発火条件に使わない。

## 反例監査

| 状態 | 許可するroute | 閉じるroute | 判定 |
|---|---|---|---|
| review obligationがempty、permission allowed | root routing後に通常実装 | contract存在だけによるreviewer起動 | pass |
| review obligationがnonempty、permission denied | 対応変更を`unavailable` | reviewer、packet、review observation | pass |
| packetだけでrequired propositionが閉じる | rootのpacket-allowed projectionを配送 | reviewerによるpacket source再読 | pass |
| packet禁止の必要値がdirect observation可 | reviewer ticketでexact allowed projectionを取得 | root resultへの流入、packet配送 | pass |
| root routingとreviewer値が同じcontainer | root predicateをbindするprojectionだけ取得 | whole-containerまたはunproven envelope | pass |
| 同一consumerへ複数projectionが必要 | 一つのinvocationで共同取得可 | 1 fieldずつの順序義務化 | pass |
| concrete counterexampleがsupport済み | `counterexample_found`でterminal | no-findingだけに必要な追加read / missing伝播 | pass |
| no-counterexampleに全scopeが必要 | nonterminal predicateを分ける全required observationを取得 | 部分観測からのroot補完 | pass |
| 必須観測がmissingで他kind未成立 | 根拠ある`unavailable` | whole-container fallback、別ownerへの再割当て | pass |
| result envelopeがconsumer外値を含み得る | invocation未発行 | 受領後の「非admission」宣言 | pass |
| review terminal後 | 未発行ticketを失効 | terminal reviewの再開、別kind用read | pass |

## C218失敗への適用

C218はowner分類後も一般`EVIDENCE_GATE`からtarget artifact全体を取得できた。Candidate219では、allowed pathだけでは発行条件にならない。rootのnonterminal predicateとrequested result projectionが一つのticketにbindされ、そのresult envelopeの全値がroot consumerへ許可される場合だけ発行できる。したがってmixed-owner container readは、result受領前に未発行となる。

reviewer側も同じgateを通るため、packet-carried projectionの再読はreviewer predicateをbindするmissing observationにならず発行できない。具体的反例がsupportされた時点でconsumer terminalとなるため、別kindだけを分けるpaired observationのmissingは結果へ伝播しない。

## 必要なalternate routeを閉じていないこと

packet配送禁止値までrootから完全に消すが、reviewerのfinite allowed direct observationは保持する。同じconsumerの複数predicateを一つのprojection resultで閉じられる場合は共同取得できるため、不要な逐次readを強制しない。

no-counterexampleまたはunavailableを判定するため本当に必要な観測は、consumerがnonterminalで値の違いが残るdispositionを分ける限り発行できる。counterexample support成立後だけ、その別kind専用routeを閉じる。

## 成功手順を規定していないこと

設計は`jq`、field名、read回数、rootとreviewerの順番を固定しない。modelが選ぶ任意のmethodについて、発行前のresult projection集合が一つのconsumerの未確定predicateへ閉じていることだけを要求する。

## 強制可能性

modelはtool発行前にcommand、requested projection、consumer、現在のpredicate stateを決められるため、この境界はpromptで強制可能である。tool result返却後にadapterが値を削る外部制御は必要ない。

ただし、modelがresult envelopeを限定できないtoolしか利用できない場合は、そのrequestを発行せず`unavailable`とする。whole-containerを取得してから無視する経路は許可しない。

## 判断

empty obligation、permission denied、packet-only、reviewer direct observation、mixed container、共同projection、missingおよびterminal supportの各反例で、必要routeを保持しながらC218の誤経路を発行前に閉じられる。blocking counterexampleは見つからなかった。

Candidate147を直接baseとし、一般`EVIDENCE_GATE`をconsumer-bound requestへ狭め、artifact変更前reviewを同じgateへ接続するCandidate219 bundleの作成を許可する。

## 評価後の訂正

ADR9 r2 N=5では、rootが最初のdesign readを「model-visibleな固定入力からreview必要条件とpacket readinessを確認するrequest」と扱い、20 / 20 packet caseでdesign container全体を取得した。`review_evidence_ticket`と`consumer_projection_closed`を宣言しても、requestの意図をroot用predicateへbindしただけで、実際にmodelへ返るstdout projectionの閉包を証明しなかった。

また、review obligationが空のケースでも、task-levelのdesign admission命題またはreview contract自体をnonempty propositionと解釈し、10件中9件でreviewerを起動した。したがって、作成時に「requested result projectionとnonempty obligationがmodelに一意に観測可能」とした強制可能性の仮定は実評価で反証された。この訂正は作成時判断を履歴から消さず、Candidate219を`quality_failed / mechanism_failed / stopped`にする。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- Candidate218の`REVIEW_INPUT_OWNERSHIP`を継承しない。
- 一般`EVIDENCE_GATE`のallowed targetだけによる発行許可を、consumer-closed result projection条件で狭める。
- review obligationがemptyならreview operationを作らない。
- reviewer ticketはpacket-carried projectionを再取得しない。
- terminal support後に別kind専用ticketを失効する。
- case / field / scope対応、具体的selector、期待dispositionまたは成功順序を追加しない。

## 参照

- [Candidate219作成前設計](candidate219-review-evidence-consumer-admission-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
