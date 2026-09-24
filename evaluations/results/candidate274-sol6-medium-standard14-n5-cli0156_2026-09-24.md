# C274 GPT-6 Sol medium・Standard14各N=5

GPT-6 SolでStandard14の14ケースを各5回、計70件実施した。全件が有効でScore 4、除外・再試行は0件だった。

| 指標 | 今回のSol | 過去のAstra medium（参考） | 差（参考） |
| --- | ---: | ---: | ---: |
| Score 4 | 70/70 | 70/70 | 同数 |
| 全エージェントトークン | 1,809,875 | 1,494,822 | +21.08% |
| 総所要時間 | 681.90秒 | 659.69秒 | +3.37% |

各反復で14ケースを合算し、5反復の中央値を指標ごとに求めた。試験全体の並列壁時計時間やケース別中央値の合計とは異なる。

## 比較条件と解釈

今回の一次結果は[登録result](7a1e38da9ccb4269b37b26ff9d18df32.json)。C274の同一プロンプト、Standard14 r1の同一fixture、TaskSpec、Rating v14、`medium`、全エージェントトークン集計v1、時間記録コード、並列上限24を使った。Solは`gpt-6-sol`、固定CLI `0.156.1`。過去の[参考Astra結果](0dfec297f0fe4d5f9d2d38fb2fff154e.json)は`gpt-6-astra`、固定CLI `0.153.3`で、実行日も異なる。したがって上表は記述的な差であり、モデル単独の効果や同一互換キーでの比較とは扱わない。Astraの新規実行は行っていない。

## 各反復の全14ケース合計

| 反復 | 品質スコア（%） | トークン | 総所要時間 | CLI実行区間 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 100 | 1,809,875 | 692.21秒 | 662.71秒 |
| 2 | 100 | 1,692,031 | 635.14秒 | 604.56秒 |
| 3 | 100 | 1,819,155 | 728.57秒 | 697.70秒 |
| 4 | 100 | 1,842,876 | 681.90秒 | 652.02秒 |
| 5 | 100 | 1,724,246 | 639.95秒 | 612.87秒 |

## ケース別中央値

| ケース | Solトークン | Astra参考トークン | Sol秒 | Astra参考秒 |
| --- | ---: | ---: | ---: | ---: |
| TC-A01-LATENT-MODE-POLICY | 68,971 | 18,437 | 50.03 | 13.11 |
| TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 116,665 | 136,779 | 47.11 | 57.64 |
| TC-F01-DOMAIN-DUPLICATE-ASSET-KEY | 139,471 | 118,966 | 61.80 | 68.21 |
| TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND | 267,939 | 166,878 | 78.86 | 84.65 |
| TC-F03-ATOMIC-CONTEXT-CLEANUP | 157,733 | 107,750 | 57.16 | 55.96 |
| TC-F04-WEB-AUDIT-COLUMN-VISIBILITY | 172,195 | 156,289 | 55.07 | 55.89 |
| TC-F05-CLARIFY-UNITS-MODE | 35,274 | 37,986 | 16.73 | 16.50 |
| TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 35,539 | 39,494 | 19.95 | 17.35 |
| TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 169,594 | 125,648 | 52.89 | 53.93 |
| TC-F07-CANONICAL-V4-RUNNER | 113,785 | 128,413 | 45.53 | 56.52 |
| TC-F07-DEPENDENCY-PROVENANCE-PAIR | 101,103 | 90,620 | 43.77 | 40.98 |
| TC-F08-CANONICAL-CLI-REFERENCE-SYNC | 139,943 | 155,667 | 49.63 | 49.72 |
| TC-F10-ENTRYPOINT-INVENTORY-REVIEW | 97,388 | 113,593 | 49.01 | 44.21 |
| TC-F10-MONTHLY-FORMAT-TEST-REVIEW | 89,212 | 75,766 | 44.54 | 35.69 |

A01のトークン・時間差が特に大きいが、この試験だけではモデル変更とCLI変更、実行時のサービス状態の寄与を分離できない。

## 時間記録と証拠

総所要時間は70件すべて取得した。CLIの直接時計も70件で取得し、各反復の14ケース合計の中央値は652.02秒。入力配送境界と時計対応が観測できず、正式な作業時間は70件すべて欠測のまま保持した。CLI 0.156.1のログ診断は70件で`unsupported_runtime`となり、ログ由来の区間分解も利用できなかった。CLI実行区間を純粋な推論時間とは扱わない。

並列実行全体の壁時計時間は175.48秒で、上記の各反復合計とは別の値である。品質監査では採点上の未達0件、コマンド規約違反0件だった。owner／producer証拠には診断上の不適合が55件あったが、固定済みRating v14では品質点へ変換していない。

[数値・条件差の機械可読記録](candidate274-sol6-medium-standard14-n5-cli0156_2026-09-24.json)、[実行profile](../profiles/candidate274-sol6-time-recording-standard14-medium-m24-n5-cli0156-r1.json)を保存した。実行前照合記録、全runと採点証拠は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-sol6-medium-standard14-n5-cli0156-20260924-r1`に保持する。新runはatomic registryへ70件を個別索引化した。採用、release、本体反映はこの計測では行っていない。
