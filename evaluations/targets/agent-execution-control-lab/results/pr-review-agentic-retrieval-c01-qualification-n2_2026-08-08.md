# PRR-C01 agentic-retrieval baseline qualification N=2

`pr-review-agentic-retrieval-c01-qualification-n2-r1`で固定した2反復のうち、1件がscore `1`、1件がscore `4`だった。pass conditionの2 / 2件score `4`を満たさないため、最小fixture qualificationは不成立で停止する。Candidate A、残り5ケース、N=5、Integrationは発行しない。

| repetition | run | result | quality_score | total_tokens | elapsed_seconds | review_seconds |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1 | [31246780893](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31246780893) | `quality_failed` | 1 | 111,137 | 96.207 | 76.657 |
| 2 | [31246781082](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31246781082) | `pass` | 4 | 152,647 | 93.817 | 77.806 |

一次run JSON:

- [`pr-review-core-r2:PRR-C01:agentic-retrieval:r1:a31246780893`](pr-review-core-r2-prr-c01-agentic-retrieval-r1-a31246780893.json)、content SHA-256 `524596702724620a511e8686286afdfc2ec14ea003d6bd22f213619b514a6d50`
- [`pr-review-core-r2:PRR-C01:agentic-retrieval:r2:a31246781082`](pr-review-core-r2-prr-c01-agentic-retrieval-r2-a31246781082.json)、content SHA-256 `86a80ebddab68a4efd67999f6a7dcdf81ac102e9ec8dc8af232e8b19af9fe85b`

反復1は対象pathとline rangeを指したが、required `rule_id` / category identityへbindせず、`false_negative = 1`、`false_positive = 2`となった。反復2はrequired findingを満たしたが、追加finding 1件を含む。両runともrequested / reported modelは`claude-sonnet-5`で一致し、`quality_score`、`total_tokens`、`elapsed_seconds`を取得できた。

先行attempt [31246647698](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31246647698)と[31246647723](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31246647723)は、reviewer成功後にgraderの`PROFILE_ID`未設定で停止したenvironment failureである。一次run JSONを生成しておらず、N=2 resultへ含めない。修正は[PR #217](https://github.com/Kenn-dclxvi/agent-execution-control-lab/pull/217)で固定した。
