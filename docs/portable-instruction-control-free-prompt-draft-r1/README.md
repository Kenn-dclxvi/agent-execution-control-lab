# Portable instruction control-free prompt draft r1

> [!IMPORTANT]
> **状態**: `zero_byte_instruction_fixed / delivery_target_agents_md_fixed / source_commit_unbound / formal_baseline_not_created / execution_not_started`

> [!NOTE]
> この状態はcommit `a544769`へ固定した登録前source artifactの履歴である。後続の正式baselineは[`evaluations/targets/portable-instruction-semantic-conformance/prompts/baselines/portable-semantic-a544769-control-free-r1/`](../../evaluations/targets/portable-instruction-semantic-conformance/prompts/baselines/portable-semantic-a544769-control-free-r1/)へ登録済みであり、この草案manifestを遡及更新しない。

この草案は、semantic protocol比較で追加portable instructionを持たない条件を固定する。本文は0 bytesで、実行時の空workspaceへ`AGENTS.md`として配送する。runtime既定instruction、共通TaskSpec wrapperおよびCase入力まで存在しないという意味ではない。

正式baselineへ昇格するには、少なくとも次が必要である。

1. このartifactを含むsource commit。
2. 正式target registrationとnamespaced baseline path。
3. Codex runtime/Profile identity。
4. `AGENTS.md`のload観測とmodel-visible capability catalog。
5. control-free qualificationの測定成立。

`manifest.json`の`source_authority.repository_commit=null`である間は、Profile、preflightまたはdispatchへ使用しない。
