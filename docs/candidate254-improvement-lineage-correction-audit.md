# Candidate254改善系列の対象訂正監査

## 結論

現在の判断対象は、Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`を正式採用するか、Candidate254を直接の親とする追加制御へ進むかである。

Candidate147は品質、token、経過時間を比較する基準であり、現在の改善対象または次Candidateの直接の親ではない。Candidate261とCandidate262は、それぞれの固定済みprompt identityに対する評価結果として保持するが、どちらもCandidate147を直接の親にしており、Candidate254の採用可否または改善効果を直接比較した証拠には使わない。

この訂正は、Candidate261、Candidate262および対応resultの当時の内容、採点、KPI、状態を削除または改変しない。現在判断での役割だけを、`off_target_diagnostic_evidence`へ限定する。

## 固定する判断境界

| 項目 | 現在の固定内容 |
| --- | --- |
| 判断対象 | Candidate254を正式採用するか、Candidate254へ追加制御が必要か |
| 次Candidateの直接の親 | Candidate254 |
| Candidate147の役割 | 保存済みKPIと正常経路の比較基準だけ |
| Candidate261の役割 | Candidate147へ`SPEC`二文を加えた別promptの診断結果。Candidate254改善の直接証拠ではない |
| Candidate262の役割 | Candidate147の`spec_ready=false`時の観測permissionを変えた別promptの診断結果。Candidate254改善の直接証拠ではない |
| 保持するCandidate254の制御 | `SPEC`の利用者向け進捗出力境界、`EVIDENCE_GATE`、`OWNER_ROLE`、開始確認と必要readの境界、検証の途中結果をAIへ返さない境界を含む全文 |
| 今回変更を検討する箇所 | `DECISION_BOUNDARY`の一般的な結果影響範囲だけ |

Candidate番号の大小、Candidate147との文字列上の近さ、またはCandidate261・262の品質合格は、この直接親関係を変更しない。

## 訂正理由

Candidate254のStandard14 N=20は280 / 280件でScore `4`を維持した一方、Candidate147との同数比較でtoken `+9.33%`、経過時間`-6.48%`だった。F03では、開始確認の結果がreadの対象または許可を変えないのに、開始確認とreadを別のAI判断へ分ける経路が6 / 20件あった。

この原因調査から必要だったのは、Candidate254が持つ制御を維持したまま、Candidate254の`DECISION_BOUNDARY`へ結果影響範囲の依存関係を戻す検討である。Candidate147へ戻って別の`SPEC`制御を加えることではなかった。Candidate261とCandidate262はこの判断対象を取り違えたため、現在系列の親にも採用根拠にもならない。

## 後続条件

後続Candidateを作る場合は、作成前に次の四点を必ず同時に固定する。

1. 判断対象がCandidate254の採用または改善であること。
2. 直接の親がCandidate254であること。
3. Candidate254から保持する制御の全件。
4. Candidate147、Candidate261、Candidate262は比較または診断だけに使い、親として継承しないこと。

現在状態は`decision_target_corrected / candidate254_direct_parent_required / candidate147_comparison_only / candidate261_candidate262_off_target_diagnostic_evidence / historical_results_preserved / candidate254_adoption_not_approved`とする。
