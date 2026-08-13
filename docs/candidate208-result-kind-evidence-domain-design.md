# Candidate208 result kind別証拠境界 設計

## 結論

Candidate208はCandidate207を直接基盤とし、artifact変更前の独立reviewについて、result kindごとの必要証拠集合とrepository read資格の対応だけを置換する。新しいreview lifecycle、判定順、operation、receipt、台帳、再取得一般則またはvalidation制御は追加しない。

作成前状態は`creation_gate_fixed / candidate_not_created / evaluation_not_started`とする。

## 1. 基準promptと評価状態

- 直接基盤: `the-caption-3ce91a4-c147-review-boundary-recomposition-r1`（Candidate207）
- 基準result: ADR9 r2 N=5、45 / 45 valid、45 / 45 Score 4
- 基準機序: packetだけで具体的反例が成立する20件のうちdirect readなし8件、direct read違反12件
- 保持対象: review要否、明示producer、packet情報封鎖、三terminal result、review resultの変更許可への局所効果、およびC147から保持した共同発行・validation制御
- 未成立部分: packet反例certificateとmanifest observationの依存境界

Candidate207が`mechanism_failed / stopped`であることは、その全差分を自動的に親として採用する根拠ではない。Candidate208で保持する差分は、ADR9でreview cardinality、result admission、result effectおよび品質が全件成立した責務に限定し、保存traceで退行した証拠依存境界は置換する。

## 2. 基準状態の最短正常経路

TaskSpecが独立reviewを要求し、許可済みmodel-visible packet内の値とprovenanceだけで、review operation、design、boundary、contract basis、具体的instance、固定designとの直接矛盾およびdesign change effectがbindできる場合、bind済みreview producerはrepository readを発行せず`counterexample_found`をterminal resultとして返す。rootは真正なresultを受理し、対応designのartifact変更だけを開かない。

packetだけでは具体的反例が成立せず、別のallowed dispositionを確定するために必要なmanifest observationが未観測の場合だけ、その必要factを得られるrepository readに資格がある。`no_counterexample_found`だけが固定review scopeと全manifest successを必要とする。

## 3. 保存traceで確認した誤経路

Candidate207のADR03からADR06までの20件では、12件がpacket反例成立後にもrepository readを発行した。同一caseの成功runは同じ種類のpacketだけから反例を構成し、readなしでterminalになった。

主な誤経路は次の二つである。

1. reviewerがpacket提供済みの設計、authority、契約、inventoryまたはconsumer relationの一部をmanifest上の「未観測」へ戻し、供給元を再読する。
2. reviewerが具体的反例の成立を認識した後も、terminal dispositionを全manifest descriptorへbindするため、certificate外のpaired scope等を読む。

ADR06 iteration 1ではreviewerがpacketだけで具体的矛盾を構成可能と明示したうえで、全manifestへterminalをbindする目的のreadを追加した。ADR06 iteration 2では不要readをcompound commandへまとめたためrootがcommand receiptを受理できず、同じreview operationへ再観測を要求した。この再観測は上流のread資格誤りから派生したものであり、別のcommand制御追加対象にしない。

## 4. 既存入力だけでは防げない理由

Candidate207の`TERMINAL`は、有効な`counterexample_found`を別scopeのmissing等で失効させないと定める一方、`no_counterexample_found`の全manifest条件と三resultのterminal条件を同じまとまりに置く。このため、別scopeがresultを失効させないことと、terminal前に別scopeを観測してよいことが分離されていない。

また`CONTEXT`はmanifest targetの現在値をreviewer-owned observationとし、`EVIDENCE_GATE`は同じrequired factをbindするmodel-visible inputがあればread資格を与えない。保存traceでは前者を直接再取得義務として解釈し、後者を適用しないrunが発生した。

TaskSpec、packet、allowed readおよびmanifest targetは同じrun内で固定されているため、追加情報ではなく、result dependencyとobservation permissionの境界置換が必要である。

## 5. 置換するpredicateと責務境界

### 5.1 `TERMINAL`

三resultを同じ全manifest closureへ読ませる記載を、result kind別の必要証拠集合へ置換する。

- `counterexample_found`: 具体的certificateを構成するsupportだけ
- `no_counterexample_found`: 固定review scopeと全manifest success
- `review_unavailable`: 残るallowed dispositionを変え得るnamed non-value observationだけ

`counterexample_found`のsupport外factは、そのresultのterminal dependencyでもrepository evidence consumerでもない。

### 5.2 `CONTEXT`

reviewer ownershipを、review predicateとterminal resultの生成責任として限定する。TaskSpec-allowedなmodel-visible projectionが同じfactとprovenanceをbind済みの場合、そのfactをnon-valueへ戻して直接再取得する義務を作らない。manifest descriptorは許可可能な観測の有限集合であり、全result kindに共通する実行義務ではない。

### 5.3 `EVIDENCE_GATE`

`review_observation_consumer_ready`を、まだ成立可能なreview result kindの必要証拠集合に属する観測だけへ限定する。packetで`counterexample_found`が成立する場合、certificate support外の全observationはconsumerを持たず、read資格を持たない。

三変更は一つの証拠依存境界を整合させるため分離不能である。`TERMINAL`だけを変えるとread permissionが旧集合を参照し、`EVIDENCE_GATE`だけを変えるとreviewer ownershipがpacket factを未観測へ戻せる。`CONTEXT`だけを変えると全manifest terminal解釈が残る。

## 6. 消す判断点と増える判断点

| 変更 | 消す判断点・誤経路 | 増える判断点 |
| --- | --- | --- |
| result kind別必要証拠集合 | `counterexample_found`にも全manifestが必要かという判断 | result kindと既存supportの対応を一度bind |
| ownership限定 | packet factを直接再取得すべきかという判断 | 同じfactとprovenanceがmodel-visibleかを既存gate内で確認 |
| consumer集合限定 | certificate外manifestが未観測というだけのread | 観測が未解決resultの必要証拠かを既存consumer判定へbind |

新しいoperation、model-step barrier、read順、tool、receipt、retry、例外または参照先は増やさない。

## 7. 非目標

- C206の`admitted_evidence_current`または手順化されたreview lifecycleの復元
- C147またはC207の全条項再構成
- review result kindごとのoperation分離
- manifestやpacketの作成手順、read順、read回数の固定
- command evidence protocolの変更
- Standard14、N=20、採用、releaseまたはprojectionの先行実施

## 8. 評価gate

初回gateはADR9 r2 N=5の45件とする。Candidate207保存resultとprompt identity以外の実効互換条件を一致させ、preflight receiptが`ready`の場合だけ不足45件を発行する。

品質gate:

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、変更path、required commandおよびreview result effectがcase期待と一致

機序gate:

- ADR03からADR06までのpacket反例成立20件でreviewer direct read 0 / 20
- ADR07は必要なdirect observation後に`no_counterexample_found` 5 / 5
- ADR09はmissing direct targetの観測後に`unavailable` 5 / 5
- review cardinality、forbidden input、root preread、command protocolに違反なし

停止条件:

- quality Score 4以外が一件でもある
- packet反例成立後のdirect readが一件でもある
- ADR07またはADR09の必要観測を省略する
- review適用、producer、result admissionまたは局所result effectが退行する
- closed source再読、mixed read、manifest外read、root prereadまたはforbidden input配送が一件でもある

一件でも停止条件が成立した場合は、repair rerun、Standard14およびN=20へ進めない。有効な低品質または機序不通過runは保存証拠として保持する。

## 9. 手順化禁止監査

- 「先にcounterexampleを判定し、成立しなければ次へ」は記載しない。
- result kindを逐次operationまたはmodel stepへ分けない。
- manifestを順番に読む規則を作らない。
- root projectionをreceipt workflowへ変えない。
- `counterexample_found`成立後のread禁止は、順序指定ではなくそのresultのsupport外にevidence consumerが存在しないというpermission境界で表す。

作成前判定は`one_observed_failure_mechanism / three_connected_boundary_replacements / no_procedural_review_lifecycle / creation_allowed`とする。

## 一次参照

- [Candidate207評価結果](../evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5_2026-08-13.md)
- [Candidate207本文](../prompts/candidates/the-caption-3ce91a4-c147-review-boundary-recomposition-r1/files/AGENTS.md.txt)
- [Candidate207実装監査](candidate207-c147-review-boundary-recomposition-implementation-audit.md)
- [prompt制御設計原則](prompt-control-design-principles.md)
