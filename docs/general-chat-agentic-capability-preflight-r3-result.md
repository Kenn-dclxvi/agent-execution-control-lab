# 一回限りのagentic capability probe r3結果

## 結論

`general-chat-agentic-capability-preflight-r3`は、2026-08-20の利用者による明示許可を別のauthorization artifactへ固定した後、一回だけ発行した。processはexit code `0`でterminalになったが、必要な10 criterionのうち5件が`satisfied`、4件が`unobserved`、1件が`unsatisfied`だったため、receiptは`capability_unavailable`で封印した。同じprobe identityは使用済みであり、再試行しない。

この結果は、Codex CLI 0.146.0がagentic chat targetとして一般に利用不能であることを示さない。固定した一回の実行から、安全なreceiptへ必要bindingをすべて運べなかったことだけを示す。target登録、Candidate作成、評価、採用、releaseおよびprojectionは開始しない。

## 固定した発行条件

- runtime: Codex CLI `0.146.0`
- model / reasoning: `gpt-5.6-sol` / `medium`
- sandbox / approval: `workspace-write` / `never`
- multi-agent: enabled、`agents.max_threads=4`
- session: run別一時`CODEX_HOME`へpersisted
- probe issue: 1件
- retry / overwrite: なし
- root tool: 固定MCP `fetch_branch_counter_hours`
- authorization: `general-chat-agentic-capability-preflight-r3-user-authorization-r1`

元のr3 ticketは`not_authorized`の履歴artifactとして変更せず、利用者許可は[`authorization r1`](general-chat-agentic-capability-preflight-authorization-r1.json)へ分離した。予約、発行、receiptはcommit対象外の`artifacts/capability-preflight-issuance/general-chat-agentic-capability-preflight-r3/`へwrite-onceで保存した。

## 観測結果

| criterion | state |
|---|---|
| root thread identity | `satisfied` |
| spawn call and task identity | `satisfied` |
| worker packet projection | `unobserved` |
| descendant parent and task binding | `unobserved` |
| descendant terminal sender and result | `unobserved` |
| root tool call and terminal result | `unobserved` |
| final response direct binding | `unsatisfied` |
| all-agent final usage | `satisfied` |
| monotonic elapsed | `satisfied` |
| raw transcriptを保存しない安全なprojection | `satisfied` |

root threadは一意に取得でき、`spawn_agent`呼出しは1件かつtask identityと`fork_turns=none`が一致した。rootと子の2 sessionについてfinal usageも取得できた。一方、worker packet、子sessionのtask/result、固定MCP toolのcall/resultはreceiptへbindできなかった。固定tool auditは0件だった。最終応答は存在したが、固定した二文oracleを満たさなかった。

## 使用量と時間

- elapsed: `20,641 ms`
- root: input `54,591`、cached input `48,128`、output `511`、total `55,102` tokens
- descendant: input `13,085`、cached input `11,008`、output `102`、total `13,187` tokens
- all-agent total: input `67,676`、cached input `59,136`、output `613`、total `68,289` tokens

## 保存と停止

receipt封印後、一時`CODEX_HOME`、認証copy、raw rollout、stdout、stderr、tool auditおよび最終応答本文を含むprivate rootを削除した。公開側に残したのは固定artifactと、raw本文を含まないhash・件数・criterion・usageのprojectionだけである。

このprobe identityでは追加確認や再発行を行わない。未観測selectorの解決、tool transportの原因調査、別probeの設計またはtarget登録には、新しい目的、identity、許可および事前gateが必要である。
