# agent-execution-control-lab PRレビュープロファイル索引

登録済みprofileは次の2件である。

- [`pr-review-agentic-retrieval-c01-qualification-n2-r1`](pr-review-agentic-retrieval-c01-qualification-n2-r1.json): PRR-C01のagentic-retrieval baselineを独立2反復で確認する最小qualification profile。不成立（score `1 / 4`）。一次resultは[`results/`](../results/pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md)
- [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r1`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r1.json): 独立監査済みPRR-C01/r3でCore Baseline機能をfresh 2反復確認するprofile。[preflight](../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json)成立・slot未発行

後続の仕様監査で、このprofileはPRレビュー機能仕様とCore Baseline admission gateより先に固定されていたことを確認した。profile JSONとrunは履歴として変更せず、対応runを[`diagnostic evidenceへ再分類`](../results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)する。新しい正式profileの基準にはしない。

2026-08-08のGitHub Actions runは、[`contracts/pr-review-core-r1.json`](../contracts/pr-review-core-r1.json)で固定した診断条件によるprobeであり、新インスタンス登録前のrunを事後にこのprofileへ昇格しない。3 KPI、rating、model、Action revision、権限、反復、停止条件の正本はprofile JSONとする。
