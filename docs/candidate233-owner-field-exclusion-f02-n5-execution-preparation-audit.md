# Candidate233 F02 N=5実行準備監査

## 結論

Candidate147の保存済みF02 result `b99e9ed0bc974a75805942f9ad05a8cc`へ固定した。Candidate233のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 発行前固定

- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- N: 5
- candidate bundle: `the-caption-3ce91a4-owner-field-exclusion-r1`、SHA-256 `e86424f86b12c2d414eb6eeb1752057b322507788784df5a8d750d47392c9cf4`
- reference result: `b99e9ed0bc974a75805942f9ad05a8cc`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `11ed92d75d5df9928137e6085972262feac45d48251d5b1cb8408625684b2ed3`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

profile SHA-256は`a6e707252f19c89cb85bd3250658725be80e52e0e86ca951907b8fa15da93fc8`、global plan SHA-256は`98068e07a9785f506e344bdf026ad037e710ccf6444af8d02f856e29a46bb418`、receipt SHA-256は`b8d59a7a65819922b582764574e20e0df91b13c333f30f4871e3e8a0be54f425`である。

## 発行前状態

`preflight_ready / authorized_5 / issued_0 / candidate147_new_runs_0`
