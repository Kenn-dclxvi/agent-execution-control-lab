# Candidate249 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate249のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate249-start-check-read-interposed-boundary-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `e5b8eff0a1f64932c554f674d9946cbc7fc4caaf7f1a41059bc545f03df5432b`
- prompt bundle: `the-caption-3ce91a4-start-check-read-interposed-boundary-exclusion-r1`
- bundle SHA-256: `bedfb4f5b91c1d65300950bdeef10972e0502be3e8da05f6b2f6739a5453a0e0`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `284c467bb454c61431f09a89a4ba5579e35f14517764bdd8dc8386549438839f`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `5104b2ae3e75cae6ce25d6622a63067516ae0fa1a4ff2bb0695b305b3dab63f0`
- global plan SHA-256: `8844f4a1c55f338a48aad695d3886f90f2ffd841eeb96771a090f19155cb4cad`
- preflight receipt SHA-256: `abc5b9cfd731dbcd3b2d0f607ae8d1cbe7b253b16389cf62b396e48f4ba395a7`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
