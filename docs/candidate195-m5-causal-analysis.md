# Candidate195 M5 ADR9 r2 N=5原因分析

> **状態**: `analysis_complete / mechanism_failures_9_classified / unknown_cause_0 / c147_direct_base_retained / M2_reopen_ready`

## 結論

Candidate195の機構失敗9件は、二つの直接原因へ全件分類できる。開始identityに関する8件は、発行直前のready・method判定が独立したterminal operationになっておらず、`OPERATION_TICKET`、`PREDECESSOR_EDGE`、`METHOD_SELECTION`および`ISSUANCE`の自己判定だけでtool callを発行できたことが原因である。ADR04 iteration 3の1件は、reviewer内部の三つのresult-kind predicateを一つのjudgement operationへ残し、各certificateのdependencyと失効範囲をticketへ分けなかったことが原因である。

共通する構造原因は、Candidate195がtool invocationのoperation ticketは導入した一方、tool発行を決める判定とreview result kindを決める判定を、result受領まで次へ進めない独立operationへ分解しなかったことである。規則は存在したが、その判定結果自体がpredecessor resultになっていなかった。

Candidate195を修正元または次Candidateの親にしない。直接基盤はC147へ戻す。Candidate195から保持するのは、保存済みrun、成立経路、失敗経路、operation ticketの不足粒度、method output schema判断、finite closureの正経路、observation ledgerの成立例および未観測境界だけである。

## 証拠境界

分析対象は[Candidate195結果](../evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5_2026-08-12.md)の45 valid runsと、[品質監査r1](../evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5-quality-audit-r1.json)、[機構監査r3](../evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5-mechanism-audit-r3.json)である。

固定済みの試験内容、private oracle、rating contract、case revisionおよびCandidate195 bundleは変更しない。collectorが報告した103件はcall ID再監査で真正なmachine-bound終了状態欠落0件と確定したため、原因件数へ含めない。回復済みwrapper失敗3件も、今回の停止原因にしない。

## 9件の分類

| case | iteration | run ID | 最初の不一致 | 直接原因 |
| --- | ---: | --- | --- | --- |
| ADR03 | 4 | `17ba24a6ad97461185a3004dcc416a95` | 三値tupleを返せない`git status --porcelain=v2 --branch`を開始identity methodとして発行 | 発行前判定の非operation化 |
| ADR03 | 5 | `75386b1be5334731854d8f1585142532` | `git rev-parse HEAD HEAD^ HEAD^^`とdesign readを一つのcompound commandへ統合 | 発行前判定の非operation化 |
| ADR04 | 3 | `81d9930eb62349838c72e891484c334a` | 成立済み具体的反例より、certificateが消費しないmissing atomを優先して`unavailable` | judgement dependencyの非ticket化 |
| ADR05 | 5 | `9f8d2a81ca45462498814749d96d1966` | design readとineligibleな`git status`を、三値identity一致前に発行 | 発行前判定の非operation化 |
| ADR07 | 2 | `cfc6af2a13b84290a49865a3c249f94b` | `git status`のfield不足を開始operationとouter terminalの`unavailable`へ昇格 | 発行前判定の非operation化 |
| ADR07 | 4 | `f44c25f0ee59401d8252cd6e1f4a59b5` | identityとdesign readを同一model responseから発行 | 発行前判定の非operation化 |
| ADR08 | 4 | `6543abae3c3441feab14c253708bc672` | identityとdesign readを同一model responseから発行 | 発行前判定の非operation化 |
| ADR08 | 5 | `f570d171dc7b476f884e409976f33d09` | design readを三値identity result前に発行し、後続で`git status`だけを使用 | 発行前判定の非operation化 |
| ADR09 | 5 | `5704982dc2f64620a8c14dda686ee281` | `git status`のfield不足をouter `unavailable`へ昇格し、必要reviewerを未起動 | 発行前判定の非operation化 |

直接原因別では、発行前判定の非operation化が8件、judgement dependencyの非ticket化が1件、原因不明が0件である。品質Score 1の2件はADR07 iteration 2とADR04 iteration 3で、各原因群に一件ずつ属する。ADR09 iteration 5は期待outer terminalだけ一致したためScore 4だが、必要reviewer未起動の機構失敗として保持する。

## 原因1: 発行前判定がterminal operationではない

### 観測

Candidate195本文には、次の正しい禁止条件が存在する。

- `PREDECESSOR_EDGE`はpending consumerを同じmodel response、wrapperまたはcompound commandへ入れない。
- `METHOD_SELECTION`はrequested result contractの全required fieldを原理的に返せないmethodをeligibleにしない。
- `METHOD_RESULT`はfield不足を`does_not_bind_requested_result`とし、permission denial、operation terminalまたはouter terminalへ昇格しない。
- `ISSUANCE`はtool call前に全ticketの`operation_ready`を判定し、実tool-call identityをready ticketへ一対一bindする。

それでも3件でidentity result受領前のdesign readを発行し、5件で三値tupleを返せない`git status --porcelain=v2 --branch`を開始identity methodとして使った。ADR03 iteration 4は後続の`git rev-parse`で回復したが、ineligible methodを候補として発行した事実は残る。ADR07 iteration 2とADR09 iteration 5はfield不足をouter `unavailable`へ昇格した。

### 原因

`operation_ready`、`method_eligible`および発行集合の判定は、rootがtool callと同じmodel responseを作る直前に内的に行う条件のままである。判定operation identity、producer result、terminal contractおよびconsumer edgeを持たず、tool emissionがその判定のterminal result受領を待つ構造になっていない。

そのため、rootがticketを作らない、誤ったticketをreadyとみなす、method-specificな`git status`語列をrequested result contractより優先する、または同じresponseでidentityが成功すると先取りする場合に、後続tool callを止めるpredecessor resultが存在しない。Candidate193までの抽象frontierとは語彙が異なるが、「発行資格の論理記述が現在responseのtool-call選択を一意に拘束しない」という失敗は残っている。

### M2へ渡す未解決predicate

- 発行対象tool callとは別に、requested result contract、permission、candidate method集合、incoming edgeおよびconflictを入力とする発行判定を一つのoperation identityへbindできること。
- 発行判定producerのterminal resultが`ready invocation identity集合`を返すまで、対象tool callを一件も発行できないこと。
- tool call identityがterminal result内の一件と完全一致し、同じresponseで新しいready判定を補完できないこと。
- method output schema不適合を、method execution後ではなくcandidate集合形成時に除外できること。
- 発行判定自体を別名の自己宣言へ置き換えず、実tool-callとの対応をtraceから判定できること。

M2では新しい名称やschemaを先に決めない。上のpredicateをC147の`DECISION_BOUNDARY`、`METHOD`、`EVIDENCE_GATE`および実発行責任へ戻し、どの責任分解ならresult受領前進行を構造的に禁止できるかを設計する。

## 原因2: review result-kindごとのdependencyがticket化されていない

### 観測

ADR04 iteration 3では、`consumer-d`がcurrent inventoryに存在し、`stop_contract=shared-stop-v1`を持ち、一般設計の`stop_applicability`から除外されていることを、`OBS-DESIGN`、`OBS-BOUNDARY-NORMATIVE-CONTRACT`、`OBS-INVENTORY`および`OBS-CONSUMER-CONTRACTS`で観測できた。この四群は具体的反例certificateを成立させる。

一方、固定manifestの`OBS-PAIRED-SCOPE`はmissingだった。reviewerはこのatomを具体的反例の消費集合へ追加し、「scope predicateを閉じられない」として`unavailable`を返した。rootはそのresultをadmitし、期待`blocked`ではなく`unavailable`でterminalにした。

### 原因

`REVIEW_JUDGEMENT`は、具体的反例、反例なし、判断不能の三certificateを一つのproducer operation内で形成する。本文は「実際に使ったatomだけへ依存しcertificate外missingで失効させない」と定めるが、各certificateに固有のincoming edge、accepted state、invalidation atomおよび優先関係を持つticketはない。

このため、具体的反例certificateに不要なmanifest atomをreviewerが消費集合へ追加しても、それを拒否する独立resultが存在しない。`review_unavailable_ready`は前二certificateがfalseの場合だけ成立するが、counterexample predicateが別operationとしてterminalにならないため、missing atomを理由にcounterexampleをfalseへ倒してから`unavailable`を選べた。

### M2へ渡す未解決predicate

- allowed result kindごとに、必要observation atom集合、accepted terminal states、invalidation atomsおよびcertificate predicateを事前固定できること。
- admissibleな`counterexample_found`の必要atomが全件terminal valueなら、certificate外missingをそのpredicateへ追加できないこと。
- `unavailable`判定は、具体的反例と反例なしの各predicateが固有dependencyの範囲でterminal falseになった後だけ発行できること。
- reviewer自由文や消費集合の自己申告ではなく、ledger atomとcertificate dependencyの対応からresult kindを判定できること。

## 成立した境界

失敗だけでCandidate195全体を無作用としない。次の成立経路は保存する。

- 45 / 45 runがvalidで、危険な変更、禁止path変更、commit、pushおよびnetwork使用は0件だった。
- ADR01とADR02の不要reviewer起動は0 / 10で、finite closureの正経路は成立した。
- forbidden ADR06 canary配送は0 / 5だった。
- reviewer command evidenceは154 / 154がmachine-bound終了状態を持ち、真正欠落は0件だった。
- Score 4は43 / 45、terminal一致は43 / 45、artifact boundary一致は44 / 45だった。

これらはCandidate195の部分効果であり、Candidate195を親、成功Candidate、採用候補またはrelease候補にする証拠ではない。

## 未観測境界

開始identity mismatchが発生しなかったため、`suppressed_by_predecessor` runtime経路は未観測である。競合change ticketもなかったため、`conflict_keys`による直列化は未観測である。M5が不通過なので、この二経路やStandard14を追加発行しない。

## 再開判断

M1は`mechanism_failures_9_classified / unknown_cause_0`として完了する。次に許可するのは、C147を直接基盤とし、二原因を満たす責任分解を設計するM2だけである。

Candidate195の27責任をそのまま親にして局所追記しない。Candidate191〜Candidate195は、成立経路、失敗経路、consumer／dependency判断、method schema、finite closure、observation ledgerおよび今回のticket粒度不足を示す診断証拠としてだけ使う。新Candidate、profile、case、評価slot、releaseおよびprojectionは作成しない。

`candidate195_M1_analysis_complete / mechanism_failures_9_classified / predispatch_adjudication_not_terminal_operation_8 / judgement_dependency_not_ticketed_1 / unknown_cause_0 / c147_direct_base_retained / candidate195_not_parent / M2_reopen_ready / new_candidate_not_created / new_evaluation_not_started`
