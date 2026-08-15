# Candidate244 F04 N=5実行準備監査

## 結論

Candidate147の保存済みF04 result `177c63c27b1645e6b01f74329656ef5f`へ固定した。Candidate244のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate244-validation-result-dependency-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1`
- profile SHA-256: `078d06018415402516b6b56ac5825b4df93ba402c917a5aa56a8e1461b244d94`
- prompt bundle: `the-caption-3ce91a4-validation-result-dependency-exclusion-r1`
- bundle SHA-256: `e2ac41057d44d72f74ce89f569893723651cdbfd23ec9aa7180d4af0e0e39945`
- reference result: `177c63c27b1645e6b01f74329656ef5f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- candidate pool: `dd8a9f198966b1e22f86c622de4da00df0129ad05cfbb478b6f6f5ad64da6929`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `3c40510a006403c901bcc5d57b32092951a8a9958ad4e7e55a7eaafb9c5cb4e4`
- preflight receipt SHA-256: `bc692a3596e24c0c1a2628699a0715f63b93951fb98688b9de01a662dfd26967`

## 準備中に停止した不一致

1. 初回は14ケースのLayer 1とF04だけの基準resultのcoverage不一致を検出した。
2. 次にF04の既存Layer 1に比較準備receiptが含まれるwrite-once衝突を検出した。receiptを含まない同一内容・同modeの準備用コピーへ切り替えた。
3. Candidate147のtemplateのprompt identityがCandidate244 poolと一致しないことを検出した。prompt名、bundle hash、bundle pathだけをCandidate244へ置換した。

いずれもpreflight完了前に停止し、評価slotは0件のままである。fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件は変更していない。

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`
