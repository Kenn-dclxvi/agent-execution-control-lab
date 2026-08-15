# Candidate254 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate254のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate254-independent-check-same-model-step-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `19656f62c7e092a17e47b78bd11a2e700180f00bb29ca060cc404fac9b576bb9`
- prompt bundle: `the-caption-3ce91a4-independent-check-same-model-step-r1`
- bundle SHA-256: `7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `6d9ef100ef27af794306a6e844f97eac828c086cc1791e1fafefae28248ea6da`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `58560cee2e87d5f6be4b18437a4ae83bbc65355bac777edf1a5114b11c246c7d`
- global plan SHA-256: `4c5f5d00a3175c38c7bda07e5b2acbcaade32f1d985bbbcb7addd58219904499`
- preflight receipt SHA-256: `0f1445a731e726e141a6ad69dda7e6efa0176dd5a8d90f56288cc26601ed63b1`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
