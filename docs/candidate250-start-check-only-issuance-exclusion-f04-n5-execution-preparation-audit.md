# Candidate250 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate250のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate250-start-check-only-issuance-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `f7303177d8258a99bc2d68021b53229af3a51840f39b078c49a761e90ef1a1cb`
- prompt bundle: `the-caption-3ce91a4-start-check-only-issuance-exclusion-r1`
- bundle SHA-256: `cd3961d4a065ef94afcf472d4bf4dc8c13fdc1f24379bb7956ed3d898480919b`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `48c739fbc63b6f4b7d7d2874ea292c23d195b1aacc05892780b48be043ccfa67`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `5569c9370b4f650b41809374f7b855dd0a6b1a7b17d345b70ece00257e9b134e`
- global plan SHA-256: `a0ed763c6b78abc60c167703299919d7596ff498e9fafbd36366ed04567218ae`
- preflight receipt SHA-256: `cd82cb15e98858df28c854ce007c49b1a56413a94b7f9d3a9a34c0fe7f2371cb`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
