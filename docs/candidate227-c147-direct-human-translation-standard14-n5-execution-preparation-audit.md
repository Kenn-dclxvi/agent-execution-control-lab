# Candidate227 C147直接人間語翻訳 Standard14 N=5実行準備監査

## 結論

Candidate147の保存済みStandard14 N=5 result `f7baeadc5bd44399ac13cc0e0a8aff48`と保存Layer 1へ直接bindした。Candidate227のprompt identity以外の互換条件は一致し、比較前receiptは`ready`、許可70件、発行0件である。

## 発行前固定

- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- N: 各ケース5件、合計70 run。
- candidate bundle: `the-caption-3ce91a4-c147-direct-human-translation-r1`、SHA-256 `bc43decca672dff6ed57d5a91eef09cdba86c50a5dc53f4bb6783ea06c11f54a`。
- reference result: Candidate147 `f7baeadc5bd44399ac13cc0e0a8aff48`。
- reference pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`。
- candidate pool: `99dd8e3b7c26cdd6e561a8149152e186e0ffce953f9d76a1f240a3809784b63b`。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- configured M: 24、all-agent token accounting v1。

`seed-pool`はCandidate147の実効条件からCandidate227の空poolを作り、runを再利用または捏造していない。`plan-missing --desired-count 5`は14ケースすべてを既存0件、不足各5件、合計70件へ固定した。

`prepare-comparison-layer1`はCandidate147 resultのcontent、compatibility key、Evaluation set、coverage、全fixture identityを保存Layer 1と照合した。profile SHA-256は`f557f958b8a63de354283c97d8d356a6a1b7103200006cf43ac17a5a74f0900b`、global plan SHA-256は`0e6af0d8fdbd5e0a4711d54e5d5cb1929f835c09f908a304a087d53eea5a87d7`、preflight receipt SHA-256は`7a7e31feefe1cd56699d4a8fb7294552aec09755c7ae8df8c677e55e9ab81389`である。

## 発行前状態

`preflight_ready / authorized_70 / issued_0 / candidate147_new_runs_0`

この状態は発行直前のreceiptを記録する。実行後の結果は[`candidate227-c147-direct-human-translation-standard14-n5_2026-08-14.md`](../evaluations/results/candidate227-c147-direct-human-translation-standard14-n5_2026-08-14.md)を正本とする。
