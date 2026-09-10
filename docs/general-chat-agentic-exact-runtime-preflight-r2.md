# General chat agentic exact runtime preflight r2

> [!IMPORTANT]
> **状態**: `r1_preserved / exact_0_146_runtime_bound / host_registry_verified / static_preflight_passed / negative_6_passed / synthetic_adapter_implemented / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / ticket_r2_adapter_gate_false / ticket_r2_fixed_not_authorized / model_not_invoked / probe_not_issued`

## 結論

r1 ticketはliteral `codex`へbindしていたため、host defaultが0.148.0へ更新された現在は`RUNTIME_VERSION_MISMATCH`で停止する。r1を変更せず、immutable aliasが解決したexact 0.146.0 runtimeをmanifest、bundle、file inventory、symlink、entrypoint、署名およびversionへbindするr2を別identityで作る。

r2のruntime identityが静的に成立した後、synthetic file packet限定adapterは実装した。ただし、r2 ticketは`real_trace_adapter_ready=false`のまま固定され、実trace selectorは未確認で、`issuance_authority=not_authorized`でもある。従ってprobeは発行できない。

## r1からの差分

| 項目 | r1 | r2 |
| --- | --- | --- |
| probe identity | `general-chat-agentic-capability-preflight-r1` | `general-chat-agentic-capability-preflight-r2` |
| executable | PATH上の`codex` | manifestから固定したabsolute entrypoint |
| default CLI更新 | version mismatchで停止 | 影響を受けない |
| runtime evidence | version文字列 | alias・manifest・bundle・5 file・symlink・署名・version |
| task / fixture | r1 bytes | 同じbytesを再bind |
| model / reasoning | `gpt-5.6-sol / medium` | 変更なし |
| permission / isolation | r1 contract | 変更なし |
| issuance | not authorized | not authorized |

r2はr1の実行transportだけを置き換え、C147 coverage、Case、oracle、Candidateまたは評価条件を作らない。

## exact runtime identity

| field | 固定値 |
| --- | --- |
| alias | `codex-0.146`、`mutable=false` |
| runtime ID | `codex-cli-0.146.0-aarch64-apple-darwin-d98c29a85f529267fca03172828e0cd6db526380f1ad4a9a2fe37b111bf649a9` |
| manifest SHA-256 | `0ab73a80a0c0ddde94e0f554219a82155ce21d56922f2e9c01e6d88677b598a2` |
| bundle identity | `d98c29a85f529267fca03172828e0cd6db526380f1ad4a9a2fe37b111bf649a9` |
| entrypoint | `bundle/bin/codex` |
| entrypoint SHA-256 | `ae1d3ffe6d48aec6a4dc3f50e7eb8e0d11962485a6a9406c5a7012139383da02` |
| version output | `codex-cli 0.146.0` |
| Team Identifier | `2DC432GLL2` |
| platform | `aarch64-apple-darwin` |

bundle全体のregistry hash contractを別実装で推測し直さない。r2 static validatorはmanifest identityを確認したうえで、ticketへ列挙した5 fileの相対path、SHA-256、byte数と一つのsymlinkを現物へ照合する。未列挙fileまたはsymlinkがあれば停止する。

## static preflight

[`general_chat_agentic_exact_runtime_preflight.py`](../scripts/general_chat_agentic_exact_runtime_preflight.py)はmodelを呼ばず次を確認する。

1. r2 ticket schema。
2. r1 ticket、task、fixtureのidentity。
3. alias file hash、alias名、immutable state、runtime ID。
4. manifest file hashと固定field。
5. bundleがwrite-protectedであること。
6. file inventoryが完全一致し、各hashとbyte数が一致すること。
7. symlinkが列挙どおりでbundle外へ出ないこと。
8. entrypointのhash、`--version`およびTeam Identifier。

成功時も返すのは`runtime_identity_state=verified`であり、dispatchは許可しない。`real_trace_adapter_ready=false`と`issuance_authority=not_authorized`を独立した停止理由として返す。

2026-08-20の静的実行ではexact runtime identityが`verified`となり、dispatchは`REAL_TRACE_ADAPTER_NOT_READY`と`ISSUANCE_NOT_AUTHORIZED`の二理由で`denied`となった。alias、manifest、bundle path、file hash、symlinkおよびtask identityを崩すnegative fixture 6件も、model invocation 0件で全件を個別理由へ拒否した。

## 停止条件

- alias、manifest、runtime ID、bundle pathまたはhashのdrift。
- file追加、欠落、hash不一致またはbyte数不一致。
- symlink追加、欠落、target driftまたはbundle外target。
- bundleまたはentrypointがwrite可能。
- version、platformまたはTeam Identifier不一致。
- task、fixtureまたはr1 lineage identity不一致。
- r2 ticketのreal trace adapter gateがfalse、または実trace selectorが未確認。
- issuance authority未許可。

runtime identity不成立時はadapterやissuance判定へ進まない。runtime identity成立時も後二条件が残るためprobeを発行しない。

## 現在許可する次作業

probe issuance preparation r3まで通過し、`ready_not_authorized`となった。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは実trace読取り、unknown selector探索、`run-once`、authority変更、probe、target登録および評価を開始しない。

## 参照

- [`capability preflight r1`](general-chat-agentic-capability-preflight-plan.md)
- [`CLI version共存試験環境設計`](codex-cli-version-coexistence-environment-design.md)
- [`real trace adapter設計`](general-chat-agentic-real-trace-adapter-design.md)
- [`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)
