# P002候補 Codex validation carrier Candidate作成前設計

> [!IMPORTANT]
> **状態**: `task_objective_fixed / direct_parent_p001 / comparison_reference_c147 / validation_carrier_only_delta / runtime_target_registered / concrete_heldout_source_frozen / p002_candidate_gate_passed / vcc6_paired_n5_valid_60 / p002_score4_30 / tokens_reduced / elapsed_increased / cost_gate_failed / standard14_not_allowed`

## 結論

次のportable full-agent Candidateは、P001の共通意味を維持し、Codex上のvalidation途中result ingressだけを閉じる一差分として`P002`へ固定した。既存の一回応答semantic targetではruntime carrierを観測できないため、[`codex-validation-carrier-conformance`](../evaluations/targets/codex-validation-carrier-conformance/target.json)を別instanceとして登録し、concrete heldout sourceを`codex-validation-carrier-heldout-r1-source-freeze-r1`へ固定した。target実行系とcontrol-free baselineのqualification後、P002 bundleを作成した。candidate-only評価はまだ開始していない。

直接の親、比較基準、診断証拠および失敗反例を次のように分ける。

| 役割 | identity | 継承または利用するもの | 継承しないもの |
| --- | --- | --- | --- |
| target改善系列 | portable full-agent | platform非依存の共通意味とplatform capabilityの組合せを、最終的に一枚へrenderする目的 | compact化、frontier carrier、他platform対応 |
| 直接の親 | P001 `portable-semantic-c147-portable-full-agent-r1` | validation以外66 primitive、portable semantic境界、一枚配送、既存10 componentの同一bytes | P001のvalidation途中model loop、Standard14 cost退行、評価結果のCandidateへの移行 |
| 品質・cost比較基準 | C147 `the-caption-3ce91a4-result-effect-scope-r1` | Standard14で成立したrequired effect、正常route、保存済み互換result | C147のCodex固有全文をportable共通kernelとして扱うこと、成功tool順の転記 |
| cost診断証拠 | P001 Standard14 N=5 result `e8bb0207c8014e5bac8d79ec2cf74bf4` | 途中model再入、token `+113.73%`、elapsed `+17.04%`という問題経路 | P001のcostを次Candidateの期待値または許容値にすること |
| counterexample only | C269〜C272 | raw output再配送、事後result対応づけ、carrier自己選択、permission不記載によるfallback | Candidate本文、条件、ticket、成功経路または親子関係 |

## `task_objective`

```text
target改善系列 := portable full-agent
required effect := C147由来81 primitiveの意味とP001のportable構成を保持したまま、
                   Codex validation planのnonterminal中に個別resultがmodel-visible consumerへ入るpermissionを閉じる
preserved effect := 個別validation identity、固定順、pass condition、fail-fast、failure診断、
                    same-identity continuation、必要evidence、terminal一回返却、validation以外66 primitive
artifact relation := P001 immutable bundleを直接の親として保持し、管理用r2 outputを新identityへbindする場合だけP002を作る
```

本文の短縮、見た目の整理、静的bytes削減はrequired effectではない。効率は品質維持後のall-agent `total_tokens`と`elapsed_seconds`で判定する。

## 1. 基準状態と最短正常経路

直接比較の基準はP001、品質と残存costの参照はC147とする。

P001の最短正常経路は、validation planを固定し、個別validationを固定順に開始し、各terminal resultを対応づけ、全required result受領後に完了を判断する経路である。required validationがない場合はcarrierを開始せず既存completionへ進む。

Codex能力が利用可能なP002候補の最短正常経路は次である。

```text
closed validation plan
  -> 全7 capabilityとrequired evidence fieldを一carrier identityへbind
  -> carrier内部で個別validationを固定順に実行・判定
  -> plan terminalまで途中resultをmodelへ配送しない
  -> 必要な個別terminal resultだけを一度投影
  -> completion consumerが一度判断
```

これは成功runのcommand列を固定する手順ではない。開始前に固定したplan以外へresultを渡せないpermission境界である。

## 2. 保存traceで確認した問題経路

P001 Standard14 N=5は70 / 70件がScore 4だったが、C147比でtoken `+113.73%`、elapsed `+17.04%`だった。prompt bytes差は9 bytesだけだった。

同一Case A02ではC147のmodel response中央値4回に対してP001は7回だった。P001はvalidation plan、個別validation、最終diffの各resultをmodelへ戻し、次validationを新しいmodel判断で発行していた。比較可能な11 Caseでは追加model response数とtoken中央値差の相関は0.804、action前後を分けた35 runではresponse超過の約72%がaction後にあった。

問題経路は次である。

```text
closed validation plan
  -> individual validation result
  -> model-visible consumer
  -> accumulated contextを再消費するmodel response
  -> 次validationの個別発行
```

結果としてrequired effectは満たしても、同じ検証系列でmodel再入とcontext伝播が増えた。

## 3. 既存authorityだけでは閉じない理由

- TaskSpecはrequired validation、pass conditionおよびstop conditionを定められるが、nested tool resultの配送surfaceを定めない。
- repository authorityはexact methodを定められるが、個別resultをmodelへ返すかcarrier-localに保持するかを定めない。
- repository stateは実行結果を供給するが、result consumerとterminal projectionのpermissionを閉じない。
- P001の共通semantic文だけでは、modelが各resultを受け取って次を個別発行するrouteも規則準拠で構成できる。

したがって、TaskSpec条件や自己分類を追加せず、platform capability blockで途中resultのconsumer permissionを閉じる。

## 4. 変更するpredicateと責務境界

P001から変更する全件は次である。

| 変更 | 種類 | 消す具体的な判断または伝播 | 分離不能な理由 |
| --- | --- | --- | --- |
| `validation-plan`を`validation-plan-semantics-r2`へ置換 | 責務分離 | plan semanticsとcarrier手段の混在 | carrierがplan identity、順序、stop dependencyを入力として必要とする |
| `validation-execution`の共通部分を`validation-result-closure-r2`へ置換 | 責務分離 | 実行surfaceとterminal result admissionの混在 | platformを替えても個別resultとcompletionの意味を保持するため |
| `validation-carrier-codex-r2`を追加 | permission閉鎖 | 個別result後のmodel判断、途中context伝播、model loop fallback | Codexの7能力を一組でbindしなければ途中ingressだけを閉じられない |
| required validation非空をcarrier admissionへ追加 | permission限定 | 空planの不要carrier開始 | validationなし正常routeを保持するため |
| 7 capabilityの全件同一identity binding | capability admission | 部分能力surfaceでの開始と事後fallback | 一能力でも欠けると個別identity、fail-fastまたは途中非配送を同時に保証できない |
| required evidenceとdocumented result fieldの事前binding | evidence admission | evidence捏造、carrier外追加read、raw outputからの事後選択 | terminal projectionが必要resultを合法に運ぶため |

既存10 componentとvalidation以外66 primitiveのbytesは変更しない。`frontier`、actor、observation、method、recovery、他platform blockまたはcompact化を同じCandidateへ入れない。

## 5. 実行不能にする問題経路

- validation plan nonterminal中のindividual resultからmodel-visible consumerへのdelivery。
- non-successまたは`unavailable`後に、そのresultへ依存するvalidationを開始するroute。
- nonterminal resultのcontinuation identityを推測、置換または別executionへ再bindするroute。
- issued raw output全体をcompletion resultへ昇格するroute。
- capability欠落、evidence field欠落またはcarrier terminal後に個別model loopへ切り替えるroute。
- required validation 0件でcarrierを開始するroute。

これらを「carrierを選ぶべき」という自己判断で避けるのではなく、carrier admissionとoutput permissionから除外する。

## 6. 維持する正常経路と情報carrier

| 状態 | owner | carrier | consumer | 維持する結果 |
| --- | --- | --- | --- | --- |
| validationなし | completion semantics | carrierなし | completion consumer | 不要なvalidationを開始しない |
| 全件success | Codex carrier | terminal output一件 | completion consumer | 全個別identityとsuccess evidence |
| 途中non-success | Codex carrier | failureと発行不能後続を含むterminal output一件 | completion consumer | failure診断、fail-fast、失敗の非隠蔽 |
| nested invocation nonterminal | 同じcarrier execution identity | 同じcontinuation identity | carrier内部 | 別operationを挟まないterminal化 |
| continuation identity観測不能 | Codex carrier | `unavailable` result | completion consumer | 推測しないfailure closure |
| capabilityまたはevidence field欠落 | platform availability receipt | carrierを開始しない | validation operation | `unavailable`、model loopへfallbackしない |

carrier外の別operationへ停止効果を広げず、追加要求またはresult失効は同じplanの再開ではなく別validation operationとして扱う。

## 7. 増えるcostと非目標

P001 rootは10,781 bytes、静的反例修正後r2は12,922 bytesで、固定instructionは2,141 bytes増える。新たに表示される主な参照は7 capability名、carrier identity、documented result fieldおよびterminal output schemaである。

増分が消す対象は、validation途中のmodel response、蓄積contextの再入力、result対応づけの事後判断およびfallback判断である。これらが減らなければ、2,141 bytesは純増costになる。

非目標は次である。

- C147より短いpromptを作ること。
- frontier carrierを同時に直すこと。
- tool順、command名またはwrapper実装を固定すること。
- Codex以外のplatform対応を主張すること。
- chat向け構成、compact構成、releaseまたはprojectionを作ること。
- model response数やcarrier使用率を第4のKPIにすること。

## 8. 評価境界

### concrete Case materialization前の固定class

本文作成と静的監査に使ったVCR-S01〜S09はtuning evidenceであり、Candidate qualityの選定には使わない。r2本文をこれ以上変更しない境界で、別literal、別validation数、別failure位置および別decoy operationを持つ新しいheld-out revisionを作る。

runtime KPI Caseは次の6件へ固定した。

1. `VCC-H01`: required validationなし。
2. `VCC-H02`: 複数validation全件success。
3. `VCC-H03`: 最初のvalidationがnon-success。
4. `VCC-H04`: 中間validationがnon-successで後続依存validationが未発行。
5. `VCC-H05`: nested validationがnonterminalになった場合のsame identity terminal化。
6. `VCC-H06`: terminal raw outputに不要な追加bytesがあり、必要evidenceだけを投影。

capability一部欠落、continuation identity観測不能、required evidence field欠落は、比較ProfileのruntimeをCaseごとに変えて互換条件を壊さないよう、3件のpreflight negative fixtureへ分離した。これらはformal KPI slotへ数えない。

具体的input、fixture modeとhash、model-invisible oracle、rating contract、response schema、TaskSpecおよびsetは`codex-validation-carrier-heldout-r1-source-freeze-r1`へbind済みである。P002作成前に固定したためP002に対してはblindであった。P002結果を使って次Candidateを設計した後も、同じVCC6を固定benchmarkとして再利用し、prompt identityだけを変えて比較する。その後の結果についてblind性は主張せず、VCC6外へ一般化しない。VCC6のcase ID、model-invisibleなliteral、oracleまたはexpected resultはpromptへ転記しない。

### 評価順序

1. **candidate-only targeted N=1**: 全Caseのvalid、schema、必須field、qualityを確認する。低品質の有効runは再実行しない。
2. **paired targeted N=5**: candidate-onlyが全件採点可能でrequired effectを満たした後、P002候補のmissing slotとP001の全missing slotを、同じcase set、比較条件および共通のグローバルキューで発行する。P002候補とP001をCase別に比較する。
3. **Standard14 N=5**: targetedで品質を維持し、P001比でtokenとelapsedがともに減った場合だけ、P002候補をStandard14へ投影する。C147とP001の保存済み互換resultを再利用する。
4. **N=20拡張**: Standard14 N=5がvalid、70 / 70 Score 4で、P001比のall-agent `total_tokens`と`elapsed_seconds`がともに減った場合だけ、同じimmutable identityと互換条件でP002候補のmissing slotをN=20まで追加する。

Nはatomic run数でありwave数ではない。targeted Caseの結果をStandard14 resultへ合算しない。

### 判定値

| 判定 | 合格条件 | 扱い |
| --- | --- | --- |
| 実行有効性 | 全required slotがvalid、schema-valid、採点可能、必須KPIあり | 不一致なら比較しない |
| 品質 | 各Caseのrequired effectとpreserved effectを満たし、事前ratingで最高score | 個別低scoreを中央値で相殺しない |
| 機序診断 | validation間のmodel-visible ingress、response数、continuation、後続発行、terminal projectionを記録 | 3 KPI差の原因説明に使い、独立KPIにしない |
| 局所cost改善 | 品質維持後、paired targetedでP001比tokenとelapsedがともに減少 | 一方でも増えればcost退行 |
| Standard14 cost回復 | 品質維持後、P001比tokenとelapsedがともに減少 | C147差も残余costとして別記する |
| portable完了候補 | N=20でも品質を維持し、P001比で両costが減り、C147比の残余cost退行がない | これだけで採用・releaseにはしない |

C147比で一方でも高い場合、validation carrier差分の局所効果が成立してもportable full-agentのcost回復は未完了とする。ただし、この残余を同じCandidateへfrontier条件として追加せず、別診断へ分ける。

### 比較互換条件とpreflight

model、reasoning effort、Codex CLI、sandbox、approval、Python、case set、rating、TaskSpec wrapper、token accounting、prompt以外のbundle surface、fixture identity、parallel上限およびrun protocolを一致させる。

さらにP002候補では、次のcapability receiptを比較前にbindする。

- Codex programmatic carrierが利用可能。
- nested execution toolがcarrierからeligible。
- documented terminal status fieldを観測可能。
- nonterminal時にsame continuation identityを観測・指定可能。
- plan terminalまでintermediate resultをmodel-visible consumerへ返さないrouteが利用可能。
- terminal output schemaと必要evidence fieldを固定可能。

一件でも未固定、不一致または未確認なら評価slotを一件も発行しない。実行後に参考値へ降格しない。

## 9. 停止条件

次のいずれかで該当段階を停止する。

- concrete held-out identity、oracle、rating、schemaまたはhashが未固定。
- Candidate outputと管理用r2 outputのbyte bindingが不一致。
- capability receiptが欠落、不一致または対象Profileへbind不能。
- preflightでprompt以外の互換条件が一件でも不一致。
- invalid、採点不能、schema不一致または必要KPI欠落。
- required validation欠落、failure無視、result identity喪失、必要evidence欠落、依存validationの誤発行、正常な非依存operationの過剰停止または完了状態の誤りがqualityへ現れる。
- 品質維持後、比較対象に対してtokenまたはelapsedの一方でも増える。
- N拡張時に個別低scoreまたは互換条件driftが一件でも生じる。

model-visible ingressまたはresponse数だけの不一致は、利用者要求またはrating対象のrequired effect欠落を直接示さない限り、それ単独で評価全体を停止しない。原因診断として保持し、3 KPIの判定を置き換えない。

## Candidate作成可否

設計項目1〜9とconcrete held-out sourceを固定し、新targetのmaterializer、grader、trace診断、capability preflight、qualification-only実行entrypointおよびall-agent token accounting contractを固定した。control-free N=1は6件すべてvalidで3 KPIを取得し、測定経路をqualificationした。Score 2と1はcontrol-freeの観測結果として再実行せず保持する。append-only registrationは次のProfile classを`candidate_only_p002_gate`だけに限定している。P002 bundleはP001直接親とCandidate用compositionへbind済みであり、現在判定は`p002_candidate_created_not_evaluated`である。

次に許可する作業は、固定済み一差分からP002 bundleを作成し、target固有の`candidate_only_p002_gate` Profileとpreflightを作ることである。P001とのpaired comparison、Standard14投影、releaseまたはruntime projectionは、P002 candidate-only quality・mechanism gate通過前には作成しない。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`P001 Standard14 N=5機能block別cost診断`](p001-standard14-n5-functional-block-cost-diagnostic.md)
- [`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)
- [`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)
- [`P001後続 Codex validation carrier composition draft r2`](p001-codex-validation-carrier-composition-draft-r2.md)
- [`P001後続 Codex validation carrier静的反例監査 r1`](p001-codex-validation-carrier-static-counterexample-audit-r1.md)
