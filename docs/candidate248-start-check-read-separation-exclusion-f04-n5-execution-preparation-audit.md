# Candidate248 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate248のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate248-start-check-read-separation-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `453c4ee5328b93d2dadda68e2029ab9b506e1c2f24c402d2749329fa9500c7de`
- prompt bundle: `the-caption-3ce91a4-start-check-read-separation-exclusion-r1`
- bundle SHA-256: `8dba56df6ea2180cb49eed6c19b6de23c36858170e61ce971130cef61cca68f7`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `06d32417932c488c149d81b8f9779c004ecc58eb9b5c850c97423e9523e63f1b`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `965b5570d53cdf75e190dc1aa47ddd5a4b188b163d270480d97ddee29fbb73df`
- global plan SHA-256: `4620c6673475015ed1d56876d0e4552ef4f283a01edb7133ad0add4f691ceec6`
- preflight receipt SHA-256: `2270504c6c63919999f8fea3105082eb94f65cff1be386f3c5fd5c0dac4685cb`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
