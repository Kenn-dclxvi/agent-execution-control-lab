# Candidate220 review observable output closure 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `direction_assumption_refuted_by_evaluation`

## 監査対象

[Candidate220作成前設計](candidate220-review-observable-output-closure-design.md)が、Candidate219で残ったwhole-container root result、不要reviewer、必要reviewer observation欠落およびterminal support後のmissing伝播を、case対応や成功手順なしで閉じられるかを確認した。

## 反例監査

| 状態 | 許可するroute | 閉じるroute | 判定 |
|---|---|---|---|
| sourceがfixed / model-visible / read allowed | 必要valueだけのobservable output | source属性だけによるwhole output | pass |
| root packetへliteral valueが必要 | packet配送可valueだけを返す任意method | reviewer用valueを含むresult | pass |
| internal processがcontainerをparse | modelへ閉じたresultだけを返す | process内部readまで禁止する過剰制御 | pass |
| observable output shapeを限定不能 | 対応work itemを`unavailable` | whole-output fallbackと受領後除外 | pass |
| review work itemがempty | reviewerなしの通常経路 | 一般review目的だけの起動 | pass |
| packetだけでpredicate充足済み | packetをreviewerへ配送 | 同valueのrepository再取得 | pass |
| 独立producerだけが分けられるpredicateが残る | reviewer direct observation | root代行、root observable resultへの流入 | pass |
| 同producerへ複数valueが必要 | 閉じた共同output | 1 valueずつの順序義務化 | pass |
| counterexample support成立 | terminal化して残りwork item失効 | 別kind用missing伝播 | pass |
| no-counterexampleに全work itemが必要 | 全required observation | 部分観測からのroot補完 | pass |

## Candidate219の誤経路への適用

Candidate219のrootは、sourceがmodel-visibleな固定入力であることと、whole-container resultがrootへadmissibleであることを同一視した。Candidate220ではsource属性はpermission ceilingにとどまり、invocationのtool resultへ含まれ得る全valueを別に判定する。routing、permission、packet readinessという正しい目的でも、observable outputに別producer用valueが含まれ得れば発行できない。

reviewer startも「review命題があるか」ではなく、独立producer resultだけがbindできる未観測predicate instanceが残るかで決める。task全体がdesign admissionを求めることやreview contractの存在はwork itemを作らない。

## 必要alternate routeを閉じていないこと

rootはpacket配送可valueを限定したobservable resultとして取得できる。reviewerはpacketで未充足のrequired observationを直接取得できる。同producerに必要な複数valueを共同取得することもできる。

source内部をparseするmethodそのものは制限せず、modelへ返るoutputだけを閉じるため、特定selectorや1 fieldずつのreadを義務化しない。

## 強制可能性

modelはtool発行前にcommandまたはread methodと、そのtool resultが返すoutput shapeを選択できる。したがって、observable outputへ別producer用valueが含まれ得るrequestを未発行にする境界はpromptで制御できる。

ただし、requestの目的だけを宣言してoutput shapeを確認しない経路を再び許すとCandidate219と同じになる。Candidate本文ではsource permission、consumer intent、observable result closureを別predicateとして固定する必要がある。

## 判断

fixed source、whole output、exact output、empty work item、packet充足、direct observation、共同output、missingおよびterminal supportの各反例で、必要routeを保持しながらCandidate219の誤経路を発行前に閉じられる。blocking counterexampleは見つからなかった。

Candidate147直接baseのCandidate220 bundle作成を許可する。

## 評価後の訂正

ADR9 r2 N=5では、empty work itemによるreviewer抑制は大きく改善したが、root mixed-owner observable resultは20 / 20 packet caseに残った。source availabilityとobservable outputを文章上分離しても、modelは最初のwhole-container readをroutingとpacket constructionに必要な閉じたresultだと分類した。

したがって「modelはtool発行前にoutput shapeを一意に判定できるため、抽象的closureだけでwhole outputを未発行にできる」という作成時仮定は反証された。ここから新しい確認手順や自己申告証跡をmodelへ追加してはならない。次に監査すべきなのは、TaskSpecのread許可、Candidate147の変更前evidence許可および共同発行境界のうち、rootによるwhole-source readを合法にしている権限辺を除いても、必要なpacket構築routeが残るかである。残らない場合は、このprompt境界では未解決として停止する。この訂正は作成時判断を履歴から消さず、Candidate220を`quality_failed / mechanism_failed / stopped`にする。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- Candidate219のticket条項を継承しない。
- source availabilityはobservable result admissionを意味しないと明記する。
- reviewer startは残存work item集合がnonemptyの場合だけにする。
- observable tool resultの全valueを一producerの未観測predicateへ閉じる。
- case / field / scope対応、具体的selector、期待dispositionまたは成功順序を追加しない。

## 参照

- [Candidate220作成前設計](candidate220-review-observable-output-closure-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate219 ADR9結果](../evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5_2026-08-14.md)
