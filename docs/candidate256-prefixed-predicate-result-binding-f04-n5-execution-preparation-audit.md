# Candidate256 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate256のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate256-prefixed-predicate-result-binding-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `c1038c28f67820e15342570193749027a26b6386cf982b9fca88509da18ebfaf`
- prompt bundle: `the-caption-3ce91a4-prefixed-predicate-result-binding-r1`
- bundle SHA-256: `d60078ae7de46c578896c466cde046e1ef5bd3cf63f8a79af69ce39b7b84e3a9`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `afb69e359be8c838892720de85b10c6098f2bf576eb436d3cc8d5a084c6d8a6a`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- dispatch plan SHA-256: `1aa5298752fa35b61e72f5092edea9fe441968461c73f74158d8664ae40a80a1`
- global plan SHA-256: `7b5ba3a668d268f7b4486ccd14a800dadf5c2722f044fd1ab81515cfaf6522d8`
- preflight receipt SHA-256: `6e921e461a46ef0307035f898f1386c224b1911f18a1d53bd1eae817b93f4f73`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
