# Candidate209 名前付きcertificate欠損境界 設計

## 結論

Candidate209はCandidate208を直接基盤とし、artifact変更前の独立reviewでrepository observationを開ける条件を、未解決resultへ影響し得るという可能性から、packet内certificateに残る名前付き欠損をその観測だけが充足できるという排他的依存へ置換する。`unavailable`にも同じ欠損identityと排他的依存を要求する。

新しいreview順序、model-step barrier、operation、rootによる意味判定、manifest固有例外またはvalidation制御は追加しない。作成前状態は`creation_gate_fixed / candidate_not_created / evaluation_not_started`とする。

## 1. 基準promptと評価状態

- 直接基盤: `the-caption-3ce91a4-result-kind-evidence-domain-r1`（Candidate208）
- 基準result: ADR9 r2累積N=50、450 / 450 valid、Score 4は449件、Score 1は1件
- 品質誤経路: `TC-ADR05` iteration 21、run `3eb2bcdb4605471daac50ab70dba953d`が期待`blocked / counterexample_found`に対して`unavailable`を返した
- 基準機序: packet反例成立後read 10 / 199件、root preread 3 / 300件、reviewer closed-source read 20件を含む23件が機序不通過
- 今回の変更対象: packet反例certificateを成立させるmodel-visible factが揃っているのに、certificate外manifest observationのmissingを`unavailable`へ昇格した一つの誤経路
- 非対象: root preread、closed-source rereadの一般問題、review cardinality、packet封鎖、result effect、共同発行およびvalidation

Candidate208は`quality_failed / mechanism_failed / stopped`であり、採用、releaseまたはprojection済みではない。Candidate209はC208の全挙動を正当化せず、保存traceで結果を反転させた証拠consumer境界だけを置換する。

## 2. 基準状態の最短正常経路

TaskSpec-allowedなmodel-visible packet内の値とprovenanceから、review operation、design、boundary、contract basis、具体的instance、固定designとの直接矛盾およびdesignを変えるeffectがすべてbindできる場合、そのcertificateに欠損はない。manifestに別の観測が列挙されていても、その観測はcertificateを完成させるconsumerを持たず、bind済みreview producerはrepository readなしで`counterexample_found`を返す。rootはresultを再判定せず、対応designのartifact変更だけを停止する。

packetに上記componentの名前付き欠損があり、TaskSpec-fixed manifest observationのsuccess resultだけがその欠損をbindできる場合に限り、その観測を開ける。観測がmissing / unreadable / non-valueで、残るallowed dispositionを決める唯一の許可sourceが失われた場合だけ`unavailable`が成立する。

## 3. 保存traceで確認した誤経路

Score 1 runでは、packetに次の値がmodel-visibleだった。

- designは`owner/local-consumer`だけを選択し、owner-local use onlyを根拠に`implementation_local`としていた
- authorityはownershipを閉じず、external consumerの不存在を保証していなかった
- inventoryに`external/report-consumer`が存在した
- contractは`external/report-consumer`が`shared-asset`へ依存すると明示した
- boundaryは反例のeffectをgeneral design changeへbindしていた

これらは具体的instance、固定designとの直接矛盾およびdesign effectを含むcertificateを完成させる。それにもかかわらずreviewerは、`OBS-PAIRED-SCOPE`が具体的な外部consumer反例を含む可能性を理由に対象をreadし、意図的に不存在だったため`unavailable`を返した。

同じcaseの正常runは同じ種類のpacketからrepository readなしで`counterexample_found`を返している。さらに累積N=50ではpacket反例成立後readが10件観測されているため、単発の文面上の懸念ではなく、C208の広いconsumer条件が繰り返し許した誤経路として扱う。

## 4. 既存入力だけでは防げない理由

C208の`review_observation_consumer_ready`は、観測が「未解決result kindのrequired evidenceへbind済み」で「requested resultがその未解決resultをbind可能」ならconsumerを開ける。この条件では、reviewerがpacket内certificateを完成済みと認識しなかった時点で、manifest observationを結果へ影響し得るsourceとして扱える。

またC208の`review_unavailable`は、残るallowed dispositionを変え得るnamed observationのnon-valueへbindすれば成立するが、どのcertificate componentが欠け、その観測がなぜ唯一の許可sourceなのかを要求しない。そのためmissing observation自体が、事後的に必要性を作れる。

TaskSpec、repository authorityおよびfixtureはpacket値とmanifestを既に固定している。誤りは入力不足ではなく、観測permissionとterminal evidenceが同じ排他的依存を共有していないことにあるため、promptの既存`TERMINAL / EVIDENCE_GATE`境界で置換する。

## 5. 置換するpredicateと責務境界

### 5.1 `TERMINAL`

`counterexample_certificate_component_set`を、review operation、design、boundary、contract basis、具体的instance、固定designとの直接矛盾、designを変えるeffectの有限集合とする。

`certificate_deficit(packet)`は、TaskSpec-allowedなmodel-visible valueとprovenanceからbindできないcomponent identityだけの集合とする。packetに明示値がないことと、値を比較した結果certificateが成立しないことを混同せず、open可能性または将来instanceを欠損componentにしない。

`review_unavailable`には、原因observationに加え、未充足component identityと、そのobservationのsuccess resultだけが同じcomponentをbindできる排他的依存を要求する。missing observationはこの依存を事後生成しない。

### 5.2 `EVIDENCE_GATE`

「requested resultが未解決resultをbind可能」をread資格から削除し、`review_observation_dependency(observation) := observationのsuccess conditionがcertificate_deficit(packet)内の一つ以上のcomponentをbind可能 ∧ 同じcomponentをbind可能なmodel-visible inputまたはadmission済みresultがない`へ置換する。

`review_observation_consumer_ready`はこのdependencyがtrueの場合だけ成立する。`certificate_deficit(packet)`が空なら、certificate外だけでなく全manifest observationのconsumerがfalseとなる。

二変更は同じ排他的依存をterminal resultとread permissionの両方へ適用するため分離不能である。`TERMINAL`だけを変えると不要readが残り、`EVIDENCE_GATE`だけを変えるとmissingを根拠に不完全な`unavailable`を返せる。

`CONTEXT`はC208のまま保持する。manifestが全result共通の実行義務ではないことと、model-visible projectionを未観測へ戻さないことは既に記載されており、今回の誤経路に対する新しい責務を増やさない。

## 6. 消す判断点と増える判断点

| 置換 | 消す判断点・誤経路 | 増える判断点 |
| --- | --- | --- |
| 名前付きcertificate欠損 | 観測に結果を変える情報があり得るかというopen-ended判断 | 既存certificate componentのうちpacketでbind不能なidentityの集合 |
| 排他的観測依存 | manifestにあるため読んでよいという判断 | 観測success conditionと欠損componentの一対一対応 |
| `unavailable`依存共有 | missingを見た後でその観測を必要証拠にする経路 | terminal recordで同じ欠損identityとdependencyを保持 |

新しいlabelは`certificate_deficit`と`review_observation_dependency`の二つである。前者は既存certificateの不足集合、後者は既存consumerの開放条件を表し、新しいoperation、参照先、read順、retryまたは例外を作らない。

## 7. 非目標

- 「まずcertificate、次にmanifest」という逐次review手順
- result kind別operationまたはmodel-step分離
- `TC-ADR05`、`OBS-PAIRED-SCOPE`または特定pathの名指し制御
- rootによるcertificateの意味判定、Reviewer resultの再構成または再採点
- manifest全件の無効化
- packet schema、TaskSpec、case、rating、fixtureまたは評価基盤の変更
- root prereadおよびclosed-source rereadの別機序を同じcandidateへ追加
- 採用、releaseまたはTHE-CAPTION本体へのprojection

## 8. 評価gate

初回gateはADR9 r2 N=5の45件とする。Candidate208保存Layer 1を再利用し、prompt identity以外の互換条件を一致させたpreflight receiptが`ready`の場合だけ不足45件を発行する。

品質gate:

- 45 / 45 valid
- 45 / 45 Score 4
- terminal、review result、変更path、required commandおよびresult effectがcase期待と一致

機序gate:

- packet反例成立caseでrepository read 0件
- `TC-ADR07`で必要なdirect observation後に`no_counterexample_found` 5 / 5
- `TC-ADR09`で排他的依存を持つmissing observation後に`unavailable` 5 / 5
- review cardinality、forbidden input、root substitutionおよびcommand protocolに違反なし

初回gate通過後も、低頻度誤経路の解消をN=5だけでは確定しない。ADR9を累積N=20へ延長し、packet反例成立後read、Score 1、必要観測の省略および`unavailable`依存recordを再監査する。Standard14はADR9累積N=20の品質・機序通過後に別設計で実施する。

停止条件:

- Score 4以外が一件でもある
- packet内certificateが完成しているrunでrepository observationを一件でも発行する
- `TC-ADR07`または`TC-ADR09`の必要観測を省略する
- `unavailable`が名前付き欠損componentと排他的観測依存へbindされない
- review適用、producer、result admission、局所result effectまたはartifact境界が退行する

一件でも停止条件が成立した場合はrepair rerun、Standard14、採用、releaseおよびprojectionへ進めない。有効な低品質または機序不通過runは保存証拠として保持する。

## 9. 手順化禁止監査

- certificate判定とobservationを順番の異なるoperationへ分けない。
- 「先に」「成立しない場合だけ」「次に」という実行順序をprompt本文へ追加しない。
- manifestの観測順、tool、read回数またはmodel stepを固定しない。
- rootへcertificate componentの意味判定を移さない。
- `certificate_deficit`は同一review predicate内のsupport境界であり、model-step barrierではない。
- 観測禁止は命令ではなく、名前付き欠損を消費しない観測にはconsumerが存在しないというpermission境界で表す。

作成前判定は`reproduced_low_frequency_failure / one_evidence_dependency_boundary / two_connected_predicate_replacements / no_procedural_review_lifecycle / creation_allowed`とする。

## 一次参照

- [Candidate208累積N=50結果](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50_2026-08-13.md)
- [Candidate208追加N=45品質監査](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50-additional-quality-audit-r1.json)
- [Candidate208追加N=45機序監査](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50-additional-mechanism-audit-r1.json)
- [Candidate208本文](../prompts/candidates/the-caption-3ce91a4-result-kind-evidence-domain-r1/files/AGENTS.md.txt)
- [prompt制御設計原則](prompt-control-design-principles.md)
