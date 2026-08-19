# P005 validation terminal projection ownership作成前設計

> [!IMPORTANT]
> **状態**: `task_objective_fixed / direct_parent_p001 / p002_p003_p004_counterexamples_not_parents / terminal_projection_ownership_only / vcc6_fixed / prompt_only / candidate_not_created`
>
> 本書はP005のCandidate作成前gateを固定する。14 classの静的反例監査でblocking counterexampleが0件となったため、Candidate bundle作成を許可した。評価slotは比較preflight成立後だけ発行する。

## 結論

P005はP001 `portable-semantic-c147-portable-full-agent-r1`を直接の実装親とし、P001のvalidation functional blockだけを置換する。P002、P003およびP004の全文は継承しない。

一つの再構成目的は、carrier内のraw nested resultと外部へ渡せるterminal projectionのproducer permissionを分離することである。

```text
nested_result
:= nested invocationが返すraw output / terminal field / continuation identity
   owner=carrier-local
   outer_projection_permission=false

terminal_projection_ready
:= plan terminal
 ∧ 開始済みvalidationのidentity / terminal status / pass判定 / 必要evidenceがbind済み
 ∧ 未開始identityと理由がbind済み
 ∧ 固定済みterminal output schemaに適合

terminal_projection
:= terminal_projection_readyを満たすcarrier生成object
   owner=carrier
   outer_projection_permission=true_once
```

raw nested result、途中状態またはモデルが作った暫定状態はouter outputのproducerになれない。required validationが一件以上ありplanがreadyなら、固定済みplan identityを登録済みcarrierへ一度渡す。capability、availabilityまたはprojection contractを別admission operationで再判定しない。

## 1. task objectiveと直接の基準

- target改善系列: Portable full-agentのvalidation実行効率改善。
- required effect: 個別validation、固定順、局所result判定、依存先fail-fast、同一identity continuation、中間model ingress拒否、必要evidenceだけのterminal一回投影を維持する。
- preserved effect: P001の非validation 66 primitive、TaskSpec、repository authority、VCC6 Case、oracle、rating、runtimeおよび評価方法を変更しない。
- artifact relation: 管理用componentを自己完結した一枚の`AGENTS.md`へ構成し、target固有Candidate bundleへbyte一致で固定する。
- 直接の実装親: P001 `portable-semantic-c147-portable-full-agent-r1`。
- 反例: P002のfield再bind、P003のtaskごとのadmission再判定、P004のraw result外部投影とpre-invocation暫定`unavailable`。いずれも直接親ではない。

P001基準の最短正常routeは、action後にvalidation planを一度固定し、必要なvalidationを個別に実行し、全result受領後に一度だけ完了を判断するrouteである。P005ではCodex carrier内のraw resultを局所保持し、carrierがterminal projectionを一度だけ生成する。

## 2. 保存済みtraceで確認した問題route

[`P004 VCC6 N=1結果とroute監査`](p004-vcc6-n1-result-and-route-audit.md)は、H06で次を確認した。

- required action、event logおよびfinal responseはoracleとexact一致した。
- nested validationは8,672 bytesのraw outputを返した。
- P004 carrierはnested command result object全体をJSON化し、outer custom tool outputへ投影した。
- forbidden raw outputが一度modelへ配送されたためScore 1、mechanism failureとなった。
- carrier invocation前の`validation_plan_state=unavailable`相当の暫定responseも残った。

問題routeは、raw nested resultまたはモデル生成の暫定状態が、plan terminal projectionと同じouter output permissionを持てたことである。

## 3. 問題routeを許したpermissionとdependency

P004はplatform contractとdocumented result-field mappingを成立済みと宣言したが、次を固定しなかった。

- raw nested resultのownerと可視範囲。
- raw resultからterminal projectionへの一方向dependency。
- outer outputを生成できるresult kind。
- invocation前の暫定状態がouter responseを生成できないpermission。

そのため、raw invocation result objectをouter carrier resultとして返し、後からmodelがfinal responseを整えるrouteがprompt準拠で残った。TaskSpec、repository authorityおよびfixtureはexpected outcomeを固定するが、carrier内部resultのouter projection permissionを制限しない。

## 4. 変更する条件と責任範囲

変更はterminal projection ownershipを成立させる一つの構造として、validation planとCodex carrierの二componentを同時に置換する。

| 条件 | 所有する責任 | 所有しない責任 |
| --- | --- | --- |
| immutable plan | validation identity、順序、pass condition、stop dependency、method、必要evidence、terminal schema | carrier capability、raw result transport |
| nested result locality | raw output、terminal field、continuation identityのcarrier-local保持 | outer response、完了判断 |
| terminal projection | planへbind済みのstatus、pass、必要evidence、未開始identityと理由だけを一objectへ構成 | raw output全体、validation追加 |
| outer projection permission | terminal projection objectだけを一度外へ渡す | raw nested result、暫定状態、途中progress |

planだけを変えるとraw resultのouter permissionが残り、carrierだけを変えると必要evidenceとschemaのownerが未固定になるため、このownership moveは分離できない。

## 5. 実行不能にする問題route

P005では次をprompt準拠で構成不能にする。

- raw nested result、command result objectまたはraw outputをouter carrier outputへ渡す。
- raw resultを外へ出した後にmodelがterminal responseを再構成する。
- plan terminal前にvalidation state、`unavailable`、progressまたは暫定responseをouter outputへ投影する。
- plan fieldをcarrier admission用に展開、再分類、再構成または再bindする。
- operationごとにcarrier capability、availabilityまたはfield mappingを自己判定する。
- carrier不成功後に個別model発行またはshell compound commandへfallbackする。
- terminal後に同じplanを別routeで再開する。

成功runのcommand、wrapper code、tool順、model step、Case IDまたはraw noise literalは転記しない。

## 6. 維持する正常routeと情報carrier

- required validationが0件ならcarrierを開始しない。
- plan readiness前はcarrierを開始しない。
- plan readyかつ一件以上なら、plan identityを登録済みcarrierへ一度だけ渡す。
- carrier内で各validationを個別nested invocationとして固定順に実行する。
- raw output、terminal fieldおよびcontinuation identityはcarrier-localに保持する。
- terminal fieldからstatusを判定し、必要evidenceだけを固定済みplanへbindする。
- non-successまたは`unavailable`の停止効果を依存先だけへ適用する。
- nonterminal resultは同じcontinuation identityだけでterminal化する。
- plan terminal時にterminal projection objectを一度生成し、それだけをouter outputへ渡す。
- terminal projection受領後、result consumerが一度だけ完了を判断する。

## 7. 新しく増える判断と対象外への影響

task実行時の新しい自己分類、ticket、Case分岐または例外を追加しない。新しい境界はresult kindのproducer permissionだけである。

P003のtaskごとのcapability・projection contract再bindingは復活させない。P004の`registered contract`宣言だけにも依存しない。変更対象外ではP001の非validation component bytesを保持する。

## 8. 評価条件と診断

固定benchmark VCC6を変更せず再利用する。Case、fixture、TaskSpec、oracle、rating、model、reasoning、Codex CLI、permission、executor、token accounting、集計方法および`max_workers=24`を固定し、実験変数をP005 prompt identityだけにする。

1. 14 classの静的反例監査。
2. candidate-only VCC6 N=1のfresh 6 slot。
3. N=1がvalid、全件Score 4かつrequired effectを維持した場合だけN=5を許可する。
4. P001〜P004の保存済みrunを再実行しない。

raw output bytes、outer projection count、pre-invocation response、input/output/reasoning tokens、command数およびaction完了からcarrier発行までの区間は3 KPI差の原因診断に限定する。N=1だけで安定傾向を主張しない。

## 9. 停止条件

- 静的監査でraw result外部投影、pre-terminal response、plan再bind、capability再判定、途中ingress、依存先誤発行、evidence補完、fallbackまたはterminal後再開が残る。
- 必要なvalidation identity、pass condition、stop dependency、continuation、terminal evidenceまたはschemaが失われる。
- preflightでprompt identity以外の互換条件が一致しない。
- invalid、採点不能、必要KPI欠落、schema不一致または個別Score 4未満がある。
- N=5でP001比tokensまたはelapsedの一方が増える。

停止後にP005へ条件を追加せず、P001へ戻りP002〜P005を反例として保持する。

## Candidate作成可否

task objective、直接親、反例、ownership、閉じるroute、正常carrier、評価条件および停止条件を固定した。[静的反例監査](p005-validation-terminal-projection-ownership-static-counterexample-audit-r1.md)は14 classすべてを確認し、blocking counterexample 0件となった。P005 Candidate bundleの作成を許可する。
