# Candidate255 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate255のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate255-partial-evidence-result-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `42e3fdbb0288c661e638147d721a3bcab4b310a4eb8720989e7dd7dd27f37ecd`
- prompt bundle: `the-caption-3ce91a4-partial-evidence-result-exclusion-r1`
- bundle SHA-256: `7578b10d76cb3aab15f36e0ae7b50a270f5798d6e6837595e041fa8ccec85fa3`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `34fd2b095f80e8a0c02a0c58e4e427ca24a1792fe0578db18d98d5b4b4259435`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `870944a54e6525dc0853036584d1e7a648259e6595a2d2101f0badf465880133`
- global plan SHA-256: `662aba8db79b2553ace6094b2eacf7fa4fe1acf2faa6264b3035127c429c44e7`
- preflight receipt SHA-256: `296f43fb5b6037c7de89e50a81c10b483ec63d04d575c4e5df2c660d209e4c84`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
