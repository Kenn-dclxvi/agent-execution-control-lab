# Candidate230 A02・F02・F03 N=5実行準備監査

## 結論

Candidate147の保存済み対象3ケースresult `0444608873624c8ab9e39726769f542d`へ固定した。Candidate230のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可15件、発行0件である。

## 発行前固定

- cases: A02 r2、F02 r1、F03 r2
- N: 各5件、合計15件
- candidate bundle SHA-256: `b7f9374e6d7d239472b69f4666de20ab5d6ed31bfc3e6bfa6aad12e572768f78`
- reference result: `0444608873624c8ab9e39726769f542d`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `982698eff5c515a35ce274fe8e302f96582bda71578d09b03a186b61fe48fe72`
- compatibility key: `ecad7b450511697e60b62d3b93db7b2fe06dacf667ed8634033e42cba0d8b718`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

Candidate228で固定した同じ3ケースのreceipt-free Layer 1とtemplate条件を再利用し、prompt identity、bundle hash、bundle pathだけをCandidate230へ置換した。`seed-pool`は空poolを作り、各ケース不足5件、合計15件だけを固定した。

profile SHA-256は`1c89fcb712150f98e596cef459d390393fae2cee34404413dba695e8d525b76f`、global plan SHA-256は`ea5b47781c8b3a66fd249b23a31e2a179091b5f8ae723656adfeb377e8eb0b7a`、receipt content SHA-256は`0e1368ab401f3c308026460d30fa0c1df844990bf7388da06806202469f67c36`である。

## 発行前状態

`preflight_ready / authorized_15 / issued_0 / candidate147_new_runs_0`
