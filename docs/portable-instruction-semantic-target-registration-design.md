# Portable instruction semantic target登録設計

> [!IMPORTANT]
> **状態**: `target_kind_gap_confirmed / descriptor_v2_schema_fixed / formal_target_registered / heldout_r1_registered / rating_registered / zero_byte_control_free_baseline_registered / source_commit_a544769_bound / single_case_packet_materializer_implemented / v2_comparison_preflight_implemented / codex_adapter_core_implemented / execution_entrypoint_disabled / profile_not_registered / v1_unchanged / baseline_not_started`
>
> 本書はportable instruction semantic conformanceを既存repository targetと誤って互換扱いしないための登録設計である。後続の正式登録は[`evaluations/targets/portable-instruction-semantic-conformance/`](../evaluations/targets/portable-instruction-semantic-conformance/)を正本とする。本書自体はProfile、Candidate、評価slotまたはresultではない。

## 結論

今回の評価対象はrepository snapshotではなく、固定operation ledgerへ一回応答するsemantic protocolである。既存target descriptor v1と`evaluation_loop.py`は`target_repository_ref`を必須比較条件にしているため、現状のまま登録すると次のどちらかになる。

1. このrepositoryのcommit/treeを借りてprotocol identityを表す。repository更新がsemantic protocol driftに見え、protocol変更がrepository refへ現れない。
2. 架空のrepository URIやcommitへprotocol hashを詰める。型と意味が一致せず、既存repository targetと同じ互換経路へ流入する。

どちらも採用しない。既存v1 descriptor、Profile、resultおよび`target_repository_ref`を変更せず、v2で評価対象を`target_subject`へ一般化する。formal targetは、Layer 1〜4がv2 subjectを扱えるまで作らない。

## 三つのidentityを分ける

| identity | 何を固定するか | 今回の値 |
| --- | --- | --- |
| `target_subject_ref` | 何を評価するか | semantic protocol ID、revision、interaction mode、response schema SHA-256 |
| `runtime_ref` | どこで実行するか | 最初はCodex CLI。model、CLI version、token accounting、permission、隔離条件をProfileへ固定 |
| `prompt_set_identity` | 何を注入するか | control-free、root-onlyまたはfull-agent。比較で変えてよい軸 |

Codexを最初に使うことはtargetをCodex専用にしない。Claude Code、Cursorまたは別agent runtimeは、同じ`target_subject_ref`でも`runtime_ref`が異なる別poolになる。runtime間のKPI差を同一prompt比較へ混ぜない。

## descriptor v2

[`evaluation-target-v2.schema.json`](../evaluations/targets/schemas/evaluation-target-v2.schema.json)は`target_kind`をdiscriminatorにする。

- `repository`: repository URI、commit、treeを持つ。
- `semantic_protocol`: protocol ID、revision、interaction mode、response schema SHA-256を持つ。

`executor_binding`は`profile`に固定する。v1のようにtarget descriptorへ単一executorを書かない。これは同じprotocolを複数runtimeで測るためであり、runtime間互換を意味しない。

登録候補は[`portable-instruction-semantic-target-draft.json`](portable-instruction-semantic-target-draft.json)へ履歴草案として保持する。commit `a544769`でsource bytesを固定した後、正式descriptorを[`target.json`](../evaluations/targets/portable-instruction-semantic-conformance/target.json)へ登録し、rating contractとnamespaced artifact rootsをbindした。

## compatibility contract v2

既存v1の互換keyは変更しない。v2 profileでは次を別fieldで必須にする。

```json
{
  "target_subject_ref": {
    "kind": "semantic_protocol",
    "protocol_id": "portable-instruction-semantic-conformance",
    "protocol_revision": "response-r2",
    "interaction_mode": "single_response_operation_ledger",
    "response_schema_sha256": "ed50b2aef60bd8e07794ee0fa13b397989df2ec0e529e39e8c8068c9fcd06076"
  },
  "runtime_ref": {
    "runtime": "codex-cli",
    "version": "unbound",
    "model": "unbound",
    "token_accounting_revision": "unbound"
  }
}
```

`unbound`は草案の説明値であり、Profileへは入れない。実値を固定できるまでProfileを作成しない。

互換判定はtagを含むobjectのexact一致とする。`kind=repository`と`kind=semantic_protocol`は、残りの文字列が偶然一致しても非互換である。v1 resultをv2へその場で変換しない。

## control-free baseline

control-freeは「runtimeのhidden/default instructionがない」という意味にしない。portable kernelを追加しない条件であり、次はkernel条件と同一にする。

- Caseの`input.json` bytes
- response schemaを要求するTaskSpec wrapper
- model、reasoning、Codex CLI versionおよびpermission
- user config、memory、skills、plugins、apps、toolsおよびconversation historyの隔離条件
- all-agent token accountingとelapsed境界
- oracle、graderおよびexpected responseの非配送

response schemaを守るためのTaskSpec wrapperは両条件へ同じbytesで渡し、portable kernelの一部にしない。baseline側だけに正解route、clause説明または例を加えない。

## 立ち上げ順

1. v2 `target_subject_ref / runtime_ref`を既存v1から分離してpreflight可能にする。これは[`semantic_protocol_comparison_preflight.py`](../scripts/semantic_protocol_comparison_preflight.py)とunit testで実装済みである。
2. Codex CLIの現在version、model、reasoning、token accounting、隔離optionおよびelapsed sourceを固定する。CLI `0.146.0`向けのcommand、一次`total_tokens`の受理、永続session transcript回収および単調時計境界は[`semantic_protocol_codex_adapter.py`](../scripts/semantic_protocol_codex_adapter.py)へ実装済みだが、modelとProfileは未固定で、実行入口は無効のままである。
3. model-visible packet materializerが`input-cases.json`から一件だけを出し、oracle、rating、freezeおよび他Caseを除外することを機械検証する。これは[`materialize_semantic_protocol_case.py`](../scripts/materialize_semantic_protocol_case.py)と対応unit testで実装済みである。
4. [`portable-instruction-control-free-prompt-draft-r1/`](portable-instruction-control-free-prompt-draft-r1/)の0-byte本文をsource commitへbindし、正式targetとProfileを登録する。
5. control-freeの最小qualificationを、結果を見てCaseを変えない条件で実行する。
6. 全14 Caseで3 KPIを欠落なく取得できた場合だけ、新インスタンスゲートの測定成立を通す。
7. その後にroot-onlyまたはfull-agentのCandidate作成前gateへ進む。

最小qualificationのquality値は合否条件にしない。schema不適合、oracleから一意に導出不能、token不完全またはelapsed欠落だけを測定不成立とする。

## 登録前停止条件

- `target_repository_ref`へprotocol identityを入れる。
- v1 Profileまたはresultをv2へ変換する。
- Codex runtime identityをtarget identityへ埋め込む。
- control-freeにportable kernelのroute説明を加える。
- held-out inputとprivate oracleを同じmodel-visible packetへ入れる。
- `total_tokens`をroot-only値、推定値または文字数から作る。
- 最小qualificationのscoreを上げるためCase、oracleまたはTaskSpecを変更する。
- v2 preflightとpacket分離が未実装のままformal targetを登録する。

## 次の実装gate

一件だけをmodel-visible packetへ出すmaterializer、private receipt、v2 subject/runtime comparison preflight、Codex CLI `0.146.0`向けadapter coreおよび0-byte control-free prompt draftは実装済みである。preflightはprompt identity以外の完全一致を要求し、`target_repository_ref`、`unbound`、runtime drift、Case driftおよびtranscript accountingと両立しない`ephemeral` sessionを拒否する。adapterはisolated workspaceへ`AGENTS.md`だけを配置し、user config、rules、memory、skills、apps、pluginsおよびmulti-agent capabilityを無効化する。tokenはterminal eventの一次`total_tokens`がある場合だけ受理し、内訳や文字数から補完しない。

commit `a544769`のsource identity、namespaced formal target、held-out r1、rating contractおよび0-byte control-free baselineは登録済みである。ただしadapterには実行入口がなく、Profileも存在しない。次に許可するのは、model、reasoning、Codex CLI runtime、capability catalog、private transcript回収方法、permissionおよび共通TaskSpec wrapper bytesを一つのProfileへ固定し、そのProfileとadapter contractの一致を静的検証する変更である。それまではdispatch、qualificationまたはbaseline runを発行しない。

## 参照

- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`Portable instruction semantic conformance held-out r1`](portable-instruction-semantic-conformance-heldout-r1/)
- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`target instance規則`](../evaluations/targets/AGENTS.md)
- [`evaluation foundation v4境界`](prompt-comparison-workflow.md)
