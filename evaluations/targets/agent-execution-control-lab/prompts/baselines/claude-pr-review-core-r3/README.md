# claude-pr-review-core-r3

`claude-pr-review-core-r2`のauthority入力を保持し、固定target treeへschema v2 caseの変更後本文をoverlayする`.git`なしのread-only repository snapshotへbindしたBaseline候補である。保存receiptは入力対応の代表としてPRR-C01/r2を固定するが、materializerとtool policyはcase IDに依存しない。

- [`source-prompt.md`](source-prompt.md): r1、r2とbyte-identicalな現行workflow prompt
- [`core-prompt.md`](core-prompt.md): r2の観点を保持し、差分外参照用の`list-files`と`file PATH`だけを追加したCore prompt
- [`manifest.json`](manifest.json): snapshot receipt、materializer、fixture tool r3、schema、content hash
- 入力対応: [`baseline-input-mapping-r3`](../../../contracts/baseline-input-mapping-r3.json)

source-to-Core入力対応後、PRR-C01/r3の独立case設計監査と[fresh N=2 preflight](../../../contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json)が別アーティファクトとして成立した。prompt manifest自体は代表receipt PRR-C01/r2へ固定した履歴identityのまま変更しない。Core Baselineの機能qualification結果は未観測であり、slotも未発行である。
