# C147 component依存閉包台帳

> [!IMPORTANT]
> **状態**: `c147_full_agent_dependency_closed / portable_root_only_draft_closed / portable_full_agent_draft_closed / candidate_not_created / evaluation_not_started`
>
> 本書は管理用compositionの依存関係と、単一actor構成へ進む前の切り分けを固定する。Agentに読ませるprompt、Candidate、評価result、採用、releaseまたはprojectionではない。

## 結論

現行のfull-agent構成は、各componentの`provides / requires`を全件解決できる。構成後の`AGENTS.md`もCandidate147とbyte一致する。

一方、worker関係の条項を外すだけでroot-only版を作ることはできない。理由は、`PRODUCER`が次の二種類を一つのcomponentに持つためである。

- 単一actorでも必要な、operationごとのactor一意binding、再割当て禁止、rebinding時の旧binding失効。
- 複数actor能力があるときだけ必要な、独立executionの選択条件とcriterion owner起点routingの禁止。

したがって、既存prompt identityへbinding検証済みの構成はfull-agent一つである。後続ではroot-onlyを「worker用componentを削除した選択集合」にせず、actor共通契約、単一actor時の`unavailable`境界、複数actor契約を意味保存して分けた二つの管理用草案を作成した。詳細は[`C147 portable kernel一枚化草案`](c147-portable-kernel-one-sheet-draft.md)を正とする。

## 台帳の意味

`provides`はcomponentが他componentへ公開する意味境界、`requires`はそのcomponentの参照先である。この台帳は次のことだけを機械的に確認する。

1. 選択した全componentの`requires`にproviderがある。
2. 同じcapabilityを複数componentが提供しない。
3. component本文、順序および最終bytesのidentityが固定されている。

依存閉包は、構成結果の品質、機序成立、runtime capability、意味削除の妥当性または処理順序を証明しない。相互参照は閉じた契約を示すが、実行順序を指示しない。

## component依存

| component | 主な`provides` | 主な`requires` | 現行判定 |
| --- | --- | --- | --- |
| `header` | `document.header` | なし | 配送単位の先頭 |
| `spec` | `operation.contract`, `spec.readiness`, `permission.boundary`, `result.locality` | `document.header` | 全構成の共通基盤 |
| `producer` | `actor.binding`, `actor.worker_admission`, `actor.rebinding` | `operation.contract`, `criterion.owner` | 共通actorとworker固有が未分離 |
| `terminal` | `operation.completion` | `operation.contract`, `actor.binding` | 共通 |
| `context` | `actor.input_boundary` | `actor.worker_admission`, `permission.boundary`, `criterion.owner` | 複数actor実行時のinput境界 |
| `evidence-gate` | `observation.admission`, `implementation.binding` | operation、permission、completion、validation plan | 共通。validation handoffを持つ |
| `owner-role` | `delegated.provenance` | actor binding、worker admission、input boundary | 複数actor固有 |
| `root` | `coordinator.boundary` | `actor.binding`, `delegated.provenance` | coordinatorがactorでない場合の境界 |
| `independence` | `operation.independence` | operation、actor、owner、result locality | 単一actorでも別operationの分離に必要 |
| `decision-boundary` | `issuance.frontier` | operation、permission、result locality | 共通 |
| `validation-plan` | `validation.plan` | `observation.admission`, `execution.method` | validation対象の構成 |
| `validation-closure` | `validation.execution` | actor、completion、validation plan | validationの発行・収集境界 |
| `method` | `execution.method` | operation、permission | 共通 |
| `recovery` | `execution.recovery` | operation、method | recovery能力を使う場合の境界 |

正確な配列は[`composition.json`](../prompts/compositions/the-caption-c147-full-agent-r1/composition.json)を正本とする。

## root-onlyの正常経路

単一actorの実行環境で保持する最短の正常経路は次である。これは成功runのtool順をprompt手順へ転記したものではなく、各後段のpermissionを開く必要dependencyである。

```text
outcomeとoperationを固定
  -> 各operationを単一actorへbind
  -> 必要なobservationだけをadmit
  -> implementation全体を一案へbind
  -> resultに依存しないfrontierを部分result消費前に開始
  -> action後のvalidation planを閉じる
  -> 個別validation resultを保持してterminalを判断
```

この経路で不要に見えるworker固有責務は、`P3 / P4`、`C1-C4`のworker packet表面、`O1-O7`のdelegated provenance、`R1 / R2`のcoordinator非代行である。ただし、これらを現行componentからそのまま削除すると、次も同時に欠落する。

- `PRODUCER`から`P1 / P2 / P5`の単一actor契約も落ちる。
- `INDEPENDENCE`は他componentが供給する`actor.binding`を失う。
- `TERMINAL`、`VALIDATION_CLOSURE`および受領resultの来歴が参照するactor identityが消える。

よって、現行C147 componentの単純削除によるroot-only compositionは存在しない。後続草案では`actor-core / actor-input`を共通化し、`single-actor / multi-actor`を択一providerにしてこの不閉包を解消した。

## 次の実装境界

後続草案は、現行`PRODUCER / OWNER_ROLE / ROOT / CONTEXT / INDEPENDENCE`の文を単純に切らず、[`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)の`ACTOR / INPUT`境界を使って次の別契約へ分けた。

1. `actor-core`: `P1 / P2 / P5 / O6 / I2`を保持し、単一actorで閉じる。
2. `multi-actor`: `P3 / P4 / O1-O5 / O7 / R1-R2`を保持し、独立executionが明示されたときだけ追加する。
3. `actor-input`: `C1-C4`をworker packet固有語からactor input境界へ変換し、単一actorではambient inputの拡大禁止として意味を残す。

この三分割と、自己完結した二つの一枚草案、81 primitiveの文単位逆引きは揃った。ただし構成結果のbytesが変わるため、新しいfull bundle、prompt identityおよびCandidate作成前gateなしに評価へ接続しない。

## 確認境界

- full-agent構成は今後もCandidate147とbyte一致させる。
- composition sourceと依存台帳は`model_visible=false / evaluation_eligible=false`とする。
- Agentへは構成済みの自己完結した一枚だけを配送する。
- root-onlyの効率は文字数やcomponent数ではなく、品質維持後の`total_tokens`と`elapsed_seconds`で判断する。
- Candidate化後の現行review制御試験はADR9 N=5から開始し、通過前にStandard14を発行しない。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`Candidate147機能分解の再分析`](c147-functional-decomposition-reanalysis.md)
- [`C147 portable kernel coverage台帳`](c147-portable-kernel-coverage-ledger.md)
- [`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)
- [`Prompt composition sources`](../prompts/compositions/README.md)
