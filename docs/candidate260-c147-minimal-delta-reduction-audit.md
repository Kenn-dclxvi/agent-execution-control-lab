# Candidate260からC147への最小差分還元監査

## 結論

Candidate260から過剰な差分を外し、改善後のprompt byte列を監査した。新しく作る差分は`valid_new_delta_count = 0`だが、改善後のbyte列は既存Candidate254と完全に一致する。したがって、Candidate147維持を改善結論にはせず、Candidate254をCandidate260の既存置換候補としてStandard14へ再評価する。同じbyte列のCandidate261は作成しない。

ここで制御点とは、問題操作へ到達できる許可または依存関係を、正常経路を残したままpromptで閉じられる箇所をいう。単にtokenを多く使ったtool順、read範囲、待ち時間またはmodel再入を観測しただけでは、制御点が見つかったことにはしない。model再入とは、AIがtool resultを受け取り、もう一度推論する一区間である。

## C147からCandidate260までに増えたもの

Candidate147のroot `AGENTS.md`は10,772 bytes、Candidate260は13,821 bytesであり、Candidate260が3,049 bytes長い。Candidate260 manifestはCandidate147を`baseline_identity`とする一方、実際の`source_prompt_identity`はCandidate254である。Candidate254はCandidate253以前の人間語再構成を含み、Candidate260はC147の一文だけを変更したbyte列ではない。

Candidate260固有の変更は、Candidate254の`EVIDENCE_GATE`冒頭を、次の機能へ置き換えた一段落である。

- 必要判定、欠けた観測値、取得結果を発行前に対応づける。
- 部分resultを受け取った後に、その対応を作り直して残りのread permissionを生じさせない。

その他の長い本文は今回のF04残存経路を閉じる差分ではなく、C147全体の人間語再構成とCandidate230以降の局所修正が累積したものだった。

## 差分ごとの判定

| 差分候補 | 保存traceで確認した効果 | 正常経路への影響 | 判定 |
| --- | --- | --- | --- |
| Candidate260固有の`EVIDENCE_GATE`冒頭 | Candidate260自身の対象機序は1 / 5件しか成立しなかった | 先行resultから検索または残りの描画領域取得へ方法を変えた正常経路まで不通過にする | 削除。C147へ追加しない |
| Candidate254までの相互非依存発行の人間語再構成 | Candidate254では方法不変の別step化を1 / 5件まで減らした | C147には、結果で対象、許可、方法、停止条件が変わらない既知の操作を同じmodel stepから発行する境界がすでにある | 重複。C147へ追加しない |
| Candidate253までの開始確認・検証の再記述 | 対象F04では共同発行と検証境界を成立させたrunがある | 成功runのmodel stepやtool順を再記述し、C147より長い本文を必要とする | 実行手順化になるため追加しない |
| 検証の非終端返却を防ぐ待機条件 | Candidate260は3 / 5件、C147も2 / 5件で非終端返却後に同じ処理を待った | C147は非終端resultを完了扱いせず、同じ処理の完了を待つ正常経路を意図的に残している | C147の未閉鎖permissionではない。追加しない |
| read範囲、回数、特定`yield_time_ms`またはmodel再入数の制限 | 観測runを同じ形で再現すれば一部のtokenを避けられる可能性がある | AIが選ぶ実装方法を成功runの処理へ合わせることになる | 設計原則に反するため追加しない |

## 待機だけのmodel再入の位置づけ

Candidate260中央値run `49f6be3b606746318fa035c424ba3cc2`では、必須検証を発行したcustom executionが非終端で返り、次のmodel再入は同じ処理の完了を待つためだけに`32,440` tokenを使った。このcostは品質、変更または検証項目を増やしていないため、必要な品質処理の対価としては正当化できない。

ただし、C147でも5件中2件に同じ非終端返却後の待機がある。C147は最初のcustom executionを必ずterminalまで保持すること、待ち時間、tool adapterの返却時点を制御していない。したがって、Candidate260の5件中3件とC147の5件中2件という差を、Candidate260のprompt差分の因果効果には帰属しない。Candidate260のtoken `+16.49%`は観測されたcost退行として保持するが、待機差または長い本文が16.49%を生んだと確定しない。

## 残った1件をpromptで閉じられるか

Candidate260 run `c611ce78e6e24edd8ae315c9a7f2e6eb`は、`App.tsx` 261〜700行のresult後に700〜850行を別stepで取得した。後半の取得は同じ連続範囲readだったが、前半resultが必要なrow cellと空表示の直前で終わったため、AIは後半の具体的な取得対象をresult受領後に決めている。

C147が同時発行を要求するのは、先行resultで対象、許可、方法または停止条件が変わらないと既に分かっている操作である。このrunでは、後半の具体的範囲が前半resultに依存したという合法な説明を作れる。これを確実に禁止するには、最初から読む行範囲、read回数、取得量、待機時間、または一回で読む手順を指定する必要がある。いずれも成果ではなく実装方法であり、prompt制御の対象にしない。

したがって、この1件から新しいpermissionまたはdependencyの辺は確定できない。効率の悪い実装方法が選ばれた観測としてcost診断には残すが、追加制御の根拠にはしない。

## 現在の判断

- Candidate260の保存済みresultと当時の`mechanism_failed / stopped`は履歴として保持する。
- Candidate260のtoken `+16.49%`は、追加品質または必要成果で正当化されていないcost退行として保持する。
- 増加原因をCandidate260の待機条件、長い本文または特定readへ因果帰属しない。
- Candidate260固有の`EVIDENCE_GATE`差分は置換候補へ含めない。
- 改善後のbyte列は既存Candidate254と同一なので、新しいCandidate261を複製しない。
- Candidate254をCandidate260の置換候補としてStandard14へ拡張した。70 / 70件Score `4`だったが、Candidate147比token `+6.29%`を必要処理として正当化できず、置換案として採用しない。評価と原因は[`Candidate260置換候補としてのCandidate254 Standard14再評価設計`](candidate254-candidate260-replacement-standard14-design.md)と[Standard14 token退行原因監査](candidate254-candidate147-standard14-token-regression-causal-audit.md)を正本とする。
- 採用、releaseおよびprojectionは開始しない。

現在状態は`candidate260_result_preserved / token_regression_observed / required_processing_justification_not_established / token_regression_cause_not_attributed / valid_new_delta_count_0 / existing_replacement_candidate254_evaluated / duplicate_candidate261_not_created / standard14_completed / quality_passed / unjustified_token_regression / replacement_not_adopted / candidate260_improvement_unresolved / release_not_created / projection_not_performed`とする。

一次参照は、[`prompt制御設計原則`](prompt-control-design-principles.md)、[`Candidate147設計`](candidate147-result-effect-scope-design.md)、[`Candidate253とC147のF04 token差監査`](candidate253-c147-f04-token-step-causal-audit.md)、[`Candidate254部分read残存経路監査`](candidate254-partial-evidence-result-failure-audit.md)、[`Candidate260 C147 result effect scope後続監査`](candidate260-c147-result-effect-scope-followup-audit.md)、[Candidate260登録result](../evaluations/results/8f3ef2f0104f4514aa6942c5824e8d2e.json)および[Candidate260後続再監査](../evaluations/results/candidate260-c147-result-effect-scope-mechanism-reassessment-r2.json)とする。
