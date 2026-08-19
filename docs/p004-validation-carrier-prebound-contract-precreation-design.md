# P004 validation carrier prebound contract作成前設計

> [!IMPORTANT]
> **状態**: `task_objective_fixed / direct_parent_p001 / p002_p003_counterexamples_not_parents / validation_ownership_move_only / vcc6_fixed / prompt_only / static_counterexample_passed / candidate_bundle_created / n1_valid_6 / score4_5_score1_1 / candidate_gate_failed / n5_not_authorized`
>
> 本書はP004のCandidate作成前gateを固定する。静的反例監査を通過するまで、Candidate bundle、評価Profileまたは評価slotを作成しない。

## 結論

P004はP001 `portable-semantic-c147-portable-full-agent-r1`を直接の実装親とし、P001のvalidation functional blockだけを置換する。P002とP003の全文は継承しない。

一つの再構成目的は、taskごとのcarrier admission判断をなくし、次の二つの責任を一度だけ固定することである。

```text
validation_plan_identity
:= validation identities / order / pass conditions / stop dependencies /
   methods / required terminal evidence / terminal output schema

codex_carrier_contract
:= one registered carrier execution identity /
   ordered individual execution / local result check / fail fast /
   intermediate ingress denial / terminal projection / continuation /
   documented result-field mapping
```

`codex_carrier_contract`はCodex機能ブロックの適用によって事前に成立済みとし、operationごとにcapability、availability、result fieldまたはprojection contractを再判定・再bindしない。required validationが一件以上ありplanがreadyなら、固定済みplan identityを登録済みcarrierへ一度だけ渡す。

## 1. task objectiveと直接の基準

- target改善系列: Portable full-agentのvalidation実行効率改善。
- required effect: 個別validation、固定順、局所result判定、依存先fail-fast、同一identity continuation、中間model ingress拒否、terminal一回投影を維持する。
- preserved effect: P001の非validation 66 primitive、TaskSpec、repository authority、VCC6 Case、oracle、rating、runtimeおよび評価方法を変更しない。
- artifact relation: 管理用componentを一枚の`AGENTS.md`へ構成し、target固有Candidate bundleへbyte一致で固定する。
- 直接の実装親: P001 `portable-semantic-c147-portable-full-agent-r1`。
- 失敗反例: P002のplan field再bindと、P003のtaskごとのcapability・projection admission再判定。両者は直接親ではない。

P001基準の最短正常routeは、action後に必要なvalidationを一つのplanへ固定し、利用可能な実行手段で個別に実行し、全result受領後に一度だけ完了を判断するrouteである。P004ではCodex機能ブロックが適用される場合の実行手段を、登録済みcarrier一つへ限定する。

## 2. 保存済みtraceで確認した問題route

[`vcc6-p001-p002-p003-shared-runner-n1-result-r1`](../evaluations/targets/codex-validation-carrier-conformance/results/vcc6-p001-p002-p003-shared-runner-n1-result-r1.json)では、P003は6 / 6件でScore 4と対象機序を維持し、P002比でtokensを10.39%減らした一方、elapsedは5.64%増えた。N=1なので安定傾向とは扱わない。

traceでは、P003がH02からH06のvalidationケースでcarrier invocation前に`validation_plan_state=unavailable`相当の暫定出力を生成した。H02ではP003のoutput tokensがP002より333、reasoning output tokensが306多く、action完了からcarrier発行まで約21.6秒を要した。H04の遅延は生成量で説明できず、実行ばらつきを含む。

確認した問題routeは次である。

1. plan readiness成立後も、7 capabilityとterminal projection contractをtaskごとにcarrier identityへbindし直せる。
2. carrier invocation resultがない段階で、モデル自身のcapability判定からvalidation `unavailable`を生成できる。
3. その暫定状態の後でもcarrierを開始でき、同じvalidation operationについてadmission判断が二回生じる。

## 3. 問題routeを許したpermissionとdependency

P003 `VALIDATION_CARRIER_CODEX`は、carrier inputをplan identityへ狭めた一方で、開始条件として7 capabilityとterminal projection contractのtaskごとのbindingを要求した。この条件は、固定platform blockの存在だけでは開始できず、モデルの再判定を経由しなければcarrier permissionへ到達できる構造である。

TaskSpecとVCC6 fixtureはvalidation planを与えるが、platform carrier能力の所有者ではない。repository stateもtaskごとのcapability再判定を禁止しないため、promptのplatform機能ブロックでcarrier contractの所有と`unavailable` resultのproducerを限定する必要がある。

## 4. 変更する条件と責任範囲

変更は一つの責任移動として、二componentを同時に置換する。

| 条件 | 変更 | 所有する責任 | 消すroute |
| --- | --- | --- | --- |
| validation plan | terminal evidenceとterminal output schemaをplan作成時に固定し、plan identityへ含める | task固有validation内容と投影要求 | carrier開始時のprojection contract再構成 |
| Codex carrier contract | block適用時点でcarrier identity、capability一式、documented result-field mappingを成立済みとする | platform固有の実行・transport能力 | taskごとのcapability列挙とavailability自己判定 |
| unavailable result | carrier invocationのterminal resultだけをproducerにする | 実際のcarrier不在・不能 | invocation前の暫定`unavailable`生成 |

validation plan側だけを変えるとplatform能力の再判定が残り、carrier側だけを変えるとtask固有のprojection要求を開始時に組み立て直す必要が残る。したがって、このownership moveは分離できない一つの再構成目的として扱う。

## 5. 実行不能にする問題route

P004では次をprompt準拠で構成不能にする。

- plan ready後に、carrier admission用としてplan fieldを展開、再分類、再構成または再bindする。
- operationごとにcarrier capability集合、availabilityまたはdocumented result fieldを判定する。
- carrier invocation resultなしにvalidation `unavailable`を生成する。
- 暫定`unavailable`を外へ投影してから同じvalidation planを開始する。
- carrier不成功後に個別model発行またはshell compound commandへfallbackする。
- terminal後に同じplanを別routeで再開する。

成功runのcommand、tool順、model stepまたはCase literalは転記しない。

## 6. 維持する正常routeとcarrier

- required validationが0件ならcarrierを開始しない。
- plan readiness前はcarrierを開始しない。
- plan readyかつrequired validationが一件以上なら、plan identityを登録済みcarrierへ一度だけ渡す。
- carrier内で各validationを個別nested invocationとして固定順に実行する。
- non-successまたは`unavailable`の停止効果は固定済みdependency先だけへ適用する。
- nonterminal resultは同じcontinuation identityだけでterminal化する。
- plan nonterminal中は中間出力をcarrier-localに保持する。
- plan terminal時だけ、planに固定済みの必要evidenceとschemaに従って一度投影する。
- 実際のcarrier invocationが`unavailable`を返した場合はそのresultを保持し、別routeで補完しない。

情報の所有は、task固有planをPortable validation block、platform能力とresult-field mappingをCodex block、実行中resultをcarrier、最終完了判断をresult consumerが持つ。

## 7. 新しく増える判断と対象外への影響

task実行時に新しい判断、ticket、自己分類または例外を追加しない。逆に、7 capabilityの列挙、projection contractの別binding、invocation前availability判定を削除する。

変更対象外ではP001の非validation component bytesを保持する。H01のvalidationなし、H03/H04のfail-fast、H05のcontinuation、H06のterminal evidenceを個別最適化しない。

## 8. 評価条件と診断

固定benchmark VCC6を変更せず再利用する。Case、fixture、TaskSpec、oracle、rating、model、reasoning、Codex CLI、permission、executor、token accounting、集計方法および`max_workers=24`を固定し、実験変数をP004 prompt identityだけにする。

1. 静的反例監査で一般classを確認する。
2. candidate-only VCC6 N=1で6 missing slotだけを発行する。
3. N=1がvalid、全件Score 4かつ必要resultを維持した場合だけ、P004の残りslotを加えてN=5へ進む。
4. P001/P002/P003の保存済み互換runを再実行せず比較へ使う。

N=1のelapsed差だけで安定傾向を主張しない。carrier invocation前のmodel-visible response、action完了からcarrier発行までの区間、input/output/reasoning tokens、command数およびcarrier bytesは3 KPI差の原因診断に限定する。

## 9. 停止条件

- 静的監査でtaskごとのcapability再判定、pre-invocation `unavailable`、plan再bind、途中ingress、依存先誤発行、evidence補完、fallbackまたはterminal後再開が残る。
- 正常routeに必要なvalidation identity、pass condition、stop dependency、continuation、terminal evidenceまたはschemaが失われる。
- preflightでprompt identity以外の互換条件が一致しない。
- invalid、採点不能、必要KPI欠落、schema不一致または個別Score 4未満がある。
- N=5でP001比tokensまたはelapsedの一方が増える。

停止後にP004へ条件を追加せず、P001のvalidation boundaryへ戻り、P002/P003/P004をそれぞれ反例として保持する。

## Candidate作成可否

task objective、直接親、反例、ownership move、閉じるroute、正常carrier、評価条件および停止条件を固定した。管理用r4 draftの静的反例監査は13 classでblocking counterexample 0件、validation primitive 15 / 15件を確認した。

静的gate通過後、同一bytesをP004 Candidate compositionと自己完結した一枚のbundleへ固定し、bundle bindingとdependency closureを検証した。

後続のcandidate-only VCC6 N=1は6 / 6件validだったが、H06がScore 1・mechanism failureとなった。事前停止条件によりP004は停止し、N=5、Standard14、採用、releaseまたはprojectionを許可しない。原因は[`P004 VCC6 N=1結果とroute監査`](p004-vcc6-n1-result-and-route-audit.md)へ分離する。
