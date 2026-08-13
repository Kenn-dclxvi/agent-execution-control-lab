# Candidate197 C147局所review応用ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate197 `the-caption-3ce91a4-local-review-application-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failureによる除外は0件だった。

固定quality oracleではScore `4 / 1 = 32 / 13`となった。12件は期待`blocked`に対して`unavailable`を返し、ADR06の1件はreviewerへ禁止入力を配送した。artifact変更境界は45 / 45、required commandは15 / 15だったが、一件でも不一致があれば停止する条件によりquality gateは不通過である。

三つの局所review接続の生trace監査も不通過だった。reviewer cardinalityは29 / 45、current review result admissionは21 / 45、対応するresult effectは33 / 45だった。最初の実repository操作を三値identityだけに限定できたrunは4 / 45である。残る41件は、主にC147の`DECISION_BOUNDARY`が許可するidentityとreadの共同発行を選び、Candidate197評価で固定したidentity単独先行を満たさなかった。

事前停止条件に従い、この結果を保持してStandard14、採用、releaseおよびprojectionへ進まない。Candidate197をCandidate147に代わる親として扱わない。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `01ec5be067fb4c25924130860f622794` |
| result content SHA-256 | `20325b3fb629796f0a62eceffb9e17030f2d3c69852adffd846533274eea7cad` |
| prompt bundle SHA-256 | `7891dcb31349a2e57581d53f518c9cd4778662ce0f3bfd430d2b803457b50901` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `b25b09e7caae4deba78b44b5ddf43e7f` |
| analysis ID | `4f2b1f30ae0542f59aeb67d38f7c1bad` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `177.39974750000692` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate197-local-review-application-adr9-r2-n5-20260812-r1`に保存した。repository内の一次証拠は[登録result](01ec5be067fb4c25924130860f622794.json)、[品質監査r1](candidate197-local-review-application-adr9-r2-n5-quality-audit-r1.json)および[機構監査r1](candidate197-local-review-application-adr9-r2-n5-mechanism-audit-r1.json)である。

## quality結果

| case | Score 4 | Score 1 | expected terminal | 不一致 |
|---|---:|---:|---|---|
| ADR01 | 5 | 0 | `completion_ready` | 0 |
| ADR02 | 5 | 0 | `completion_ready` | 0 |
| ADR03 | 0 | 5 | `blocked` | 5件が`unavailable` |
| ADR04 | 2 | 3 | `blocked` | 3件が`unavailable` |
| ADR05 | 4 | 1 | `blocked` | 1件が`unavailable` |
| ADR06 | 1 | 4 | `blocked` | terminal不一致3件、禁止入力配送1件 |
| ADR07 | 5 | 0 | `completion_ready` | 0 |
| ADR08 | 5 | 0 | `unavailable` | 0 |
| ADR09 | 5 | 0 | `unavailable` | 0 |

ADR06では`blocked`を返した2件のうち1件が禁止入力をreview packetへ含めたため、terminal一致だけではScore 4にしていない。command collectorが報告したprotocol violation 2件はmachine-bound終了状態の欠落ではなく、required command 15件は全件成功している。

## 局所review接続監査

| predicate | 結果 |
|---|---:|
| obligation分類 | `not_required=10 / required=30 / denied=5` |
| reviewer cardinality一致 | 29 / 45 |
| current review result admission一致 | 21 / 45 |
| review result effect一致 | 33 / 45 |
| reviewer欠落時に変更・外側terminalへ進まない | 45 / 45 |
| 最初の実repository操作が三値identityのみ | 4 / 45 |
| required command機構成立 | 45 / 45 |
| 禁止入力境界成立 | 44 / 45 |
| ticket、receipt、ledger、adjudication command、新dispatch機構の追加 | 0 |

Candidate197は、reviewer resultが欠けたときに変更や偽のterminalへ進まない安全側の停止は維持した。一方、required reviewを実際に起動できなかったrunが11件あり、不要reviewを起動したrunも5件あった。したがって`REVIEW_OBLIGATION`は安定していない。reviewerを起動できた場合もexpected result kindと対応effectの全件一致には至らなかった。

開始identityの41件の不一致は、新しいticketやreceiptの欠落ではない。C147本文が、identity resultでreadのpermissionやtargetが変わらない場合にidentityとreadを同じmodel stepから発行するよう要求している一方、今回の固定機構predicateは最初の実repository操作をidentityだけにしたため、両者の適用境界が競合した。この競合はCandidate197の三追加条項が所有していない開始経路に残っている。

固定caseで観測されなかったidentity mismatch、saved prior resultの肯定的admissionおよびreview subject外の独立operationは`not_observed`のままである。

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

`candidate197_ADR9_completed / valid_45 / score4_32_score1_13 / quality_failed / mechanism_failed / reviewer_cardinality_29_of_45 / review_result_admission_21_of_45 / review_result_effect_33_of_45 / initial_identity_only_4_of_45 / forbidden_input_boundary_44_of_45 / Standard14_not_started / stopped / c147_direct_base_retained / candidate197_not_parent`
