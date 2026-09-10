# 固定MCP tool transport診断probe r4

## 目的

r3で同時に未観測となった固定tool経路とworker trace経路を分離する。r4は固定MCP serverへの接続、tool一覧取得、tool call、terminal result、root rollout上のcall、最終一文およびroot usageだけを観測する。workerは起動せず、worker trace binding、target登録、Candidate作成および評価を判定しない。

## r3からの限定差分

- 直接の前段は`general-chat-agentic-capability-preflight-r3`の封印済みresultとする。
- multi-agentを無効にし、駐車場資料とworker操作をmodel-visible inputから除く。
- 固定tool serverは`initialize`、`notifications/initialized`、`tools/list`、正しい`tools/call`だけを内容非依存の安全なaudit eventへ投影する。
- `--ignore-user-config`で利用者設定を除き、一時`CODEX_HOME`には認証だけをcopyする。plugin設定は読み込まず、追加のplugin disable flagにも依存しない。

成功runの手順を新しいchat制御へ転記する作業ではない。r3で到達しなかったtool dependencyだけを独立して観測可能にする評価基盤上の診断である。

## 合格条件

一回の実行でroot threadが一意にbindされ、MCP initializeとtool listが確認でき、固定入力によるtool callと固定resultが一件ずつ対応し、root rolloutにもcallが一件あり、最終一文、root final usage、単調時間およびrawを保存しないprojectionがすべて`satisfied`の場合だけ`tool_transport_available`とする。

一件でも`unobserved`または`unsatisfied`なら`tool_transport_unavailable`とする。process exit codeだけで合格にしない。安全なerror categoryは原因の切分けにだけ使い、欠けたtool resultを補わない。

## 発行と停止

probe identityは`general-chat-agentic-tool-transport-preflight-r4`、発行上限は一件、retryとoverwriteは不可とする。予約後は失敗してもidentityを再利用しない。receipt封印またはterminal failure後にprivate root、raw rollout、stdout、stderr、認証copyおよび最終本文を削除する。
