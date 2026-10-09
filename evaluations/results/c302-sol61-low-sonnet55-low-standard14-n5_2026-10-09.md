# C302のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（2026-10-09）

2026-10-09。[C302](../../docs/candidate302-c301-success-closure-and-wait-time-design.md)（C301の書式で、C298とC299の二項目をC301へ加えたもの）を、実行環境を切り離した系列で、基準の[C301](c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)と同じ条件（両セルを一つの待ち行列、合計24本）で測った。**両セルとも有効70件すべてが4点。費用の中央値は、Sol Lowが基準の幅より下（−9.64%）、Sonnet lowが基準の幅より上（+12.85%）だった。** 経過時間は両セルとも基準の幅の中だった。除外と再試行は0件。

## 条件

- プロファイル：[Sol Low](../profiles/c302-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r1.json)、[Sonnet low](../profiles/c302-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r1.json)。基準のC301（`-20261009-r3`）とは、prompt identityとプロファイル名だけが違う。
- prompt identity：`the-caption-3ce91a4-uniform-success-closure-and-wait-time-r1`、bundle SHA-256 `d5601a80de209dcab041a2c875084ebb9b64e6803c41fb463490b6dec8fb5a31`。
- 評価コード：コミット`bfe5ce7`（`scripts/`と`layer2/`は#361と同じ）。両セル140スロットを一つの待ち行列（合計24本）で発行した（[待ち行列の記録](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)）。準備・実行・登録・比較は`campaign-tools/single-prompt-r1/campaign.py`で行った。
- 単価表：`api-standard-2026-10-09`。140件すべてで起動前の実行環境の確認が通った。

## 結果（基準C301との比較）

| セル | 指標 | 基準C301の中央値（幅） | C302の中央値（幅） | 差 | 差（%） | 基準の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Sol Low | 品質（0〜100） | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | +0.00 | +0.00% | 幅の中 |
| Sol Low | 費用（USD） | 0.8851（0.8704〜0.9324） | 0.7998（0.7118〜0.8905） | −0.0853 | −9.64% | 幅より下 |
| Sol Low | 経過時間（秒） | 583.89（567.79〜617.29） | 600.34（564.00〜652.27） | +16.45 | +2.82% | 幅の中 |
| Sol Low | 生のトークン（参考） | 2,001,626（1,900,312〜2,098,758） | 1,657,230（1,555,689〜1,995,681） | −344,396 | −17.21% | 幅より下 |
| Sonnet low | 品質（0〜100） | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | +0.00 | +0.00% | 幅の中 |
| Sonnet low | 費用（USD） | 0.6578（0.6380〜0.6878） | 0.7423（0.6889〜0.8198） | +0.0845 | +12.85% | 幅より上 |
| Sonnet low | 経過時間（秒） | 291.60（283.87〜301.27） | 289.91（278.38〜310.60） | −1.69 | −0.58% | 幅の中 |
| Sonnet low | 生のトークン（参考） | 809,691（794,017〜821,478） | 888,452（841,868〜1,047,753） | +78,761 | +9.73% | 幅より上 |

比較は`compare-analyses`による（[Sol Low](c302-sol61-low-standard14-n5_2026-10-09-c301-comparison.json)、[Sonnet low](c302-claude-sonnet55-low-standard14-n5_2026-10-09-c301-comparison.json)）。中央値と幅は、14ケースを合算した各反復の値を5回分集計したもの。

## 処理の適切さ

- 両セルとも全件4点で、TaskSpecが求める必須の確認は全件で成功していた。
- F06とF07でTaskSpecが別に求める`git diff --check`は、基準と同じく両セルとも10件中10件で成功していた。C298の一項目による、求められた確認の抜けは見られなかった。

## 機序の診断（合否にしない）

[診断の記録](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)。数え方は[設計記録](../../docs/candidate302-c301-success-closure-and-wait-time-design.md)の項目2と同じ。

| セル | 項目 | C301（1反復あたり） | C302（1反復あたり） |
| --- | --- | --- | --- |
| Sol Low | 最後に成功したfull gateより後のコマンド | 10〜11回 | 0〜6回 |
| Sol Low | 既定値より短い待機時間の指定 | 13〜18回 | 0回 |
| Sol Low | 待機だけの呼び出し | 4〜8回 | 0〜2回 |
| Sonnet low | 最後に成功したfull gateより後のコマンド | 3〜4回 | 4〜5回 |

Sonnet lowの費用の増加は、F01（+26%）とF03（+35%）に集中し、数件の高いrun（F03の反復4が$0.196など）によるものだった。これらのrunでは、`main_verify.sh`の出力（約155KB）をそのまま返す形で実行し、Claude Codeが出力をファイルへ退避して一部だけを返したため、成功したかを確かめるために退避されたファイルを読み直していた。

| Sonnet lowの`main_verify.sh`の実行（20件） | C301 | C302 |
| --- | ---: | ---: |
| 出力をファイルへ書き出す、または末尾だけを表示する形 | 15件 | 6件 |
| 出力をそのまま返す形 | 5件 | 14件 |
| 出力が退避された回数 | 5回 | 14回 |
| 退避された出力を読んだ回数（文字数） | 5回（1,916字） | 18回（81,271字） |

C298の一項目（必須の確認がすべて成功した後はコマンドを発行せずに報告する）が、出力を整える後処理を避けさせた可能性がある。ただし、この因果は確かめていない。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Sol Low：[登録結果](636f8d60ae32454ea80c8ac854916dc2.json)・[analysis](c302-sol61-low-standard14-n5_2026-10-09-analysis.json)・[selection](c302-sol61-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c302-sol61-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c302-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)・[C301との比較](c302-sol61-low-standard14-n5_2026-10-09-c301-comparison.json)
- Sonnet low：[登録結果](b90ee4a10b8d4f42bca36e6794aaecad.json)・[analysis](c302-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c302-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c302-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c302-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)・[C301との比較](c302-claude-sonnet55-low-standard14-n5_2026-10-09-c301-comparison.json)
- 両セル：[待ち行列の記録](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)・[機序の診断](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)
