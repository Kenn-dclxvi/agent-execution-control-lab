# Candidate269 F01・F02・F03・F10 entrypoint N=20ばらつき確認実行監査

## 結論

Candidate269のN=5では、上振れrouteが中央値を切り替えていたため、四ケースを各N=20へ拡張した。これはCandidate状態を前進させる追加Gateではなく、原因頻度をN=5の偶然から分離する分析用拡張である。

既存の各5件、合計20件をatomic poolから再利用した。`plan-missing`で各ケース15件、合計60件だけを不足として固定し、容量ガードに従って20件ずつ三つのbatchへ分けた。各batchは発行前にC269 N=5の保存済みclean Layer 1と登録result `2398d22125bd4e658fe5b653679167b5`へpreflightし、設定上の並列上限を24へ固定した。

## 実行状態

| 累積N | 既存run | 新規発行 | valid | Score 4 | excluded | 登録result |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 10 | 20 | 20 | 20 | 20 | 0 | `9e0bc080a4aa48ac98e470f6b03026d6` |
| 15 | 40 | 20 | 20 | 20 | 0 | `2c3fc3a0f650407e9abab82e1bc8b3de` |
| 20 | 60 | 20 | 20 | 20 | 0 | `544afbe7e2444037932c7313da4489b6` |

60件一括の容量見積りは、free 32,760,651,776 bytesに対して予測free 24,707,588,096 bytesとなり、新規dispatch停止線26,843,545,600 bytesを下回ったため発行しなかった。各20件の2.5 GiB見積りでは毎回`dispatch_allowed`となった。各batchは事前観測、execution seal、Layer 3採点、atomic登録、selection登録、final compactの順で閉じ、runの再実行は0件だった。

## 結果の用途

N=20はF01・F03・F10のN=5中央値が上振れ頻度を過大に反映していたことと、F02では上振れrouteが11 / 20件に残ることを確認した。詳細は[`N=20結果`](../evaluations/results/candidate269-natural-language-validation-carrier-closure-f01-f02-f03-f10-entrypoint-n20_2026-08-16.md)と[`KPI原因分析`](candidate269-f03-shared-issuance-failure-route-analysis.md)へ固定する。

この拡張はStandard14、採用、releaseまたは本体反映を許可しない。現在状態は`preflight_consumed / additional_60_valid / selected_80 / distribution_precision_extended / stopped`である。
