# Candidate257 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate257のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate257-evidence-permission-binding-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `6856b1c5fe8428abffecfc77050e72c669760f94bce85e33e9020e34debfca76`
- prompt bundle: `the-caption-3ce91a4-evidence-permission-binding-r1`
- bundle SHA-256: `73f671c8a9b83b411c5187382b1d937ed765536ae9692856f48518b52a46d03a`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `e5075a570a8edd0fba556f4f18ab70b474b4cdabf6f85f0bd0547c1522918cab`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `3acd5792ae2a0c2411bc97c6a759ec765449f86374a324e40bbdf387065633e0`
- global plan SHA-256: `fd3354b23c5be8396cb72cc09392fe08dab4711736b4344cf85aa17476b9dad2`
- preflight receipt SHA-256: `ecec966e7f46ba9cbadd45539dacfa027025074adc7e64de29035fe284e0f2ff`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
