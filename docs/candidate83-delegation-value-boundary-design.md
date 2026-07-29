# Candidate83: delegation value boundary

## 結論

Candidate83は、Candidate82を直接親とし、root `AGENTS.md`の`OWNER_ROLE`にある「TaskSpecが独立producer executionを明示した場合だけworkerを起動する」predicateを、AIがWorkerの正味価値を実行前に確定する`delegation_value_ready`へ置換する。

Workerの起動可否をTaskSpecの明示指定だけへ限定しない。一方、criterion owner語列だけによる起動、rootと同じpredicateの再実行、既知contextの逐次再取得にはWorker価値を認めない。

## Identity

| 項目 | Candidate82 | Candidate83 |
| --- | --- | --- |
| prompt identity | `the-caption-3ce91a4-producer-gate-deduplication-r1` | `the-caption-3ce91a4-delegation-value-boundary-r1` |
| full bundle target | 19 path | 19 path |
| changed target | — | root `AGENTS.md`のみ |

## Candidate作成前gate

1. **基準prompt set**: Candidate82 `the-caption-3ce91a4-producer-gate-deduplication-r1`を直接親とする。
2. **最短正常経路**: rootが既に必要なsourceとtestを持つF02 / F04では、実装、静的確認、required validationをroot一つのproducerで閉じる。明示独立producerを要求するD01では指定workerを起動し、rootはpredicateを再実行しない。広い独立operationがある場合、AIは並列化、context分割、独立性、worker固有capabilityの価値からWorkerを選べる。
3. **保存済み誤経路**: Candidate82 B20のF02とF04各1件は、rootが対象sourceを読んで実装した後、同じsource、test、diffを読むchildを逐次起動した。2 runは各case 100件中tokenとelapsedが最大で、childは新しい問題、修正、reworkを生まなかった。
4. **既存入力だけでは防げない理由**: 現行`OWNER_ROLE`は明示producer指定だけを許可するためAIの裁量を過剰に制限する一方、保存traceでは`owner=independent ... check`を明示指定へ誤変換した。明示有無だけではWorkerの正味価値を表せない。
5. **置換するpredicate**: `OWNER_ROLE`の明示producer限定predicateを、`delegation_value_ready`一つへ置換する。
6. **消す判断点**: criterion ownerからworker指定を推測する判断、TaskSpecの明示有無だけで委譲を禁止する判断、root既知contextを逐次childへ再取得させる判断を消す。
7. **新規cost**: Worker resultの用途、rootとのpredicate重複、価値根拠の確認が増える。価値根拠は「明示独立性、相互非依存operationの並列化、root context再処理の削減、worker固有capability」の一つの限定列挙へ閉じ、新labelは追加しない。
8. **品質維持範囲**: 最初のtargeted gateはF02、F04、D01とする。F02 / F04は成果とrequired validationを維持し、root既知contextの逐次再確認だけを目的とするchildを0件にする。D01は指定worker、terminal result binding、root非再実行を維持する。AI裁量による正の委譲はA06を別diagnosticとして扱い、targeted品質gateへ混ぜない。
9. **停止条件**: score `4`未満、required validation欠落、許可外drift、D01 worker欠落、terminal result誤binding、rootによるD01 predicate再実行、またはF02 / F04で価値根拠のない逐次重複workerが1件でもあれば停止する。Worker数そのものやTaskSpecの明示有無だけでは停止しない。

## 置換predicate

`delegation_value_ready`は次をすべて要求する。

1. Worker resultを未完了criterionまたは未発行invocationのdecision boundaryへbindできる。
2. rootが同じpredicateを実行しない。
3. TaskSpecが要求する独立性、相互非依存operationの並列化、root context再処理の削減、worker固有capabilityのいずれかが成立する。

criterion owner語列だけではこの状態を成立させない。`delegation_value_ready=false`ならrootをproducerへbindする。trueなら、Workerのtask identityを起動前に固定し、既存の`delegated_result_ready`でresult provenanceを検証する。

## 評価境界

- Candidate artifactの作成は、targeted評価済み、採用済み、release済み、本体反映済みを意味しない。
- F02 / F04 / D01は同一setではないため、各resultを別のcompatibility comparisonとして扱う。
- A06はAI裁量の正例候補だが、既存resultがdiagnostic-onlyで条件も重いため、F02 / F04 / D01のtargeted gate通過後に別判断する。
- Candidate82 B20の公式resultと`stopped`履歴は変更しない。

## 評価結果

[`Rating v14 Medium F02 N=5`](../evaluations/results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md)は5 / 5 valid・rateable・score `4`だった。一方、5 / 5で独立contract check Workerを起動し、1 runは同じ確認を2人目へ再割当てした。合計6 child session、child token合計503,695である。

「TaskSpecが独立性を要求」を`owner=independent contract check`から成立させ、後続の「criterion owner語列だけでは成立させない」を迂回した。停止条件に従いCandidate83を`targeted_f02_evaluated / stopped`とし、F04、D01、A06、標準14、採用、release、本体反映は実施しない。

## 2026-07-28の現在解釈

当時の一次resultと`stopped`判定は変更しない。一方、後続の[`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により、Worker起動を独立停止条件にした判定基準は採用しない。

C83は5 / 5 score `4`で品質を満たした。child tokenは全体の22.74%、同一確認の再割当ては1 runだった。互換root-only baselineと事前固定したtoken / elapsed toleranceがないため、現在stateは`quality_passed / cost_control_not_demonstrated`とする。Workerが起動したこと自体を失敗理由にしない。
