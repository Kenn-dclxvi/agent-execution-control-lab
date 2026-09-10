# worker trace binding診断probe r5結果

## 結論

`general-chat-agentic-worker-trace-preflight-r5`を一回だけ発行した。rootのspawn request、root最終一文、rootとchildのfinal usageは成立し、processはexit code `0`だった。子sessionも一件存在した。一方、runtimeの`function_call_output`からchild thread IDとtask nameを安全に取り出せず、worker packet、runtime spawn result、child sessionおよびchild terminal resultは`unobserved`となった。receiptは`worker_trace_unavailable`で封印し、同じidentityを再試行しない。

## 観測できたこと

- `spawn_agent` request: 1件、task nameと`fork_turns=none`は一致
- runtime output: 2件存在
- session: root 1件、child 1件
- root最終回答: 指定一文に一致
- all-agent usage: 完全
- stderr: 空
- event type: `sub_agent_activity`、`function_call_output`、`task_complete`を含む

したがって、worker処理やrootへの結果到達が失敗したとは判定しない。未成立なのは、runtime output内のchild identityを現在のselectorで取り出し、spawn request、child session、terminal resultへ同じidentityとして結ぶ部分である。

## 数値

- elapsed: `16,177 ms`
- root total: `45,615` tokens
- child total: `16,349` tokens
- all-agent total: `61,964` tokens

## 次の限定範囲

次の診断は、観測済みの`function_call_output`内部と`sub_agent_activity`にあるruntime生成fieldからchild identityを投影する部分だけを扱う。`agent_path`単独、最終回答の内容、子sessionが一件であることからidentityを推測しない。packetについても、message内の駐車場資料projectionと禁止record不在を直接確認する。
