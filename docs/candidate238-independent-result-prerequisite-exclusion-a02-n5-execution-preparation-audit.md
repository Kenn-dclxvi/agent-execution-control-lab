# Candidate238 A02 N=5実行準備監査

## 結論

Candidate147の保存済みA02 result `c08d676a0d97424f88dc2ab1d7fe2961`へ固定した。Candidate238のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate238-independent-result-prerequisite-exclusion-v14-reasoning-medium-a02-m24-n5-cli0146-r1`
- profile SHA-256: `79f5f3b41d9120a1c999f7a5600e90b35aad9bd10eacc72ffd86fb9622ac34d7`
- prompt bundle: `the-caption-3ce91a4-independent-result-prerequisite-exclusion-r1`
- bundle SHA-256: `1dfca2ca29c0a66af6c11f956c231c80622322c0e5a008d9bf6f35d13152f8f9`
- reference result: `c08d676a0d97424f88dc2ab1d7fe2961`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- candidate pool: `2bb638a18b07b4e44f579c9624489a9af62349e800ca7e3c5065b74a697d19c3`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `15f660cc84f9630e3d1846f147e0b5e1ea9d7b122a4452b61320e9d01d67c4f6`
- preflight receipt SHA-256: `9470fa8d5e6e908b5e9317bc01f3f382b97bb99241144e8815485779de9cbcb6`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`

不一致が生じた場合は一件も発行しない。実行後に条件差を見つけて参考値へ降格する経路は採らない。
