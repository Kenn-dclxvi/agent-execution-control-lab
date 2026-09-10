# agentic runtime capability probe r8結果

## 結論

`general-chat-agentic-capability-preflight-r8`を一回だけ発行した。processはexit code `0`でrootとworkerのsessionおよびfinal usageを保存できたが、13 criterionは9件`satisfied`、3件`unsatisfied`、1件`unobserved`となり、`agentic_runtime_capability_unavailable`で封印した。同じidentityを再試行しない。

## worker経路

path-only carrierの基礎経路は成立した。

- rootによるfixture read: 0件
- workerによるfixture read: 1件
- spawn request: 成立
- `sub_agent_activity`、child session、parentおよびcanonical agent path: 成立
- worker terminal result: 存在

一方、rootからworkerへ渡したmessageは固定した許可内容境界を満たさず、worker terminal resultも固定した結論と終了時刻のoracleを満たさなかった。したがって、資料本文をrootへ見せないdependencyは作れたが、必要packetとrequested resultを保った正常carrier全体は未成立である。

## 固定tool経路

MCP initialize、initialized notificationおよびtool listは成立した。model-visible TaskSpecは完全identity`mcp__branch_hours__fetch_branch_counter_hours`へ修正済みだったが、root rolloutとserver auditのcallはいずれも0件だった。r4の短いtool identityだけを原因とする仮説は棄却する。

tool terminal resultは未観測であり、root final responseも固定した二文oracleを満たさなかった。成功時のtool順を追加指示へ転記せず、必要tool callをmodelの選択に依存させないpermissionまたはdependency境界が未解決であると判定する。

## 数値

- elapsed: `19,922 ms`
- root total: `77,430` tokens
- worker total: `32,333` tokens
- all-agent total: `109,763` tokens

## 停止状態

r8は、root-visible資料本文を除き、完全tool identityとpath-only worker carrierを結合した正常経路の一回確認だった。この経路でもrequired resultがそろわなかったため、agentic target全体を登録せず、baseline、Candidate、C147チャット総合評価、採用、releaseおよびprojectionを開始しない。
