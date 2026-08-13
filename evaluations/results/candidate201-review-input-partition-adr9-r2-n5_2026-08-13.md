# Candidate201 review入力分割 ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate201 `the-caption-3ce91a4-review-input-partition-r1`を固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failure、再試行および除外は0件だった。

固定quality oracleではScore `4 / 1 = 30 / 15`となった。期待terminalは30 / 45、artifact境界は43 / 45、required commandは13 / 15で一致した。required reviewer 30件のうち15件でreviewerが起動されず、起動した15件のうち1件は具体的反例よりmissing observationを優先して期待`counterexample_found`ではなく`unavailable`を返した。

起動したreviewerではexact read set 15 / 15、closed source read 0、mixed read 0で、rootのreviewer-owned target先読みとforbidden canary配送も0件だった。一方、projected observation五件をfinal resultから直接bindできたのは7 / 15で、残る8件はprojection completenessを生traceから確定できず`unobserved`である。未観測をpassedへ補完しない。

Candidate200の入力owner未分割を直す狙いに対し、Candidate201はrequired reviewer欠落を14件から15件へ増やし、Score分布も`30 / 15`のままだった。さらに最初の実repository operationが三値identity確認一件だけでないrunが3件発生した。入力partition条項は安全なread閉鎖を維持したが、reviewer起動を一意に拘束せず、開始境界も維持できなかった。

事前停止条件に従い、追加反復、Standard14、採用、releaseおよびprojectionへ進まない。Candidate201を新しい直接親として扱わず、C147を直接基盤として維持する。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `ba6c59a08d8744c08600207791c3b34f` |
| result content SHA-256 | `141e34fd20f0b1c5f1d068deb99857ce0dac054db288bc33eb76a1cf9a416a66` |
| prompt bundle SHA-256 | `3cdc42ddb363315889b71909e6fbb272c6b007f8c589d4ccfea39e2c013951e3` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `65f88ac1e1a14cb8bc82f6a5b24660a8` |
| analysis ID | `d0ddbadad7be454f89f1c42fae9329c1` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `183.33794549999584` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate201-review-input-partition-adr9-r2-n5-20260813-r3`に保存した。repository内の現在正本は[登録result](ba6c59a08d8744c08600207791c3b34f.json)、[品質監査r2](candidate201-review-input-partition-adr9-r2-n5-quality-audit-r2.json)および[機構監査r9](candidate201-review-input-partition-adr9-r2-n5-mechanism-audit-r9.json)である。

## quality結果

| case | Score 4 | Score 1 | terminal観測 | reviewer起動 |
|---|---:|---:|---|---:|
| ADR01 | 5 | 0 | `completion_ready=5` | 0 |
| ADR02 | 5 | 0 | `completion_ready=5` | 0 |
| ADR03 | 1 | 4 | `blocked=1 / unavailable=4` | 1 |
| ADR04 | 2 | 3 | `blocked=2 / unavailable=3` | 3 |
| ADR05 | 2 | 3 | `blocked=2 / unavailable=3` | 2 |
| ADR06 | 2 | 3 | `blocked=2 / unavailable=3` | 2 |
| ADR07 | 3 | 2 | `completion_ready=3 / unavailable=2` | 3 |
| ADR08 | 5 | 0 | `unavailable=5` | 0 |
| ADR09 | 5 | 0 | `unavailable=5` | 4 |

ADR09のreviewer欠落1件はouter terminalだけなら期待`unavailable`と一致するためScore 4だが、review operation contractを満たさないため機構不通過である。qualityとmechanismを混同しない。

## 機構結果

| predicate | 結果 |
|---|---:|
| review obligation | `required=30 / not_required=10 / denied=5` |
| reviewer cardinality一致 | 30 / 45 |
| required runのreviewer欠落 | 15 / 30 |
| current review result admission一致 | 29 / 45 |
| review result effect一致 | 30 / 45 |
| 最初の実repository operationが三値identityのみ | 42 / 45 |
| required command機構成立 | 43 / 45 |
| rootのreviewer-owned target先読みなし | 45 / 45 |
| reviewer readを観測できたrun | 15 / 45 |
| 観測reviewerのexact read set一致 | 15 / 15 |
| projected observation五件を直接bind | 7 / 15 |
| projection completeness未観測 | 8 / 15 |
| reviewerのclosed source read | 0 |
| reviewerのmixed read | 0 |
| forbidden canary配送 | 0 |

開始identity単独発行の不一致3件はADR02の2件とADR05の1件である。read閉鎖とforbidden input境界の成立は保持するが、quality失敗、reviewer cardinality、result admission、開始境界、required commandおよび未観測projection completenessの各gateが不通過である。

## 停止境界

Candidate201は`quality_failed / mechanism_failed`である。Standard14、追加反復、採用、release、projectionは開始しない。次の設計を行う場合もCandidate201を親にせず、Candidate200とCandidate201を反例証拠に限定してC147から再開する。

`candidate201_ADR9_completed / valid_45 / score4_30_score1_15 / quality_failed / mechanism_failed / reviewer_missing_15_of_30 / wrong_review_result_1 / initial_identity_only_42_of_45 / reviewer_exact_read_15_of_15 / projection_complete_observed_7 / projection_complete_unobserved_8 / closed_source_read_0 / mixed_read_0 / forbidden_canary_delivery_0 / Standard14_not_started / stopped / c147_direct_base_retained / candidate201_not_parent`
