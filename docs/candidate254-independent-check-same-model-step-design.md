# Candidate254 影響しない複数確認の同一model step発行境界

## 結論

Candidate254はCandidate147を直接の基準とし、Candidate253で復元した開始確認との共同発行境界へ、C147の一般的な相互非依存発行境界を人間語で一文だけ戻す。Candidate253はF04で成立した開始境界を保持するsourceとして使うが、直接の親にはしない。

追加する一文は次のとおりとする。

> 受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 意図しない動作 | 結果で次の確認が変わらない複数readを別model stepへ分け、各result受領を次readの発行条件にする |
| 最短の失敗経路 | 開始確認と最初のreadを共同発行 → 一つの連続範囲をread → そのresult受領後に独立した残り範囲を別発行 |
| 閉じる辺 | 互いに影響しない確認resultから待機および次確認の発行へ向かうdependency |
| 保持する正常経路 | 結果によって対象、許可、方法、停止条件が変わる確認だけは別stepへ置ける |
| 合法なcarrier | 同一model step内の個別invocation。特定command、範囲、toolは固定しない |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保持するsource | Candidate253の開始確認との共同発行境界、Candidate246の検証境界 |
| counterexample | Candidate253のF04 trace。直接の親または継承元にはしない |

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、required validationの単一発行判断5 / 5に加え、結果で対象、許可、方法、停止条件が変わらない複数確認を別model stepへ分けたrunが0 / 5の場合だけ機序成立とする。その後にC147との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がC147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`へ一文追加
- 維持target: 追加一文以外をCandidate253と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / independent_check_boundary_passed_4_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
