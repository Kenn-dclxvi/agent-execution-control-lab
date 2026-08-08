# agent-execution-control-lab PRレビューrating contract索引

- [`pr-review-finding-quality-v1`](pr-review-finding-quality-v1.json): 固定oracleとsanitized review outputから0〜4の`quality_score`を生成する現行contract
- [診断用review contract](review-contract-r1.md): Claudeへ提示するfinding構造とレビュー境界

診断用review contractはmodel-visible、quality rating contractとoracleはmodel-invisibleである。2026-08-08のr1 probeを新contractで事後採点しない。
