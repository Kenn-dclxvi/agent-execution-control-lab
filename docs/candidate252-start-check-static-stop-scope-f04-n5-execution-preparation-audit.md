# Candidate252 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate252のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate252-start-check-static-stop-scope-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `ae39580a32d6bdbefb327ba10af8e46a1c064b5e258dd8691d4327b59c3b6637`
- prompt bundle: `the-caption-3ce91a4-start-check-static-stop-scope-r1`
- bundle SHA-256: `3642a4bc9b996339ca7f6b0bcb999ea80cd86dd06117a635d756c10acacaffe1`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `39309bd8e4fe3f4cc79a0361644b3f39ee1caf371b14b4b8e50a712e892b9377`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `a43dda16fb39a082af8af8c3da71f9d504c788953b8d0554f92490cc24864696`
- global plan SHA-256: `45e462b6657b3eee0366019c1380428f233c4bbbd6821b1f7431ac2ba172df46`
- preflight receipt SHA-256: `44ee7b549b1d43e107f3b325dfa4903a9110eafe9911faeffeda7c76a7d2047a`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
