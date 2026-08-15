# Candidate228 A02・F02・F03 N=5実行準備監査

## 結論

Candidate147の保存済みatomic runからA02、F02、F03各5件を選び、参照result `0444608873624c8ab9e39726769f542d`へ固定した。Candidate228のprompt identity以外の実効互換条件は一致し、比較前receiptは`ready`、許可15件、発行0件である。

## 発行前固定

- cases: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- N: 各5件、合計15件
- candidate bundle: `the-caption-3ce91a4-c147-direct-human-permission-boundaries-r1`、SHA-256 `5d6b1913c31893b14601e94c001082746ef8486528ebbc78cbd896e5108e84b6`
- reference result: `0444608873624c8ab9e39726769f542d`
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`
- candidate pool: `50917cf07f575b29b14c7f85961d4312974b088fd3454241f4b1aedf70c1b412`
- compatibility key: `ecad7b450511697e60b62d3b93db7b2fe06dacf667ed8634033e42cba0d8b718`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- permission: `workspace-write / never`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24、all-agent token accounting v1

`select-runs`はCandidate147 poolから対象3ケース各5件だけを選び、15件の参照resultをwrite-onceで登録した。`seed-pool`はCandidate228の空poolを作り、`plan-missing --desired-count 5`は既存0件、不足各5件、合計15件を固定した。

最初の準備では14ケースcoverageの参照Layer 1を指定したため不一致で停止し、次の準備ではfixtureのcopy mode不一致を検出した。いずれもpreflight前で発行0件だった。最終の`cycle-r4`では保存Layer 1のfixture modeとsymlinkを保持し、coverageだけを登録済み参照resultの3ケースへ一致させた。

profile SHA-256は`6c2ef322c219c0885d60bcf9d8dcb20badebded0a77fcc8ee0164fc3d65d63dc`、global plan SHA-256は`53fde2930a87dea83cfd34cfb7043d4255bbbb8a1be4ce272dbbecbb955a66ff`、receipt content SHA-256は`1c863a1bdbc2636bbce5bef630ecdad95e4ee07f9f7c565febbbaf03b5e77db3`である。

## 発行前状態

`preflight_ready / authorized_15 / issued_0 / candidate147_new_runs_0`
