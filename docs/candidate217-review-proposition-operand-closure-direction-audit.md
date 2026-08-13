# Candidate217 review proposition operand closure 方向監査

## 状態

- `direction_passed_at_creation`
- `candidate_creation_allowed`
- `candidate_created`
- `ADR9_r2_N5_completed`
- `direction_assumption_refuted_by_evaluation`
- `stopped`

## 監査対象

[Candidate217作成前設計](candidate217-review-proposition-operand-closure-design.md)が、Candidate216で残った既取得operandの再取得routeと必須operand欠落routeを、成功手順やcase対応へ変えずに閉じられるかを確認した。

## 直接観測できる入力

- TaskSpec-required review proposition
- propositionの他入力を固定したとき、値の違いが真偽またはallowed terminal kindを変え得るvalue identity
- TaskSpec-declared fixed inputと変更前evidence operationのadmission済みresult
- packet construction receipt
- finite evidence manifest上で未取得operandをbind可能なobservation target

case名、field名、scope名、期待terminal、成功runのtool順または別sourceとのvalue equalityはoperand生成に使わない。

## Candidate216失敗への適用

Candidate216の失敗routeでは、rootがinventory / contract current valueを既にadmitしていたにもかかわらずpacketから省略し、reviewerがrepositoryから同じ値を再取得した。別runでは必要なcurrent inventory valueがpacketにもobservationにもbindされなかった。

Candidate217では、required propositionのdirect operandごとに供給先を一つ固定する。current valueがadmission済みならpacket receipt以外へbindできず、未取得でterminalを分け得る値だけがobservation targetになれる。供給先のない必須operandがあればreviewerを起動しない。

これにより、既取得値を未取得へ再分類するpermission辺と、必須値を欠いたpacketをadmitする辺を同時に閉じる。

## 正常経路監査

| operand状態 | binding | reviewer route |
|---|---|---|
| current valueがadmission済み | packet receipt | 同operandのrepository readなし |
| current valueが未取得、finite targetがterminalを分ける | observation target | exact targetだけread可 |
| current valueがmissing / unreadable | observation result | 根拠ある`unavailable`へbind |
| current valueがadmission済みだがpacket省略 | closure false | reviewer起動不可 |
| 同じoperandをpacketとobservationへ二重bind | closure false | reviewer起動不可 |
| 必須operandの供給先なし | unavailable | artifact変更不可 |
| proposition support成立 | terminal support | 他kind専用の未発行readを失効 |
| review permission denied | packet未作成 | reviewer / readなし |
| review不要 | packet未作成 | Candidate147通常経路 |

## 必要なalternate routeを閉じていないこと

ADR03からADR06のように、terminalを分けるcurrent operandが未取得ならfinite manifest上の対応targetを観測できる。既取得値の再取得だけを閉じ、未取得の必要値までpacket必須にはしない。missingまたはunreadableも観測resultとして`unavailable`を支えられる。

## 成功手順を規定していないこと

設計は「rootが先にinventoryを読む」「reviewerがpaired targetを後で読む」といった順序を要求しない。reviewer起動時点で各direct operandの供給先が一意であることだけを要求する。rootが値を取得した方法、packet内の並び、reviewerの判断順は固定しない。

## 判断

Candidate217は、Candidate216の本文を親にせず、C147へprechange review全体を一つのoperand supply closureとして再構成できる。発火条件はrequired proposition、admission済みcurrent value、finite manifest targetというmodel-visible入力へbindされ、case表や名前対応を必要としない。

既取得operandの再取得routeを閉じながら未取得operandの必要観測routeを残すため、Candidate147を直接baseとするCandidate217 bundleの作成を許可する。

## 評価後の再判定

ADR9 r2 N=5により、この方向監査の「admission済みcurrent valueはpacket receiptへbindできる」という前提が反証された。ADR03からADR06では、必要operandがmodel-visible fixed inputであっても、TaskSpecのreviewer packet許可項目には含まれなかった。したがって、packetへbindできないadmission済みoperandを未取得observationへも戻せず、20 / 20 runでcarrier conflictになった。

作成時点の監査結果とCandidate作成許可は履歴として保持するが、評価後の次案根拠としては不通過とする。次の方向監査では、operandをadmitする前にTaskSpecが許すcarrierとownerを固定できるかを確認しなければならない。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- direct operandをpredicate dependencyから固定する。
- admission済みcurrent operandを必ずpacket receiptへbindする。
- 未admit operandだけをobservation targetへbindする。
- exactly one bindingがない必須operandを含むpacketでreviewerを起動しない。
- packet constructionのための新規read、root先読み、case / field / scope対応を追加しない。
- Candidate216その他の失敗Candidate本文を親にしない。

## 参照

- [Candidate217作成前設計](candidate217-review-proposition-operand-closure-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate216 ADR9結果](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
