# Candidate197停止後のC147最小operation選択方向review

> **結果**: `direction_review_passed / reviewed_states_18 / blocking_counterexamples_0 / candidate_implementation_allowed`

## 結論

[`C147最小operation選択設計`](post-candidate197-c147-minimal-operation-selection-design.md)を、case名を使わない18状態で確認した。候補完全性、最小選択、条件付き拡張、依存による同時発行、review必要性、permission denial、result admissionおよびC147既存正常経路への非干渉について、Candidate実装を停止させるblocking counterexampleは残っていない。

実装時はCandidate147を直接親とし、変更位置を`SPEC`、`DECISION_BOUNDARY`およびreview候補形成の一接続へ限定する。Candidate191からCandidate197までのprompt本文、ticket、receipt、ledger、adjudication commandおよびdispatch機構は継承しない。

## review方法

各状態について、次を順に確認した。

1. operation候補が明示input、適用中authorityまたはadmit済みresultから直接形成できる。
2. `operation_needed`が現在のconsumerとguardから判定できる。
3. 選択集合から一件除いた場合に必要bindingが失われるものだけが残る。
4. 先行resultが必要性、target、permission、methodまたはstop conditionを変える場合だけ依存が生じる。
5. reviewは明示required scopeと未確定consumerがある場合だけ選ばれる。
6. 候補形成自体にtool、repository read、ticket、receiptまたは別turnを追加しない。

## 一般18状態

| # | 一般状態 | 必要な選択 | 結果 |
|---:|---|---|---|
| 1 | required outcome valueが未固定 | clarificationだけを選ぶ | 通過 |
| 2 | outcome固定、target未固定、authorityで一意解決可能 | targetをbindする必要readだけを選ぶ | 通過 |
| 3 | 同じpredicateへ複数methodがある | operationは一件、methodは一つだけ選ぶ | 通過 |
| 4 | guardが未観測でguard producerが固定済み | guard producerだけを選ぶ | 通過 |
| 5 | guardがfalse | 対応operationを選ばない | 通過 |
| 6 | 二operationが同じ先行resultに依存 | 先行result後に一度だけ再選択 | 通過 |
| 7 | 二operationが相互非依存 | 同じmodel stepから発行 | 通過 |
| 8 | resultが一方のoperationだけを無効化 | 対応候補だけを除き他を維持 | 通過 |
| 9 | resultが新authorityを直接明示 | 許可範囲の条件付きread一件を追加 | 通過 |
| 10 | resultが既存classへbindできない未知操作を示唆 | 推測追加せず`unavailable` | 通過 |
| 11 | required review scopeがない | review operationを候補へ入れない | 通過 |
| 12 | required scope、consumer、producer、result kindが固定されpermissionあり | reviewer一件だけを選ぶ | 通過 |
| 13 | required review resultをadmit済み | 新しいreviewerを選ばない | 通過 |
| 14 | required review、permission denied | reviewerと変更を選ばず`unavailable` | 通過 |
| 15 | required review packetを許可入力だけで形成不能 | reviewerと変更を選ばず`unavailable` | 通過 |
| 16 | current reviewerがcounterexampleを返す | 対応変更だけを除き`blocked` | 通過 |
| 17 | current reviewerがno-counterexampleを返す | 対応変更のguardを開く | 通過 |
| 18 | current reviewerがunavailableを返す | 対応変更を選ばず`unavailable` | 通過 |

## 候補完全性

候補集合は将来の具体commandや全fileを予測しない。現在の成果または次分岐へconsumerを持つoperation classと、そのguardをbindするoperationだけを含む。未知の具体値は`missing / unreadable / 具体的矛盾 / 充足不能 / 別authority明示`というC147 `EVIDENCE_GATE`の既存結果から条件付きで一件ずつ具体化できる。

この構造では、候補にない操作を即時発行する必要はない。既存classへbindできない新操作は`unavailable`で停止できるため、場当たり的拡張を完了条件にしない。

## 最小性と並列性

「最小」は候補数またはmodel turn数の固定上限ではない。現在の成果または次分岐をbindする集合から一件除くと必要bindingが失われるという包含最小性である。

先行resultが後続候補を変え得る場合だけ待つため、必要な依存を壊さない。変え得ない選択済みoperationは同時発行するため、全resultを逐次受領する過剰直列化も生じない。ターン数、wave数および固定step数を追加する必要はない。

## review必要性

reviewを選ぶ直接値は、subject、独立producer identity、allowed result kind、consumerおよび一件以上のrequired scope identityである。これらはADR9のmodel-visible review contractから取得できる。required scopeが空ならreviewerを選ばず、一件以上でpermissionがあれば一件だけ選び、permission deniedなら起動しない。

Standard14には追加review operationのrequired scope identityがない。`non_machine_risk`、owner語列、task名のreviewまたは独立確認という一般語だけではreview候補を形成しないため、追加reviewerは流入しない。

## C147非干渉

変更しない11条項はproducer、terminal、context、evidence admission、owner、root、independence、validation、methodおよびrecoveryを引き続き所有する。新設計はそれらをticket、receiptまたは別schemaへ移さない。

`SPEC`はoperation分解時の候補属性を追加し、`DECISION_BOUNDARY`は現在候補の選択とresult後の再選択を所有する。review接続は候補形成とcurrent result bindingだけを所有する。この三位置は同じ「現在必要なoperationを選ぶ」という一つの再構成目的へ閉じており、別Candidateへ分けるとreviewだけが旧選択経路の外へ残るため分離しない。

## 実装条件

- direct parentはCandidate147とする。
- C147の`SPEC`と`DECISION_BOUNDARY`だけを置換し、他11条項は逐語保持する。
- 追加labelはreview候補形成の一件だけとする。
- case ID、期待terminal、private oracleおよび過去findingをpromptへ入れない。
- Candidate artifact作成後も`not_evaluated`とし、ADR9評価設計を別アーティファクト単位にする。
- ADR9がqualityまたはmechanismで一件でも不通過なら結果を保持し、Standard14へ進まない。

`post_candidate197_minimal_operation_direction_review_passed / reviewed_states_18 / blocking_counterexamples_0 / c147_spec_and_decision_boundary_replacement / review_selection_one_connection / candidate_implementation_allowed / candidate_not_yet_created`
