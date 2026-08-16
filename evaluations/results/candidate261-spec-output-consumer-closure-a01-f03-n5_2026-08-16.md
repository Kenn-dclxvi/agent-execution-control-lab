# Candidate261 A01 / F03 N=5

## 結論

Candidate261はA01とF03の10 / 10件でScore `4`を維持した。しかしCandidate147との同数比較では、2ケース合算のall-agent token中央値が`+6.09%`、経過時間中央値が`-0.08%`だった。時間差は実質同水準だが、token増加を必要な品質または成果の対価と説明できないため、`unjustified_cost_regression`とする。追加NとStandard14は実施せず、採用を承認しない。

## 比較条件

- Candidate261 result: `ceb2507860c74bc1834126c94b44d6c6`。
- Candidate147参照result: `ea9b4bfba2054405896a886be25fe6b1`。
- A01 r2、F03 r2、各N=5。
- model / reasoning: `gpt-5.6-sol / medium`。
- Codex CLI 0.146.0、Python 3.14.5、`workspace-write / never`、設定上の同時実行上限24。
- prompt identity以外のcomparison compatibilityは一致した。

Candidate147は再実行していない。保存済みatomic runから対象10件だけを選び直した。

## 品質

10 / 10件がvalidかつ採点可能で、10 / 10件すべてScore `4`だった。A01は未指定のmodeを推測せず、変更と試験を開始せず質問して停止した。F03は許可対象だけを変更し、focused gateとfull gateを完了した。command protocol違反、許可外変更、外部失敗は0件だった。

## KPI比較

| 対象 | 指標 | Candidate147 | Candidate261 | 変化 |
| --- | --- | ---: | ---: | ---: |
| A01 | token中央値 | 19,195 | 18,764 | `-2.25%` |
| A01 | 経過時間中央値 | 12.148秒 | 15.532秒 | `+27.85%` |
| F03 | token中央値 | 104,320 | 128,202 | `+22.89%` |
| F03 | 経過時間中央値 | 70.866秒 | 74.504秒 | `+5.13%` |
| 2ケース合算 | token中央値 | 138,564 | 147,007 | `+6.09%` |
| 2ケース合算 | 経過時間中央値 | 90.765秒 | 90.696秒 | `-0.08%` |

合算の時間だけを見るとわずかに短いが、ケース別ではA01とF03の両方が長い。selection iterationの組み合わせで生じた合算中央値の差を、時間改善とは扱わない。

## 行動経路の違い

### A01

Candidate261は5件中4件でrepository commandを一件も発行せず、未固定のmodeだけを質問した。残る1件はworkspace、branch、HEAD、clean状態を確認してから質問し、38,028 tokenを使った。開始状態resultの受け取り先を利用者向け進捗にしない二文は、不要な開始確認を減らす方向と対応した。ただし観測自体のpermissionは残るため、5 / 5件を実行不能にしたとは判定しない。

### F03

Candidate147の参照5件は、開始identityの結果を次の発行判断へ使う前に、identity観測と許可済みreadの両方を発行対象へ入れていた。Candidate261で同じ関係を明確に保ったのは、一つのcommand内へidentity観測と二つのreadを入れた1件だけだった。

残る4件では、identity側またはread側のresultがterminalになった後に他方を別発行した。root本文の`DECISION_BOUNDARY` bytesはCandidate147と同一でも、追加した`SPEC`二文を含むprompt全体として、Candidate147の初回発行関係は再現しなかった。これは「条項をbyte保持したこと」と「モデル挙動が再現したこと」を分ける反例である。

F03の最大runは166,625 tokenだった。必須試験後のdiff出力が上限で欠落し、試験を再実行せずdiffとstatusだけを追加確認している。この追加確認は最大値の一因だが、中央値を決める他のrunも約127,850〜129,809 tokenであり、最大run一件を除いてもF03の退行は消えない。

F03で初回発行関係が崩れたrunとtoken増加は対応するが、一対一ではない。低tokenの不成立runも一件あるため、機序不成立をtoken増加の完全な原因または品質失敗へ読み替えない。それでも品質も成果も増えていないF03でtokenと時間がともに増えたため、追加費用は正当化できない。

## 判断

Candidate261は、A01で保持したい境界を小さい本文差分で再現できることを示した。一方、その二文をC147へ全体適用する構成は、非対象のF03でC147の成立済み発行関係とcostを維持できなかった。

次の改善点は、利用者向け進捗への出力禁止を全TaskSpecへ重ねることではない。`spec_ready=false`で、開始状態resultが未固定値の質問、permission、または停止条件を変えず、受け取り先が進捗出力しかない場合に、その観測を合法にしているrepository evidence permissionを閉じる必要がある。これは開始確認回数やtool順を指示する案ではなく、結果を使える後続operationがない観測のpermissionを閉じる案として、次Candidate作成前に設計する。

## 状態

`targeted_a01_f03_n5_completed / valid_10_of_10 / score4_10_of_10 / a01_start_check_1_of_5 / f03_c147_initial_issuance_preserved_1_of_5 / quality_passed / aggregate_token_regressed_6_09_percent / aggregate_elapsed_effectively_flat / f03_token_regressed_22_89_percent / f03_elapsed_regressed_5_13_percent / unjustified_cost_regression / additional_n_not_authorized / standard14_not_authorized / adoption_not_approved / release_not_created / projection_not_performed`

一次証拠は、[登録result](ceb2507860c74bc1834126c94b44d6c6.json)、[品質監査](candidate261-spec-output-consumer-closure-a01-f03-n5-quality-audit-r1.json)、[行動経路監査](candidate261-spec-output-consumer-closure-a01-f03-n5-mechanism-audit-r1.json)および比較作業領域の保存analysisである。
