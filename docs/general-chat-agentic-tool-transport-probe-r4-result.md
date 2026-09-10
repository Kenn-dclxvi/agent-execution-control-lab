# 固定MCP tool transport診断probe r4結果

## 結論

`general-chat-agentic-tool-transport-preflight-r4`を一回だけ発行した。MCP serverの`initialize`、初期化完了通知および`tools/list`は各1件成立し、stderrは空、processはexit code `0`だった。一方、`fetch_branch_counter_hours`のcallはserver auditとroot rolloutの双方で0件であり、最終一文もoracleを満たさなかった。receiptは`tool_transport_unavailable`で封印し、同じidentityを再試行しない。

## r3から切り分けられたこと

r3の固定tool未観測は、MCP serverが起動できないこと、初期handshakeに失敗すること、tool一覧を取得できないことではなかった。r4ではそこまでの経路を直接確認できた。未成立の境界は、一覧に現れた固定toolをmodelがcallし、terminal resultを受け取る部分に限定された。

これはtool callをpromptだけで常に強制できないことの一般証明ではない。また、成功時のtool順をchat向け制御へ転記する根拠にもならない。固定した一回の診断ではcallが発行されなかったという結果だけを保持する。

## 観測結果

| 項目 | 状態 |
|---|---|
| root thread | `satisfied` |
| MCP initialize | `satisfied` |
| MCP tools list | `satisfied` |
| 固定tool callとresult | `unobserved` |
| root rollout上のtool call | `unobserved` |
| 最終一文 | `unsatisfied` |
| root final usage | `satisfied` |
| 単調時間 | `satisfied` |
| rawを保存しないprojection | `satisfied` |

- elapsed: `9,965 ms`
- input: `29,862` tokens
- cached input: `11,008` tokens
- output: `209` tokens
- total: `30,071` tokens
- safe error category: 0件

## 現在の停止境界

r4ではtarget登録、Candidate作成および評価へ進まない。固定toolを必要とするagentic chat Caseは、tool call/resultを観測できる別の合法なdependency境界が確定するまで未登録のままにする。r3で同時に未観測だったworker trace bindingは別の原因なので、tool callの成否を流用せず別probeで確認する。
