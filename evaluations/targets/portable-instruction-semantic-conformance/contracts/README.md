# Runtime contracts

| contract | 役割 |
| --- | --- |
| [`task-spec-wrapper-r1.txt`](task-spec-wrapper-r1.txt) | 全prompt条件へ同じbytesで渡す一回応答TaskSpec wrapper。正解routeを含まない |
| [`codex-cli-0.146.0-capability-catalog-r1.json`](codex-cli-0.146.0-capability-catalog-r1.json) | instruction load、隔離、permissionおよびtool surfaceの観測可能条件 |
| [`codex-rollout-token-accounting-r1.json`](codex-rollout-token-accounting-r1.json) | exec JSONL root usageとprivate persisted transcriptからall-agent tokenを受理する境界 |

これらはProfileの固定入力であり、単独ではdispatchを許可しない。
