# 一般チャットChatControlFree N=1 attempt r2外部失敗

## 結論

run別一時`CODEX_HOME`へskillsとmodel cacheを隔離したprofile r2でも、core-r1 8 Caseは8 / 8件がprocess exit code `1`となり、測定は成立しなかった。stderrは全件空で、runtime r2がCodex JSONL stdoutのerror eventをresultへ要約しなかったため、失敗原因を確定できない。

一次resultは[`chat-control-free-core-r1-n1-qualification-r2.json`](../evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n1-qualification-r2.json)である。Case、prompt品質、schema適合またはtokenの結果として扱わない。

## r1から維持した条件

Case、fixture、TaskSpec、oracle、rating、prompt、model、reasoning、permissionおよび8 slot coverageはr1から変更していない。変更したのはruntime stateの置き場所だけである。

## r2で確認できたこと

- 共有`CODEX_HOME`の`Directory not empty`と古いCLIによる共有`models_cache.json`読込エラーはstderrに再出現しなかった。
- model final response、schema validation、quality ratingおよびtokenは取得できなかった。
- stdout error eventの保存または安全な要約がないため、認証、schema transport、model requestまたは別のterminal failureを区別できない。

## 次の許可範囲

同じ8 Caseを再実行しない。Candidateを作成しない。固定JSON一件だけを返す非評価transport probeを一回実施し、次を同一receiptへ保存する。

- process exit code
- Codex JSONLのthread、terminal、usageおよびerror eventの種類と安全なmessage
- stderrのSHA-256と非機密tail
- final responseの有無、schema適合およびSHA-256
- 単調時計elapsed

probeが認証またはtransportの修正点を一意に示した場合だけ、新しいruntime/profile identityでqualificationを再設計する。原因をbindできない場合は`measurement_not_established`で停止する。
