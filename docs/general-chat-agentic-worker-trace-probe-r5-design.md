# worker trace binding診断probe r5

## 目的

r3で子sessionが存在した一方、worker packet、runtime spawn result、子sessionのtask identityおよびterminal resultを一つの対応関係へbindできなかった原因を、固定MCP tool経路から分離して観測する。r5はworker一件だけを起動し、toolを与えない。

直接の前段はr3である。r4のtool transport resultは別原因の診断であり、r5へ継承しない。

## 対応関係

rootの`spawn_agent` requestにあるcall ID、task name、`fork_turns`およびmessage全体を固定する。同じcall IDのruntime outputからchild thread IDとtask nameを受け取り、そのchild thread ID、root parent IDおよびsession metadataのcanonical agent pathが一致する一件だけをworker sessionとする。この対応が成立した場合だけ、そのsessionの`task_complete.last_agent_message`をworker terminal resultとして採用する。

`agent_path`単独、子sessionが一件であること、terminal本文の内容またはroot最終回答からtask identityやsenderを推測しない。runtime outputのselectorが未観測ならcriterionを`unobserved`にし、安全なevent typeとresponse item typeの一覧だけをreceiptへ残す。

## 合格条件と停止

root identity、spawn request、packet、runtime spawn result、child session binding、child terminal result、root final response、rootとchildのfinal usage、単調時間および安全なprojectionがすべて`satisfied`の場合だけ`worker_trace_available`とする。一件でも不足すれば`worker_trace_unavailable`とする。

identityは`general-chat-agentic-worker-trace-preflight-r5`、発行は一回、retryとoverwriteは禁止する。receipt封印後にprivate rawと認証copyを削除する。r5だけではtarget登録、Candidate作成または評価へ進まない。
