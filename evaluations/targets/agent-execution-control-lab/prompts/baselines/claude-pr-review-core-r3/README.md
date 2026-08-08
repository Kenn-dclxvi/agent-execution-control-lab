# claude-pr-review-core-r3

`claude-pr-review-core-r2`のauthority入力を保持し、固定target treeへschema v2 caseの変更後本文をoverlayする`.git`なしのread-only repository snapshotへbindしたBaseline候補である。保存receiptは入力対応の代表としてPRR-C01/r2を固定するが、materializerとtool policyはcase IDに依存しない。

- [`source-prompt.md`](source-prompt.md): r1、r2とbyte-identicalな現行workflow prompt
- [`core-prompt.md`](core-prompt.md): r2の観点を保持し、差分外参照用の`list-files`と`file PATH`だけを追加したCore prompt
- [`manifest.json`](manifest.json): snapshot receipt、materializer、fixture tool r3、schema、content hash
- 入力対応: [`baseline-input-mapping-r3`](../../../contracts/baseline-input-mapping-r3.json)

source-to-Core入力対応は成立した。これはBaseline qualification、profile、preflight、evaluation slotの成立を意味しない。次のblockはcase設計の独立qualificationである。
