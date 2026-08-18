# Codex validation carrier capability probe実行票

> [!IMPORTANT]
> **状態**: `probe_ready / non_comparative / single_invocation / retry_forbidden / candidate_not_used / evaluation_result_not_registered`

## 目的

Codex CLI `0.146.0`が、個別validation resultをmodelへ途中配送せず、固定済み終了条件だけを内部判定してfail-fastできるprogrammatic carrierを、現在の標準tool surfaceへ提供するかを一回だけ観測する。

P001、C147または他Candidateの品質・KPIを測らない。prompt本文の選定、比較、採用、releaseまたはprojectionにも使わない。

## 固定fixture

作業directoryは`/Users/kenn/repos/_verification/codex-validation-carrier-probe-r1.O2soMN`とする。repositoryではなく、親directoryにも`AGENTS.md`は存在しない。`--skip-git-repo-check`、`--ignore-user-config`および`--ignore-rules`を使い、probe本文以外の指示を混ぜない。

| file | SHA-256 | 役割 |
| --- | --- | --- |
| `validation-1.sh` | `bf7775a2a9881593d69505a2b17da86e553086e33254d71ed813aae7fdfc11b5` | `probe-events.log`へ`validation-1`を追加してexit 0 |
| `validation-2.sh` | `3f7848ddb59edd2b0a51b7bd45f74f45cc2b306c6763d0f24927ba6243f48f65` | `validation-2`を追加してexit 7 |
| `validation-3.sh` | `1f93e79d1035979ee59ac654375f111c7a93e3d3035e5b904473b990063b18f5` | `validation-3`を追加してexit 0 |
| `final-schema.json` | `d75759454e699a8d169ba1b0c3d0226258fb2679232b94d19e4951a068b6ceee` | terminal JSONの4 fieldを固定 |
| `probe-prompt.txt` | `bc293e4917176250187c773b1defa11822f2c56be82380837f7c7b26626e84bf` | model-visibleなcapability probe本文 |

発行前に`probe-events.log`が存在しないことを確認済みである。

## required route

programmatic carrierが利用可能な場合だけ、次を一つのcarrier identityへbindする。

1. `bash validation-1.sh`を個別executionとして開始し、exit 0を内部判定する。
2. `bash validation-2.sh`を個別executionとして開始し、exit 7をnon-successとして内部判定する。
3. `bash validation-3.sh`を開始しない。
4. 1と2の個別identity、exit code、status、および3の未開始をplan terminal時に一度返す。

途中resultをmodelへ返すdirect tool loop、三commandのshell compound、個別identityを失う一実行、またはmodelによる事後判定はrequired routeに含めない。

carrierが提供されない場合の唯一の合法routeは、validation commandを一件も開始せず`unavailable`を返すことである。

## 実行条件

| field | 固定値 |
| --- | --- |
| CLI | `codex-cli 0.146.0` |
| model | `gpt-5.6-sol` |
| reasoning | `medium` |
| sandbox | `workspace-write` |
| approval | `never` |
| session | persisted。内部response境界確認のため`--ephemeral`を使わない |
| attempts | 1 |
| comparison | なし |
| formal KPI | なし |

exact commandは次とする。

```bash
codex exec \
  --skip-git-repo-check \
  --ignore-user-config \
  --ignore-rules \
  -m gpt-5.6-sol \
  -c 'model_reasoning_effort="medium"' \
  -s workspace-write \
  -a never \
  --json \
  --output-schema final-schema.json \
  - < probe-prompt.txt > raw.jsonl 2> stderr.log
```

`raw.jsonl`、`stderr.log`、process exit、`probe-events.log`、terminal JSONおよび対応するpersisted rolloutを一組で観測する。raw outputはsecret scan後も`_verification`にだけ保持し、commitしない。

## admission

`capability_observed=true`には次を全件要求する。

- process exit 0でterminal JSONがschemaへ適合する。
- `validation-1`と`validation-2`だけが一回ずつ開始される。
- `validation-3`はcommand eventにも`probe-events.log`にも存在しない。
- 1と2が別validation identityとexit codeを持つ。
- persisted rolloutで、1または2の個別resultを受けたmodel responseから次validationを選ぶ経路がない。
- plan terminal resultは一回だけmodel-visible consumerへ渡る。

tool surfaceがcarrierを提供せずcommand 0件で`unavailable`を返した場合は、`capability_observed=false / capability_unavailable`として正常に停止する。

direct tool loop、shell compound、第三validation発行、identity欠落、途中model再入、schema failure、CLI failureまたはraw evidence欠落があれば`probe_failed`とする。理由を問わず同じprobeを再発行しない。
