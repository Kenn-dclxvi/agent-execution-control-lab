# C02 finding admission calibration r1

## 目的

PRR-C02/r2を変更せず開発用の固定ベンチマークとして再利用し、Opus関係レビュー役が最終findingを採用するときの同一性確認だけを変えたCandidateを1回測定する。

## 比較基準

基準は保存済みの`pr-review-held-out-workflow-topology-comparison-r1:PRR-C02:held-out-relationship-reviewer-opus:r1:a31292887371`である。基準runを再実行しない。新しいrunの発行前に、case、fixture、TaskSpec、repository snapshot、authority、review contract、rating、root model、関係レビュー役model、Action revision、権限、timeout、token accountingが基準と一致することを機械照合する。

## 変更するもの

変更軸は、関係レビュー役がfindingを最終出力へ採用する条件だけである。規則一覧に存在する`rule_id`との完全一致、review contractに基づくcategory、同じ違反の重複排除、違反成立に必要なchanged path集合の一貫性を最終確認する。

関係レビュー役を1人・Opusに固定する構成、rootの役割、fixture-tool、入力、権限、採点、3 KPIの測定方法は変えない。fixture-toolの呼出し回数を減らす制御は別の変更軸なので含めない。

## 実行と解釈

- 対象はPRR-C02/r2、repetition 1だけとする。
- `quality_score`、all-agent `total_tokens`、`elapsed_seconds`を記録する。品質値に実行前の合否閾値を置かない。
- 測定が不成立なら、同じ条件の環境回復以外へ進まない。
- C02/r2は結果確認後の開発用ケースであり、この結果を同じrevisionのfresh held-out evidenceとして扱わない。
- 1ケース1回の結果から、一般化、model ranking、採用、release、本体反映を判断しない。
