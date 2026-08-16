# Candidate262 A01 / F03 N=5

## 結論

Candidate262はA01とF03の10 / 10件でScore `4`を維持した。A01は5 / 5件でrepository commandを発行せず、未指定modeだけを質問した。F03は5 / 5件で必要成果と必須検証を完了した。

Candidate147との同数比較では、2ケース合算のall-agent token中央値が`-13.83%`、経過時間中央値が`-10.33%`だった。F03もtokenと時間がともに減った。一方、A01単体はtokenが`-2.53%`だが、経過時間は`+21.38%`、絶対値で`+2.60`秒だった。品質を維持してもケース単体で一方の費用が増えているため、`tradeoff_requires_human_judgement`とする。追加N、Standard14、採用は自動承認しない。

## Result identity

- Candidate262 result: `d060b792b7c1498480a39fb78519bfaa`。
- Candidate147 reference result: `ea9b4bfba2054405896a886be25fe6b1`。
- Candidate262 selection: `6a4aaf23fa2449e9b8f4fc8d957c69a4`。
- Candidate262 analysis: `579b9490a3d34af3a7492ed13da0974d`。
- compatibility key: `740cb6782860f75b91235e9f2c9926554e68bd1838e7749f8f414265d6050c8f`。
- valid / excluded / execution error: `10 / 0 / 0`。
- score distribution: Score `4`が10件。

## KPI比較

| 対象 | 指標 | Candidate147 | Candidate262 | 変化 |
| --- | --- | ---: | ---: | ---: |
| A01 + F03 | quality | 100 | 100 | 0 |
| A01 + F03 | all-agent token中央値 | 138,564 | 119,402 | -19,162（-13.83%） |
| A01 + F03 | 経過時間中央値 | 90.765秒 | 81.389秒 | -9.375秒（-10.33%） |
| A01 | quality | 4 / 5件すべて | 4 / 5件すべて | 同値 |
| A01 | all-agent token中央値 | 19,195 | 18,709 | -486（-2.53%） |
| A01 | 経過時間中央値 | 12.148秒 | 14.746秒 | +2.598秒（+21.38%） |
| F03 | quality | 4 / 5件すべて | 4 / 5件すべて | 同値 |
| F03 | all-agent token中央値 | 104,320 | 100,693 | -3,627（-3.48%） |
| F03 | 経過時間中央値 | 70.866秒 | 66.643秒 | -4.222秒（-5.96%） |

合算中央値は各iterationでA01とF03を組にした標本の中央値であり、ケース別中央値の単純な足し算ではない。

## A01の挙動

5件すべてでrepository commandは0件だった。いずれも変更先のmodeを推測せず、artifact変更と試験を開始する前に必要な値だけを質問した。

Candidate261は同じ品質を維持したが、5件中1件でworkspace、branch、HEAD、clean状態を読み取ってから質問した。Candidate262では、開始状態resultが未指定mode、質問permission、質問operationのstop conditionを変えない場合に直接観測するpermissionを閉じた。今回の5件では、この変更対象と観測された行動変化が対応した。

ただしA01のtoken中央値はCandidate147より486少ない一方、経過時間は2.598秒長い。5件のCandidate262実測は14.736秒から14.761秒へ狭く集中し、単一の外れ値だけで中央値が増えた形ではない。この時間増を必要処理の対価とはまだ確認していない。

## F03の挙動

F03は`spec_ready=true`であり、Candidate262の変更対象外である。5件中4件は、開始identity観測と許可済みの対象source・test読み取りを、どちらかのresultを後続発行の判断へ使う前に発行対象へ入れた。残る1件は、pwd、branch、HEAD、statusを個別に完了し、その結果を報告した後にsourceとtestを別発行した。

Candidate147参照は5 / 5件、Candidate261は1 / 5件、Candidate262は4 / 5件でこの初回発行関係が成立した。Candidate262はCandidate261の全体`SPEC`出力制御を継承せず、F03のtoken中央値はCandidate261の128,202から100,693へ`-21.46%`、経過時間中央値は74.504秒から66.643秒へ`-10.55%`となった。これは全体制御を外した方向と対応するが、N=5だけで差分の効果へ全量を因果帰属しない。

初回発行関係が不成立だったrun `635d8cbc83cf44d19431da52e64ddcaf`は149,724 tokenで、F03の最大値だった。ただし同関係が成立したrunにも123,977 tokenがあり、関係の成立だけをtokenまたは品質の完全な予測条件にはしない。

## 判断

今回の局所permission境界は、対象A01で5 / 5件観測され、非対象F03の品質も維持した。合算とF03ではtokenと時間がともに減っており、Candidate261で見られた全体費用増も解消した。

一方、A01単体の経過時間は増えている。利用者が定めた「品質を維持し、tokenと時間がともに少なければ正解。一方が増える場合は人間が判断する」という境界に従い、ここでは追加N、Standard14、正式採用、release、target本体への反映を承認しない。次の判断点は、A01のtoken `-2.53%`と時間`+2.60`秒を許容してStandard14へ広げるか、現行N=5の時間増を先に原因分析するかである。

一次証拠は、[登録result](d060b792b7c1498480a39fb78519bfaa.json)、[品質監査](candidate262-spec-false-start-state-consumer-permission-a01-f03-n5-quality-audit-r1.json)、[行動経路監査](candidate262-spec-false-start-state-consumer-permission-a01-f03-n5-mechanism-audit-r1.json)および比較作業領域の保存analysisである。

`targeted_n5_completed / valid_10_of_10 / score4_10_of_10 / a01_no_repository_command_5_of_5 / f03_c147_initial_issuance_relation_4_of_5 / aggregate_tokens_reduced_13_83_percent / aggregate_elapsed_reduced_10_33_percent / a01_tokens_reduced_2_53_percent / a01_elapsed_increased_21_38_percent / tradeoff_requires_human_judgement / additional_n_not_authorized / standard14_not_authorized / adoption_not_approved / release_not_created / projection_not_performed`
