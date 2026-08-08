# agent-execution-control-lab PRレビューケース索引

PRレビュー実行経路の診断用固定ケースを引くための索引である。各revisionの`input.json`はmodel-visible、`oracle.json`はmodel-invisibleである。6ケースは新インスタンスゲート前に作られたため、現時点ではfixture qualification済みの正式evaluation setとして扱わない。

| case revision | 主な観測対象 | 状態 |
| --- | --- | --- |
| [`PRR-C01/r1`](PRR-C01/r1/README.md) | prompt変更と評価条件変更の混在 | diagnostic probe使用済み |
| [`PRR-C01/r2`](PRR-C01/r2/README.md) | 複数path関係としてのprompt変更と評価条件変更の混在 | development case設計済み・独立qualification未実施 |
| [`PRR-C02/r1`](PRR-C02/r1/README.md) | artifact、evaluation、release、projectionの状態混同 | 未qualification |
| [`PRR-C03/r1`](PRR-C03/r1/README.md) | ダミーcredential相当値の混入 | 未qualification |
| [`PRR-C04/r1`](PRR-C04/r1/README.md) | 文書の日本語既定 | 未qualification |
| [`PRR-C05/r1`](PRR-C05/r1/README.md) | 複数finding処理 | 未qualification |
| [`PRR-C06/r1`](PRR-C06/r1/README.md) | clean control | 未qualification |
