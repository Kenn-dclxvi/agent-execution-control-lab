# Candidate229 A02 N=5実行準備監査

## 結論

Candidate147の保存済みA02 result `c08d676a0d97424f88dc2ab1d7fe2961`へ固定した。Candidate229のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 発行前固定

- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- N: 5
- candidate bundle: `the-caption-3ce91a4-c147-direct-human-wait-permission-closure-r1`、SHA-256 `4ca0c25b38db273f82d6f7555c3f9d70bb69a4a75cdb440ab330ceab3b241c14`
- reference result: `c08d676a0d97424f88dc2ab1d7fe2961`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `f50842aa954dd3c324d5fcd24515d15730b51a7df2c39722c1e29d30f75a6c60`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

最初の準備先には参照用Layer 1に残っていた既存comparison receiptが複製されたため、write-once衝突で停止した。評価slotは0件だった。`cycle-r2`では同じ保存Layer 1から`set.json`、A02 coverage、fixtureだけをmodeとsymlinkを保持して複製し、receiptを含めずに固定し直した。

profile SHA-256は`8d8708ce5f4bb69012f86111a5ee69840c4ebf1fe685a6e2bafdbfa9ab3a026b`、global plan SHA-256は`757b3b7f0ed6f16214ffafef99836e53ad06683afae288afbb75d07d101d5c8a`、receipt content SHA-256は`85a7ed7f9b3d287499373075dd61c230c1a9b27d1b7bed67863095894ce3100e`である。

## 発行前状態

`preflight_ready / authorized_5 / issued_0 / candidate147_new_runs_0`
