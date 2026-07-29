# Planning-first route diagnostic

## 結論

route diagnosticはWorker数を採点するものではない。品質、all-agent token、elapsedの差を、planningと実行順から説明するための補助記録である。

## Runごとの記録

保存済みrolloutとall-agent usageから次を記録する。

- operation identity、scope、producer identity、dependency、result consumer
- Worker起動時刻、root command発行時刻、Worker terminal時刻
- root-only、Workerとrootの時間重複あり、Worker後にroot開始の3分類
- Worker待機中に未発行のready root operationがあったか
- 同一operationまたは同一predicateの重複実行とproducer再割当て
- Worker resultが変更、rework、未発行invocation、明示identity requirementのどれへbindされたか
- `fork_turns`、allowed read、root / child token内訳

時刻またはplan stateを保存traceから確定できない項目は`unknown`とする。推測で補完しない。

## 判定境界

route分類、Worker起動数、child token比率だけでqualityまたはcost gateを反転させない。公式KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`だけである。

同一scopeの重複、ready root operationを残した待機、通常経路でのproducer再割当ては制御が狙った経路を実現したかの診断に使う。発生しても、事前固定した停止条件に該当しない限り、routeだけでcandidateを停止しない。
