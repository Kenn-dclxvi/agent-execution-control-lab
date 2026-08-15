# Candidate242 A02 N=5実行準備監査

## 結論

Candidate147の保存済みA02 result `c08d676a0d97424f88dc2ab1d7fe2961`へ固定した。Candidate242のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate242-start-check-only-completion-exclusion-v14-reasoning-medium-a02-m24-n5-cli0146-r1`
- profile SHA-256: `4446c9ce3ee75df64fe210e5a170c7fb875cb605258b5c9a5161ee4163afbeae`
- prompt bundle: `the-caption-3ce91a4-start-check-only-completion-exclusion-r1`
- bundle SHA-256: `685c08b155bff522d20b9110264cdcaf11f894acc790c2df12dbefaddd82b283`
- reference result: `c08d676a0d97424f88dc2ab1d7fe2961`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- candidate pool: `fb0ccb640522078b804be081e9ef2dc59daa9a4f2c9bbdc1a5c2f9c1fd1b1942`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `f6e9bf1054a0f14ea2eb7845c233d7b7bb806a3fcfc0879ef5eec326c4df65a8`
- preflight receipt SHA-256: `4c34d887b62fb433dae745197ca3bab13171300e66e889582aa99a87d5783452`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
