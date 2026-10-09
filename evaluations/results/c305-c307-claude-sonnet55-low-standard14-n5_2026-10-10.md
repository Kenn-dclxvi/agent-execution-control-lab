# C305・C306・C307のSonnet 5.5 low、Standard14 N=5（ベースC302の弱点を潰す、2026-10-10）

2026-10-09〜10。利用者の判断でベースをC302に決め、[C302の測り直し](c302-admission-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)で見つけた弱点を、Sonnet lowで順に潰した。利用者の指示により、Sonnet lowで確立するまでSolは測っていない。すべて、負荷を見て次のrunを始める条件（CPU使用率70%以下、間隔1秒）で測った。**三つとも有効70件すべてが4点。C307（C306に確認コマンドの出力を絞ってよいとする一項目を加えたもの）は、C306比で費用−9.74%（幅より下）、基準のC301 `-r5`比でも費用−5.14%（幅より下）だった。** 利用者の判断で、ベースはC302からC306に移した。

| Candidate | 中身 | 設計記録 |
| --- | --- | --- |
| C305 | C301＋C299の一項目だけ（出力の形の変化の切り分け） | [設計](../../docs/candidate305-c301-wait-time-design.md) |
| C306 | C302のC298の一項目を「TaskSpecが求める確認がすべて成功した後は、TaskSpecが求めていないコマンドを発行せずに報告する。」に置き換える | [設計](../../docs/candidate306-c302-taskspec-scoped-success-closure-design.md) |
| C307 | C306＋「TaskSpecが求める確認のコマンドは、出力を絞って実行してよい。確かめる終了コードは、そのコマンド自身のものとする。」 | [設計](../../docs/candidate307-c306-validation-output-trim-design.md) |

## 結果

| 計測 | 品質 | 費用（USD） | 経過時間（秒） | 生のトークン（参考） |
| --- | --- | ---: | ---: | ---: |
| C301 `-r5`（基準） | 4点70件 | 0.6811（0.6634〜0.6938） | 286.68（269.85〜343.71） | 822,676 |
| C302 `-r2`（元のベース） | 4点70件 | 0.7363（0.7119〜0.8138） | 297.07（255.30〜315.08） | 850,176 |
| C305 | 4点70件 | 0.6909（0.6816〜0.7040） | 326.26（315.27〜363.85） | 832,597 |
| C306 | 4点70件 | 0.7158（0.6802〜0.7289） | 299.44（285.89〜362.57） | 867,364 |
| C307 | 4点70件 | 0.6461（0.6199〜0.7125） | 284.20（275.11〜327.25） | 816,981 |

| 比較 | 費用 | 経過時間 | 生のトークン（参考） |
| --- | --- | --- | --- |
| C305 − C301 `-r5` | +1.44%（幅の中） | +13.81%（幅の中） | +1.21% |
| C306 − C302 `-r2` | −2.78%（幅の中） | +0.80%（幅の中） | +2.02% |
| C306 − C301 `-r5` | +5.09%（幅より上） | +4.45%（幅の中） | +5.43% |
| C307 − C306 | −9.74%（幅より下） | −5.09%（幅より下） | −5.81% |
| C307 − C301 `-r5` | −5.14%（幅より下） | −0.87%（幅の中） | −0.69% |

比較は`compare-analyses`による（一次アーティファクトを参照）。

## 処理の適切さと機序の診断（合否にしない）

[診断の記録](c305-c307-claude-sonnet55-low-standard14-n5_2026-10-10-diagnostics.json)。

| 項目 | C301 `-r5` | C302 `-r2` | C305 | C306 | C307 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F06・F07の`git diff --check`の成功 | 10/10 | 9/10 | 10/10 | 10/10 | 10/10 |
| 退避された出力を読まずに終えたrun | 0 | 2 | 0 | 0 | 0 |
| `main_verify.sh`をそのままの形で実行 | 4 / 21 | 13 / 20 | 7 / 20 | 12 / 20 | 6 / 21 |
| 個別のテストをそのままの形で実行 | 6 / 36 | ― | ― | 8 / 33 | 2 / 34 |
| 出力が退避された回数 | 4 | 13 | 7 | 12 | 6 |
| 退避された出力を読んだ文字数 | 1,545 | 45,044 | 2,830 | 5,561 | 4,142 |

- **C306：** 求められた確認を止める経路（C302のF07が`git diff --check`を実行しなかった件）と、退避された出力を読まずに終える経路は、どちらも0件になった。
- **C305：** C299の一項目だけでは、そのままの形は7件で、C298だけのC303（7件）と同じだった。二つの文がそろったC302とC306でだけ12〜14件に増えていた。
- **C306の費用の増加：** C301 `-r5`比の増加は、ほとんどがF01だった。F01の5件中4件で、個別のテスト（`pytest … -v`）の出力約19,000字を絞らずに受け取り、その1回のリクエストが1件あたり約$0.04だった。
- **C307：** そのままの形は、`main_verify.sh`が21件中6件、個別のテストが34件中2件に戻った。課題文の指定に反する実行（`command_protocol_violations`）は0件で、終了コードの取り違えによる品質の低下はなかった。

## 計測の経過

C305とC306の最初の発行は、計測用のClaudeアカウントが5時間の利用上限に達したため、途中から外部失敗として除外された（C305は70件中39件が有効、C306は0件）。上限が戻った後、不足分だけを新しい回として発行した（C305は31件、C306は70件）。有効なrunは再実行していない。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- C305：[登録結果](306f51df0a7a46f59f0e2702cfa5c1bf.json)・[analysis](c305-claude-sonnet55-low-standard14-n5_2026-10-10-analysis.json)・[selection](c305-claude-sonnet55-low-standard14-n5_2026-10-10-selection.json)・[品質監査](c305-claude-sonnet55-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](c305-claude-sonnet55-low-standard14-n5_2026-10-10-prepare-receipt.json)・[C301 `-r5`との比較](c305-claude-sonnet55-low-standard14-n5_2026-10-10-c301-r5-comparison.json)
- C306：[登録結果](f100bf5699b14840a0bff63891aa8aab.json)・[analysis](c306-claude-sonnet55-low-standard14-n5_2026-10-10-analysis.json)・[selection](c306-claude-sonnet55-low-standard14-n5_2026-10-10-selection.json)・[品質監査](c306-claude-sonnet55-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](c306-claude-sonnet55-low-standard14-n5_2026-10-10-prepare-receipt.json)・[C302 `-r2`との比較](c306-claude-sonnet55-low-standard14-n5_2026-10-10-c302-r2-comparison.json)・[C301 `-r5`との比較](c306-claude-sonnet55-low-standard14-n5_2026-10-10-c301-r5-comparison.json)
- C307：[登録結果](3fff51f0f02d4929b2b75af1ba05aa7e.json)・[analysis](c307-claude-sonnet55-low-standard14-n5_2026-10-10-analysis.json)・[selection](c307-claude-sonnet55-low-standard14-n5_2026-10-10-selection.json)・[品質監査](c307-claude-sonnet55-low-standard14-n5_2026-10-10-quality-audit.json)・[発行前の記録](c307-claude-sonnet55-low-standard14-n5_2026-10-10-prepare-receipt.json)・[C306との比較](c307-claude-sonnet55-low-standard14-n5_2026-10-10-c306-comparison.json)・[C301 `-r5`との比較](c307-claude-sonnet55-low-standard14-n5_2026-10-10-c301-r5-comparison.json)
- 三つ共通：[診断の記録](c305-c307-claude-sonnet55-low-standard14-n5_2026-10-10-diagnostics.json)
