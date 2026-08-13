# Candidate202 review admission routing receipt ADR9 r2全9ケースN=5結果

> **結論**: `quality_passed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate202 `the-caption-3ce91a4-review-admission-routing-receipt-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failure、再試行および除外は0件だった。

固定quality oracleでは45 / 45がScore `4`だった。期待terminal、artifact境界、reviewer cardinalityおよびrequired commandは全件一致し、forbidden canary配送は0件だった。command収集器がADR05 iteration 2の失敗read一件を`unparsed_exec_command_call`として報告したが、生rolloutではreviewerが許可されたexact targetを読み、終了コード1とmissingを正しく保持していた。required commandの欠落ではないため、collector false positiveとして分離した。

機構監査では、決定的routing、projection receipt acknowledgement、root/reviewer read閉鎖、reviewer cardinality、current result admissionおよびresult effectはすべて通過した。一方、投影済み観測だけで具体的反例証明が成立した20件のうち9件で、reviewerが終端判定前に`paired-scope-evidence.json`を読んだ。Candidate202が固定した「counterexample certificateを最初に判定し、成立時はterminalにする」という順序に反するため、機構gateは不通過である。

事前停止条件に従い、Standard14、追加反復、採用、releaseおよびprojectionへ進まない。Candidate202を新しい直接親として扱わず、C147を直接基盤として維持する。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `0a509a780f0e40ae857ea602f00ff89b` |
| result content SHA-256 | `837b84f9dea868714c3fa258fb309f0b5d2ac7414a33f7167c638373abdf8d90` |
| prompt bundle SHA-256 | `425208248292cd147e6a005d73912e5268856c3ab34e2ae14ad4b39f1893cca4` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `1709331597d24720a460625a8a767e17` |
| analysis ID | `37223bf18a0d4fe3a77bf4b76b4d2327` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `212.591144083` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate202-review-admission-routing-receipt-adr9-r2-n5-20260813-r1`に保存した。repository内の現在正本は[登録result](0a509a780f0e40ae857ea602f00ff89b.json)、[品質監査r2](candidate202-review-admission-routing-receipt-adr9-r2-n5-quality-audit-r2.json)および[機構監査r2](candidate202-review-admission-routing-receipt-adr9-r2-n5-mechanism-audit-r2.json)である。

## quality結果

| case | Score 4 | expected terminal | reviewer起動 | artifact変更 |
|---|---:|---|---:|---:|
| ADR01 | 5 / 5 | `completion_ready` | 0 / 5 | 5 / 5 |
| ADR02 | 5 / 5 | `completion_ready` | 0 / 5 | 5 / 5 |
| ADR03 | 5 / 5 | `blocked` | 5 / 5 | 0 / 5 |
| ADR04 | 5 / 5 | `blocked` | 5 / 5 | 0 / 5 |
| ADR05 | 5 / 5 | `blocked` | 5 / 5 | 0 / 5 |
| ADR06 | 5 / 5 | `blocked` | 5 / 5 | 0 / 5 |
| ADR07 | 5 / 5 | `completion_ready` | 5 / 5 | 5 / 5 |
| ADR08 | 5 / 5 | `unavailable` | 0 / 5 | 0 / 5 |
| ADR09 | 5 / 5 | `unavailable` | 5 / 5 | 0 / 5 |

## 機構結果

| predicate | 結果 |
|---|---:|
| 最初の実repository operationが三値identityのみ | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| current review result admission一致 | 45 / 45 |
| review result effect一致 | 45 / 45 |
| routing complete | 30 / 30 required reviewer run |
| projection receipt acknowledgement | 30 / 30 |
| rootによるreviewer direct target先読みなし | 30 / 30 |
| reviewer exact read set | 30 / 30 |
| reviewerのclosed source read | 0 |
| reviewerのmixed read | 0 |
| reviewerの集合外read | 0 |
| counterexample certificate優先 | 11 / 20 |
| counterexample成立後の不要direct read | 9 / 20 |
| forbidden canary配送 | 0 |

優先順違反の内訳はADR03が1件、ADR04が1件、ADR05が5件、ADR06が2件である。結果kind、外側terminalおよびartifact effectは正しかったためqualityは満点だが、不要なrepository observationを発行した事実は消えない。品質成功を機構成功へ読み替えない。

## KPIとCandidate175比較

両登録resultのcompatibility keyは一致する。

| KPI中央値 | Candidate175 | Candidate202 | C202 - C175 |
|---|---:|---:|---:|
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,123,616 | 1,289,669 | `+166,053`（`+14.78%`） |
| elapsed seconds | 733.368 | 692.947 | `-40.421秒`（`-5.51%`） |

Candidate202はC175と同じ45 / 45 Score 4、required reviewer 30 / 30を回復した。elapsed中央値は短い一方、token中央値は増えた。さらに新たに固定した優先順predicateを9件で満たしていないため、このcost差を改善、winner、採用またはrelease判断へ使わない。

C175の保存traceにも、現在のCandidate202 predicateで見ると、counterexample 20件中7件でpaired-scope readがある。ただしC175の当時の監査はこのrepository read順序をgateへ固定していないため、C175を遡及的に機構不通過へ変更しない。比較上言えるのは、Candidate202の明文化が新しい順序を実挙動へ拘束せず、同種readを`7 / 20`から`9 / 20`へ減らせなかったことである。

C175はStandard14 70 / 70 Score 4まで実行済みであり、このADR9判断時点ではCandidate202のStandard14 KPI比較は存在しなかった。その後、利用者の明示的な別実行許可により[Candidate202 Standard14 N=5](candidate202-review-admission-routing-receipt-standard14-n5_2026-08-13.md)を実施した。ADR9機構不通過は維持しており、後続試験はADR9 gate通過を意味しない。

## 状態境界

- artifact existence: `true`
- static verification: `passed`
- evaluation validity: `45 / 45 valid`
- quality: `passed`
- mechanism: `failed`
- Standard14: `not_started_at_ADR9_decision / later_executed_by_separate_user_authorization`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_performed`
- direct future base: Candidate147を維持

`candidate202_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / reviewer_30_of_30 / routing_30_of_30 / projection_receipt_30_of_30 / exact_read_set_30_of_30 / counterexample_priority_11_of_20 / premature_direct_read_9_of_20 / Standard14_not_started_at_ADR9_decision / Standard14_later_executed_by_separate_user_authorization / stopped / c147_direct_base_retained / candidate202_not_parent`
