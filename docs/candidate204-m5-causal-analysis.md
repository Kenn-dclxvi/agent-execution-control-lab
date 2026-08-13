# Candidate204 M5原因分析

> **状態**: `superseded / single_cause_claim_withdrawn / C147_direct_base_retained / Candidate204_not_parent`
>
> `eligible -> issued` owner欠落は観測された不足の一つだが、C147全機能を正しく分解する前に単独原因へ確定した判断は撤回した。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とし、本文は旧原因仮説として保持する。

## 結論

Candidate204の機構失敗15件を、当時は次の一原因へbindした。

> `INVOCATION`は`ineligible -> eligible`を所有したが、`eligible -> issued`を所有する責任を再構成から落とした。

そのため`既知に独立なeligible invocation間へdependencyを追加しない`という否定条件は成立しても、開始identity resultを判断へ消費する前に、同じ発行frontierの許可readをissuedへ進める正の遷移がなかった。全15 runはTaskSpecの「開始identityを最初に確認する」を、identity result受領まで後続を待つ直列経路として解釈した。

これは語句の不足ではなく、状態遷移ownerの欠落である。

## 観測事実

- quality: 15 / 15 Score 4。
- 初回command group: 15 / 15が開始identityだけ。
- identity result受領後の許可read: 15 / 15。
- identity result前のartifact変更・required validation: 0 / 15。
- child session・不要producer: 0 / 15。
- command failure・protocol violation・許可外変更: 各0件。

品質と安全停止は保持したが、C147で成立していた非直列化経路を全件失った。低頻度の揺らぎではなく、再構成構造の系統的欠落である。

## M1で見落とした対応

M1はC147 `DECISION_BOUNDARY`を次へ再配置した。

- eligibilityと偽dependency禁止: `INVOCATION`
- resultの局所効果: `RESULT_EFFECT`

しかしC147の同条項が実際には持っていた三つ目の責任を割り当てなかった。

```text
eligible invocation set -> issued invocation set
```

M2の状態と単一owner表にも、この遷移が存在しない。したがって12責任は完全ではなかった。「足りないものを足す」再構成ではなく、runtime固有配送語を外す際に必要な発行責任まで落としていた。

## runtime固有語との境界

失敗は、`same model step`というCodex固有表面語をそのまま戻す根拠ではない。保持すべき意味は次である。

```text
issuance_frontier :=
  eligibleであり、未解決resultのeffect scopeへ入らないinvocationの集合

frontier_closed :=
  frontier内の全invocationがissuedまたは明示的unavailable
```

未解決resultを次判断へ消費できるのは`frontier_closed=true`の後だけとする。この定義はresponse、model step、tool名または待機IDを必要としない。一方、実行環境が一つ目のinvocation resultを強制配送して残りを発行不能にする場合はpromptだけで保証できない。その場合は`prompt_control_not_demonstrated`として停止し、外部executor変更へ広げない。

## 次の再設計境界

次M2ではReview責任0件とCodex固有表面語0件を維持したまま、13番目の責任候補`ISSUANCE`を検討する。

`ISSUANCE`が所有するのは次だけである。

- `eligible -> issued / unavailable`。
- current issuance frontierの閉包。
- frontier閉包前のpartial result consumption禁止。

`INVOCATION`はeligibilityだけ、`RESULT_EFFECT`はadmitted resultの後続効果だけを所有し、互いを再定義しない。atomic dispatchやreturn timingを成功宣言へ含めない。

Candidate204は失敗counterexampleとして保持し、次Candidateの親にしない。Candidate147を直接基盤としてM2へ戻す。新しいCandidate bundle、profile、preflightまたは評価slotは、修正M2とM3が閉じるまで作成しない。

`candidate204_failure_runs_15 / eligibility_without_issuance_transition_15 / unknown_cause_0 / portable_core_M2_reopened / ISSUANCE_owner_missing / review_remains_excluded / runtime_surface_remains_excluded / candidate205_not_created`
