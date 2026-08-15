# Candidate243 A02 N=5実行準備監査

## 結論

Candidate147の保存済みA02 result `c08d676a0d97424f88dc2ab1d7fe2961`へ固定した。Candidate243のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate243-unstarted-read-completion-exclusion-v14-reasoning-medium-a02-m24-n5-cli0146-r1`
- profile SHA-256: `1b85a98554ea6ed2c152b38cd348ac5fc77e39c17dd79f9a61bf194b6fbc122b`
- prompt bundle: `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- bundle SHA-256: `229f6edc654c8cd6fd1375774c464d3305885befb8e44b1f9b7e85bdd3668193`
- reference result: `c08d676a0d97424f88dc2ab1d7fe2961`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- candidate pool: `a89b26c3fefa2eff454f84328d88dab24be955d30e33558405eacde9855cf21f`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `976a771a104932f20bc52aeba8bb1d0e0a38bc5bb80686cdbbf3e630e340fddd`
- preflight receipt SHA-256: `7d9c0f6c30b742b2760540ad08b9ae83dd66524cf6b5850eb1ce02a3649514df`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
