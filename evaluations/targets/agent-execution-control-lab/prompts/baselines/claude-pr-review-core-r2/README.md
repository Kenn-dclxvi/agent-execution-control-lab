# claude-pr-review-core-r2

`claude-pr-review-core-r1`のレビュー観点を保持し、固定treeから検証済みauthority原文をmodel-visible packetへmaterializeするfixture tool r2へbindしたBaseline候補である。

- [`source-prompt.md`](source-prompt.md): r1とbyte-identicalな現行workflow prompt
- [`core-prompt.md`](core-prompt.md): r1とbyte-identicalなCore prompt
- [`manifest.json`](manifest.json): authority packet materializer、fixture tool r2、schema、content hash
- 入力対応: [`baseline-input-mapping-r2`](../../../contracts/baseline-input-mapping-r2.json)

authority入力は意味同一性まで成立した。changed path以外のrepository read範囲が未固定であるため、現在状態は`admission_blocked`である。
