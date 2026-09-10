# holdout reference panel preflight r1 結果

## 結論

sealed holdoutのreferenceを形成する独立AI panel 3件について、実行機能、発行Schema、reference report Schemaおよびrun result Schemaを含む発行前preflightが成功した。全slotは`ready_not_issued`であり、モデル呼び出しは行っていない。資格graderも未発行である。

## 固定したreceipt

- receipt ID: `general-chat-semantic-holdout-reference-r1-preflight-r1`
- 外部run root: `/Users/kenn/repos/_verification/general-chat-response-control/semantic-holdout-reference-r1-attempt-r2`
- `preflight.json` file SHA-256: `76482c7c99ebfead2ec5c44b53a09b28a515fb70fe6c91087a12600349958df9`
- receipt content identity: `d67af0388ce21b39b2f433487ee3380525dd90407b1c397c0f8b51d4f834c76a`
- authorized slot count: `3`
- issued slot count: `0`
- state: `ready_not_issued`

## runtime identity

- runtime ID: `codex-cli-0.148.0-aarch64-apple-darwin-ed2ccedcb9671e09ba92aa31eecdf60492b7c145609f02a1d22e066b7a10e4e7`
- alias: `codex-0.148`
- version output: `codex-cli 0.148.0`
- entrypoint SHA-256: `b0308517b20543012fa2171aa3d46ce455a7456c4eb2a552ab9468ba4eeb1e50`

## 固定slot

- `semantic-holdout-reference-terra-r1-run-1`
- `semantic-holdout-reference-terra-r1-run-2`
- `semantic-holdout-reference-terra-r1-run-3`

各slotは別のpacket ID、提示順、stdinおよび一時`CODEX_HOME`を持つ。他slotのlabel、organizer map、holdout正本ID、将来のreference labelおよび資格grader resultは渡さない。

## 現在の効果

このpreflightが許可するのは、固定receiptからreference panel 3件を同時に一度だけ発行することだけである。referenceの成立、graderの適格性、正式評価、r2有効化、prompt採用、releaseまたはprojectionを意味しない。

次の発行前にreceiptを再検証し、repository source、外部material、runtime bindingまたはreceipt identityのdriftがあれば3件とも発行しない。

## 失効したpreflight

`attempt-r1`はpreflight作成後にrunnerへ実行、集計および二重発行拒否を追加したため、runnerとSchemaのdriftにより失効した。発行数は`0`であり、モデルslot、labelまたはreference resultは存在しない。`attempt-r1`を更新または再利用せず、実行経路全体を固定した`attempt-r2`を現在の発行receiptとする。
