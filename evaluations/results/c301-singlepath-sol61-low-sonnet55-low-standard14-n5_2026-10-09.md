# C301のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（一つのプロンプトを計測する経路での測り直し、2026-10-09）

2026-10-09。利用者の依頼で、実行環境を切り離した系列の基準C301を、#361で置き換えた評価経路（評価セットの保管場所からの複製、`preflight-execution`、`create-pool`、使用量の内訳と費用のKPI）で測り直した。同じ日に旧来の経路で測った[C301の計測](c301-sol61-low-sonnet55-low-standard14-n5-shellenv_2026-10-09.md)は、使用量の内訳と複製の記録を持たず、この系列の費用の比較に使えないためである。**品質はSol Lowが4点69件・3点1件、Sonnet lowが4点70件。費用の中央値はSol Low $1.0003、Sonnet low $0.6820。** 除外と再試行は両セルとも0件だった。

比較相手を持たない、この系列の基準の計測である。以後のCandidateは、同じ経路で測り、この計測のanalysisと`compare-analyses`で比べる。

## 条件

- プロファイル：[Sol Low](../profiles/c301-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r2.json)、[Sonnet low](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r2.json)。旧来の経路で使ったC301のプロファイルと、比較条件は同じで、記録だけの項目（評価コードのSHA-256）だけが違う。
- prompt identity：`the-caption-3ce91a4-outcome-binding-uniform-markdown-r1`、bundle SHA-256 `ba025ba64b54ec8d7fc9fb5cf244168f9fd0ec0ed613737f557bb164c349b7a2`。
- 評価コード：コミット`6b95e95`（#361のマージ）。評価セットは、保管場所のStandard14 r1（identity `2096d15e…`）を各セルのcycleへ複製した。
- 発行：両セルともatomic経路（`global_queue`、`max_workers` 24）で、両セルを同時に発行した。準備・実行・登録は、計測の置き場所の道具`campaign-tools/single-prompt-r1/campaign.py`で行った。発行前の記録：[Sol Low](c301-singlepath-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)、[Sonnet low](c301-singlepath-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)。
- 単価表：`api-standard-2026-10-09`（SHA-256 `dce6c9d6…`）。
- 140件すべてで、起動前の実行環境の確認が通り、個人のシェル設定は読まれていなかった。

## 結果

KPI（品質、費用、経過時間）と参考の生のトークンを、中央値と反復の最小〜最大で示す。

| セル | 指標 | 中央値 | 反復の最小〜最大 |
| --- | --- | ---: | ---: |
| Sol Low | 品質（0〜100） | 100.00 | 98.21〜100.00 |
| Sol Low | 費用（USD） | 1.0003 | 0.9261〜1.0331 |
| Sol Low | 経過時間（秒） | 758.63 | 745.42〜794.96 |
| Sol Low | 生のトークン（参考） | 2,150,330 | 2,079,113〜2,263,205 |
| Sonnet low | 品質（0〜100） | 100.00 | 100.00〜100.00 |
| Sonnet low | 費用（USD） | 0.6820 | 0.6656〜0.7005 |
| Sonnet low | 経過時間（秒） | 478.20 | 462.20〜495.00 |
| Sonnet low | 生のトークン（参考） | 857,180 | 761,649〜876,548 |

品質の件数は、Sol Lowが4点69件・3点1件、Sonnet lowが4点70件。中央値と幅は、14ケースを合算した各反復の値を5回分集計したもの。費用の幅は、[計測と記録の基準r2](../../docs/shared-instruction-evaluation-criteria-r2.md)の揺れの幅として、以後の比較で使う。

使用量の内訳（1反復あたり、反復の最小〜最大）：

| セル | キャッシュを使わない入力 | キャッシュ読み取り | キャッシュ書き込み（1時間） | 出力 |
| --- | ---: | ---: | ---: | ---: |
| Sol Low | 307,029〜361,494 | 1,725,568〜1,920,640 | — | 12,454〜15,083 |
| Sonnet low | 120〜136 | 638,382〜752,046 | 104,986〜110,014 | 17,474〜18,662 |

## 4点未満の1件

Sol LowのF02の反復5（run `5b0c2c04…`）は3点だった。モデルが追加したテストに重複したassertionによる`NameError`があり、focused gateとfull gateがそれぞれ1件失敗した。モデルは最後のやり直しでこれを直したが、TaskSpecのやり直しの上限（1回）に達したため、再検証せずに「done条件は未達」と報告した。実行環境に由来する失敗ではない。削除、相殺、再実行はしていない。

## 旧来の経路の計測との関係（参考）

同じ日に旧来の経路で測ったC301は、生のトークンの中央値がSol Low 2,041,902、Sonnet low 794,780、試算で求めた費用の中央値が$0.930、$0.661だった。発行方式（旧来は`wave_barrier`、今回は`global_queue`）、評価コード、使用量の内訳の記録の有無が違うため、二つの差をプロンプトや経路の効果として扱わない。経過時間は、全140件を一つのqueueで同時に流したため、今回のほうが長い。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Sol Low：[登録結果](99f8d1a27247474ea0499f2b9ca1f1e2.json)・[analysis](c301-singlepath-sol61-low-standard14-n5_2026-10-09-analysis.json)・[selection](c301-singlepath-sol61-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c301-singlepath-sol61-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c301-singlepath-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)
- Sonnet low：[登録結果](566d77654eca42989398951c77927e58.json)・[analysis](c301-singlepath-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c301-singlepath-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c301-singlepath-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c301-singlepath-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)
