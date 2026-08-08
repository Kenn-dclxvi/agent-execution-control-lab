# claude-pr-review-core-r3

`claude-pr-review-core-r2`のauthority入力を保持し、固定target treeへschema v2 caseの変更後本文をoverlayする`.git`なしのread-only repository snapshotへbindしたBaseline候補である。保存receiptは入力対応の代表としてPRR-C01/r2を固定するが、materializerとtool policyはcase IDに依存しない。

- [`source-prompt.md`](source-prompt.md): r1、r2とbyte-identicalな現行workflow prompt
- [`core-prompt.md`](core-prompt.md): r2の観点を保持し、差分外参照用の`list-files`と`file PATH`だけを追加したCore prompt
- [`manifest.json`](manifest.json): snapshot receipt、materializer、fixture tool r3、schema、content hash
- 入力対応: [`baseline-input-mapping-r3`](../../../contracts/baseline-input-mapping-r3.json)

source-to-Core入力対応後、PRR-C01/r3の独立case設計監査とfresh N=2 preflightを別アーティファクトとして作成した。[初回条件](../../../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json)と[二回目の条件](../../../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r2-preflight.json)は測定環境の問題で終了した。[三回目の条件](../../../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r3-preflight.json)ではreviewerが動作したが、ターン上限までに構造化結果を返せなかった。後続の[`実行互換監査`](../../../contracts/baseline-execution-parity-r1.json)で、入力値は対応していても元workflowと実行条件が一致しないことを確認した。prompt manifest自体は代表receipt PRR-C01/r2へ固定した履歴identityのまま変更しない。Core Baselineの品質はまだ観測していない。
