# Candidate84: delegation marginal-value boundary

## 結論

Candidate84はCandidate83を直接親とし、root `AGENTS.md`の`OWNER_ROLE`だけを変更する。

Candidate83の`TaskSpecが独立性を要求`という語義判定を削除する。代わりに、Workerがrootと重複しない専有scopeを持ち、別execution identity、並列化、context分離、固有capability、未解決判断のいずれかに実質的な価値がある状態を要求する。

## Identity

| 項目 | Candidate83 | Candidate84 |
| --- | --- | --- |
| prompt identity | `the-caption-3ce91a4-delegation-value-boundary-r1` | `the-caption-3ce91a4-delegation-marginal-value-boundary-r1` |
| full bundle target | 19 path | 19 path |
| changed target | — | root `AGENTS.md`のみ |

## Candidate作成前gate

1. **基準prompt set**: Candidate83 `the-caption-3ce91a4-delegation-value-boundary-r1`を直接親とする。
2. **最短正常経路**: F02ではrootが既に取得したsource、test、diffをWorkerへ再読させず、root一つのproducerで成果とrequired validationを閉じる。D01では、成果成立条件が別execution identityのresultを要求するため指定Workerを起動し、rootは同じpredicateを再実行しない。将来の別taskでも、並列化、context分離、固有capability、未解決判断のいずれかに実質的価値があればAIがWorkerを選べる。
3. **保存済み誤経路**: Candidate83 F02 N=5は品質score `4`を5 / 5で維持したが、5 / 5で不要なWorkerを起動した。合計6 child session、child token 503,695であり、1 runでは同じ確認を2人目へ再割当てした。
4. **既存入力だけでは防げない理由**: Candidate83は`criterion owner語列だけでは`起動条件を満たさないとしたが、実行modelは`owner=independent contract check`を`TaskSpecが独立性を要求`へ言い換えた。この語義判定により、後段の除外規則を迂回できた。
5. **置換するpredicate**: `OWNER_ROLE`の`delegation_value_ready`だけを、専有scopeと限界価値を表すstateへ置換する。新しいtop-level labelは追加しない。
6. **消す判断点**: `independent`という語、criterion owner、risk owner、独立確認という作業名から別execution identityの必要性を推測する判断を消す。root取得済みevidenceの再読と、同一predicateの別Workerへの再割当ても起動根拠から除く。
7. **新規cost**: `exclusive_worker_scope_ready`、`separate_identity_required`、`parallel_gain_ready`、`context_gain_ready`、`capability_gain_ready`、`unresolved_judgment_gain_ready`の6 stateを確認する。参照先はTaskSpec、outcome authority、rootの実行済み／予定scope、既存evidenceに限定する。
8. **品質維持範囲**: 評価順はF02 N=5、F04 N=5、D01 N=5とする。F02 / F04はscore `4`とrequired validationを維持し、重複Workerを0件にする。D01は指定Worker、terminal result binding、root非再実行を維持する。A06はAI裁量の正例を観測する別diagnosticであり、targeted品質gateへ混ぜない。
9. **停止条件**: score `4`未満、required validation欠落、許可外drift、またはF02 / F04でWorkerが1件でも起動した場合は停止する。D01ではWorker欠落、terminal result誤binding、rootによる同一predicate再実行があれば停止する。

## 置換predicate

`delegation_value_ready`は、まずWorkerのpredicateが未実行であり、rootが同じpredicateを実行済みでも実行予定でもないことを要求する。その上で、次のいずれか一つを要求する。

1. outcome authorityが別execution identityのresultを成果成立条件にする。
2. 未開始の相互非依存operationをrootとの重複なしで並列化できる。
3. Workerだけがroot未取得inputを読み、rootが同じinputを再取得せずresultで次を判断できる。
4. required outcomeにWorker固有capabilityが必要である。
5. 既存evidenceでは決着しない判断があり、Worker resultが未発行invocationのdecision boundaryを変え得る。

criterion owner、risk owner、`independent`という語、独立確認という作業名だけでは、これらのstateを成立させない。rootがrequired evidenceを取得済みで、別execution identityが成果成立条件でもなく、Workerが同じevidenceを再読するだけなら`delegation_value_ready=false`とする。

## 評価境界

- Candidate artifactの作成は、targeted評価済み、採用済み、release済み、本体反映済みを意味しない。
- 最初にCandidate84のF02 N=5だけを実行する。Candidate82またはCandidate83は再実行しない。
- F02が通過するまでF04、D01、A06、標準14へ進めない。
- Candidate83 F02の公式resultと`stopped`履歴は変更しない。

## 評価結果

[`Rating v14 Medium F02 N=5`](../evaluations/results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md)は5 / 5 valid・rateable・score `4`だった。3 / 5はroot-onlyで完了したが、2 / 5は`owner=independent contract check`を「TaskSpec指定の独立確認」と再分類し、test差分を読むWorkerを各1件起動した。

語列除外だけでは`separate_identity_required`への意味上の昇格を完全に防げなかった。停止条件に従いCandidate84を`targeted_f02_evaluated / stopped`とし、F04、D01、A06、標準14、採用、release、本体反映は実施しない。

## 2026-07-28の現在解釈

当時の一次resultと`stopped`判定は変更しない。一方、後続の[`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により、「F02でWorkerが1件でも起動した場合は停止」という判定基準は採用しない。

C84は5 / 5 score `4`で品質を満たした。root-only 3件に対し、Workerあり2件のうち1件はrequired validationと並行し、もう1件は逐次化して216.409秒だった。互換baselineと事前固定したtoken / elapsed toleranceがないため、現在stateは`quality_passed / cost_control_mixed`とする。C84を採用可能とは判断せず、制御再設計gateを満たすまで追加評価へ進めない。
