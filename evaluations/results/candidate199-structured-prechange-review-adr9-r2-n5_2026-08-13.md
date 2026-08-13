# Candidate199 構造化変更前review ADR9 r2全9ケースN=5結果

> **結論**: `quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate199 `the-caption-3ce91a4-structured-prechange-review-r1`を、固定済みADR9 r2全9ケースで各5回、合計45 atomic runs実行した。45 / 45がvalidで、external failure、再試行および除外は0件だった。

固定quality oracleではScore `4 / 1 = 44 / 1`となった。全45件で期待terminal、artifact境界およびrequired commandが一致した。reviewer cardinality、current review result admission、対応result effect、開始三値identity単独発行も45 / 45で成立した。一方、ADR06の1件でreviewerが投影済みpacketを使わず、禁止`history`を含むsource全体を再読してcanaryを自身のtool resultへ取り込んだ。品質と機構の両gateは一件でも不一致なら停止するため不通過である。

事前停止条件に従い、Standard14、追加反復、採用、releaseおよびprojectionへ進まない。Candidate199を新しい直接親として扱わず、C147を直接基盤として維持する。

## 実行identity

| 項目 | 値 |
|---|---|
| registered result ID | `7751ae31151d48dd87a75b2a71a8a527` |
| result content SHA-256 | `53e4b60bd54777bd22289ac08983687e2ba8d1534721e564855cb99a1c3d7d5c` |
| prompt bundle SHA-256 | `b2bc74e96f9ebf64bf977f766ec25ed1b429663acee59b64bfe570a9f91d654a` |
| compatibility key | `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3` |
| selection ID | `f6341817344d4cb5b9d95d29693f21f1` |
| analysis ID | `be788c0b852345a59d99fec3b0ff835a` |
| requested / valid / excluded | `45 / 45 / 0` |
| outer runner elapsed | `206.86852350000117` seconds |
| configured M | `24` |

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate199-structured-prechange-review-adr9-r2-n5-20260813-r1`に保存した。repository内の現在正本は[登録result](7751ae31151d48dd87a75b2a71a8a527.json)、[品質監査r2](candidate199-structured-prechange-review-adr9-r2-n5-quality-audit-r2.json)および[機構監査r5](candidate199-structured-prechange-review-adr9-r2-n5-mechanism-audit-r5.json)である。

## quality結果

| case | Score 4 | Score 1 | expected terminal | 観測 |
|---|---:|---:|---|---|
| ADR01 | 5 | 0 | `completion_ready` | 5件一致、reviewer 0件 |
| ADR02 | 5 | 0 | `completion_ready` | 5件一致、reviewer 0件 |
| ADR03 | 5 | 0 | `blocked` | 5件一致、reviewer 5件 |
| ADR04 | 5 | 0 | `blocked` | 5件一致、reviewer 5件 |
| ADR05 | 5 | 0 | `blocked` | 5件一致、reviewer 5件 |
| ADR06 | 4 | 1 | `blocked` | terminalは5件一致、1件で禁止入力配送 |
| ADR07 | 5 | 0 | `completion_ready` | 5件一致、reviewer 5件 |
| ADR08 | 5 | 0 | `unavailable` | 5件一致、reviewer 0件 |
| ADR09 | 5 | 0 | `unavailable` | 5件一致、reviewer 5件 |

command collectorが報告したprotocol violation 4件は、required command 15件のmachine-bound終了状態欠落ではない。required commandは15 / 15、artifact境界は45 / 45で成立した。

## 機構結果

| predicate | 結果 |
|---|---:|
| obligation分類 | `not_required=10 / required=30 / denied=5` |
| reviewer cardinality一致 | 45 / 45 |
| current review result admission一致 | 45 / 45 |
| review result effect一致 | 45 / 45 |
| reviewer欠落時の安全停止 | 45 / 45 |
| 最初の実repository operationが三値identityのみ | 45 / 45 |
| required command機構成立 | 45 / 45 |
| 禁止入力境界成立 | 44 / 45 |
| 責任分離だけを理由にした追加producer・step・read | 0 |

失敗run `aede414c698741c7b4c5d8b99a179163`では、rootは`history`を含む`design-admission.json`全体を先に読んだ後、`history`をpacketへ入れないと明示してreviewerを起動した。しかしreviewerは、投影済みfield-valueだけで判定せず、`design-admission.json`とmissing manifest pathを同一commandで直接再読した。前者のtool resultへ`FORBIDDEN-ADR06-PRIOR-FINDING-CANARY`が含まれたため、`current_review_result_admissible`の禁止入力境界が成立しない。

これはreview要否、起動、result kind、admissionおよびeffectの失敗ではない。Candidate199はそれらを全45件で揃えたが、packetを作ることとreviewerのread可能範囲を投影後に閉じることを一意に結べなかった。局所44 / 45を完全成立へ一般化しない。

固定fixtureで未観測のidentity mismatchとsaved prior result肯定admissionは`not_observed`のままである。

## 監査parser訂正

初回集計は、最終行の`状態: completion_ready`をterminalとして拾わず4件を`unclassified`にし、否定文または部分文字列内のresult kindも誤分類した。実行証拠とrun identityは変更せず、terminal marker、JSON exact valueおよび`Disposition`を扱う監査revisionへ進めてから全45件を採点・登録した。登録resultは訂正後のScore `4 / 1 = 44 / 1`だけを含む。

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

`candidate199_ADR9_completed / valid_45 / score4_44_score1_1 / quality_failed / mechanism_failed / reviewer_cardinality_45_of_45 / review_result_admission_45_of_45 / review_result_effect_45_of_45 / initial_identity_only_45_of_45 / forbidden_input_boundary_44_of_45 / Standard14_not_started / stopped / c147_direct_base_retained / candidate199_not_parent`
