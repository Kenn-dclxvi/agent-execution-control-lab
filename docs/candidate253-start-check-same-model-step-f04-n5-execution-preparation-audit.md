# Candidate253 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate253のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate253-start-check-same-model-step-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `c25646239c6e71554acbd22ff104af9fdc2845ff696ada0b4f5c93dceb77d1d0`
- prompt bundle: `the-caption-3ce91a4-start-check-same-model-step-r1`
- bundle SHA-256: `b48c7160ae14fa2fcd5716b27dbc7e194423ea1f484ad5a00fdc2b04d267fec2`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `38202db5d0be5b68ac9ef2177a1b961bc1834a2c2be89c3ede3c5581e23423ed`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `19e8c2d0af1cdbd2b7e64bc2526547c9d5e282cc4ade13f99e5e21677e74a287`
- global plan SHA-256: `cc7f17914dc45c448f008a31d71da7e34bf8f653bc3508c19c0692568cd13037`
- preflight receipt SHA-256: `15b6fa7929c7d9fc272f4040437a55b03baeeddbc1532106762e1703cd11cc76`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
