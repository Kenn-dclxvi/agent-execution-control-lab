# Candidate274: C147の実行境界を残したAstra medium N=5

Candidate274の初回6ケース各N=5は30 / 30件がvalidかつScore 4で、除外attemptと実行エラーは0件だった。C273比でトークン52.19%減、経過時間9.69%減となり、大幅な増加は解消した。一方、C147比ではトークン0.80%増、経過時間4.24%減であり、両KPIが減少するという事前条件には届いていない。今回は6ケースのN=5で止め、Standard14全体・追加N・採用へ自動的に進めない。

## 変更と固定条件

C147を直接の親とし、`CONTEXT`・`OWNER_ROLE`・`ROOT`・`INDEPENDENCE`だけを削除した。成果確定、実行者と確定結果、探索、判断境界、検証の一括実行と待機、方法選択、復旧の9条項は原文のまま残した。root本文は7,090文字から5,855文字、非rootの18対象はbyte一致で保持した。

- prompt: `the-caption-3ce91a4-execution-boundary-core-r1`
- bundle: `7454c6921e60db3334d8308b9cc016833a6a8588bc2ca4c275d78197780e4e66`
- model / reasoning: `gpt-6-astra / medium`
- CLI / Python: `0.153.3 / 3.14.5`
- Rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `approval_policy=never / sandbox=workspace-write`
- token accounting: `all_agents / v1`
- configured max_workers: `24`
- ケース: A01 r2・A02 r2・F01 r3・F02 r1・F04 r2・F07 dependency r1、各N=5

C147の保存済み同6ケース結果とLayer 1を再利用し、公式の実行前照合を通過してから不足30件を発行した。基準runの再実行、fixture・TaskSpec・採点・executorの変更はない。詳細は[事前設計と実行前照合](../../docs/candidate274-c147-execution-boundary-core-design.md)。

## 比較

同一6ケース・各N=5のselection sampleごとの合計中央値。経過時間はrunの計測値の合計であり、並列実行全体の壁時計時間ではない。

| 指標 | C147 | C273 | C274 |
| --- | ---: | ---: | ---: |
| Score分布 | 4が30件 | 4が30件 | 4が30件 |
| 品質中央値 | 100 | 100 | 100 |
| 全エージェントトークン | 693,205 | 1,461,546 | 698,726 |
| 経過時間（秒） | 589.081 | 624.660 | 564.105 |

| C274の比較相手 | トークン差 | 経過時間差 |
| --- | ---: | ---: |
| C147 | +0.80% | -4.24% |
| C273 | -52.19% | -9.69% |

C147比の小さなトークン差を「同等と証明した」とは扱わない。N=5の観測ではC147に近い水準へ戻ったが、事前の許容増加幅0を事後に緩めず、コスト条件不通過と記録する。新規実行の壁時計時間は191.168秒であり、上表のKPIとは別の運用情報である。

## ケース別中央値

| ケース | total_tokens | elapsed_seconds | 推論回数 |
| --- | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 18,418 | 13.048 | 1 |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 144,374 | 80.509 | 5 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 119,580 | 94.486 | 4 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 165,976 | 126.544 | 5 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 159,896 | 109.969 | 5 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 92,467 | 86.813 | 4 |

## 経路診断

C274のF01・F02・F04の15runでは、変更後の外側呼び出しがすべて1回となった。検証開始・待機をモデルが別々に発行する形は0 / 15だった。C147と同様、待機は外側呼び出しの内部で行われ、C273で観測した途中のモデル再入が減った。推論回数中央値はF01が4、F02とF04が5へ戻り、C147と一致した。全60runの診断でroot以外のsessionと子エージェントトークンは0だった。

この結果は、検証と判断の境界を残す方針を支持する。ただしC274はC273に比べて検証・判断境界に加えRECOVERYも保持しており、各条項の独立効果を証明する実験ではない。また今回の6ケースで委任自体が発生していないため、削除した委任管理条項の安全性を全経路へ一般化しない。モデル間の差の縮小も本試験では測っていない。

[診断のrun別数値とrollout hash](candidate274-c147-astra-medium-six-case-n5-diagnostic_2026-09-05.json)はKPI差の説明資料であり、品質や採用の独立した第4のKPIではない。

## 一次アーティファクト

- [登録result](98288d00fabb41b5b73bfc71509fd5f4.json)
- [C147とのatomic比較](candidate274-c147-astra-medium-six-case-n5-comparison_2026-09-05.json)
- [C273とのatomic比較](candidate274-c273-astra-medium-six-case-n5-comparison_2026-09-05.json)
- [C273とC147の先行結果](candidate273-c147-astra-medium-six-case-n5_2026-09-05.md)

実行・採点・互換照合の生証跡はローカルの`candidate274-v14-medium-six-case-astra-n5-cli0153-20260905-r1`へ保存し、生ログはcommitしない。既存の採点手順で全30件を採点し、atomic runを個別登録してから集計した。

## 状態

`targeted_n5_completed / quality_gate_passed / c273_cost_recovered / c147_token_regression / cost_gate_not_passed / no_expansion / not_adopted / release_not_created / not_projected`
