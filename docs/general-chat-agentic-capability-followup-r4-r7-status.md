# agentic chat capability追試 r4–r8の現在地

## 現在の判定

C147までの制御を一般チャット向けに評価するためのagentic targetは、まだ登録できない。r4–r7で「記録を読めないだけ」の問題と「実際の動作が要求を満たさない」問題を分離し、r8で完全tool identityとpath-only worker carrierを結合した正常経路を一回確認したが、required resultはそろわなかった。

### 固定tool経路

r4でMCP serverの起動、初期化、tool一覧取得までは成立したがcallは0件だった。r8では短いtool名を完全identity`mcp__branch_hours__fetch_branch_counter_hours`へ直したが、再びcallは0件だった。tool transportの入口は利用可能だが、必要resultを得るcall経路は成立していない。

### worker経路

r5とr6ではchild identity selectorが不足していた。r7で専用`sub_agent_activity`を使い、spawn requestからchild sessionとterminal resultまでのidentity bindingは成立した。ところがworkerへ渡されたmessageは許可資料の固定条件を満たさず、worker terminal resultも要求した結論と時刻を満たさなかった。

r8では資料本文をroot inputから除き、root read 0件、worker read 1件、親子identity bindingを成立させた。path-only carrierの基礎経路は確認できたが、worker packetの内容境界とworker terminal resultは固定条件を満たさず、root finalも不通過だった。

## C147チャット対応への影響

現時点で確認できたのは、rootとchildのpersisted session、親子identity、専用activity event、terminal本文、all-agent usageおよび単調時間を安全に投影できることまでである。

まだ確認できていないのは、次の二つである。

1. rootが必要な固定toolを呼び、terminal resultを最終回答へ運ぶこと。
2. rootがworkerへ許可資料だけを渡し、workerが要求されたterminal resultを返すこと。

これらが欠けたままでは、C147の`PRODUCER`、`CONTEXT`、`OWNER_ROLE`、`ROOT`および結果配送を実agentic chat Caseで採点できない。単発応答の既存Caseが通っていても、この不足を補ったことにはならない。

## 停止状態

- capability probe: r3、r4、r5、r6、r7、r8を各一回で封印
- 同一identityの再試行: なし
- agentic target登録: 未実施
- Candidate作成: 未実施
- 総合評価: 未開始
- 採用、release、projection: 未実施

成功したtool順やworker messageを追加指示として転記しない。現在のprompt／TaskSpec／repository authorityの範囲で、modelの選択に依存せず必要なtool resultと限定packetを運べるpermissionまたはdependency境界が一意に定まるまで、次Candidateと評価へ進まない。
