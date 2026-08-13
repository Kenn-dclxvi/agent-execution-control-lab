# Candidate214 packet source container closure 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_not_started`

## 監査対象

[Candidate214作成前設計](candidate214-packet-source-container-closure-design.md)が、source名、field名、scope名または期待resultの意味対応を使わず、Candidate213のcontainer fragment readとmanifest-to-packet promotionを閉じながら必要な未投影source経路を残すかを確認した。

## 直接観測できる入力

rootはpacket itemを構築する時点で次を観測できる。

- packet item identityとliteral value
- valueを供給したadmission済みinput result identity
- repository-backed resultのcontainer identity
- resultがselectorを固定していればsource region identity
- TaskSpec-fixed manifest targetのcontainer / region identity

reviewerはread発行前にrequested targetのcontainer / region identityを選ぶ。したがって同一、包含または重複は内容の意味を読まず照合できる。

## Candidate213 traceへの適用

### ADR05のfield別read

Candidate213の2 runは、同じrepository fileからinventory fieldとcontract fieldを別々に読んだ。packet construction receiptのcontainer identityがそのfileへbindされていれば、両targetは同じcontainer内にあるため`review_read_conflicts=true`となる。

field名がinventoryかcontractかは判定に使わない。`jq`、部分selectorまたは別invocationであることも例外にしない。

### ADR06のfield read

reviewerがpacket投影元fileの一fieldを読んだrunも、同じcontainer conflictで禁止される。packetに具体的反例supportがあればreadなしで`counterexample_found`を返せる。

### ADR07の代替read

reviewerが必要paired targetの代わりにpacket投影元fileの一fieldを読んだrunでは、代替targetがclosed container内なので禁止される。paired targetは別containerで、packet receiptにも含まれないため、disposition-changing consumerが成立すれば直接readできる。

### ADR06のroot preread

missing paired targetはmanifestに存在するが、packet itemを供給していない。construction receiptは作られず、packet constructionは新しいrepository evidence consumerを開かないため、rootによる起動前readは許可されない。missingはreviewerが必要な場合に直接観測するresultであり、packet readinessを失効させない。

## 過去のclosed-source退行を繰り返さないこと

Candidate200はsource全体を閉じたが、root projectionとreviewer observationの割当てを安全に分けられずrequired reviewerを14件欠落させた。

Candidate214はmanifest全体を投影済みsourceへ分類しない。実際に構築したpacket itemにreceiptがあるsource containerだけを閉じる。未投影manifest targetはpacket不足ではなく、reviewer evidence consumerの候補として残る。

Candidate202の成功tool順やcounterexample-first手順も導入しない。readの可否は、container conflictとterminal dispositionへのeffectだけで決まり、判定順には依存しない。

## 正常経路監査

| 経路 | packet construction receipt | reviewer read permission |
|---|---|---|
| packet内に具体的反例あり | 実際のpacket source containerだけ | closed containerと全fragmentは禁止、追加readなし |
| packetにterminal supportなし | 実際のpacket source containerだけ | closed container外でdispositionを分けるtargetだけ許可 |
| 必要paired observation success | paired targetはpacket receiptなし | direct read可、success後に後続readなし |
| 必要paired observation non-value | paired targetはpacket receiptなし | direct read可、`unavailable`後に後続readなし |
| review permission denied | packet未作成 | reviewer / readなし |
| review不要 | packet未作成 | Candidate147通常経路 |

## 新しい誤経路を増やさないこと

- manifest membershipからreceiptを作らない。
- container pathからpacket valueの意味を推定しない。
- closed container外の全sourceを一律許可しない。
- rootにreview judgementまたはreviewer observationを実行させない。
- source containerをrepository全体へ拡張しない。
- terminal support前後の成功手順を固定しない。

## 判断

Candidate214のconstruction receipt限定とcontainer包含閉鎖は、Candidate213で観測した6件の投影元fragment readと1件のmanifest promotion prereadへ、意味分類なしで適用できる。別containerの必要paired observationを保持できる。

Candidate200の過剰停止を繰り返す可能性は、receiptを実際のpacket itemだけへ限定し、未投影manifest targetをpacket readinessから外すことで閉じた。効果は未評価であり、ADR9 r2 N=5のzero-tolerance gateで判定する。

したがってCandidate147を直接baseとするCandidate214 bundleの作成を許可する。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- packet itemごとに実source container receiptを固定する。
- manifest membershipだけではreceiptを作らない。
- closed containerとその全regionへのreviewer readを禁止する。
- 未投影sourceはdisposition-changing consumerがある場合だけ許可する。
- Candidate200、Candidate202、Candidate213のprompt本文またはcase固有対応を継承しない。

## 参照

- [Candidate214作成前設計](candidate214-packet-source-container-closure-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate213 ADR9結果](../evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5_2026-08-14.md)
