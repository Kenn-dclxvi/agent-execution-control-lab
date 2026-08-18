# Runtime contracts

| contract | 役割 |
| --- | --- |
| [`task-spec-wrapper-r1.txt`](task-spec-wrapper-r1.txt) | 全prompt条件へ同じbytesで渡す一回応答TaskSpec wrapper。正解routeを含まない |
| [`task-spec-wrapper-r2.txt`](task-spec-wrapper-r2.txt) | response配列を入力snapshotではなく今回の遷移へ限定したC147校正用wrapper。契約矛盾を残した履歴revision |
| [`task-spec-wrapper-r3.txt`](task-spec-wrapper-r3.txt) | 明示scope失効と必要recovery closureを明確化した校正revision。合法なrecovery triggerまで失効させた履歴revision |
| [`task-spec-wrapper-r4.txt`](task-spec-wrapper-r4.txt) | failed ordinary inputの失効と許可済みenvironment recovery triggerを分離し、C147 14 / 14で資格確認した現行transition contract |
| [`codex-cli-0.146.0-capability-catalog-r1.json`](codex-cli-0.146.0-capability-catalog-r1.json) | instruction load、隔離、permissionおよびtool surfaceの観測可能条件 |
| [`codex-rollout-token-accounting-r1.json`](codex-rollout-token-accounting-r1.json) | exec JSONL root usageとprivate persisted transcriptからall-agent tokenを受理する境界 |
| [`codex-rollout-token-accounting-r2.json`](codex-rollout-token-accounting-r2.json) | thread-bound workspaceからpersisted rollout usageを収集する現行all-agent token境界 |

これらはProfileの固定入力であり、単独ではdispatchを許可しない。
