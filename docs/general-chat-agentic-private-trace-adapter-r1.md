# General chat agentic private trace adapter r1

> [!IMPORTANT]
> **状態**: `real_input_contract_fixed / externally_selected_files_only / synthetic_shadow_verified / focused_16_passed / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / issued_trace_not_read / model_invocations_0 / probe_issues_0 / ticket_unchanged`

## 結論

private probe traceをadapter自身が探索せず、runnerが事前に選択したfile identityだけから安全なnormalized traceを作るreal-input revisionを別identityで実装した。実装確認にはrepository上のsynthetic shadow bytesだけを使い、実0.146.0 trace、既存Codex sessionおよびmodelを読んでいない。

`trace_origin`は`synthetic_shadow`と`issued_probe`を区別し、出力にも保持する。`issued_probe_projected`はrunnerがそのoriginへbindした入力を投影したことだけを表し、実trace selectorの成立、capability available、発行許可またはreceipt完成を意味しない。

## 入力境界

[`general-chat-agentic-private-trace-adapter-input.schema.json`](general-chat-agentic-private-trace-adapter-input.schema.json)は次を固定する。

- `input_mode=externally_selected_private_trace`。
- exact r2 probe identityとCodex CLI 0.146.0 runtime identity。
- runner manifestが選んだroot events、root thread、session集合、thread / parent、path、SHA-256およびbyte数。
- adapterによるfile discovery禁止。
- normalized r2 schema identity。
- runnerがtrace rootを所有し、adapterは変更も削除もしない責任境界。
- receipt sealまたはterminal failure後にrunnerがcleanupする条件。

`synthetic_shadow`はrepository内shadow rootだけを許可し、`issued_probe`はrepository外のprivate temporary rootだけを許可する。relative path外への移動、`..`、absolute file pathおよびsymlinkを拒否する。

## 出力境界

[`general-chat-agentic-private-trace-adapter-output.schema.json`](general-chat-agentic-private-trace-adapter-output.schema.json)へ、origin付きのprojection envelopeを返す。

- confirmed fieldだけを含むr2 normalized trace。
- `synthetic_shadow_verified`または`issued_probe_projected`。
- 読んだtrace file件数。
- raw path出力0件、model invocation 0件、probe issue 0件。
- mutationなし、cleanup責任はrunner。

workspace path、file path、`source`、`agent_path`、unknown response itemおよびcommand本文は出力しない。task identity、terminal sender、spawn、packet、tool resultおよびroot final responseは推測せず、未観測のままにする。

## synthetic shadow

[`general-chat-agentic-private-trace-shadow-packet-r1.json`](general-chat-agentic-private-trace-shadow-packet-r1.json)と[`general-chat-agentic-private-trace-shadow/`](general-chat-agentic-private-trace-shadow/)は、root events一件、root session一件、child session一件を固定する。`source.agent_path`とunknown eventを含むが、normalized outputへ写さない。

2026-08-20のfocused test 16件では次を確認した。

- input / output schemaとshadow正常投影。
- binding admissionが`agentic_runtime_capability_unavailable`のままであること。
- path、source、agent pathおよびunknown eventを出力しないこと。
- 選択fileを変更または削除しないこと。
- hash drift、workspace drift、root境界違反およびsymlinkの拒否。
- absolute path、parent traversal、adapter側discoveryおよびlifecycle責任変更の拒否。
- issued originとrepository shadow rootの混同拒否。

## 現在許可する次作業

model-free composition r2に続くprobe issuance preparation r3は`ready_not_authorized`まで通過した。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断であり、許可されるまでは追加artifactや実行を開始しない。

実trace読取り、`run-once`、r2 ticket変更、issuance authority変更、probe発行、capability receipt、target登録および評価はまだ許可しない。

## 参照

- [`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`synthetic adapter設計`](general-chat-agentic-real-trace-adapter-design.md)
- [`exact runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)
