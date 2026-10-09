# C301のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（全セルを一つの待ち行列で測った系列の基準、2026-10-09）

2026-10-09。[一つのプロンプトを計測する経路での測り直し](c301-singlepath-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)では、両セルをそれぞれ並列上限24で同時に流したため、同時に動くrunが最大48本（平均35.7本）になり、このホストの上限24を超えていた。テストやビルドがCPUを取り合い、コマンドを実行するケースの経過時間が延びていた。利用者の指示で、両セルの全スロットを一つの待ち行列へ入れ、同時実行の合計を24以内にして測り直した。**両セルとも有効70件すべてが4点。費用の中央値はSol Low $0.8851、Sonnet low $0.6578、経過時間の中央値はSol Low 583.89秒、Sonnet low 291.60秒。** 除外と再試行は0件だった。

この計測を、実行環境を切り離した系列の基準とする。以後のCandidateは同じ発行のしかたで測り、この計測のanalysisと比べる。

## 条件

- プロファイル：[Sol Low](../profiles/c301-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r3.json)、[Sonnet low](../profiles/c301-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r3.json)。前回（`-r2`）との違いは、比較条件へ発行のしかた（`executor_parameters.campaign_dispatch`：全セルで一つの待ち行列、合計24本）を加えたことだけである。経過時間を変えうる条件なので、前回のrunとは別のpoolになる。
- prompt identity：`the-caption-3ce91a4-outcome-binding-uniform-markdown-r1`、bundle SHA-256 `ba025ba64b54ec8d7fc9fb5cf244168f9fd0ec0ed613737f557bb164c349b7a2`。
- 評価コード：コミット`33e5809`（`scripts/`と`layer2/`は#361の`6b95e95`と同じ）。評価セットは保管場所のStandard14 r1を各セルへ複製した。
- 発行：両セル140スロットを`campaign_runner.py`の一つの待ち行列（`global_queue`、`max_workers` 24）で発行した。同時に動いたrunは最大24本、平均22.3本、全体の所要は約198秒だった（[待ち行列の記録](c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)）。準備・実行・登録は、計測の置き場所の道具`campaign-tools/single-prompt-r1/campaign.py`（`run-all`）で行った。
- 単価表：`api-standard-2026-10-09`。140件すべてで起動前の実行環境の確認が通った。

## 結果

| セル | 指標 | 中央値 | 反復の最小〜最大 |
| --- | --- | ---: | ---: |
| Sol Low | 品質（0〜100） | 100.00 | 100.00〜100.00 |
| Sol Low | 費用（USD） | 0.8851 | 0.8704〜0.9324 |
| Sol Low | 経過時間（秒） | 583.89 | 567.79〜617.29 |
| Sol Low | 生のトークン（参考） | 2,001,626 | 1,900,312〜2,098,758 |
| Sonnet low | 品質（0〜100） | 100.00 | 100.00〜100.00 |
| Sonnet low | 費用（USD） | 0.6578 | 0.6380〜0.6878 |
| Sonnet low | 経過時間（秒） | 291.60 | 283.87〜301.27 |
| Sonnet low | 生のトークン（参考） | 809,691 | 794,017〜821,478 |

中央値と幅は、14ケースを合算した各反復の値を5回分集計したもの。費用の幅は、[計測と記録の基準r2](../../docs/shared-instruction-evaluation-criteria-r2.md)の揺れの幅として以後の比較で使う。

使用量の内訳（1反復あたり、反復の最小〜最大）：

| セル | キャッシュを使わない入力 | キャッシュ読み取り | キャッシュ書き込み（1時間） | 出力 |
| --- | ---: | ---: | ---: | ---: |
| Sol Low | 282,700〜321,844 | 1,586,304〜1,802,112 | — | 12,198〜13,946 |
| Sonnet low | 124〜130 | 668,956〜701,432 | 98,497〜107,829 | 17,364〜18,757 |

## 前回の測り直しとの関係（参考）

| セル | 指標 | 2セル同時・各24（`-r2`） | 一つの待ち行列・計24（今回） |
| --- | --- | ---: | ---: |
| Sol Low | 費用（USD） | 1.0003 | 0.8851 |
| Sol Low | 経過時間（秒） | 758.63 | 583.89 |
| Sol Low | 生のトークン（参考） | 2,150,330 | 2,001,626 |
| Sonnet low | 費用（USD） | 0.6820 | 0.6578 |
| Sonnet low | 経過時間（秒） | 478.20 | 291.60 |
| Sonnet low | 生のトークン（参考） | 857,180 | 809,691 |

発行のしかたが違うため、二つは比較条件が異なる（`compare-analyses`は受け付けない）。前回の延びは、同時実行の超過でコマンドの実行が遅くなったことによる。前回の測り直しは当時の記録として残し、比較の基準には使わない。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Sol Low：[登録結果](4349caed06d34a2b83c26281e3280475.json)・[analysis](c301-onequeue-sol61-low-standard14-n5_2026-10-09-analysis.json)・[selection](c301-onequeue-sol61-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c301-onequeue-sol61-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c301-onequeue-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)
- Sonnet low：[登録結果](6d3c16ebd3f34dbda5563c0e6f201dfc.json)・[analysis](c301-onequeue-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c301-onequeue-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c301-onequeue-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c301-onequeue-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)
- 両セル：[待ち行列の記録](c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)
