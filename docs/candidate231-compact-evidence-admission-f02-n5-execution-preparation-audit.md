# Candidate231 F02 N=5実行準備監査

## 結論

Candidate147の保存済みF02 result `b99e9ed0bc974a75805942f9ad05a8cc`へ固定した。Candidate231のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可5件、発行0件である。

## 発行前固定

- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- N: 5
- candidate bundle: `the-caption-3ce91a4-compact-evidence-admission-r1`、SHA-256 `b12b09d692a1ec945ef82593011409e1319272a24ace66b581f8072ea2aef1d7`
- reference result: `b99e9ed0bc974a75805942f9ad05a8cc`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `484fddd4acaf7adc43488c387b9fddbbccecebe6a669acd3c5e2314ea08ae213`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

Candidate228で保存したreceipt-free Layer 1から同じset、fixture、modeを再利用し、F02だけのcoverageをCandidate147の保存済みatomic runへ固定した。Candidate147 F02のtoken中央値は`128,236`、elapsed中央値は`100.60693224985152`秒である。

profile SHA-256は`c1fda3b6ce85cc2afdfafa3c66fe310e904d6dfd9facde3b395afbabce05dd6c`、global plan SHA-256は`424806523a9a3f7af03fee13e4fef75dab809cd4e34bed2a6090917987458561`、receipt content SHA-256は`2dfbb8025fca46c4188fde785d078f8d605e4fba624e5c4e58c404b2e258334e`である。

## 発行前状態

`preflight_ready / authorized_5 / issued_0 / candidate147_new_runs_0`
