# Codex validation carrier capability probe r2結果

> [!IMPORTANT]
> **状態**: `capability_observed / single_carrier_passed / fail_fast_negative_passed / intermediate_ingress_denied / third_not_started / individual_identity_preserved / terminal_projection_passed / continuation_unobserved / no_retry`

## 結論

Codex CLI `0.146.0`は、今回の固定条件でvalidation carrierの中核を成立させた。

一つの`custom_tool_call name=exec`が、内部で`validation-1`と`validation-2`を別々の`exec_command`として実行した。第二resultのexit 7をprogram内で`non_success`へbindし、条件分岐により`validation-3`を開始しなかった。個別command resultは二command間でmodelへ返らず、carrier terminal時に二つの対応づけ済みresultが一つの`custom_tool_call_output`として返った。

これにより、[`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)で未観測だったfail-fast negative routeは成立した。long-running nested commandを同じcarrier identity内でterminalまで継続するrouteはこのfixtureが消費していないため、`carrier.continuation_identity`だけは未観測のまま残る。

## 実行identity

| field | 値 |
| --- | --- |
| observed date | `2026-08-18` |
| workdir | `/Users/kenn/repos/_verification/codex-validation-carrier-probe-r2.dDDnH3` |
| resolved workdir | `/Volumes/SN7100/_verification/codex-validation-carrier-probe-r2.dDDnH3`。両pathのinodeは`4598862`で一致 |
| CLI / model / reasoning | `codex-cli 0.146.0` / `gpt-5.6-sol` / `medium` |
| permission | `workspace-write / never` |
| process exit | `0` |
| attempts | `1` |
| thread ID | `01a0127b-30d8-7c72-8cc2-90f79f9376f9` |
| persisted rollout | `/Users/kenn/.codex/sessions/2026/08/18/rollout-2026-08-18T10-27-38-01a0127b-30d8-7c72-8cc2-90f79f9376f9.jsonl` |

## 保存証拠

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `raw.jsonl` | 1,555 | `05be595b4922a837fc69fa3e9ea8c5f70eceed89e592f1e8e501260c6ab4b48b` |
| `stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `probe-events.log` | 26 | `cd017f7bf4034a2f0fd32d09b8429c5dc2cbb209f58287ff4b4d6809dbc6d677` |
| persisted rollout | 63,821 | `2dca3ca9a2ef70dc3f1078bc663f0c3a9a03a7e4c32839b34b5bc50e1b63711a` |

raw evidenceとmarkerにsecret patternはなかった。raw evidenceは`_verification`、persisted rolloutはCodex session storageにだけ保持し、repositoryへcommitしない。

## carrier内部

persisted rolloutには`custom_tool_call name=exec`が1件ある。そのprogramは次の状態を所有した。

- `terminal_results=[]`
- `third_started=false`
- validation-1のnested `exec_command`
- validation-2のnested `exec_command`
- `second.exit_code === 0`の場合だけvalidation-3を開始する条件分岐
- plan terminal時だけの`text(JSON.stringify(...))`

実測では次となった。

| validation | command event | exit | terminal binding |
| --- | ---: | ---: | --- |
| validation-1 | 1 | 0 | `success` |
| validation-2 | 1 | 7 | `non_success` |
| validation-3 | 0 | - | 未開始 |

`probe-events.log`も`validation-1`と`validation-2`の2行だけで、validation-3はない。

## model-visible境界

二つのnested commandの間にmodel responseはない。programは第一resultを内部配列へbindし、第二resultを内部で判定してから一度だけterminal JSONを出力した。persisted rollout上の形は次である。

```text
assistant commentary
  -> custom_tool_call exec
       -> nested exec_command validation-1
       -> nested exec_command validation-2
       -> validation-3 branch not taken
       -> text(terminal JSON)
  -> custom_tool_call_output 1件
  -> final answer
```

carrier開始前に、`terminal_results=[]`を含むschema形状のcommentaryが1件出た。これは個別validation resultを含まず、command間のmodel再入でも、carrier terminal outputでもないためadmission failureにはしない。ただし`probe_status=observed`を観測前に記述した不正確な進行表示であり、将来のprompt品質または出力契約へ継承しない。

`custom_tool_call_output`は1件で、final answerはその受領後の下流応答である。tool resultがmodel-visible consumerへ渡った回数を2件と数えない。

## terminal JSON

final answerは固定schemaへ適合した。

```json
{
  "carrier_route": "programmatic_carrier",
  "probe_status": "observed",
  "terminal_results": [
    {"exit_code": 0, "status": "success", "validation_id": "validation-1"},
    {"exit_code": 7, "status": "non_success", "validation_id": "validation-2"}
  ],
  "third_started": false
}
```

usageはinput 32,259、cached input 15,104、output 713、total 32,972だった。これは一回のcapability診断値であり、formal KPI、P001比較または効率改善値には使わない。

## admission判定

| 条件 | 判定 |
| --- | --- |
| process exit 0、schema適合 | pass |
| validation-1と2を各1回 | pass |
| validation-3未発行 | pass |
| 個別identityとexit保持 | pass |
| command間model再入なし | pass |
| carrier terminal output 1件 | pass |

`capability_observed=true`とする。同じprobeを再発行しない。

この結果だけではCodex validation carrier全体を完成扱いにしない。次に分離して確認するのは`carrier.continuation_identity`だけであり、validation semantics、fail-fast、frontierまたはP001本文を同時に変更しない。

## 参照

- [`r2実行票`](codex-validation-carrier-capability-probe-r2-plan.md)
- [`r1結果`](codex-validation-carrier-capability-probe-r1-result.md)
- [`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)
