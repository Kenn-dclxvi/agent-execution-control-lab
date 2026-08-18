# P001 validation carrier platform分離設計

> [!IMPORTANT]
> **状態**: `interface_fixed / semantic_kernel_preserved / platform_carrier_separated / codex_seven_capabilities_observed / composition_draft_ready / candidate_not_created / evaluation_not_started`

## 結論

P001の`VALIDATION_PLAN`と`VALIDATION_EXECUTION`を、全platformへ同じ文面で配送する一つのblockとして扱わない。次の二層へ分ける。

1. **validation semantics**は、required validation、順序、個別pass condition、stop condition、result identity、fail-fastおよびterminalの意味を所有する。
2. **validation carrier**は、その意味をplatform上で実行するために、個別resultをmodelへ途中配送せず、carrier内で固定済みpass conditionだけを判定し、planがterminalになった時に対応づけ済みresultを一度返せる能力を所有する。

意味を一般化しただけではcarrier能力は生まれない。carrierがないplatformで、modelが個別resultを受け取って次validationを判断するrouteを代替正常経路にしない。required validationがあるのに必要能力をbindできなければ、そのvalidation operationを`unavailable`へ閉じる。

この分離はP001本文の修正案ではなく、次の管理用compositionを作る前のinterface設計である。P001、C269、C270、C271またはC272を直接の実装親とするCandidateは作成しない。

## 固定した目的と根拠

`task_objective`は、C147由来のvalidation意味を保持しながら、agent platformでP001に生じた途中result ingressを閉じ、chatを含む能力の異なるplatformへ不要なagent専用機能を混ぜない構成境界を作ることである。

P001 Standard14 N=5では、C147比token `+113.73%`、elapsed `+17.04%`だった。action前後を分けた診断では、model response超過の約72%がaction後にあり、validation-heavyな経路で個別resultがmodelへ戻っていた。詳細は[`P001 Standard14 N=5 機能block別cost診断`](p001-standard14-n5-functional-block-cost-diagnostic.md)を正とする。

C269〜C272は次の失敗反例としてだけ使う。

| 反例 | 閉じなかったroute | 本設計で継承しないもの |
| --- | --- | --- |
| C269 | 外側wrapperは成立したが、発行済みoutput全件をcompletion resultとして再配送できた | issued output集合を返却対象にするpermission |
| C270 | predicate-bound resultを事後に作るため、focused resultをmodelへ返して次validationを発行できた | modelによる事後対応づけ |
| C271 | ticket terminal分類を加えても、外側carrier routeを選ばせる判断点が残った | ticketまたは自己分類 |
| C272 | 明示permissionを削除してもdenyにならず、raw output再配送の既定routeが残った | permission不記載をdenyとみなす設計 |

これらのCandidate本文、成功tool順および評価通過は継承しない。

## validation semanticsが所有するもの

共通semantic kernelは次だけを所有する。

| interface | 意味 |
| --- | --- |
| `validation.plan` | required validation identity、固定順、個別pass condition、stop dependency、method bindingおよび完了条件 |
| `validation.readiness` | action完了とplan closureが揃うまでvalidationを開始しない |
| `validation.result_binding` | 各terminal resultを対応するvalidation identity、pass conditionおよび終了状態へbindする |
| `validation.fail_fast` | non-successまたは`unavailable`の後に、そのresultへ依存する後続を開始しない |
| `validation.completion` | 全required resultまたはfail-fastによる発行不能closureが揃うまでplanをterminalにしない |
| `validation.scope` | このclosureを探索、変更前観測、review finding、method探索またはrecoveryへ流用しない |

semantic kernelは、tool名、wrapper名、model step、待機token、出力byte上限またはplatform固有APIを所有しない。また、platformが途中result ingressを抑止できると仮定しない。

## validation carrierが提供しなければならない能力

platform capability blockは、required validation planを受理する前に次の能力を一組としてbindする。

| capability | 必須の境界 |
| --- | --- |
| `carrier.single_admission` | plan全体を一つのcarrier identityへbindし、個別validationを別々のmodel判断へ開放しない |
| `carrier.ordered_individual_execution` | 個別validation identityを潰さず、固定順で開始できる |
| `carrier.local_result_check` | 各resultを開始前に固定したpass conditionだけでcarrier内判定できる |
| `carrier.fail_fast_control` | non-successまたは`unavailable`で依存する後続をcarrier内から発行不能にできる |
| `carrier.intermediate_ingress_denial` | planがnonterminalの間、個別resultをmodel-visible consumerへ返せない |
| `carrier.terminal_projection` | plan terminal時に、各validationへbindした終了状態と必要な完了evidenceを一度だけ返せる |
| `carrier.continuation_identity` | carrier自体がnonterminalなら、別判断を挟まず同じidentityだけをterminalまで継続できる |

一部だけを持つplatformを対応済みとしない。とくに、複数commandを実行できても途中resultをmodelへ返すsurface、または途中resultを抑止できても個別result identityとfail-fastを保持できないsurfaceは、このcarrierを提供しない。

## 閉じるpermission edge

主な誤経路は次である。

```text
closed validation plan
  -> individual validation result
  -> model-visible consumer
  -> 次validationを発行する新しいmodel判断
```

`carrier.intermediate_ingress_denial`は、planがnonterminalである間の`individual validation result -> model-visible consumer`を閉じる。carrier内部の固定済みpass-condition判定は許可するが、新しいvalidation選択、追加read、別tool、進捗報告または完了判断へresultを渡さない。

同時に、次の辺も閉じる。

- invocationを発行した事実から、そのraw output全体をcompletion resultへ昇格する辺
- carrier terminal前に、modelがresultとvalidation identityの対応先を選び直す辺
- nonterminal carrier resultから、同じcarrierの継続以外へ進む辺

これは「wrapperを使うと判断する」というmodel predicateを追加する設計ではない。必要能力がbind済みならそのcarrierだけがvalidation planのproducerになり、bindできなければ当該operationは`unavailable`になる。

## 合法なroute

| 状態 | route |
| --- | --- |
| required validationなし | validation carrierを開始せず、別のcompletion predicateへ進む |
| required validationあり、全capabilityあり | plan全体を一つのcarrierへbindし、carrier terminal resultを一度だけconsumerへ渡す |
| carrierがnonterminal | 同じcarrier identityのterminal化だけを継続する |
| required validationあり、capability欠落 | 個別model loopで代替せず、validation operationを`unavailable`にする |
| validationがnon-success | 対応resultと発行不能になった後続を保持してplanをterminalにし、失敗をconsumerへ返す |

正常routeとして、個別result identity、fail-fast、failure診断、nonterminal継続、追加要求またはresult失効時の新しいvalidation operationは保持する。

## platform構成

platformごとの選択単位は、instructionの配置だけでなくcapability blockになる。

| 構成 | validation semantics | validation carrier | 現在状態 |
| --- | --- | --- | --- |
| full agent | 含む | platformで実証済みのcarrierを一つ含む | Codexの7能力を確認し、管理用draftへ構成済み |
| single-agent tool surface | 含む | 同じclosureを提供できる場合だけ含む | 未確認 |
| chat + action/toolなし | agent用validation operationを含めない | 含めない | 対象機能外 |
| chat + action/toolあり | 含む | surfaceが全capabilityを持つ場合だけ含む | platform別確認が必要 |

Chat向けにagent用carrierの語を一般化して残さない。逆に、carrierを外すためにvalidationの意味を削除しない。構成がrequired validationを扱う場合はsemantic blockと対応carrierを一緒に選ぶ。

## 一枚へのcomposition境界

管理用sourceでは、現在の`validation-plan`と`validation-execution`を次へ再分割する。

```text
common semantic components
  validation-plan
  validation-result-closure

platform capability components
  validation-carrier-<platform>

platform composition
  common semantic components
  + そのplatformで必要かつ提供可能なcapability components
  -> 自己完結した一枚のAGENTS.md
```

Agentへcomponent fileやcapability catalogを追加readさせない。composition manifestとcomponentは`model_visible=false / evaluation_eligible=false`の管理用sourceとし、評価または配送へ渡すのはrender済みの一枚だけにする。

## 次の作業とCandidate作成前gate

Codex向けcarrierの一次資料と保存trace監査に加え、独立probe r2でfail-fastのnegative route、途中result ingress denial、個別identityおよびterminal projectionを確認した。continuation probe r1では、nonterminal nested commandを同じsession identityへbindし、program内部でterminalまで継続した。現行判定は[`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)、一次記録は[`r2結果`](codex-validation-carrier-capability-probe-r2-result.md)と[`continuation結果`](codex-validation-carrier-continuation-probe-r1-result.md)を正とする。7 capabilityが揃ったため管理用composition draftへ進めるが、Candidate本文または評価入力にはしない。

確認できた場合も、最初の新しい管理用compositionはvalidation carrierだけを差分にする。`frontier carrier`、actor、observation、methodまたはprompt短縮を同じ差分へ入れない。

Candidateを作成するには、さらに次を先に固定する。

1. 直接の基準と、P001およびC147の役割。
2. Codex carrierが閉じる上記permission edgeと、増やす判断点が0件であること。
3. required validation、個別result、fail-fast、failure診断およびnonterminal継続の保持case。
4. 途中result ingress、model response数、tokenおよびelapsedを別々に判定するtargeted gate。
5. 既知のStandard14を診断・回帰に限定し、本文選定に使っていない評価境界。
6. 一件でもvalidation欠落、失敗無視、result identity喪失、model間再入または対象外route後退があれば停止する条件。

このgateを満たすまで、P002、評価Profile、dispatch plan、releaseまたはprojectionを作成しない。
