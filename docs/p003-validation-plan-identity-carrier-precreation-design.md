# P003 validation plan identity carrier作成前設計

> [!IMPORTANT]
> **状態**: `task_objective_fixed / direct_parent_p001 / p002_counterexample_not_parent / c147_comparison_reference / validation_block_single_replacement / vcc6_fixed / prompt_only / static_counterexample_passed / candidate_bundle_created / shared_runner_n1_valid_score4_mechanism_passed / n5_allowed / no_stability_claim`
>
> 本書はP003の作成前gateを固定した設計記録である。後続の静的gate通過後にCandidate bundleを作成したが、Profile、dispatch plan、評価slot、releaseまたはprojectionではない。

## 結論

P003はP001を直接の実装親とし、P001のvalidation functional blockだけを、immutableなplan identityを直接carrierへ渡す構造へ置換する。P002全文へ修正条件を追加せず、P002はvalidation閉鎖の成立証拠と、carrier admission用の項目別再bindが生成costを増やした反例として使う。

設計する一差分は次である。

```text
carrier_input_ready
:= validation_result_closure_ready
 ∧ immutable_validation_plan_identityがbind済み
 ∧ terminal_projection_contractがbind済み
 ∧ required carrier capabilityが一つのexecution identityへbind済み

carrier_input
:= immutable_validation_plan_identity + terminal_projection_contract
```

bind済みplanのvalidation identity、method、pass condition、順序またはstop dependencyを、carrier admission用に再分類、再構成または再bindするrouteは許可しない。planに必要fieldが欠ける場合は既存plan readinessが成立しないのであり、carrier側で補完しない。

## 1. 直接の基準と正常な最短route

- 直接の実装親: P001 `portable-semantic-c147-portable-full-agent-r1`。
- 比較参照: C147 `the-caption-3ce91a4-result-effect-scope-r1`。
- 失敗反例: P002 `p002-portable-full-agent-codex-validation-carrier-r1`。
- 固定benchmark: VCC6 `codex-validation-carrier-heldout-r1` revision `r1`。

正常な最短routeは、action後に一度固定したvalidation plan identityとterminal projection contractを一つのcarrier identityへ直接渡し、carrier内で個別validation、局所判定、依存先fail-fastおよび同一identity continuationを行い、plan terminal時に必要fieldだけを一度投影するrouteである。

P002から全文、文順またはcarrier inputの項目別bindingを継承しない。P002で成立した効果はrequired effectとして再固定し、P001からの一つのvalidation block置換で実現する。

## 2. 保存済みtraceで確認した問題route

[`P002 VCC6 cost再進入原因監査`](p002-vcc6-cost-reentry-causal-audit.md)は、P002の30 runでP001比output tokensが13,726、reasoning output tokensが4,447、elapsedが86.477秒増えたことを確認した。command output bytes差は300 bytes、carrier event bytes差は0である。

問題routeは、固定済みplan全体をcarrier identityへbindした後、その構成fieldをcarrier input用に項目別に再bindできるrouteである。その結果はvalidation commandまたはterminal bytesの増加ではなく、model生成側の追加処理として観測された。

## 3. 問題routeを許したdependency

P002 `VALIDATION_CARRIER_CODEX`は、次を同時に要求する。

- 固定済みplan全体を一つのcarrier execution identityへbindする。
- 固定順のvalidation identity、個別method、pass conditionおよびstop dependencyをcarrier inputへ再びbindする。
- 必要terminal evidence、documented result fieldおよびterminal schemaを開始前にbindする。

二番目は一番目のimmutable identityを別表現へ展開するdependencyである。三番目は過剰投影と観測不能evidenceを閉じる独立責任なので維持する。

## 4. 変更する条件と責任範囲

変更対象はP001のvalidation functional block一件だけとする。

| 条件 | 変更 | 所有する責任 | 所有しない責任 |
| --- | --- | --- | --- |
| plan semantics | P002で実証した順序、pass condition、stop dependency、terminal条件を一つのimmutable identityへ固定 | validation planの内容と完了条件 | Codex capability、terminal field transport |
| result closure | 個別terminal resultと完了判断をplan identityへ対応付ける | result binding、欠落時nonterminal | carrier API、tool順 |
| Codex carrier | plan identityとterminal projection contractだけを入力にする | 途中ingress deny、局所判定、fail-fast、continuation、一回投影 | plan fieldの再分類、再構成、再bind |
| terminal projection contract | 必要evidence、documented result field、terminal schemaを開始前に固定 | 観測可能性と出力範囲 | validationの追加選択、pass condition作成 |

validation以外のP001 component、TaskSpec、repository authority、Case、rating、runtimeおよび評価基盤は変更しない。

## 5. 実行不能にする問題route

P003では次をprompt準拠で構成不能にする。

- plan identityを受領した後、そのfieldをcarrier admission用に列挙または再bindする。
- planの欠落fieldをcarrier側で補完する。
- terminal projection contractをplan fieldの再構成から推測する。
- capability欠落時に個別model発行またはshell compound commandへfallbackする。
- carrier terminal後に同じplanを個別model発行routeで再開する。

単に「簡潔に処理する」「必要な場合だけ展開する」とは書かない。展開の要否をモデルへ判断させず、carrierが受け取れる入力を二つのidentityへ限定する。

## 6. 維持する正常route

- required validationが0件ならcarrierを開始しない。
- plan readiness前はcarrierを開始しない。
- 必要evidenceをdocumented result fieldへbindできなければ`unavailable`とし、補完しない。
- 7 capabilityを一つのcarrier identityへ全件bindできなければ`unavailable`とし、fallbackしない。
- 各validationを個別identityとして扱い、non-successまたは`unavailable`の停止効果を依存先だけへ限定する。
- nonterminal resultは同じcontinuation identityだけでterminal化する。
- plan terminal時に必要evidenceだけを一つのterminal outputへ投影する。
- validation以外の独立operationへ停止効果を広げない。

## 7. 新しく増える判断と対象外への影響

新しい自己分類、ticket、label、Case分岐またはtool順を追加しない。plan identityとterminal projection contractは既に必要な二責任の境界名であり、modelがvalidation種別を選ぶ分類には使わない。

変更対象外ではP001 bytesとcomponent relationを保持する。H01のcarrier非開始、H05のcontinuation、H06の必要field projectionを個別最適化せず、同じ二identity入力で扱う。

## 8. 評価条件

VCC6を固定benchmarkとしてそのまま再利用し、実験変数をP003 prompt identityだけにする。Case ID、fixture、TaskSpec、oracle、rating、model、reasoning、Codex CLI、permission、executor挙動、token accounting、集計方法および`max_workers=24`を変更しない。

評価は次の順とする。

1. 静的反例監査: P002で使った一般的な9 classにplan再構成とplan field欠落の2 classを加えた11 classへP003設計を適用し、誤routeと正常routeを確認する。Case literalやexpected resultを本文へ入れない。
2. candidate-only VCC6 N=1: P003の6 missing slotだけを発行する。
3. VCC6 N=5: N=1通過後、P003の残り24 slotだけを発行し、P001/P002の保存済み各30 runを再利用する。
4. Standard14 N=5: VCC6 gate通過後だけ、固定済みStandard14でP003のmissing slotを発行し、C147/P001の互換resultを再利用する。
5. N=20: Standard14 N=5通過後だけ、同じimmutable identityと互換条件でP003のmissing slotを追加する。

VCC6の主gateは、P003が30 / 30件でScore 4を維持し、P001比でall-agent `total_tokens`と`elapsed_seconds`がともに減少することとする。P002比も併記し、P002で得たtoken減少を失って時間だけ短縮する交換にはしない。mechanism、output tokens、reasoning、command数およびresponse数は3 KPI差の原因診断に限定する。

## 9. 停止条件

次のいずれかで該当段階を停止する。

- 静的監査で項目別再bind、evidence補完、capability部分集合開始、途中ingress、依存先誤発行、identity喪失、raw output過剰投影またはfallbackがprompt準拠で残る。
- immutable plan identityの直接入力によって必要なvalidation identity、pass判定、stop dependency、continuationまたはterminal evidenceが失われる。
- preflightでprompt identity以外の互換条件が一件でも異なる。
- invalid、採点不能、schema不一致、必要KPI欠落または個別Score 4未満が一件でもある。
- VCC6 N=5でP001比tokenまたはelapsedの一方でも増える。
- Standard14またはN=20で事前の品質・cost条件を満たさない。

停止後に同じP003へ条件を追加せず、P003を反例としてP001のvalidation boundaryへ戻る。

## Candidate作成可否

task objective、直接親、失敗反例、変更対象、正常route、評価条件および停止条件を作成前に固定した。immutable plan identityの直接入力が11 classすべてで必要情報を維持し、項目別再bindを実行不能にする静的反例監査も完了した。

静的反例監査は11 classでblocking counterexample 0件、validation primitive 15 / 15として通過した。その後、管理用renderとbyte一致するP003 Candidate bundleを作成し、target固有bindingまで検証した。Candidate名を持たない共通runnerでP001、P002、P003のfresh N=1を実行し、P003は6 / 6件valid、Score 4、mechanism passとなった。N=1のcost差は安定傾向とせず、次に許可するのは同じ固定runnerとVCC6によるN=5だけである。
