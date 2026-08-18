# Codex validation carrier能力監査

> [!IMPORTANT]
> **状態**: `codex_cli_0_146_programmatic_carrier_observed / seven_capabilities_observed / fail_fast_negative_passed / intermediate_ingress_denied / terminal_projection_passed / continuation_passed / composition_draft_ready / candidate_not_created`

## 結論

Codex向けvalidation carrierを構成する技術的なrouteは存在し、独立probeにより必要な7 capabilityまで観測できた。これは管理用composition draftを作れる根拠であり、P001へplatform blockを事後追加したり、新Candidateを自動的に作れたりすることは意味しない。

- OpenAI公式のProgrammatic Tool Callingは、複数tool call、loop、condition、intermediate resultのruntime内保持および小さい結果への集約を提供する。
- ローカルのCodex CLIは評価時と同じ`0.146.0`であるが、`features list`では`code_mode`が`under development / false`で、評価ProfileもProgrammatic Tool Callingの有効化を固定していない。
- 同じCodex CLI `0.146.0`の保存済みC147 traceには、個別validationをmodel messageなしで連続発行し、最後に一回だけ完了messageへ進むrouteがある。一方、P001は同じruntimeでvalidation間にmessageを挟んだ。よってrouteは観測済みだが、runtime permissionとして強制されてはいない。
- 保存済み成功traceだけではvalidation失敗時のnegative routeを確認できなかったため、後続の独立probeで切り分けた。

後続の[`capability probe r2`](codex-validation-carrier-capability-probe-r2-result.md)では、一つのprogrammatic carrier内で第二validationのexit 7を判定し、第三を未発行にした。さらに[`continuation probe r1`](codex-validation-carrier-continuation-probe-r1-result.md)では、250msでnonterminalになったnested commandを同じsession identityへbindし、program内部の`write_stdin`だけでterminalまで継続した。Codex carrierの7 capabilityは全件観測済みとなり、管理用composition draftへ進める。

## 公式能力

OpenAI公式の[Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)は、programがtoolを並行または順次に呼び、loopとconditionを使い、intermediate resultをhosted runtime内に保持できるとしている。また、予測可能なflowで複数resultを処理し、小さいstructured resultを返す用途にvalidationを挙げている。

[GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)も、各resultのたびに新しいmodel judgmentを要しないbounded stageにProgrammatic Tool Callingを使い、stage、allowed tools、output schema、required evidence、retryおよびstop conditionを明示するよう求めている。

この公式能力は、[`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)の次と一致する。

- `carrier.ordered_individual_execution`
- `carrier.local_result_check`
- `carrier.fail_fast_control`
- `carrier.intermediate_ingress_denial`
- `carrier.terminal_projection`

ただし、Responses APIで利用可能な能力がCodex CLIの対象Profileへ自動的に提供されるとは扱わない。applicationがavailabilityとeligible toolを決めるため、Profileまたはruntime receiptでのbindingが必要である。

## ローカルruntimeの確認

2026-08-18に次をread-onlyで確認した。

```text
codex-cli 0.146.0
code_mode                 under development  false
code_mode_host            stable             true
unified_exec              stable             true
```

feature名だけではcarrier semanticsを証明しない。特に`code_mode=false`であり、Programmatic Tool Callingと同一能力が評価runへ提供されると解釈しない。

P001 Standard14 N=5 Profileは`codex_cli=0.146.0`、model `gpt-5.6-sol`、reasoning `medium`を固定しているが、Programmatic Tool Calling、allowed callersまたはprogram output schemaを互換条件へ持たない。現在の保存resultへこの能力を事後追加しない。

## 保存traceによるroute確認

同じCase A02の保存済みtraceを比較した。

### C147

validation plan messageの後に、次の個別`command_execution`があり、その間に`agent_message`はない。

1. `bash -n run.sh`
2. `pytest tests/ -v`
3. `git diff --check`
4. `git diff -- run.sh`
5. `git status --short`
6. 完了message

個別command identityと終了状態は保持されている。これは`single admission -> ordered individual execution -> terminal projection`の正常routeがCodex CLI `0.146.0`で到達可能だった証拠である。

### P001

同じruntimeとCaseで、開始identity、source read、validation plan、`bash -n`、pytest、最終diffの各段階にmodel responseが入り、Case中央値はC147の4 responseからP001の7 responseへ増えた。

runtime差ではなくprompt構成差でrouteが変わったことは示せる。しかしC147正常routeの成功をそのまま新しい実行手順へ転記せず、途中resultをmodel consumerへ渡せるpermission edgeを閉じる設計だけに使う。

## 7 capabilityの判定

| capability | 公式能力 | CLI保存trace | 現在判定 |
| --- | --- | --- | --- |
| `carrier.single_admission` | bounded programとして表現可能 | C147 A02で連続routeを観測 | `route_observed` |
| `carrier.ordered_individual_execution` | loopとdependent callで表現可能 | 個別command 5件を順序保持 | `route_observed` |
| `carrier.local_result_check` | intermediate resultをprogram内処理可能 | r2でexit 7を内部判定 | `observed` |
| `carrier.fail_fast_control` | conditionで表現可能 | r2で第三validation未発行 | `observed` |
| `carrier.intermediate_ingress_denial` | intermediate resultをruntime内保持可能 | r2で二command間のmodel再入なし | `observed` |
| `carrier.terminal_projection` | program outputを明示可能 | r2でtool output 1件 | `observed` |
| `carrier.continuation_identity` | 一program内のawaitは可能 | continuation r1で同じsessionを内部継続 | `observed` |

7件は全て`observed`である。これはCodex CLI `0.146.0`、`gpt-5.6-sol`、probe固定条件でrouteが利用可能だったことを示す。全taskでの強制、他model、他versionまたは他platformへ一般化しない。

## 次のcapability probe境界

fail-fast negativeとcontinuationはそれぞれ独立probeで確認済みである。次は新しいprobeではなく、管理用composition draftでsemantic blockとCodex capability blockを別fileへ分ける。

draftはAgentへ直接読ませず、一枚へrenderする。bytesが変わるため既存P001 identityへbindせず、Candidate作成前gateを満たすまでP002、評価Profile、dispatch plan、releaseまたはprojectionを作らない。
