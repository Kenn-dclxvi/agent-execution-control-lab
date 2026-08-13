# Candidate205 M5原因分析

> **状態**: `superseded / cause_scope_reopened / strong_event_order_0_of_15 / C147_direct_base_retained / Candidate205_not_parent`
>
> 14件分類は原因をexact eligible invocation setへ狭めすぎていた。また、共同発行1件はagent message境界では成立したが、command event順ではidentity完了後の別発行だった。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とし、本文は旧原因仮説として保持する。

## 結論

Candidate205はC204で欠けていた`eligible -> issued / unavailable`のownerを`ISSUANCE`として足した。しかし強いcommand event順では15 / 15件で開始identityだけが先行した。`eligible invocation set`の具体化不足は一つの欠落だが、C147全体を正しく分解する前に単独原因へ確定した旧判断は維持しない。

つまり、足したのは遷移規則であり、まだ足りないのは次の入力bindである。

```text
current task facts + unresolved result effect scope
  -> exact eligible invocation identities
  -> issuance frontier
```

`current issuance frontier`を抽象集合として定義しただけでは、TaskSpecの「開始identityを最初に確認する」という語を、identity result受領までreadをeligibleにしない直列解釈から守れなかった。

## 観測事実

- quality: 15 / 15 Score 4。
- identity完了前の許可read command開始: 0 / 15。
- 開始identityだけの先行発行: 15 / 15。
- isolated内訳: F01 5 / 5、F02 5 / 5、F03 5 / 5。
- identity result前のartifact変更・required validation: 0 / 15。
- child session・不要producer: 0 / 15。
- command failure・protocol violation・許可外変更: 各0件。

C204の0 / 15からC205の1 / 15へ変化したという旧解釈は撤回する。旧1件はagent message境界のfalse positiveであり、command event順ではC204/C205とも0 / 15である。

## 成立runと失敗runの差

旧監査で成立扱いにしたF02 iteration 5は、最初のagent messageで「まず開始identityを確認」と述べ、identity command完了後に4対象fileのreadを別tool callとして発行した。agent messageを挟まなかったことは、result消費前の共同発行を意味しない。他14件も「driftがなければ読む」「開始identityだけを確認する」と述べ、identity resultをread発行資格の前提にした。

候補本文とTaskSpecは全runで同じなので、結果差はcase固有契約や別producerの有無では説明できない。抽象的なfrontier定義が、許可readのexact identityを初回frontierへ必ず含めるまで拘束していないため、二つの解釈を許した。

## 設計上の不足

Candidate205の責任分離は次で止まっている。

- `INVOCATION`: invocationのeligibilityを決める。
- `ISSUANCE`: eligible invocationをissuedまたはunavailableへ進める。
- `RESULT_EFFECT`: admitted resultの局所効果を後続へ反映する。

ここには、未解決resultで可否が変わらない既知の許可readを、開始identityと同じ判断時点のexact eligible setへ列挙してbindするownerがない。`ISSUANCE`自身にこの入力を補完させるとeligibility ownerと競合するため、次M2では新しい語句を足す前に、`INVOCATION -> ISSUANCE`境界の入力・出力契約を再設計する必要がある。

## 次の再設計境界

次のCandidateを直ちに作らない。C147を直接基盤に戻し、まず次を満たすM2を作る。

1. TaskSpecと既知result effect scopeから、初回に発行可能なexact invocation identity集合を決定する。
2. 開始identityのdriftがreadを禁止せず、read targetまたはpermissionも変えない場合、そのread identityを集合から除外できない。
3. その集合を`ISSUANCE`へ入力として渡し、全件を`issued / unavailable`へ進めるまでpartial resultを次判断へ使わない。
4. artifact変更とrequired validationは、開始identity resultで禁止され得るため同じ集合へ入れない。
5. Review責任0件とCodex固有表面語0件を維持する。

特定のresponse、model step、tool名、wrapperまたは配送atomicityを本文へ戻さない。promptだけで一意にできない場合は未解決として停止し、外部executor変更へ広げない。

Candidate205は成功候補の親にせず、15件すべてをC147機能鎖の欠落を示す反例として保持する。

`candidate205_strong_event_order_failure_runs_15 / coissued_success_trace_0 / cause_scope_reopened / c147_functional_decomposition_required / review_remains_excluded / runtime_surface_remains_excluded / candidate206_not_created`
