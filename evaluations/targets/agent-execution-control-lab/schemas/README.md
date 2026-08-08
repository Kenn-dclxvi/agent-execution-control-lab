# PRレビューschema索引

- [fixture input r1](fixture-input-r1.schema.json)
- [fixture oracle r1](fixture-oracle-r1.schema.json)
- [review output r1](review-output-r1.schema.json)
- [fixture input r2](fixture-input-r2.schema.json)
- [fixture oracle r2](fixture-oracle-r2.schema.json)
- [review output r2](review-output-r2.schema.json)
- [fixture input r3](fixture-input-r3.schema.json)
- [fixture oracle r3](fixture-oracle-r3.schema.json)
- [authority selection r1](authority-selection-r1.schema.json)
- [authority packet r1](authority-packet-r1.schema.json)
- [repository snapshot r1](repository-snapshot-r1.schema.json)
- [diagnostic run result r1](run-result-r1.schema.json)
- [qualification以後のrun result r2](run-result-r2.schema.json)
- [PRR-C01/r3 Core Baseline qualification run result r3](run-result-r3.schema.json)
- [PRR-C01/r3 Core Baseline qualification recovery run result r4](run-result-r4.schema.json)
- [PRR-C01/r3 Core Baseline qualification recovery run result r5](run-result-r5.schema.json)

r1は診断経路の履歴schemaである。`fixture-oracle-r2`と`review-output-r2`は複数path finding identityを扱うcase設計で導入した。`fixture-input-r3`と`fixture-oracle-r3`は独立監査済みPRR-C01/r3を既存revisionから分離した。`run-result-r3`は初回実行の条件を、`run-result-r4`は固定commitを取得できるようにした条件を保持する。`run-result-r5`はreviewerの読取り権限と結果回収経路を修正した条件である。過去のschemaとresultは事後変換しない。
