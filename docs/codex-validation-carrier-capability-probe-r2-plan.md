# Codex validation carrier capability probe r2実行票

> [!IMPORTANT]
> **状態**: `probe_ready / r1_transport_corrected / model_visible_bytes_unchanged / non_comparative / single_invocation / retry_forbidden`

## 結論

r2は、model前に終了したr1のCLI transportだけを修正する別probe identityである。`-a never`を`codex exec`の後からroot commandの前へ移す。fixture、model-visible prompt、output schema、model、reasoning、sandbox、required route、admissionおよびstop conditionはr1と同一byte・同一値に保つ。

## 固定identity

| field | 値 |
| --- | --- |
| workdir | `/Users/kenn/repos/_verification/codex-validation-carrier-probe-r2.dDDnH3` |
| CLI | `codex-cli 0.146.0` |
| model | `gpt-5.6-sol` |
| reasoning | `medium` |
| sandbox / approval | `workspace-write / never` |
| attempts | 1 |
| comparison / formal KPI | なし / なし |

fixture SHA-256はr1と一致する。

| file | SHA-256 |
| --- | --- |
| `validation-1.sh` | `bf7775a2a9881593d69505a2b17da86e553086e33254d71ed813aae7fdfc11b5` |
| `validation-2.sh` | `3f7848ddb59edd2b0a51b7bd45f74f45cc2b306c6763d0f24927ba6243f48f65` |
| `validation-3.sh` | `1f93e79d1035979ee59ac654375f111c7a93e3d3035e5b904473b990063b18f5` |
| `final-schema.json` | `d75759454e699a8d169ba1b0c3d0226258fb2679232b94d19e4951a068b6ceee` |
| `probe-prompt.txt` | `bc293e4917176250187c773b1defa11822f2c56be82380837f7c7b26626e84bf` |

## exact command

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

このargument orderがparserに受理されることは、発行前に同じroot option列と`exec --help`を使ってread-only確認した。help成功をcarrier成功として扱わない。

## admissionとstop

required route、`capability_observed`の全条件、`unavailable` routeおよびfailure条件は[`r1実行票`](codex-validation-carrier-capability-probe-plan.md)から変更しない。

r2もmodel前、途中またはterminal後の理由を問わず一回だけ発行する。失敗時にoption、prompt、fixture、modelまたはtool routeを変更して再試行しない。

## 参照

- [`r1結果`](codex-validation-carrier-capability-probe-r1-result.md)
- [`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)
