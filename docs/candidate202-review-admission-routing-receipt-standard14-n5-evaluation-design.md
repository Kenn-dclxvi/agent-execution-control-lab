# Candidate202 Standard14全14ケースN=5評価設計

## 結論

Candidate202 `the-caption-3ce91a4-review-admission-routing-receipt-r1`について、Standard14全14ケースを各5回、合計70 atomic runsで実施する。ADR9の`quality_passed / mechanism_failed`判定とStandard14未開始という既存記録は変更しない。今回の利用者による明示的な実行依頼を、Standard14の別実行許可として記録する。

本試験は、Candidate202をADR9 gate通過、採用、releaseまたはprojection済みとみなさない。Standard14の品質、既存実行制御の退行および3 KPIを独立に観測する。

## 固定条件

- evaluation set: `the-caption-standard14-r1 / r1`
- cases: Standard14全14ケース
- iterations: 各5回
- requested slots: 70
- reference result: Candidate175 `c31b560bce92400293c7b3bc40715246`
- model / reasoning: `gpt-5.6-sol / medium`
- Agent/runtime/CLI / Python: reference resultと同一
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- quality rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- target ref: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`

比較前にCandidate175の保存済みresultと保存Layer 1へbindし、宣言したprompt identity以外の互換条件が完全一致するpreflight receiptを保存する。一項目でも不一致、未固定または未確認なら一件も発行しない。

## quality gate

70 / 70 validかつScore `4`を通過条件とする。external failureは同じslotの除外・再発行として別記し、プロンプト品質へ混ぜない。結果確認後にcase、fixture、TaskSpec、oracle、rating、required commandまたはprofileを変更しない。

## 機構診断

Standard14では、少なくとも次を品質と分けて保存する。

- 不要な独立review producer起動
- owner語列だけによるproducer生成
- 開始identityと許可済みreadの共同発行を持つ既存経路の退行
- consumerなし開始identity観測
- terminal補完
- forbidden input配送
- required commandのmachine-bound exit status
- artifact境界

ADR9で確認したcounterexample certificate順序はStandard14では観測不能なので、Standard14通過をADR9機構failureの解消証拠にしない。

## KPI

登録resultの`quality_score`、all-agent `total_tokens`、`elapsed_seconds`だけを保存する。Candidate175との比較はcompatibility key一致後の記述統計とし、採用判断へ自動接続しない。

## 状態

`candidate202_ADR9_quality_passed_mechanism_failed_retained / user_authorized_standard14 / standard14_design_frozen / slots_issued_0 / adoption_not_decided / release_not_created / projection_not_performed`
