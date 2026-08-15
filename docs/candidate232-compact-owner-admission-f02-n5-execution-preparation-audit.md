# Candidate232 F02 N=5実行準備監査

## 結論

Candidate147の保存済みF02 result `b99e9ed0bc974a75805942f9ad05a8cc`へ固定した。Candidate232のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 発行前固定

- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- N: 5
- candidate bundle: `the-caption-3ce91a4-compact-owner-admission-r1`、SHA-256 `561983cde70b6eea16fbb334692e4d00e9c058467ae21b2731a4bde68bc4eb7e`
- reference result: `b99e9ed0bc974a75805942f9ad05a8cc`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `7e8608902d0c351cba8edbe703e4b0894c3efd4bc2125b59fffab209cf88cebf`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

Candidate231でC147 F02 resultへ照合済みのreceipt-free Layer 1を、fileとdirectoryのmodeを含めてそのまま再利用した。最初の二つの準備先はcopy時のfixture identity不一致でpreflight前に拒否され、評価slotは発行されていない。modeを保持した`r3`だけを実行対象とする。

profile SHA-256は`ce760f680bd7fc235721b8808911c9ab739304683a2f64c826f6e2a4f82b254c`、global plan SHA-256は`99a4621c7f2d5d9d59c228900709346db3ac1416467aec203b1a628d26073f8e`、receipt SHA-256は`a5887adbe42fda8838fd89e799a908bdf3959295b04242faaf9b7f56e8e3d57c`である。

## 発行前状態

`preflight_ready / authorized_5 / issued_0 / candidate147_new_runs_0`
