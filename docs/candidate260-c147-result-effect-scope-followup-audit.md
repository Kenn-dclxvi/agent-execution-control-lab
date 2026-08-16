# Candidate260 C147 result effect scope後続監査

## 結論

Candidate260のF04 N=5 result `8f3ef2f0104f4514aa6942c5824e8d2e`、品質監査、機序監査および`mechanism_failed / stopped`という当時の評価状態は履歴として変更しない。一方、Candidate260で追加した`post_result_consumer_rebinding_exclusion`は、C147が残した結果依存の正常経路まで不通過にするため、C147のcost最適化目的を判定する基準には使わない。

C147は、modelへresultを返して次を判断することを一律に禁止していない。受領resultが未発行operationの対象、許可、方法または停止条件を変え得ない場合だけ待機を外し、変え得る場合の結果依存判断は保持する。C260の5件をこの境界で再監査すると、4件はC147の正常経路と整合し、1件だけが方法の変化を伴わない連続範囲readをさらに別のmodel stepへ分けていた。

したがって、次の改善で目標にする動作を「変更前readをすべて最初のmodel stepから発行する」または「正常result後の追加readを0件にする」とは定めない。一方、Candidate260のtoken `+16.49%`は、必要な結果依存処理の対価だと確認できていない。経過時間の短縮と対等な交換条件にはせず、現時点では`unjustified_token_regression`とする。後続の[最小差分還元監査](candidate260-c147-minimal-delta-reduction-audit.md)では、待機だけのmodel再入がC147でも2 / 5件にあること、Candidate260固有の差分が正常な結果依存readまで閉じること、および残存1件を閉じるには実装方法の指定が必要になることを確認した。Candidate260から新しく残す差分は0件だが、改善後のbyte列は既存Candidate254と一致するため、Candidate254をCandidate260の置換候補としてStandard14へ拡張した。70 / 70件Score `4`を維持した一方、Candidate147比token `+6.29%`を必要処理として正当化できず、置換案として採用しない。同一内容のCandidate261は作成しない。

## 設計書から確定したC147の目的

Candidate145のcost原因分析は、shell command数とmodel step数を混同した先行分析を訂正した。Candidate145で共通して増えたのは、開始identity resultが許可済みcontent readを変えないのに、identityとcontentを別のmodel stepへ分けた一回である。各追加stepでは、それまでのprompt、TaskSpec、messageおよびtool resultが再びmodel inputへ入り、cached input増加と整合した。

Candidate147はこの原因に対し、`result_effect_scope`を「受領resultが対象、許可、方法または停止条件を変え得る未発行operation classの集合」と定義した。開始identity resultはartifact変更とrequired validationを変え得るが、TaskSpecで許可済みのreadは変えないため、identityとreadを共同発行する。一方、先行resultで次の方法が変わり得る区間は依存関係を保持する。

この設計は、成功runのread範囲、検索語、固定spanまたは一回で読む手順を要求していない。最適化対象はmodel step数そのものではなく、先行resultが未発行operationを変えないのに作られた不要な待機である。

## C253からC260までのずれ

Candidate253の原因監査は、Candidate253にC147より一回多いmodel stepがあり、その一回で`39,903` tokenを使用したことを確認した。対象にしたのは、結果で対象、許可、方法、停止条件が変わらない複数readまたは検証後確認を別stepへ分けた経路だった。

Candidate254はこの一般境界を人間語で戻し、問題経路を1 / 5件まで減らした。残ったrun `342cf77221a14660908dbb7e6cf6cc27`は、261〜620行を読んだ後、同じ連続範囲取得のまま621〜980行を別stepで読んだ。設計監査は、この途中resultで対象、許可、方法、停止条件が変わっていないと固定した。

Candidate255からCandidate260までは、この一件を閉じようとして、問題の単位を「方法が変わらない残りの取得」から「同じ必要判定について正常result後に残りを取得すること」へ広げた。Candidate260の`post_result_consumer_rebinding_exclusion`は、先行resultによって検索または次の証拠取得方法を選んだ経路まで不通過にした。この拡張はC147の正常経路と一致しない。

## F04 5件の再監査

ここでいうmodel stepは、modelがtool invocationを発行し、その全resultを受け取って次の判断を行う一区間である。同じmodel stepから複数commandを発行した場合、command間でresultを見ていないため、個別のmodel再入とは数えない。

| dispatch iteration | run ID | C147境界での観測 | 判定 |
| ---: | --- | --- | --- |
| 1 | `69949b48d8f84eaba33fa9d1b60d1409` | `App.tsx` 1〜260行で定義を確認した後、残り全体ではなく`hasAuditKey / Audit Key / colSpan`の局所検索へ方法を変更した | 正常な結果依存経路 |
| 2 | `d6aa72ab30ed42279a2ad2b047b1233d` | 1〜260行にtable描画がないresultから残りの描画領域を取得する方法へ移り、261〜620行と621〜940行を同じ次のmodel stepから共同発行した | 正常な結果依存経路 |
| 3 | `49f6be3b606746318fa035c424ba3cc2` | 1〜260行のresultから残りの描画領域を取得する方法へ移り、261〜760行を一回発行した | 正常な結果依存経路 |
| 4 | `c611ce78e6e24edd8ae315c9a7f2e6eb` | 1〜260行のresult後に261〜700行を取得したことまでは正常。続いて同じ連続範囲readのまま700〜850行を別stepへ分けた時点では、対象、許可、証拠取得方法、停止条件は変わっていない | 不要な依存関係1件 |
| 5 | `64d6b43aa5ba4c148cd2fd22633c36cd` | 開始identity、Node定義、`App.tsx` 1〜760行を最初のmodel stepから発行し、変更前の後続readはなかった | 正常な共同発行経路 |

C147目的との整合は4 / 5件、方法が変わらない残りの取得をさらに別stepへ分けた観測は1 / 5件である。これは既存機序監査の`independent_checks_same_model_step = 4 / 5`と一致する。既存の`post_result_consumer_rebinding_exclusion = 1 / 5`はCandidate260固有の厳しい対象機序の判定として履歴に保持するが、C147のcost最適化目的の達成度として読み替えない。また、この1件を観測したことだけで、AIへ別のread方法や順序を指示する修正対象にはしない。

5件はすべて品質Score `4`である。旧機序が不通過だった4件でも、C147境界で方法不変の別step化が残った1件でも、品質は再現されている。したがって、この試料では機序の不成立と品質再現性の喪失に100％の相関はなく、現在のcost最適化判定で機序の100％成立を要求する根拠はない。機序成立率は、どの経路がtokenまたは経過時間へ影響した可能性があるかを調べる診断値として保持する。

## KPIの位置づけ

Candidate147比でCandidate260はquality中央値が同値、all-agent token中央値が`+16.49%`、elapsed中央値が`-28.69%`だった。KPI比較はそのまま保持する。ただし、一方のcostが減ったというだけでは、増えたtokenを許容可能な交換条件にはしない。token増加が要求品質または必要な正常経路を維持するために必要だったことを先に示す必要がある。

この判定を、機序が4 / 5件または1 / 5件だったことだけで不合格にはしない。一方、このN=5比較だけでは、どの制御差分がelapsed短縮を生んだかを分離できない。唯一の変更前read共同発行runを次の成功手順として固定しない。

### token増加のtrace再監査

Candidate147とCandidate260の中央値runは、どちらも`App.tsx`の最初の範囲を取得した後、先行resultに基づいて残りの描画領域を取得し、`hasAuditKey`の同じ1行を変更して、同じ3つの必須検証を完了した。Candidate260だけに品質維持のための追加成果、追加変更または追加検証はない。

| 観測 | Candidate147 | Candidate260 | 判定 |
| --- | ---: | ---: | --- |
| 品質Score `4` | 5 / 5 | 5 / 5 | 追加品質なし |
| prompt本文bytes | 10,772 | 13,821 | Candidate260が3,049 bytes長い |
| model再入中央値 | 5 | 6 | Candidate260が1回多い |
| validation中の非終端返却後`wait` | 2 / 5 | 3 / 5 | Candidate260で1件多い |
| 変更内容 | `hasAuditKey`の1行 | `hasAuditKey`の1行 | 同じ成果 |

Candidate260中央値run `49f6be3b606746318fa035c424ba3cc2`は、必須検証を発行したcustom executionを`yield_time_ms=1000`で非終端のままmodelへ返し、次のmodel再入では同じ実行の完了を待つことだけを行った。この再入の`last_token_usage.total_tokens`は`32,440`であり、新しい品質判断、変更または検証を追加していない。Candidate147中央値run `af0d3316d0da498684b8bb1aca8b05c0`は、同じ必要read、同じ変更、同じ必須検証を5回のmodel再入で完了している。

この証拠では、Candidate260のtoken増加を必要な結果依存処理の対価とは説明できない。品質へ寄与しない待機だけのmodel再入と、全model再入へ入る長い制御本文は増加候補として残るが、待機はC147でも2 / 5件にあり、N=5の差だけでCandidate260の制御差分へ因果帰属しない。特定の`yield_time_ms`をAIへ指示する解決策にはせず、非終端返却を含む実行方法の差があっても追加costを正当化できる必要結果があったかを判定する。現在は確認できないため`unjustified_token_regression`とする。

## 置換候補の評価gate

Candidate260の置換候補をStandard14へ拡張する前に、次を満たす必要がある。

1. 改善対象をCandidate260、KPIの比較基準をCandidate147として混同しない。
2. C147が残した、先行resultによって対象、許可、方法または停止条件が変わる結果依存経路を維持する。
3. 問題対象を、先行resultでこれらが変わらないのに既知の残りの取得を別stepへ分ける依存関係へ限定する。
4. read回数、行数、範囲数、同一artifactの序数または「一回で十分」という量をpermission条件にしない。
5. 検索、連続範囲read、特定commandまたは成功runの順序を実行義務にしない。
6. C147の元の`result_effect_scope`だけで問題経路が既に禁止されているなら、追加条件ではなく人間語再構成の意味欠落として扱う。
7. 品質再現性との相関が100％と確認されていないcost経路では、機序の全件成立をCandidate作成または拡張の必須条件にしない。
8. AIへ特定のread方法、取得範囲、tool順、判断順またはmodel stepを選ばせることを解決策にしない。
9. 品質を維持し、all-agent `total_tokens`と`elapsed_seconds`がともに減った場合だけcost改善方向を自動判定する。片方が増える場合はその指標をcost退行とし、増加分が必要な正常処理の結果だとtraceで確認できた場合だけ、人間へ交換条件として提示する。確認できなければ`unjustified_cost_regression`とする。

## 現在状態

`candidate260_result_preserved / original_mechanism_failed_preserved_as_history / c147_design_intent_reassessed / c147_result_effect_scope_conforming_4_of_5 / unchanged_method_dependency_observed_1_of_5 / mechanism_quality_reproducibility_correlation_not_100_percent_in_n5 / mechanism_100_percent_not_required_for_current_cost_judgement / token_regressed_16_49_percent / required_processing_justification_not_established / token_regression_cause_not_attributed / valid_new_delta_count_0 / existing_candidate254_replacement_evaluated / duplicate_candidate261_not_created / candidate254_standard14_completed / candidate254_quality_passed / candidate254_unjustified_token_regression / replacement_not_adopted / candidate260_improvement_unresolved / release_not_created / projection_not_performed`

一次参照は、[`Candidate145 cost原因分析`](candidate145-f01-f02-f03-cost-causal-analysis.md)、[`Candidate147設計`](candidate147-result-effect-scope-design.md)、[`Candidate253とC147のF04 token差監査`](candidate253-c147-f04-token-step-causal-audit.md)、[`Candidate254部分read残存経路監査`](candidate254-partial-evidence-result-failure-audit.md)、[Candidate260登録result](../evaluations/results/8f3ef2f0104f4514aa6942c5824e8d2e.json)、[既存機序監査](../evaluations/results/candidate260-canonical-evidence-consumer-binding-restoration-f04-n5-mechanism-audit-r1.json)および[後続機序再監査](../evaluations/results/candidate260-c147-result-effect-scope-mechanism-reassessment-r2.json)とする。
