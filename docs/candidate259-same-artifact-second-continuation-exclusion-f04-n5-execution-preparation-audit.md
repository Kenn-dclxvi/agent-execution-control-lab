# Candidate259 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate259のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate259-same-artifact-second-continuation-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `f77b9e969314c41f089466782fbfca8c66abfa8692eac3a7048d8cea003be470`
- prompt bundle: `the-caption-3ce91a4-same-artifact-second-continuation-exclusion-r1`
- bundle SHA-256: `93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `88cd93fb4ddcffa8903a7658733848e9985e21590aa1f754fa93fd82e03bfe4d`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `aca2576b7a184134c87949882170daf1fe857993e6511d8d8f40c1cb5ee26699`
- global plan SHA-256: `66993641bc45d881e5ca52d853150aa297ca3541b09cda8c75788ecbd82ab7bd`
- preflight receipt SHA-256: `038d6b0eb7a1fdeb2acf97e730cb4c640fb69900663d38b62ad5f0ec777b00be`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
