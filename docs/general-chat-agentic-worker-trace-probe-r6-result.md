# worker trace selector診断probe r6結果

r6を一回だけ発行した。spawn、子session、最終一文、all-agent usageは再び成立したが、同じcall IDの`function_call_output`内部から固定したfield名でchild thread IDを取得できず、runtime spawn result以降は`unobserved`だった。messageから固定JSON objectも一意に取得できなかった。`worker_trace_unavailable`を封印し、r6は再試行しない。

- process: exit code `0`
- elapsed: `18,623 ms`
- root total: `45,838` tokens
- child total: `16,424` tokens
- all-agent total: `62,262` tokens
- root最終一文: `satisfied`

r5とr6の二回で、`function_call_output`を汎用JSONとして読む方法はこのruntimeのchild identity carrierにならないことが確認された。次は観測済みの専用`sub_agent_activity` eventに限定する。packetは表示形式を成果にせず、spawn messageに許可資料の全必須値があり、禁止recordがないことを直接確認する。
