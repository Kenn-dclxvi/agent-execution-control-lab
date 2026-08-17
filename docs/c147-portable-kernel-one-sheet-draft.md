# C147 portable kernel一枚化草案

> [!IMPORTANT]
> **状態**: `exact_draft_written / root_only_dependency_closed / full_agent_dependency_closed / primitive_coverage_81_of_81 / q01_q08_static_counterexamples_repaired / full_agent_candidate_bundle_registered / full_agent_n1_valid_14_score4_7_quality_failed / c147_reference_not_authorized / root_only_prompt_identity_unbound`
>
> 本書は、C147由来のruntime非依存本文をcomponentから自己完結した一枚へ構成できるところまで固定する。生成物は管理用草案であり、Candidate、評価result、採用、releaseまたはprojectionではない。

## 結論

単一actor用とfull-agent用を、共通componentとactor capability blockの差だけで構成できる形にした。

```text
共通: vocabulary + outcome + actor-core + actor-input
  ├─ root-only:  single-actor
  └─ full-agent: multi-actor
共通: observation + frontier + completion + validation + method/recovery
```

両variantとも構成後は一枚の`AGENTS.md`で自己完結し、component readまたはruntime includeを要求しない。root-onlyはmulti-actor責務を無言で削除せず、別actorをrequired outcomeとするoperationを`unavailable`へ閉じる。full-agentは独立executionの開始、provenanceおよびcoordinator非代行を追加する。

## 構成結果

| variant | bytes | content SHA-256 | lifecycle |
| --- | ---: | --- | --- |
| root-only draft | 10,418 | `0e625b4c527e8b520c676cee15424ba222576ebc0e29d6f37eeea1ec08166a36` | `draft / bundle_binding_eligible=false` |
| full-agent draft | 10,781 | `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3` | `draft / bundle_binding_eligible=false` |
| C147 verified full-agent | 10,772 | `46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7` | 既存Candidate147 identityへbyte一致 |

この差は静的な入力bytesの差だけである。文字数、component数または見出し数を効率改善と扱わない。Candidate化後に品質を維持し、互換条件でall-agent `total_tokens`と`elapsed_seconds`がともに減少した場合だけcost改善方向と判定する。

## actor境界

### `actor-core`

全variantが次を持つ。

- operationごとの一actor binding。
- 同じpredicateまたはresult生成の再割当て禁止。
- actor変更時の旧binding失効。
- `false / failed` resultのoperation内terminal化と別operationへの非伝播。

### `actor-input`

全variantが、actorへ渡す入力をcriterion、pass condition、対象、admission済みresult、必要証拠、許可観測および禁止入力へ閉じる。single actorでambient contextを利用できる場合も、無関係な履歴を入力拡大の理由にしない。

### actor capability block

- `single-actor`はactor identityを一つへ固定し、独立execution要求を役割名や自己宣言で補完しない。
- `multi-actor`はrequest contractが独立executionを明示した場合だけactorを開始し、起動identity、送信元、operationおよびresult kindが対応するresultだけをadmitする。

どちらも`actor.execution_mode`と`actor.result_admission`を提供するため、後続のcompletionとvalidationはplatform名ではなく同じcapabilityへ依存できる。同じ構成へ両blockを入れるとprovider競合になり、composerが拒否する。

## 81 primitive逆引き

[`primitive-coverage.json`](../prompts/compositions/c147-portable-kernel-draft-r1/primitive-coverage.json)は、C147の81 primitiveをcomponent内のsemantic statementへ一件ずつ対応づける。

- 共通statement: 71件。
- actor capability別statement: 10件。
- full-agent: 81 / 81件を`preserved`として対応。
- root-only: 共通71件に加え、actor/result対応の`O3`を`actor-core`で`preserved`。独立actor能力にしか成立しない残り9件を`single-actor`の`closed_as_unavailable`へ対応。
- 重複primitive: 0件。
- 未対応primitive: 0件。

`closed_as_unavailable`はfull-agentの意味がroot-onlyでも成立したという主張ではない。能力がない環境で独立actor resultを推測、自己生成または別resultから補完する経路を閉じたことを示す。

## 互換性境界

草案compositionはschema `v3`を使う。`v1`と`v2`はそのまま読み込み可能であり、既存C147 compositionのschema、output prompt identity、構成bytesおよびbundle bindingを変更しない。

`v3` draftは次を要求する。

- `lifecycle_state=draft`
- `bundle_binding_eligible=false`
- `output_prompt_identity=null`
- component dependency closure
- 固定済みoutput SHA-256

`render`は許可するが`verify-bundle`は拒否する。したがって、草案manifestを既存Candidate147、評価profile、compatibility keyまたはLayer 1 identityへ誤接続できない。

## 残るgate

本文草案と81件の逆引きは揃った。Q01〜Q08への静的反証で初回草案の4境界を見つけ、正のobservation開始、actor result admission、frontier不可分性およびrecovery欠落時terminalを修正した。詳細は[`Q01〜Q08静的反例監査`](c147-portable-kernel-q01-q08-static-counterexample-audit.md)を正とする。

Q01〜Q08は本文作成に使ったtuning Caseであり、修正後の静的反例0件を評価通過または一般化証拠にしない。kernel草案固定後に[`held-out r1`](portable-instruction-semantic-conformance-heldout-r1/)の14件、private oracle、ratingおよび汎用graderを固定した。以後、held-out結果を見てこのdraft identityを修正しない。Candidate作成はまだ許可しない。

1. held-out inputをkernel本文または修正判断へ流入させない。
2. control-free baselineでschema、3 KPIおよび実行経路の測定成立を確認する。
3. formal target identity、直接の基準、allowed delta、非目標、評価順および停止条件は、full-agent variantについて[`直接比較設計`](portable-full-agent-kernel-direct-comparison-design.md)へCandidate作成前gateとして固定した。root-onlyにはこのgateを流用しない。

評価へ進む場合も、現行review制御系列ではADR9 N=5を先に実行し、通過前にStandard14を発行しない。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)
- [`C147 component依存閉包台帳`](c147-component-dependency-ledger.md)
- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`C147 portable kernel draft composition`](../prompts/compositions/c147-portable-kernel-draft-r1/README.md)
