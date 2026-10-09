# C303のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（2026-10-09）

2026-10-09。[C303](../../docs/candidate303-c301-success-closure-design.md)（C301の書式で、C298の一項目だけをC301へ加えたもの）を、基準の[C301](c301-onequeue-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)と同じ条件（両セルを一つの待ち行列、合計24本）で測った。[C302](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)でSonnet lowの確認コマンドの出力の形が変わったため、二項目のどちらに伴うかを切り分ける材料を得ることが、この計測の理由である。**両セルとも有効70件すべてが4点。費用の中央値は、Sol Lowが基準の幅より下（−8.07%）、Sonnet lowが幅の中（+0.71%）だった。** 経過時間は、Sol Lowが幅の中、Sonnet lowが幅より下だった。除外と再試行は0件。

## 条件

- プロファイル：[Sol Low](../profiles/c303-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r1.json)、[Sonnet low](../profiles/c303-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r1.json)。基準のC301（`-20261009-r3`）とは、prompt identityとプロファイル名だけが違う。
- prompt identity：`the-caption-3ce91a4-uniform-success-closure-r1`、bundle SHA-256 `f94f3b4358c305f95c902f9797f5d163382bf02ee65f283eed0200b0fb43214c`。root `AGENTS.md`は、C302から最後の一行（C299の一項目）を除いたものとバイト一致する。
- 評価コード：コミット`7d770b3`（`scripts/`と`layer2/`は#361と同じ）。両セル140スロットを一つの待ち行列（合計24本）で発行した（[待ち行列の記録](c303-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)）。準備・実行・登録・比較は`campaign-tools/single-prompt-r1/campaign.py`で行った。
- 単価表：`api-standard-2026-10-09`。140件すべてで起動前の実行環境の確認が通った。

## 結果（基準C301との比較）

| セル | 指標 | 基準C301の中央値（幅） | C303の中央値（幅） | 差 | 差（%） | 基準の幅に対する位置 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Sol Low | 品質（0〜100） | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | +0.00 | +0.00% | 幅の中 |
| Sol Low | 費用（USD） | 0.8851（0.8704〜0.9324） | 0.8137（0.7568〜0.9257） | −0.0714 | −8.07% | 幅より下 |
| Sol Low | 経過時間（秒） | 583.89（567.79〜617.29） | 612.28（610.32〜659.34） | +28.39 | +4.86% | 幅の中 |
| Sol Low | 生のトークン（参考） | 2,001,626（1,900,312〜2,098,758） | 1,892,210（1,802,277〜2,155,540） | −109,416 | −5.47% | 幅より下 |
| Sonnet low | 品質（0〜100） | 100.00（100.00〜100.00） | 100.00（100.00〜100.00） | +0.00 | +0.00% | 幅の中 |
| Sonnet low | 費用（USD） | 0.6578（0.6380〜0.6878） | 0.6625（0.6454〜0.6795） | +0.0047 | +0.71% | 幅の中 |
| Sonnet low | 経過時間（秒） | 291.60（283.87〜301.27） | 267.22（263.68〜275.50） | −24.38 | −8.36% | 幅より下 |
| Sonnet low | 生のトークン（参考） | 809,691（794,017〜821,478） | 794,993（773,048〜826,367） | −14,698 | −1.82% | 幅の中 |

比較は`compare-analyses`による（[Sol Low](c303-sol61-low-standard14-n5_2026-10-09-c301-comparison.json)、[Sonnet low](c303-claude-sonnet55-low-standard14-n5_2026-10-09-c301-comparison.json)）。中央値と幅は、14ケースを合算した各反復の値を5回分集計したもの。

参考として、同じ基準と比べたC302は、Sol Lowが費用−9.64%（幅より下）・経過時間+2.82%（幅の中）、Sonnet lowが費用+12.85%（幅より上）・経過時間−0.58%（幅の中）だった。

## 処理の適切さ

- 両セルとも全件4点で、TaskSpecが求める必須の確認は、評価の仕組みが取るコマンドの記録では全件で成功していた。
- F06とF07でTaskSpecが別に求める`git diff --check`は、両セルとも10件中10件で成功していた。
- Sonnet lowのF03の反復1（run `a2258f3f…`）では、`main_verify.sh`の出力が退避され、終了状態が見えないまま、退避された出力を読まずに終えていた。報告では「full gateが通ったかは確認できていない」「確かめるためのコマンドは実行していない」と述べ、成功とは報告していない。成功を確かめる前の読み取りは一項目の対象外だが、モデルは読み取りを行わなかった。C301とC302には、この形のrunはなかった。

## 機序の診断（合否にしない）

[診断の記録](c303-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)。数え方は[C302の診断](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)と同じで、C301とC302の数は同じ記録から再計算して一致を確かめた。

| セル | 項目（1反復あたり） | C301 | C302 | C303 |
| --- | --- | --- | --- | --- |
| Sol Low | 最後に成功したfull gateより後のコマンド | 10〜11回 | 0〜6回 | 2〜8回 |
| Sol Low | 既定値より短い待機時間の指定 | 13〜18回 | 0回 | 9〜16回 |
| Sol Low | 待機だけの呼び出し | 4〜8回 | 0〜2回 | 3〜8回 |
| Sonnet low | 最後に成功したfull gateより後のコマンド | 3〜4回 | 4〜5回 | 2〜4回 |

| Sonnet lowの`main_verify.sh`の実行（20件） | C301 | C302 | C303 |
| --- | ---: | ---: | ---: |
| 出力をファイルへ書き出す、または末尾だけを表示する形 | 15件 | 6件 | 13件 |
| 出力をそのまま返す形 | 5件 | 14件 | 7件 |
| 出力が退避された回数 | 5回 | 14回 | 7回 |
| 退避された出力を読んだ回数（文字数） | 5回（1,916字） | 18回（81,271字） | 6回（2,237字） |

- Sonnet lowで出力をそのまま返す形は、C303では7件（F07の5件とF03の2件）で、C301の5件（F07の5件）に近く、C302の14件ほど増えなかった。退避された出力を`Read`で大きく読んだrunはなかった。C302で見た形の変化は、C298の一項目だけでは同じ大きさでは生じなかった。
- C302とC303の違いはC299の一項目の有無だけだが、N=5の一系列ずつの比較であり、C299の一項目が形の変化を起こしたとは確定しない。
- Sol Lowでは、短い待機時間の指定と待機だけの呼び出しがC301と同じ程度に残り、C302で見た減少はC299の一項目に伴うものと読める。成功後のコマンドはC301より減った。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Sol Low：[登録結果](056402b9980941bdabca92766a2d56aa.json)・[analysis](c303-sol61-low-standard14-n5_2026-10-09-analysis.json)・[selection](c303-sol61-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c303-sol61-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c303-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)・[C301との比較](c303-sol61-low-standard14-n5_2026-10-09-c301-comparison.json)
- Sonnet low：[登録結果](23f793aa4201406ba13ca73de77f4d9b.json)・[analysis](c303-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c303-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c303-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c303-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)・[C301との比較](c303-claude-sonnet55-low-standard14-n5_2026-10-09-c301-comparison.json)
- 両セル：[待ち行列の記録](c303-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)・[機序の診断](c303-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)
