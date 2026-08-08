# PRレビューschema索引

- [fixture input r1](fixture-input-r1.schema.json)
- [fixture oracle r1](fixture-oracle-r1.schema.json)
- [review output r1](review-output-r1.schema.json)
- [fixture input r2](fixture-input-r2.schema.json)
- [fixture oracle r2](fixture-oracle-r2.schema.json)
- [review output r2](review-output-r2.schema.json)
- [authority selection r1](authority-selection-r1.schema.json)
- [authority packet r1](authority-packet-r1.schema.json)
- [repository snapshot r1](repository-snapshot-r1.schema.json)
- [diagnostic run result r1](run-result-r1.schema.json)
- [qualification以後のrun result r2](run-result-r2.schema.json)

r1は診断経路の履歴schemaである。`fixture-oracle-r2`と`review-output-r2`は複数path finding identityを扱うPRR-C01/r2のcase設計用であり、Baseline profileまたはworkflowへ未接続である。`run-result-r2`はprofile identity、`quality_score`、`total_tokens`を追加した履歴identityであり、r1 resultを事後変換しない。
