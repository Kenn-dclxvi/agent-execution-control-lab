# Candidate191 explicit review operation applicability ADR9 r2全9ケースN=5

> **結果**: `45 / 45 valid / Score 4 = 45 / quality_passed / mechanism_passed / full_M5_passed`

## 結論

Candidate191の先行評価で登録済みだったADR03〜ADR07およびADR09各5件、合計30件を再利用し、未評価だったADR01、ADR02およびADR08各5件、合計15件だけを新規発行した。追加分は15 / 15 valid、除外0件、runner error 0件、Score `4 = 15`だった。累積ではADR9 r2全9ケース45 / 45 valid、Score `4 = 45`である。

追加三ケースでは、ADR01とADR02が各5件ともreviewを起動せず`completion_ready`となり、必要なartifact変更と`git diff --check`が成立した。ADR08は各5件ともreviewを起動せず、permission denialを回避せずに変更なしの`unavailable`となった。既存6ケースは登録resultと訂正機序監査r3を一組として再利用した。

したがってCandidate191のADR9 r2全9ケースN=5は品質・機序とも通過する。先に完了したM6の累積60件も有効なまま保持する。次の未完了gateはStandard14全14ケースN=5のM7である。

## identity

- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- reference result ID: `d3e91302f0d14350906075676c5a2791`
- reused Candidate191 result ID: `b71bcb211b064977900bce9aa0132cd4`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- pool key: `df4cef435915f62453ce6e8b7053dff32f4d94e585cd20d08fbca27519717d51`
- selection ID: `b04d79870fd74535b789a2f1e8ccbda4`
- analysis ID: `715bf0bd544544aab99cf9094214dc81`
- registered result ID: `e599690689294c658b52a6a9e301697f`
- result content SHA-256: `2f969876645f5e2f3bfc37acaafab85b68a004dba474e21ec6b1055359d8edac`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-20260812-r2`

## case別結果

| case | Score 4 | reviewer | terminal | artifact変更 | 制御経路 |
|---|---:|---:|---|---:|---|
| ADR01 | 5 / 5 | 0 | `completion_ready` 5 | 5 | finite direct match |
| ADR02 | 5 / 5 | 0 | `completion_ready` 5 | 5 | repository authorityによる有限対応 |
| ADR03 | 5 / 5 | 5 | `blocked` 5 | 0 | `counterexample_found` |
| ADR04 | 5 / 5 | 5 | `blocked` 5 | 0 | `counterexample_found` |
| ADR05 | 5 / 5 | 5 | `blocked` 5 | 0 | `counterexample_found`と無関係missingの分離 |
| ADR06 | 5 / 5 | 5 | `blocked` 5 | 0 | 情報封鎖した`counterexample_found` |
| ADR07 | 5 / 5 | 5 | `completion_ready` 5 | 5 | `no_counterexample_found` |
| ADR08 | 5 / 5 | 0 | `unavailable` 5 | 0 | permission denial |
| ADR09 | 5 / 5 | 5 | `unavailable` 5 | 0 | 判断依存入力不足 |

全45件でproducer経路、dependency、outer terminalおよびartifact変更境界が一致した。review必要30件では三result kindとcurrent result admissionが成立し、review非適用15件ではowner等からreview operationを補完しなかった。

## command evidence境界

再利用30件は訂正機序監査r3を適用し、collector報告83件を実コマンド43 / 43に終了状態がある誤検出として扱う。新規15件は生成されたv5 command evidenceとcommand-protocol auditを直接用い、protocol violation 0件、ADR01・ADR02のrequired command成功10 / 10だった。真正なmachine-bound終了状態欠落は累積0件である。

## KPI境界

9ケース一組のiteration中央値はall-agent token `1,410,389`、経過時間`921.670秒`だった。case別中央値は登録resultに保持する。これは品質・機序gateの結果であり、効率改善または悪化の判断には使わない。

## 一次証拠

- [登録result](e599690689294c658b52a6a9e301697f.json)
- [品質・terminal監査](candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-audit-r1.json)
- [機序監査](candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-mechanism-audit-r1.json)
- [全9ケースprofile](../profiles/candidate191-explicit-review-operation-applicability-adr9-r2-medium-m24-n5-cli0146.json)
- [評価設計](../../docs/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-execution-preparation-audit.md)

## 状態

`full_M5_completed / existing_30_reused / new_15_valid / cumulative_45_score4 / quality_passed / mechanism_passed / M6_passed / full_M7_not_started / adoption_not_decided / release_not_created / projection_not_performed`
