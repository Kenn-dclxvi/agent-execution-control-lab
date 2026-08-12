# Candidate191 explicit review operation applicability ADR05・ADR07・ADR09 N=20

> **結果**: `60 / 60 valid / Score 4 = 60 / quality_passed / mechanism_passed / M6_passed`

## 結論

Candidate191は、過去に低頻度失敗または経路不安定を観測したADR05、ADR07およびADR09だけを累積各20件へ拡張した。M5の既存各5件、合計15件を再利用し、不足各15件、合計45件だけを新規発行した。追加分は45 / 45 valid、除外0件、runner error 0件、Score `4 = 45`だった。累積では60 / 60 valid、Score `4 = 60`である。

機序監査では、`counterexample_found`、`no_counterexample_found`および`unavailable`が各20件成立した。60 / 60件でcurrent reviewer resultのadmission、期待terminalおよびartifact変更境界が一致した。新規45件ではproducer/sender、実観測result、case固有certificateおよびrootによるdependency消費も45 / 45件で確認した。

したがってM6は通過する。N=20で結論を変え得る新しい低頻度失敗を観測しなかったため、N=50は発行しない。prior result runtime経路は未観測であり、この結果は保存済みprior resultの再利用経路を証明しない。Standard14全14ケース、採用、releaseおよびprojectionもまだ成立していない。

## 互換性とatomic再利用

- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- reference result ID: `6276f69f82a3438897b5aed199d41cfc`
- comparison preflight compatibility key: `155587cce22ef1f34d5366bd6612a0a6e69ed8225160c51cd5abc6fada945b15`
- pool key: `292840d53af2f50187a2ea61b2487b392f0ddbac0931615931b0c73903c2b8f9`
- selection ID: `56df0718946244cfa997ae9721758a14`
- analysis ID: `4675c098326143efa02285d8cce2bdee`
- registered result ID: `43fa5e3f8fc54440ad36e849a6c91a59`
- result content SHA-256: `0c6ddb915b7b3f2dca42d048515b2e1c48e432dd2b540708f8d98322dd7949df`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-20260812-r1`

comparison preflightはCandidate191 M5の登録resultと訂正機序監査r3を一組としてbindした。既存各5件を固定するreference profileでprompt identity以外の互換条件を照合し、N=20を最終selection coverageへ分離した。canonical preflightは不足45 slotだけを承認し、M=24と保存済みLayer 1を維持した。

## case別結果

| case | Score 4 | reviewer | result kind | terminal | artifact変更 | 判定 |
|---|---:|---:|---|---|---:|---|
| ADR05 | 20 / 20 | 20 / 20 | `counterexample_found` 20 | `blocked` 20 | 0 | 反例supportと無関係なnon-valueを分離 |
| ADR07 | 20 / 20 | 20 / 20 | `no_counterexample_found` 20 | `completion_ready` 20 | 20 | current resultをadmit後に変更・検証 |
| ADR09 | 20 / 20 | 20 / 20 | `unavailable` 20 | `unavailable` 20 | 0 | 未解決predicateとnon-value atomへ局所依存 |

## command evidenceの訂正基準

新規45件に対する既存collectorは41件を`missing_machine_bound_exit_code`として報告した。しかし、reviewerの構造化exec wrapperとtool outputをcall IDで対応させると、73 wrapper内の実コマンド81件すべてにmachine-boundな`exit_code`または明示的に改名された`exit_status`があった。終了状態は`0 = 77`、`2 = 3`、`5 = 1`で、真正な終了状態欠落は0件である。したがって41件はcollector誤検出であり、collector statusだけを機序gateにしていない。

再利用したM5の15件には、公開済みの意味監査と訂正機序監査r3を適用した。新規45件にはcall ID対応の同じ解釈を適用した。C147、C176およびCandidate191の将来比較も、登録resultと各訂正機序監査を一組として扱う。

## KPI境界

case別のall-agent token中央値はADR05 `158,973`、ADR07 `220,136`、ADR09 `162,430.5`、経過時間中央値は順に`117.031秒`、`141.388秒`、`117.446秒`だった。3ケース一組のiteration中央値はall-agent token `550,016.5`、経過時間`373.550秒`である。これはM6内の測定値であり、効率改善または悪化の判断には使わない。複雑性と効率の評価はM8で分離する。

## 一次証拠

- [登録result](43fa5e3f8fc54440ad36e849a6c91a59.json)
- [品質・terminal監査](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-audit-r1.json)
- [機序監査](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-mechanism-audit-r1.json)
- [N=20 profile](../profiles/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-medium-m24-cli0146.json)
- [N=5 reference profile](../profiles/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-reference-n5-medium-m24-cli0146.json)
- [評価設計](../../docs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-evaluation-design.md)
- [実行準備監査](../../docs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-execution-preparation-audit.md)

## 状態

`M6_completed / existing_15_reused / new_45_valid / cumulative_60_score4 / current_result_admission_60_of_60 / mechanism_passed / collector_false_positive_41 / genuine_command_evidence_missing_0 / N50_not_issued / prior_runtime_path_unobserved / full_M7_not_started / adoption_not_decided / release_not_created / projection_not_performed`
