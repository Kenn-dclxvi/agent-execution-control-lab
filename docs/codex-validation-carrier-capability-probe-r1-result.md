# Codex validation carrier capability probe r1結果

> [!IMPORTANT]
> **状態**: `invocation_rejected_pre_model / cli_argument_order_invalid / raw_jsonl_empty / validation_not_started / carrier_unobserved / retry_forbidden`

## 結論

r1はmodelまたはvalidationを一件も開始せず、Codex CLIのargument parserで終了した。carrier能力の成立・不成立には使えない。

固定commandは`codex exec`の後に`-a never`を置いたが、Codex CLI `0.146.0`の`exec` subcommandはその位置の`-a`を受理しなかった。process exitは2、stderrは203 bytes、raw JSONLは0 bytes、`probe-events.log`は存在しない。

同じprobe identityは実行票どおり再発行しない。`-a never`をroot commandの前へ移すCLI transport correctionだけを行う別identity `r2`を作成する。fixture、model-visible prompt、schema、model、reasoning、sandbox、admissionおよびstop conditionは変えない。

## 保存証拠

| field | 値 |
| --- | --- |
| workdir | `/Users/kenn/repos/_verification/codex-validation-carrier-probe-r1.O2soMN` |
| process exit | `2` |
| raw JSONL | `0 bytes` / SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| stderr | `203 bytes` / SHA-256 `cf5ba05f93d786dc2e92e164f54df943c49d91281945ef653ac85aafd4b16a43` |
| marker | `probe-events.log`不存在 |
| stderr cause | `error: unexpected argument '-a' found` |

これはenvironment failureをprompt mechanismへ混ぜないための非admission resultである。r2はr1の結果を再利用せず、新しいworkdirとraw evidenceを持つ。

## 参照

- [`Codex validation carrier capability probe実行票`](codex-validation-carrier-capability-probe-plan.md)
- [`Codex validation carrier能力監査`](codex-validation-carrier-capability-audit.md)
