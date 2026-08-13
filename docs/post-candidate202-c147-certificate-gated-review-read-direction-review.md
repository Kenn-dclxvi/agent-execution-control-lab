# Candidate202後 certificate-gated review read方向レビュー

## 結論

Candidate実装へ進める。C147を直接基盤に、明示review operationだけへ二責務を追加する設計は、保存済み正常経路と失敗反例を分離できている。一般反例16状態にblocking counterexampleは0件である。評価条件は別アーティファクトで固定し、comparison preflight前にslotを発行しない。

## 確認した状態

| 状態 | 期待結果 |
|---|---|
| required outcome未固定 | toolなしclarification terminal |
| review非適用、identity mismatchがreadを禁止しない | identityと必要readを共同発行 |
| review非適用、identity resultがread経路を変える | identityだけを先行 |
| consumerなし開始観測 | 発行しない |
| owner語列だけが存在 | producerを起動しない |
| review operationと専用producerが明示 | 一reviewerへbind |
| model-visible許可値 | root projection |
| allowed exact target | reviewer direct observation |
| 両routeが成立 | root projectionを優先 |
| route不能 | reviewer起動前`unavailable` |
| forbidden fieldが空またはnull | keyと存在状態も配送しない |
| projectionだけでcounterexample成立 | direct read 0、`counterexample_found` |
| projectionでcounterexample不成立 | consumerを持つdirect readだけ発行 |
| direct resultからcounterexample成立 | 残りreadを失効し`counterexample_found` |
| required direct observationがnon-value | `unavailable` |
| 全scope成功、反例なし | `no_counterexample_found` |

## 退けた方向

- Candidate202へ文言を追記する: strict `START_BOUNDARY`と大きな共通`DESIGN_ADMISSION`を親化し、Standard14退行を保持する。
- C175を直接親にする: 現在のADR9 read順で7 / 20の先読みがあり、C147直接基盤規律にも反する。
- 新しいdispatch ticketやreceiptを全operationへ追加する: C192〜C196で抽象gateが実tool-call選択を拘束しなかった反例を再導入する。
- counterexample判定用repository readを追加する: projectionだけで成立する20件の不要readを閉じられない。
- routingまたはreceiptを削る: C199〜C201のsource再読、root先読み、input authority欠落を再発する。
- Standard14用の開始条項を追加する: C147正常経路を変更し、新しい判断点を非review経路へ持ち込む。

## 実装許可

C147 full bundleを直接複製し、root `AGENTS.md`だけへ`PRECHANGE_REVIEW`と`REVIEW_READ_TRANSITION`を追加する。C147の既存13条項は逐語保持する。prompt本文へ過去Candidate名、case ID、private oracle、期待scoreを入れない。

静的検証では、非変更target identity、13条項逐語保持、review非適用時のC147経路、projection-first terminal、direct read consumer、owner語列非権限化、forbidden inputおよび三result kindを確認する。

`M3_passed / reviewed_states_16 / unresolved_blocking_counterexamples_0 / candidate_implementation_allowed / evaluation_not_started`
