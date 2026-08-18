# Portable semantic heldout r3 N=1比較結果

> [!IMPORTANT]
> **状態**: `completed / compatible / c147_score4_14_of_14 / portable_score4_14_of_14 / token_regression / elapsed_improvement / n_extension_required / adoption_not_decided`

## 結論

heldout r3ではC147 referenceとportable full-agent r1がともに14 / 14 valid、14 / 14 Score 4、14 / 14機序成立となった。portableはC147の機能境界を全件再現した。

効率は一方向に改善していない。portableは経過時間を短縮したが、tokenは増加した。したがって現時点ではcost改善と判定せず、互換条件を維持したN拡張が必要である。

| 指標 | C147 | portable | portable - C147 |
| --- | ---: | ---: | ---: |
| token中央値 | 15,811.5 | 15,837.5 | +26.0 |
| token合計 | 221,559 | 221,926 | +367 |
| elapsed中央値 | 10.033秒 | 9.773秒 | -0.260秒 |
| elapsed合計 | 151.734秒 | 135.840秒 | -15.894秒 |

対応Caseではportableのtokenが少ないのは4 / 14件、elapsedが短いのは10 / 14件だった。N=1のため安定傾向とは扱わない。

## 境界

- portable prompt、TaskSpec r4、heldout r3、oracle、rating、runtimeは比較中に変更していない。
- r2の設計不適格resultをr3比較へ混ぜない。
- qualityと機序の全件成立は確認済みだが、採用、release、projectionは未決定である。
- 次は同じatomic条件でNを拡張し、tokenとelapsedの両方が減るかを確認する。

このN拡張は完了した。後続の正本は[`N=5比較結果`](portable-semantic-heldout-r3-n5-comparison-result.md)とする。
