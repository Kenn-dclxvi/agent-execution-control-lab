# C302のGPT-6.1 Sol Low・Sonnet 5.5 low、Standard14 N=5（負荷を見て始める条件、2026-10-09）

2026-10-09。利用者の判断で、汎用指示のベースをC302（C301＋C298の一項目＋C299の一項目）に決めた。弱点を洗い出すため、負荷を見て次のrunを始める発行の条件（CPU使用率70%以下、間隔1秒、[試行の記録](c301-sonnet55-low-load-admission-trials_2026-10-09.md)）で両セルを測り直した。**両セルとも有効70件すべてが4点。Sonnet lowは、同じ条件のC301（`-r5`）比で費用+8.10%（幅より上）、経過時間+3.63%（幅の中）。** 同じ条件のC301のSolはまだないため、Sol Lowは比べていない。除外と再試行は0件。

## 条件

- プロファイル：[Sol Low `-r2`](../profiles/c302-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r2.json)、[Sonnet low `-r2`](../profiles/c302-claude-sonnet55-low-standard14-n5-cli2288-shellenv-20261009-r2.json)。前回の[C302](c302-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)（`-r1`）とは、発行の条件と並び順の見積もり時間だけが違う。
- 両セル140件を一つの待ち行列で、負荷を見て発行した（[発行の記録](c302-admission-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)）。

## 結果

| セル | 指標 | C302 `-r2`の中央値（幅） | 同じ条件の基準 |
| --- | --- | ---: | --- |
| Sol Low | 品質（0〜100） | 100.00（100.00〜100.00） | なし |
| Sol Low | 費用（USD） | 0.8440（0.7990〜0.8797） | なし |
| Sol Low | 経過時間（秒） | 628.06（605.40〜650.69） | なし |
| Sol Low | 生のトークン（参考） | 1,667,104（1,616,080〜1,740,360） | なし |
| Sonnet low | 品質（0〜100） | 100.00（100.00〜100.00） | C301 `-r5`：100.00（幅の中） |
| Sonnet low | 費用（USD） | 0.7363（0.7119〜0.8138） | C301 `-r5`：0.6811（0.6634〜0.6938）、+8.10%、幅より上 |
| Sonnet low | 経過時間（秒） | 297.07（255.30〜315.08） | C301 `-r5`：286.68、+3.63%、幅の中 |
| Sonnet low | 生のトークン（参考） | 850,176（832,769〜902,780） | C301 `-r5`：822,676、+3.34%、幅の中 |

Sonnet lowの比較は`compare-analyses`による（[記録](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-c301-r5-comparison.json)）。

## 弱点の洗い出し（合否にしない）

[診断の記録](c302-admission-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)。

1. **成功後の一項目が、TaskSpecの求める確認まで止めた（Sonnet low、処理の適切さ）。** F07（反復4）は、`main_verify.sh`の成功を受けた後、TaskSpecが`F07-C3`で求める`git diff --check`と変更path確認を実行せずに報告した。報告では「確認コマンドが成功した後はコマンドを発行せず報告する、というCLAUDE.mdの指示に従った」と理由を述べ、`F07-C3`が未完了であることを自ら記した。F06とF07で`git diff --check`が成功した件数は10件中9件（C301 `-r5`とC304は10件中10件）。同じrunとF01（反復3）は、退避された`main_verify.sh`の出力を読まずに報告した。品質の採点は4点である。
2. **確認コマンドの出力をそのまま返し、退避された大きな出力を読み直した（Sonnet low、費用）。** `main_verify.sh`を出力そのままの形で実行した件数は20件中13件で、前回のC302（14件）と同じ傾向だった。同じ条件のC301 `-r5`は4件、C304は2件、本数の上限だけで測ったC303（C298だけ）は7件だった。退避された出力は12回、計44,229字読まれた。費用の増加はF01に集中した（ケースの中央値で+$0.050、最大のrunは$0.189で、退避された出力を37,708字読み直していた）。
3. **Solの最初のリクエストがキャッシュに乗らないrun（発行の側の揺れ）。** C302 `-r2`では70件中20件あった（C301-r3は14件、C302 `-r1`は10件、C303は3件）。1反復あたり最大で約$0.09を上乗せする。Sol LowのF05（確認だけのケース）の費用が高く出たのはこのためで、プロンプトの差ではない。

Sol Lowでは、二項目が閉じる操作はほぼ起きていなかった（成功後のコマンドは1反復あたり0〜3回、短い待機時間の指定は0回、待機だけの呼び出しは0〜1回）。F06とF07の`git diff --check`は10件中10件で成功した。

弱点1はC306（成功後の一項目をTaskSpecが求める確認で区切る）、弱点2はC305（C299の一項目だけを加えて切り分ける）で扱う。採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- Sol Low：[登録結果](5fa14d7a0c5b48a1ae891181525f4b98.json)・[analysis](c302-admission-sol61-low-standard14-n5_2026-10-09-analysis.json)・[selection](c302-admission-sol61-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c302-admission-sol61-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c302-admission-sol61-low-standard14-n5_2026-10-09-prepare-receipt.json)
- Sonnet low：[登録結果](d1caad9ba39e496ab7e10bdf4095094a.json)・[analysis](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-analysis.json)・[selection](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-selection.json)・[品質監査](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-quality-audit.json)・[発行前の記録](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-prepare-receipt.json)・[C301 `-r5`との比較](c302-admission-claude-sonnet55-low-standard14-n5_2026-10-09-c301-r5-comparison.json)
- 両セル：[発行の記録](c302-admission-sol61-low-sonnet55-low-standard14-n5_2026-10-09-campaign-summary.json)・[機序の診断](c302-admission-sol61-low-sonnet55-low-standard14-n5_2026-10-09-mechanism-diagnostics.json)
