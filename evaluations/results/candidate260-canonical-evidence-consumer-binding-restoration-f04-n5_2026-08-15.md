# Candidate260 証拠取得条件の発行後作り直し禁止 F04 N=5

## 結論

Candidate260はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。開始確認と必要readの共同発行、およびrequired validationの単一発行判断も5 / 5件で成立した。

しかし4 / 5件では、最初の`App.tsx` readが正常に完了した後、その取得範囲に含まれなかった描画箇所を新しい不足として扱い、同じ変更判断のための残りのreadを許可した。ここで証拠取得条件とは、必要判定、現在欠けている観測値、その判定を確定できる取得結果の組を指す。発行後にこの組を作り直す問題経路を閉じられなかったため、機序は不成立である。

`quality_passed / mechanism_failed / stopped`とし、追加N、Standard14、採用、release、projectionへ進めない。Candidate147との3 KPIは比較する。一方、対象機序が不成立のため、観測したKPI差をCandidate260の制御効果へ帰属しない。

## 固定条件

- prompt: `the-caption-3ce91a4-canonical-evidence-consumer-binding-restoration-r1`
- bundle SHA-256: `b9e01c6785d4abb977fa8e7733a24b3c94288f03e0726d57d3153836fea7852f`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- composition source: Candidate254
- 問題経路が閉じていないことを示す反例としてだけ使用: Candidate254の失敗run、Candidate255、Candidate256、Candidate257、Candidate258、Candidate259
- 継承しないもの: Candidate255からCandidate259までの追加条件
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison preflight reference: Candidate147 result `177c63c27b1645e6b01f74329656ef5f`
- Candidate260 result: `8f3ef2f0104f4514aa6942c5824e8d2e`

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| 開始確認と必要readの共同発行 | 5 / 5 |
| 影響しない複数確認を別stepへ分けなかった | 4 / 5 |
| 途中result後に同じ必要判定用の証拠取得条件を作り直さなかった | 1 / 5 |
| required validationの単一発行判断 | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |

## 対象経路の時系列

機序監査の`iteration`は実行時のdispatch iterationである。登録resultの集計用iterationとは別なので、run IDを対応の正本とする。

| dispatch iteration | run ID | 発行後に証拠取得条件を作り直した回数 | 判定 |
| ---: | --- | ---: | --- |
| 1 | `69949b48d8f84eaba33fa9d1b60d1409` | 1 | 不通過 |
| 2 | `d6aa72ab30ed42279a2ad2b047b1233d` | 1 | 不通過 |
| 3 | `49f6be3b606746318fa035c424ba3cc2` | 1 | 不通過 |
| 4 | `c611ce78e6e24edd8ae315c9a7f2e6eb` | 2 | 不通過 |
| 5 | `64d6b43aa5ba4c148cd2fd22633c36cd` | 0 | 通過 |

不通過4件の先行readはいずれも`exit_code=0`で、対象は存在し、読み取り可能で、固定済み値との矛盾も観測していない。したがって、Candidate147が許す失敗時の追加調査には該当しない。

## KPI比較

| 指標 | Candidate147 | Candidate260 | 差 |
| --- | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 176,103 | +24,933（+16.49%） |
| elapsed中央値 | 91.431秒 | 65.196秒 | -26.235秒（-28.69%） |

品質は同値、tokenは増加、経過時間は短縮した。これは同じ互換条件での記述的な比較結果である。対象機序は1 / 5件しか成立していないため、token増加または経過時間短縮を、Candidate260が狙った証拠取得条件の発行前固定による効果とは断定しない。

## 判定の意味

Score `4`は、要求されたUI変更、許可path、必須3コマンド、終了応答が成立したことを示す。今回の不通過は成果品質ではなく、成果へ到達する途中で、禁止した追加readの許可経路が残ったことを示す。品質点が高くても、この経路が実行可能なため機序成立とはしない。

## 状態

`f04_n5_completed / quality_passed / kpi_compared / quality_same / token_regressed_16_49_percent / elapsed_improved_28_69_percent / joint_issuance_passed_5_of_5 / independent_check_boundary_passed_4_of_5 / post_result_consumer_rebinding_exclusion_passed_1_of_5 / validation_mechanism_passed_5_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 後続再監査

当時のresult、機序監査および`mechanism_failed / stopped`は変更しない。後続の[`C147 result effect scope監査`](../../docs/candidate260-c147-result-effect-scope-followup-audit.md)では、C147が一律のmodel再入禁止ではなく、先行resultが対象、許可、方法または停止条件を変え得ない場合だけ不要な待機を閉じた設計であることを正本から確認した。

この基準では、結果から検索または残りの描画領域取得へ方法を変えた3件と、最初から共同発行した1件は正常経路である。261〜700行の正常result後に、同じ連続範囲readのまま700〜850行を別stepへ分けた1件だけが、方法の変化を伴わない別step化として残る。C147目的との整合は4 / 5件であり、既存の`post_result_consumer_rebinding_exclusion = 1 / 5`をC147のcost最適化目的へ読み替えない。この1件を理由にAIへ特定の処理方法を指示しない。

5件はすべて品質Score `4`であり、機序の不成立と品質再現性の喪失は100％対応していない。したがって、当時の`mechanism_failed / stopped`は履歴として保持するが、現在のcost最適化判定では機序の100％成立を要求しない。

その後のtoken trace再監査では、Candidate260中央値runに、必須検証の非終端返却後に完了を待つだけで`32,440` tokenを使ったmodel再入が1回あった。Candidate147中央値runは同じ必要read、同じ1行変更、同じ3検証を1回少ないmodel再入で完了している。Candidate260には追加品質または追加成果がなく、token `+16.49%`を必要処理の対価とは説明できない。elapsed `-28.69%`で相殺せず、現在は`unjustified_token_regression`とする。一方、C147にも同じ非終端返却後の待機が2 / 5件あるため、待機差をCandidate260のprompt差分へ因果帰属しない。[最小差分還元監査](../../docs/candidate260-c147-minimal-delta-reduction-audit.md)では、有効な追加差分0件、C147維持、`candidate_not_created`とした。[後続機序再監査](candidate260-c147-result-effect-scope-mechanism-reassessment-r2.json)へ記録した。

[登録result](8f3ef2f0104f4514aa6942c5824e8d2e.json)、[品質監査](candidate260-canonical-evidence-consumer-binding-restoration-f04-n5-quality-audit-r1.json)、[機序監査](candidate260-canonical-evidence-consumer-binding-restoration-f04-n5-mechanism-audit-r1.json)を一次証拠とする。
