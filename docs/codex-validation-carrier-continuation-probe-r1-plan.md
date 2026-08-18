# Codex validation carrier continuation probe r1実行票

> [!IMPORTANT]
> **状態**: `probe_ready / continuation_only / non_comparative / single_invocation / retry_forbidden / candidate_not_used`

## 目的

[`validation carrier probe r2`](codex-validation-carrier-capability-probe-r2-result.md)で唯一未観測となった`carrier.continuation_identity`だけを確認する。

250msでnonterminalになる一つのnested commandを、一つのprogrammatic carrier内で同じsession identityへbindし、modelへ途中resultを返さずterminalまで継続できるかを一回観測する。fail-fast、複数validation、prompt Candidate、品質またはKPIを同時に測らない。

## 固定fixture

workdirは`/Users/kenn/repos/_verification/codex-validation-carrier-continuation-probe-r1.fzgj2f`とする。

| file | SHA-256 | 役割 |
| --- | --- | --- |
| `validation-long.sh` | `f1fb0a567617c85f24570f8fbff1cc8565f0f11aaf9f5037470794c4e06940de` | start marker、2秒sleep、terminal marker、exit 0 |
| `final-schema.json` | `838ced60b69293fbae539c26359cb93210585e8d20bba63c064be120d1a22606` | continuation結果の8 fieldを固定 |
| `probe-prompt.txt` | `9ea4e620fbda72e64c73cb4ade549fe49ad1ff0ceeac9592e772cee74076cde8` | model-visible probe本文 |

発行前に`probe-events.log`が存在しないことを確認済みである。親directoryにも`AGENTS.md`はない。

## required route

1. 一つのprogrammatic carrierを開始する。
2. carrier内部から`bash validation-long.sh`を`yield_time_ms=250`で一回開始する。
3. 初回resultがnonterminalなら、返されたsession identityを保持する。
4. carrier内部から、そのidentityだけを使うcontinuation callをterminalまで行う。
5. modelへ途中resultを返さず、terminal時に8 fieldを一度だけ返す。

初回resultがterminalだった場合は事実を記録するが、continuation capabilityを通過扱いにしない。内部continuation toolがなければcommandを開始せず`unavailable`を返す。modelへnonterminal resultを返してdirect tool callで継続するrouteは禁止する。

## 実行条件

| field | 値 |
| --- | --- |
| CLI | `codex-cli 0.146.0` |
| model / reasoning | `gpt-5.6-sol / medium` |
| sandbox / approval | `workspace-write / never` |
| session | persisted |
| attempts | 1 |
| comparison / formal KPI | なし / なし |

exact commandは次とする。

```bash
codex \
  -a never \
  -s workspace-write \
  -m gpt-5.6-sol \
  -c 'model_reasoning_effort="medium"' \
  exec \
  --skip-git-repo-check \
  --ignore-user-config \
  --ignore-rules \
  --json \
  --output-schema final-schema.json \
  - < probe-prompt.txt > raw.jsonl 2> stderr.log
```

## admission

`continuation_observed=true`には次を全件要求する。

- process exit 0とschema適合。
- nested command eventは`validation-long`一件だけ。
- 初回nested resultがnonterminalで、session identityを返す。
- program内のcontinuation callが同じsession identityだけを使う。
- carrier外にnonterminal resultを返したmodel responseがない。
- terminal exit 0とstart / terminal markerを確認できる。
- carrier terminal outputが一件だけ。

初回terminal、command 0件の`unavailable`、identity不一致、model再入、別command、marker欠落、schema failureまたはCLI failureでは通過しない。同じprobeを再発行しない。
