# agent-execution-control-lab PRレビュープロファイル索引

登録済みprofileは次の4件である。

- [`pr-review-agentic-retrieval-c01-qualification-n2-r1`](pr-review-agentic-retrieval-c01-qualification-n2-r1.json): PRR-C01のagentic-retrieval baselineを独立2反復で確認する最小qualification profile。不成立（score `1 / 4`）。一次resultは[`results/`](../results/pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md)
- [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r1`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r1.json): 独立監査済みPRR-C01/r3を使った初回profile。repetition 1は[GitHub Actions run 31253512886](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253512886)でreviewer開始前に`execution_failed`となった。profileと[preflight](../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json)は変更せず履歴として残す
- [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r2`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r2.json): 固定commitを取得できるようにした二回目のprofile。[GitHub Actions run 31253838176](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253838176)ではreviewerが構造化結果を返せず、`execution_failed`となった。profileと[preflight](../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r2-preflight.json)は変更せず履歴として残す
- [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r3`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r3.json): reviewerの読取り権限と結果回収経路を修正したprofile。[GitHub Actions run 31254138818](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31254138818)では12ターン以内に構造化結果を返せず、`execution_failed`となった。[一次result](../results/pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31254138818.json)を保存済み

一覧の先頭にある旧profileは、PRレビュー機能仕様とCore Baseline admission gateより先に固定されていた。profile JSONとrunは履歴として変更せず、対応runを[`diagnostic evidenceへ再分類`](../results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)する。新しい正式profileの基準にはしない。

2026-08-08のGitHub Actions runは、[`contracts/pr-review-core-r1.json`](../contracts/pr-review-core-r1.json)で固定した診断条件によるprobeであり、新インスタンス登録前のrunを事後にこのprofileへ昇格しない。3 KPI、rating、model、Action revision、権限、反復、停止条件の正本はprofile JSONとする。
