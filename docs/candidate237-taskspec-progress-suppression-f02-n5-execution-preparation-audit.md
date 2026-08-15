# Candidate237 F02 N=5実行準備監査

## 結論

Candidate147の保存済みF02 result `b99e9ed0bc974a75805942f9ad05a8cc`へ固定した。Candidate237のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 固定値

- profile: `candidate237-taskspec-progress-suppression-v14-reasoning-medium-f02-m24-n5-cli0146-r1`
- profile SHA-256: `6cb50645b34c7ba41ea13b9beb66ff418a556bc88d82d028d06f75f62bec49f9`
- prompt bundle: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- bundle SHA-256: `2c6f93c228d5b77fc0de4766d54119733aa2e839eaa8b94b786f59703acd0eb7`
- reference result: `b99e9ed0bc974a75805942f9ad05a8cc`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- candidate pool: `18bc36ae647ef44d506872152b91fa7d68e93d17869511268486f47ab122b87b`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- iterations: `1..5`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI: `0.146.0`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: all-agent v1
- `max_workers=24`
- global plan SHA-256: `e710bdecb4da929bdecad2b2cdb24bf27b7c764e264663f0a47624c1e57aae42`
- preflight receipt SHA-256: `ce688da46a00d649b257bd005188dc8a32af21e771a0857b169767c2a35a5bc5`

## 発行前状態

`comparison_preflight_ready / authorized_slots_5 / issued_slots_0 / missing_candidate_runs_5`

不一致が生じた場合は一件も発行しない。実行後に条件差を見つけて参考値へ降格する経路は採らない。
