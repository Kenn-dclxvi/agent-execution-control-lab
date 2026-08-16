# Candidate262 Standard14 N=5

## 結論

Candidate262をStandard14全14ケース各N=5へ拡張した。既存A01 / F03各5件を再利用し、不足60件だけを発行した。70 / 70件が有効かつ採点可能で、70 / 70件すべてScore `4`だった。

Candidate147比では品質中央値は同値、all-agent総token中央値は`+5.06%`、経過時間中央値は`-2.65%`だった。A02、F02、F04、F07 canonical runnerのtoken増加に追加品質または追加成果はなく、必要処理の対価と確認できない。時間短縮で相殺せず、`quality_passed / unjustified_token_regression / candidate262_adoption_not_approved`とする。

## 実行と品質

- 比較前receipt: `ready`、許可60件。
- 新規実行: 60 / 60 valid、除外0、実行エラー0。
- 再利用: A01 5件、F03 5件。
- 集計: 14ケース×5件、合計70件。
- Score分布: `4 = 70`。
- 登録result: `21fc9d743aa14251a7a17c63425ff4c0`。
- selection: `ae533492844b43f98caad012a9c5dc4f`。
- analysis: `ee782aafbfc6435cb63984971fc4e7a0`。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。

## KPI比較

| KPI | Candidate147 | Candidate262 | 差 |
| --- | ---: | ---: | ---: |
| 品質中央値 | 100 | 100 | 0 |
| all-agent総token中央値 | 1,447,626 | 1,520,846 | +73,220（+5.06%） |
| 経過時間中央値 | 852.543秒 | 829.987秒 | -22.556秒（-2.65%） |

ケース別の全数値とtrace分解は[Standard14 token退行原因監査](../../docs/candidate262-standard14-token-regression-causal-audit.md)を正本とする。

## Targeted境界の保持

再利用したA01 5件はrepository command 0件のままで、変更先modeだけを質問した。F03 5件もScore `4`を維持した。したがってtargeted N=5で確認したA01 permission閉鎖と必要品質は失効していない。

ただし、targeted境界の成立はStandard14全体の費用増を正当化しない。Candidate262の評価単位全体では、品質同値でtokenが5.06%増えた。

## 判断

Candidate262は品質条件を通過したが、tokenと時間をともに減らす採用条件を満たさない。主要token増加に追加成果を確認できないため、`tradeoff_requires_human_judgement`ではなく`unjustified_token_regression`と判断する。

追加N、正式採用、release、target本体への反映は承認しない。Candidate262のresultとA01の成立は履歴として保持する。

一次証拠は[登録result](21fc9d743aa14251a7a17c63425ff4c0.json)、[70件品質監査](candidate262-spec-false-start-state-consumer-permission-standard14-n5-quality-audit-r1.json)、[targeted行動経路監査](candidate262-spec-false-start-state-consumer-permission-a01-f03-n5-mechanism-audit-r1.json)である。

`standard14_completed / valid_70_of_70 / score4_70_of_70 / quality_passed / aggregate_token_regressed_5_06_percent / elapsed_improved_2_65_percent / unjustified_token_regression / additional_n_not_authorized / adoption_not_approved / release_not_created / projection_not_performed`
