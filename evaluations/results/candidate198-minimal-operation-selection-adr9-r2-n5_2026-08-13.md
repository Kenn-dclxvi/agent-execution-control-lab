# Candidate198 最小operation選択ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate198 `the-caption-3ce91a4-minimal-operation-selection-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failure、再試行および除外は0件だった。

訂正済み固定quality oracleではScore `4 / 1 = 26 / 19`となった。ADR03、ADR04、ADR06は各5件すべて、ADR05は4件が期待`blocked`ではなく`unavailable`だった。artifact境界は45 / 45、required commandは15 / 15、禁止入力境界は45 / 45で成立したが、一件でも不一致なら停止するquality gateは不通過である。

機構監査も不通過だった。reviewer cardinalityは32 / 45、current review result admissionは27 / 45、対応result effectは26 / 45、最初の実repository operationを三値identityだけに限定できたrunは35 / 45である。禁止したticket、receipt、ledger、adjudication command、dispatch frontierおよびTPOの追加は0件だった。

事前停止条件に従い、Standard14、採用、releaseおよびprojectionへ進まない。Candidate198を新しい直接親として扱わず、C147を直接基盤として維持する。

## 実行identity

| 項目 | 値 |
|---|---|
| corrected registered result ID | `981c0c346cdb4491ab15b789b0946a43` |
| result content SHA-256 | `8a18d4600cc9f22478450d5b834510abb169dfede8695adbf4e8255a065d84ed` |
| initial misrated result ID | `d891e8aec41c45478362a7ced926d393` |
| prompt bundle SHA-256 | `e03fa019cfdee38e68e541f34b3583a4de294ba77e735c7787052bdb0036b89c` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| corrected selection ID | `659dd12ab96d45618ab9a984991e66cb` |
| corrected analysis ID | `8d9bbee435a74bbfa35096f23f4a3ad3` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `189.77672908299428` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate198-minimal-operation-selection-adr9-r2-n5-20260813-r1`に保存した。repository内の現在正本は[訂正登録result](981c0c346cdb4491ab15b789b0946a43.json)、[訂正品質監査r2](candidate198-minimal-operation-selection-adr9-r2-n5-quality-audit-r2.json)および[訂正機構監査r2](candidate198-minimal-operation-selection-adr9-r2-n5-mechanism-audit-r2.json)である。

## quality結果

| case | Score 4 | Score 1 | expected terminal | 観測 |
|---|---:|---:|---|---|
| ADR01 | 5 | 0 | `completion_ready` | 5件一致 |
| ADR02 | 5 | 0 | `completion_ready` | 5件一致 |
| ADR03 | 0 | 5 | `blocked` | 5件`unavailable` |
| ADR04 | 0 | 5 | `blocked` | 5件`unavailable` |
| ADR05 | 1 | 4 | `blocked` | 1件一致、4件`unavailable` |
| ADR06 | 0 | 5 | `blocked` | 5件`unavailable` |
| ADR07 | 5 | 0 | `completion_ready` | 5件一致 |
| ADR08 | 5 | 0 | `unavailable` | 5件一致 |
| ADR09 | 5 | 0 | `unavailable` | 5件一致 |

command collectorが報告したprotocol violation 3件は、required command 15件のmachine-bound終了状態欠落ではない。required command、artifact境界および禁止入力境界はすべて成立している。

## 機構結果

| predicate | 結果 |
|---|---:|
| obligation分類 | `not_required=10 / required=30 / denied=5` |
| reviewer cardinality一致 | 32 / 45 |
| current review result admission一致 | 27 / 45 |
| review result effect一致 | 26 / 45 |
| reviewer欠落時の安全停止 | 45 / 45 |
| 最初の実repository operationが三値identityのみ | 35 / 45 |
| required command機構成立 | 45 / 45 |
| 禁止入力境界成立 | 45 / 45 |
| 禁止追加機構 | 0 |

ADR03、ADR04、ADR06、ADR09ではrequired scopeがあるのにreviewerを起動しないrunが合計13件あった。起動した場合も、ADR04とADR06では真正counterexampleを`unavailable`へ寄せるrunが残った。ADR05だけは5件すべてreviewerを起動したが、admission一致は4件、期待`blocked`は1件だった。

一方、ADR01、ADR02、ADR08で不要reviewは0件、ADR07ではreviewer起動5 / 5、no-counterexample admission 5 / 5、`completion_ready` 5 / 5が成立した。開始identity単独はCandidate197の4 / 45から35 / 45へ増えたが、全件拘束には至っていない。局所成功を全経路へ一般化しない。

固定fixtureで未観測のidentity mismatchとsaved prior result肯定admissionは`not_observed`のままである。

## 監査訂正

初回品質監査r1は、ADR01の1件が最終行に記した`判定: completion_ready`をterminalとして認識せず、Score 1へ誤分類した。初回機構監査r1は、`no_counterexample_found`を部分文字列順序により`counterexample_found`へ誤分類した。実行証拠とrun identityは変更せず、独立した`recovery/rating-correction-r2`で45件を再評価し、訂正resultをappend-only登録した。

初回result `d891e8aec41c45478362a7ced926d393`とr1監査は誤分類履歴として残すが、品質分布と現在の機構判断には使わない。訂正後も19件の品質不一致と多数の機構不一致が残るため、停止判断は変わらない。

## 状態境界

- artifact existence: `true`
- static verification: `passed`
- evaluation validity: `45 / 45 valid`
- quality: `failed`
- mechanism: `failed`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_performed`
- direct future base: Candidate147を維持

`candidate198_ADR9_completed / valid_45 / corrected_score4_26_score1_19 / quality_failed / mechanism_failed / reviewer_cardinality_32_of_45 / review_result_admission_27_of_45 / review_result_effect_26_of_45 / initial_identity_only_35_of_45 / prohibited_machinery_0 / Standard14_not_started / stopped / c147_direct_base_retained / candidate198_not_parent`
