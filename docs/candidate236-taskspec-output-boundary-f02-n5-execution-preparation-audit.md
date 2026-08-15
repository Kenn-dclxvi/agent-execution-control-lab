# Candidate236 F02 N=5実行準備監査

## 結論

Candidate147の保存済みF02 result `b99e9ed0bc974a75805942f9ad05a8cc`へ固定した。Candidate236のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate236-taskspec-output-boundary-v14-reasoning-medium-f02-m24-n5-cli0146-r1`
- profile SHA-256: `641f72fdd746e8ba057298729c5e9c8578ec4aaf440bbf574898a01fccd758bd`
- prompt bundle: `the-caption-3ce91a4-taskspec-output-boundary-r1`
- bundle SHA-256: `f345646bf3ad44296ff52466e9c71922df5a69b92e2b9241a84653d891ad043d`
- reference result: `b99e9ed0bc974a75805942f9ad05a8cc`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- candidate pool: `d3c6c20e957b9960ae11eacd2b4f785577a42c70f9c50f5322340fa07457b8c5`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `b795598cdcb6d66bfc42f6f5177227b336904582b2b93835033d5350273a4b47`
- preflight receipt SHA-256: `344922a3f80a4459154a1d3cda2662fc630297ac3b41c1a225b335b707d88666`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`

不一致が生じた場合は一件も発行しない。実行後に条件差を見つけて参考値へ降格する経路は採らない。
