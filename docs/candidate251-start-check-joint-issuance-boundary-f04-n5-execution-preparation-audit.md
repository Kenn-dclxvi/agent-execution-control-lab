# Candidate251 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate251のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate251-start-check-joint-issuance-boundary-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `2b751353d211db472f08fd0ca62be8c71cf7bc3c0844cee6b6eb72afa4df93d1`
- prompt bundle: `the-caption-3ce91a4-start-check-joint-issuance-boundary-r1`
- bundle SHA-256: `a6d25f4930f5a4f6af59fdfbc901565ab3feb3c115530d936be1912f479d5707`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `554c5451dc877c68387b59d3333a55c56b02804d96f1f898ee3bef4fb3c98561`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `5012d21e5c4aef5c129445887e1f59c26f6d805ce79bf9f69405de13fcd01ce4`
- global plan SHA-256: `c269666932a0887086620735b32378bbc723c8c5a3bde9ef49f6517eb3435be6`
- preflight receipt SHA-256: `68244a224967d53f254777f9c225f39d58053982c11ebb80142bf00b7c5f719c`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
