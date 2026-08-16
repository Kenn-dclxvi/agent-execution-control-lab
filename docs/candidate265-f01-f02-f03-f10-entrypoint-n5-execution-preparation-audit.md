# Candidate265 F01・F02・F03・F10 entrypoint N=5実行準備監査

> **設計gate訂正（2026-08-16）**: 比較互換preflightは成立したが、Candidate265はpermission開放条件へ禁止済みのモデル自己判定を含んでいた。本来はbundle、profileおよび評価枠を作らず`candidate_not_created`とすべきであり、不足20件の発行は設計gateを通過した正式評価として扱わない。以下は実際の発行履歴を保存し、比較互換性だけではCandidate作成前gateを代替できないことを示す監査である。

## 結論

Candidate264の保存済み四ケース各N=5を基準result `1a64c1b2429c4e89aff3aedd6836944e`へ固定した。Candidate265のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、Candidate265の不足20件だけを許可した。Candidate264は再実行していない。

## 発行前固定

- 対象: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1、各N=5。
- Candidate265 bundle SHA-256: `cc44d86239ebc96fa65f9aaa2652c3824c76bf3f793e1cd340308d4225ce0130`。
- 直接比較基準: Candidate264。
- 基準result: `1a64c1b2429c4e89aff3aedd6836944e`。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate264 pool: `2492f6513ec56a00e80104de1ff63f1252448b273cede8d6d2d1c56e04c18d8c`。
- Candidate265 pool: `16ed6b00180437568c813d404e0db8ca3a18d6a80f1590700e1c241d98ddd499`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- 比較前receipt: `ready`、許可20件、発行前0件。

最初の一時rootでは、比較receiptを含むLayer 1を参照元にしてしまい、`prepare-comparison-layer1`がfail closedで停止した。評価slotは発行していない。次の新規rootで、保存済みの比較receiptを含まないLayer 1へbindし直してからpreflightを再実行した。失敗rootは上書きまたは評価結果への混入をしていない。

## 評価境界

- F01、F02、F03では開始確認と影響を受けない必要readを同じAI判断から発行したかを診断する。
- F10では、`src/AGENTS.md`のterminal result受領前に配下listingまたはentrypoint本文を発行していないことと、受領後に必要readを完遂したことを別々に診断する。
- 品質、機序、token、時間およびvalidation完了待ちの追加モデル再入を分離して記録する。
- validation完了境界、wrapper、yield、wait時間または実行方法はCandidate265の変更対象にしない。

許可した20件だけを発行し、20 / 20件がvalidかつ採点可能、Score `4`となった。Candidate264の再実行は0件だった。Candidate265 selectionは`84ffe31b1c9443bebfdf3b754a657ef5`、analysisは`2e653c61085c4ae6872cdd266b3a7132`、登録resultは`cd29f61f140d400c821e9b1900b40f8a`である。評価後の判断は[`Candidate265 F01・F02・F03・F10 entrypoint N=5`](../evaluations/results/candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)へ分離する。

Layer 3採点とLayer 4登録後にstorage sealを完了した。execution archive SHA-256は`eafff0cb11ed332ccc001697a1ba4119dc1cd6b1a974750492884e4173ba71b8`、final evidence archive SHA-256は`275cc3b764fa78cb8338546b89c6326b99d0acd214988413d93c34d3a5d9605f`である。封印時に再生成した20件のrating viewは、採点時viewと比べてdiffのblob ID表記がfull indexになったことと`generated_at`以外は同一であることを確認した。

当時の実行状態は`preflight_ready / authorized_20 / issued_20 / valid_20 / reference_rerun_0 / registration_completed`として保持し、現在の位置づけを`design_gate_violation_confirmed / should_not_have_been_issued / diagnostic_execution_history`とする。
