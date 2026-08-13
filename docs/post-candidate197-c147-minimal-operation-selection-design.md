# Candidate197停止後のC147最小operation選択設計

> **状態**: `design_fixed / c147_direct_base / operation_selection_reframed / review_necessity_direct_bound / known_cases_23_classified / direction_review_required / candidate_not_created`

## 結論

次の方向は、タスク全体の具体的な全操作や最短経路を事前に予測することではない。Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接基盤とし、各判断時点で現在成立し得るoperation候補を先に並べ、現在の成果または次の分岐を確定するために必要な最小集合だけを選び、先行resultで選択が変わるものだけを待たせる。

ターン数、wave数または固定step数を制御へ入れない。選択を更新する境界は、admit済みresultが未発行operationの必要性、target、permission、methodまたはstop conditionを変えた時だけとする。

reviewは独立した中心制御にしない。TaskSpecまたは適用中authorityが直接固定したreview scopeが、現在の変更または停止判断に必要な場合だけoperation候補へ入れる。owner語列、task名、一般的安全性、openに見える対象または「役立つかもしれない」という推測からreviewを追加しない。

Candidate197の三条項を親または修正元にしない。Candidate197の保存結果は、開始経路とreview選択を別々に局所制御しても最小経路を安定して形成できなかった反例として使う。次Candidateを作る場合もC147の直接childとする。

本設計はCandidate、profile、case、rating contract、評価slotまたはreleaseを作成しない。一般状態での方向reviewが完了するまで実装を開始しない。

## 設計入力

直接入力は次に限定する。

- C147の13条項原文
- Candidate197のADR9 r2全9ケース45 run、品質監査および機構監査
- ADR9 r2全9ケースのmodel-visible `trial-prompt-input.json`と、実行時にmodel-visibleになる固定fixture
- Standard14全14ケースのmodel-visible `trial-prompt-input.json`
- C191からC196までの保存済み失敗経路。ただし後続Candidateのprompt本文または機構を継承しない

private expected result、採点用command、過去findingおよびcase IDをprompt判断へ追加しない。既知23ケースは設計の静的分類と後続試験設計にだけ使う。

## Candidate197で確認した設計上の不足

Candidate197はreview要否、review result admission、review result effectをC147末尾へ局所追加したが、operation候補を選ぶ位置を一つにできなかった。

| 観測 | 結果 | 本設計での扱い |
|---|---:|---|
| reviewer cardinality一致 | 29 / 45 | reviewを独立したobligation形成ではなく、全operationと同じ選択へ入れる |
| review result admission一致 | 21 / 45 | current resultのproducer、subject、result kindを既存C147境界へ直接bindする |
| review result effect一致 | 33 / 45 | review resultを消費する変更または停止判断だけを再選択する |
| reviewer欠落時の危険な進行防止 | 45 / 45 | result欠落時に変更を選ばない安全境界は維持する |
| 最初の実repository操作が三値identityのみ | 4 / 45 | identity固有規則ではなく、TaskSpecのstop scopeから先行依存を選ぶ |
| 禁止入力境界 | 44 / 45 | reviewを選んだ場合もC147 `CONTEXT`のallowed readとforbidden inputを維持する |

問題は制御の不足数ではない。review選択と開始identity、evidence、変更、validationが別々の局所判断になり、その時点で不要なoperationを落とす共通の選択がなかったことである。

## 全体最短ではなく現在の最小集合

repository taskでは、将来見つかるauthority、missing、validation failureまたは具体的反例を実行前に全て具体化できない。そのため、全タスクのglobal shortest pathは要求しない。

代わりに、各選択時点で次を満たす集合を作る。

```text
candidate_operation :=
  operation class
  + result predicate
  + result consumer
  + selection guard
  + permission
  + result effect scope

operation_needed :=
  selection guardがsatisfied
  ∧ result consumerがnonterminal
  ∧ admit済みresultがconsumerをまだbindしていない
  ∧ operation resultが現在の成果または次の分岐をbindできる
  ∧ permissionがある
```

`selected_operations`は`operation_needed=true`の候補から、現在の成果または次の分岐をbindするための包含関係上の最小集合とする。選択済みoperationを一件除くとそのbindingが不可能になることを必要条件とする。

同じpredicateへ複数methodが使える場合、method候補を別operationとして全て選ばない。C147 `METHOD`に従い、一つのoperationへ一つのmethodだけを選ぶ。

## 候補を先に並べる境界

### 並べるもの

候補へ入れるのは、現在受領済みのTaskSpec、適用中authorityおよびadmit済みresultから直接導ける次のoperation classである。

- required outcomeまたは次の分岐を直接bindするoperation
- そのoperationのselection guardをbindするevidence operation
- TaskSpecが要求する独立producer operation
- change後にだけ開くrequired validation
- 明示された失敗resultでだけ開くrecovery
- permission denial、充足不能または必要result欠落から形成するterminal disposition

### 並べないもの

- 念のためのread、review、testまたはstatus確認
- exact methodの候補を探すためだけのevidence
- current resultで既にbind済みのpredicateを再確認するoperation
- guardが成立しない変更、validationまたはreview invocation
- 一般的に起こり得るだけで、現在のTaskSpecまたはauthorityへbindできない将来操作
- case IDまたはprivate oracleから逆算したoperation

候補集合を作るためのtool invocation、repository read、ticket、receiptまたは別model turnは追加しない。候補集合はmodel内部の選択であり、外部artifactとしてmaterializeしない。

## 条件付き拡張

具体的な全操作を事前に並べる代わりに、現在のresultが直接開き得る条件付きoperation classをguard付きで保持する。guardが`unobserved`のoperation自体は選ばず、そのguardをbindするために必要なoperationだけを選ぶ。

許可済みresultが`missing / unreadable / 具体的矛盾 / allowed path内で充足不能 / 別authorityの明示`を返した場合は、C147 `EVIDENCE_GATE`が許す一件だけを新候補として追加する。実行中の候補へ場当たり的に操作を継ぎ足さず、受領resultをbindした後に候補集合を選び直す。

新しい候補が現在のTaskSpec、authority、result consumerまたは既存の条件付きclassへbindできない場合は、操作を推測で追加せず`unavailable`とする。

## 依存と同時発行

先行operation `a`と未発行候補`b`について、次のいずれかを`a.result`が変え得る場合だけ`a`を先行させる。

- `b`が必要か
- `b`のtarget
- `b`のpermission
- `b`のmethod eligibility
- `b`のstop condition

変え得ない選択済みoperationは既知の相互非依存として同じmodel stepから発行する。結果を一件ずつmodelへ戻して再選択しない。全ての選択済みresultを受領した後に一度だけ候補集合を更新する。

これにより、開始identityを常に単独化も常に共同発行もしない。

- mismatch時にreadを含む全operationが禁止される場合は、identityだけを選ぶ。
- mismatchがartifact変更とrequired commandだけを禁止し、readのtargetとpermissionを変えない場合は、identityと必要なreadを同時に選ぶ。

判断根拠はTaskSpecのstop scopeであり、case family、慣行または安全側の一般化ではない。

## review必要性の直接判定

review要否をopen / closedという印象、owner語列または`implementation_bound`から推測しない。review operationを候補へ入れる条件は、model-visibleなTaskSpecまたは適用中authorityが固定する値へ限定する。

```text
review_scope_bound :=
  review subjectが固定済み
  ∧ independent producer identityが固定済み
  ∧ allowed result kindが固定済み
  ∧ review result consumerが固定済み
  ∧ required review scope identityが一件以上ある

new_review_needed :=
  review_scope_bound
  ∧ review result consumerがnonterminal
  ∧ consumerをbindできるadmit済みresultがない
```

### 選択

| 条件 | 選択 |
|---|---|
| `review_scope_bound=false` | review operation、packet、producerおよびinvocationを候補へ入れない |
| `new_review_needed=false` | 新しいreview invocationを選ばない |
| `new_review_needed=true`かつpermission allowed | current review operationを一件だけ選ぶ |
| `new_review_needed=true`かつpermission denied | reviewerを起動せず、対応変更を選ばず`unavailable`を形成する |
| review packetを許可入力だけで形成不能 | reviewerを推測起動せず、対応変更を選ばず`unavailable`を形成する |

review taskであること、`non_machine_risk`、criterion ownerまたは独立確認という一般語だけでは`review_scope_bound`をtrueにしない。root自身が行うread-only review taskと、その成果を検査する追加の独立review operationを区別する。

### result admissionと効果

current review resultは、C147の`PRODUCER`、`CONTEXT`、`OWNER_ROLE`、`ROOT`および`TERMINAL`を満たし、subjectとallowed result kindへbindできる場合だけadmitする。saved prior resultはTaskSpecが許可し、current consumer dependencyと一致する場合だけ使う。

admit済みreview resultを受領した後は、そのresult consumerと、resultが必要性またはpermissionを変え得る未発行operationだけを候補選択へ戻す。task全体を再計画せず、無関係な完了済みresultを失効させない。

## C147で変更する設計位置

次Candidateを作る場合、C147の13条項をそのまま保持して末尾へreview条項だけを追加しない。設計上の変更位置は次に限定する。

1. `SPEC`のoperation分解へ、result consumer、selection guardおよび条件付きoperation classを追加する。
2. `DECISION_BOUNDARY`を、候補列挙、最小選択、依存による同時発行、result後の再選択までを所有する規則へ置換する。
3. review固有の直接値からreview候補を形成し、current resultを対応consumerへbindする局所規則を追加する。

`PRODUCER`、`TERMINAL`、`CONTEXT`、`EVIDENCE_GATE`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`および`RECOVERY`の責務は再構成しない。C191からC196のdispatch、ticket、receipt、ledgerまたはadjudication machineryを継承しない。

## ADR9 r2への静的適用

ADR9全9ケースでは、開始identity不一致時の停止対象が特定operation classへ限定されていないため、最初の選択は三値identityだけになる。identity一致後に、review selectionと実装判断をbindするための必要readを選ぶ。

| ケース | model-visibleなreview値 | 最小review選択 |
|---|---|---|
| ADR01・ADR02 | `required_review_scope_identities=[]` | reviewerを選ばず直接authorityから変更候補へ進む |
| ADR03〜ADR07・ADR09 | required scopeが一件以上、permission allowed | current reviewerを一件だけ選ぶ |
| ADR08 | required scopeが一件以上、permission denied | reviewerと変更を選ばず`unavailable` |

required reviewerのresult kindは既存固定contractどおり`counterexample_found / no_counterexample_found / unavailable`とする。ADR03〜ADR06の具体的反例、ADR07の固定manifest成功、ADR09の必要観測non-valueはreviewer resultの判定対象であり、rootが先に期待resultを作らない。

ADR06のhistoryとuntrusted inputは候補選択にもreview packetにも使わない。reviewerに渡す値はTaskSpecが許可したsemantic projection、boundary、authority、required scopeおよびmanifestだけとする。

## Standard14への静的適用

Standard14全14ケースには、追加の独立review operationを直接固定する`required review scope identity`がない。したがって、task名のreview、`non_machine_risk`またはowner語列を理由に追加reviewerを選ばない。

| 経路 | ケース | 主な候補選択 |
|---|---|---|
| clarification / out-of-scope terminal | F05の2ケース | 許可された開始確認と単一terminalだけを選び、edit、test、外部operationを落とす |
| read-only report / review | F10の2ケース | TaskSpec明示readとterminal responseを選び、edit、test、追加reviewerを落とす |
| implementation | 残る10ケース | required outcomeをbindするread、限定change、required validationだけを選ぶ |

A01、A02およびF項目の開始確認は各TaskSpecのstop scopeから依存を決める。owner文字列だけでproducerを追加せず、required validationは変更完了後にだけ選ぶ。これによりStandard14へ新しいreview、ticket、receiptまたは共通dispatch operationを流入させない。

## 一般反例

| 反例 | 本設計の応答 |
|---|---|
| 将来の具体操作を全て予測できない | 条件付きoperation classとresult後の再選択で扱う |
| 候補を多く並べると全て実行してしまう | guardとconsumerから`operation_needed`を判定し、最小集合だけを選ぶ |
| 結果ごとに逐次化して遅くなる | 必要性を変えない選択済みoperationは同じmodel stepから発行する |
| reviewは常に何かを発見し得る | 明示required scopeと未確定consumerがなければ候補へ入れない |
| review permissionがないためrootが代行する | reviewerも変更も選ばず`unavailable`にする |
| review packet不足をrootが推測補完する | 許可入力だけで形成不能ならreviewを起動せず`unavailable`にする |
| validation failureで無関係なreadを再開する | failure resultがguardを開く条件付きrecoveryだけを再選択する |
| 候補選択自体が新しい実行costになる | tool、ticket、receipt、別turnを追加せずmodel内部選択に限定する |

## 実装前停止条件

次のいずれかが方向reviewで成立した場合はCandidateを作らない。

- 候補を作るためだけにrepository evidence、追加model turn、ticketまたはreceiptが必要になる。
- `operation_needed`を明示input、authorityまたはmachine-bound resultから直接判定できない。
- review必要性をrequired scope、consumer、current resultおよびpermission以外の「有用そう」という判断へ依存させる必要がある。
- 条件付き拡張へ入らないoperationを実行中に場当たり的に追加しないと完了できない一般状態がある。
- 同時発行可否をresult effectではなくcase名または固定step数で判断する必要がある。
- Standard14へ追加reviewer、追加read、追加terminalまたは新しい共通実行operationが流入する。
- ADR9のADR01・02、ADR03〜07・09、ADR08をmodel-visibleな直接値で分けられない。
- C147の上記三位置以外に共通method、validation、terminalまたはproducer体系の再構成が必要になる。

## 現在状態

ADR9 9ケースとStandard14 14ケースの計23ケースは、現在の候補operation、review必要性およびterminal経路へ未分類0件で静的に配置できた。これはprompt挙動、品質、機構、採用、releaseまたはprojectionの成立を意味しない。

次に許可する作業は、case名を使わない一般状態で、候補完全性、最小選択、条件付き拡張、review必要性およびC147既存正常経路への非干渉を確認する方向reviewだけである。

`post_candidate197_minimal_operation_selection_design_fixed / c147_direct_base / no_turn_limit / current_minimal_set_not_global_shortest / conditional_operation_classes / review_scope_direct_bound / adr9_9_classified / standard14_14_classified / known_cases_23_classified / unclassified_0 / candidate_not_created / evaluation_not_started`
