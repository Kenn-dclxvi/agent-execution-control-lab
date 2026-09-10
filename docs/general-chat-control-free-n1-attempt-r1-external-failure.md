# 一般チャットChatControlFree N=1 attempt r1外部失敗

## 結論

`general-chat-response-control`のcore-r1 8 Caseへ`ChatControlFree` N=1を発行したが、8 / 8件がmodel応答前の外部失敗となり、測定は成立しなかった。Case、TaskSpec、oracle、ratingまたはprompt品質の結果として扱わない。

一次resultは[`chat-control-free-core-r1-n1-qualification-r1.json`](../evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n1-qualification-r1.json)である。状態は`measurement_not_established / candidate_not_created / adoption_not_decided / release_not_created / projection_not_authorized`とする。

## 固定済み条件

- target: `general-chat-response-control`
- set: `general-chat-core-r1`
- prompt: `chat-control-free-r1`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0
- permission: `read-only / never`
- preflight: 8 slot authorized、0 issuedで保存後に発行
- dispatch: 8 slotを一回だけ発行

## 観測した外部失敗

全8件がprocess exit code `1`だった。共通して次を観測した。

- 共有`CODEX_HOME`のsystem skills更新時に`Directory not empty`が発生
- 共有`models_cache.json`をCodex CLI 0.146.0が読み、`missing field base_instructions`で失敗

Desktopと複数CLI runが共有状態を更新する環境競合であり、model応答、schema検証、採点およびtoken取得へ到達していない。

## 回復境界

同じr1 slotを再実行しない。Case、fixture、TaskSpec、oracle、rating、prompt、modelおよびreasoningを変えず、runtime stateだけをrunごとの一時`CODEX_HOME`へ隔離したprofile r2を新しく作る。

- 認証はホストの既存auth identityを一時homeへsymlinkし、内容をresultまたはリポジトリへ保存しない。
- system skillsとmodel cacheをrun間で共有しない。
- 一時home、stdout、stderrおよびraw transcriptをリポジトリへ保存しない。
- r2も外部失敗なら、追加再試行せず測定基盤を`blocked`ではなく`measurement_not_established`で停止し、別の実行transportを設計する。

これはprompt Candidateの修正ではなく、新targetの測定成立に必要なenvironment-only recoveryである。
