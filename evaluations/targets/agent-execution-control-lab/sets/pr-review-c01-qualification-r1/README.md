# PRR-C01 qualification r1

- set identity: `pr-review-c01-qualification-r1 / r1`
- membership: `PRR-C01/r1`
- target ref: `8cd97283e60f13393fb1302c601c9a4fe0a5381f`
- 用途: `agentic-retrieval` baselineの独立2反復による最小fixture qualification
- pass condition: 2 / 2件がrateable、`quality_score = 4`、model identity一致、3 KPI取得可能
- stop condition: 1件でもscore `4`未満、unrateable、model不一致、`total_tokens`または`elapsed_seconds`欠落なら停止

このsetは新インスタンスゲート4の実行系安定性確認だけに使う。6ケース全体のcontrol-free qualificationまたはvariant比較のresultへ混ぜない。
