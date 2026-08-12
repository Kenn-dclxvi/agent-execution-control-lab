# Candidate191 explicit review operation applicability ADR9 r2 N=5

> **訂正後結果**: `30 / 30 valid / Score 4 = 30 / terminal_result_evidence_dependency_path_passed / mechanism_passed_reassessed`

## 結論

Candidate191は、reviewを必要な独立operationとして直接固定するADR03、ADR04、ADR05、ADR06、ADR07およびADR09を各5件、Candidate190の保存済みresultとprompt identity以外が一致する条件で実行した。30 / 30件がvalid、除外0件、Score `4 = 30`となった。

全30件でbind済みreviewerは一件だけ起動し、期待result kind、outer terminal、current result admission、artifact変更境界および情報封鎖が成立した。`counterexample_found`は20件、`no_counterexample_found`は5件、`unavailable`は5件で、禁止canary配送は0件だった。

初回機序監査r2は、reviewerのrepository evidence tool callについて83件の`missing_machine_bound_exit_code`を報告し、`mechanism_failed_stopped`と判定した。後続の生trace再監査では、8 wrapperが実行した43 commandすべてにmachine-bound exit codeがあり、83件は非command文字列の抽出またはcommand resultの対応付け失敗だった。したがって対象6ケースN=5の機序は`mechanism_passed_reassessed`へ訂正する。M6、M7全体、M8、採用、releaseおよびprojectionは別gateであり未完了のままとする。

## 互換性と実行

- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- reference result ID: `2d8c2500cab64220ab1fe76b7e87adac`
- compatibility key: `d09c57a94101d4e2682efbf93a44a456a04e9378556859726d58af872edb6152`
- pool key: `ec84b9fdca3fdaf9672c2177235a9a37a8758df1365e92a980130501b955f250`
- registered result ID: `b71bcb211b064977900bce9aa0132cd4`
- result content SHA-256: `108fcd0ffa769c98a00244c4ffd0a43b1aab6b8d36ecc64ea8c704c1fa87dc1e`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-adr9-review-required-n5-20260812-r1`

Candidate190の保存済み6ケースresultを互換基準へbindし、Candidate191の空poolをseedした。`plan-missing --desired-count 5`が固定した不足30件だけを発行し、TPOを別系列として追加していない。Layer 4登録はStandard14限定結果と同じ派生登録viewを用い、原cycleと証拠を変更していない。

## terminal別結果

| case | Score 4 | reviewer | result kind | terminal | artifact変更 | 真正evidence violation |
|---|---:|---:|---|---|---:|---:|
| ADR03 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 0 |
| ADR04 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 0 |
| ADR05 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 0 |
| ADR06 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 0 |
| ADR07 | 5 / 5 | 5 / 5 | `no_counterexample_found` 5 | `completion_ready` 5 | 5 | 0 |
| ADR09 | 5 / 5 | 5 / 5 | `unavailable` 5 | `unavailable` 5 | 0 | 0 |

terminal、result kind、dependencyの意味関係は30 / 30で一致した。collectorが違反とした8 wrapperは43個の実commandを発行し、37件がexit `0`、6件がexit `2`だった。ADR03〜06ではpaired-scope missingを反例certificateのdependencyにせず、ADR07は必要観測全件成功、ADR09はpaired-scope missingを`unavailable`のdependencyとして用いた。producer、観測result、dependencyおよびterminalの経路は対象30件で閉じている。

## KPI境界

6ケースを一つのiterationへ束ねた中央値はquality `100.0`、all-agent token `1,145,786`、elapsed `761.903秒`である。これは測定値であり、訂正後の機序合格を効率値から導いていない。

## 一次証拠

- [登録result](b71bcb211b064977900bce9aa0132cd4.json)
- [品質・terminal監査](candidate191-explicit-review-operation-applicability-adr9-r2-n5-audit-r1.json)
- [機序監査r2](candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r2.json)
- [訂正機序監査r3](candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json)
- [C147・C176・C191横断再判定](review-control-command-evidence-reassessment-c147-c176-c191_2026-08-12.md)
- [評価profile](../profiles/candidate191-explicit-review-operation-applicability-adr9-review-required-medium-m24-n5-cli0146.json)
- [Standard14限定退行確認](candidate191-explicit-review-operation-applicability-standard14-f02-f03-f04-n5_2026-08-12.md)

## 状態

`candidate191_M5_passed_reassessed / thirty_valid / thirty_score4 / terminal_result_evidence_dependency_path_passed / collector_false_positive_83 / genuine_command_protocol_violation_0 / M6_not_started / full_M7_not_started / M8_not_started / adoption_not_decided / release_not_created / projection_not_performed`
