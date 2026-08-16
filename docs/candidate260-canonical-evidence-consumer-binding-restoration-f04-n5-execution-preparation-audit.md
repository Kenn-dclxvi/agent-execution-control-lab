# Candidate260 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate260のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate260-canonical-evidence-consumer-binding-restoration-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `4c59a0a5cae0fbad27ac185a446fccf70c831bedeccf2cd5b4ee04d78e60168a`
- prompt bundle: `the-caption-3ce91a4-canonical-evidence-consumer-binding-restoration-r1`
- bundle SHA-256: `b9e01c6785d4abb977fa8e7733a24b3c94288f03e0726d57d3153836fea7852f`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `aa718844adb63dfb3a49c0d38b9a877eeca788f49dbab82e7edf77d674904db8`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan content SHA-256: `7d802edae55a1e85275a2c6be47073ac4ff416cfea69c0efa043c531652124da`
- global plan SHA-256: `d89935cd2d5f3a800dd88d5b207e541d3881e5a8bdd05917f13c5a35af6fdc01`
- preflight receipt content SHA-256: `de66745820bb7c1541d95894c3b6e6c2f389a136dbc0b52360b3b049d9ca758c`

## 発行前状態

F04の5件だけを発行する。品質と既存の実行境界に加え、途中result受領後に同じ必要判定用の新しい証拠取得条件を作り、残りのreadを許可した実行が0件であることを確認する。一件でも不通過ならStandard14へ進まない。

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
