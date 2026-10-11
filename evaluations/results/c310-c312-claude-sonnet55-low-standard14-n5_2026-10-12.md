# C310・C311・C312のSonnet 5.5 low、Standard14 N=5（C309を実際の使い方でも通じる言葉にする、2026-10-12）

2026-10-12。利用者の指摘（C309の「TaskSpec」は試験でしか通用しない）を受けて、C309の言葉を実際の使い方でも通じる言葉にそろえ、その過程で見つかった弱点を潰した。利用者の指示で、Sonnet lowで確かめてからSol Lowを測る。すべて、負荷を見て次のrunを始める条件（CPU使用率70%以下、間隔1秒）で、プールは実効互換の規則（`effective-v1`）で作った。**三つとも有効70件すべてが4点。C312は、確認コマンドの終了コードを示す形が81件中79件になり、出力そのままの実行と、終了コードを確かめない報告がなくなった。費用はC309比+1.81%（幅の中）だった。**

| Candidate | 変更 | 設計記録 |
| --- | --- | --- |
| C310 | C309の二つの項目の「TaskSpecが」を「依頼や適用中の指示が」に置き換える | [設計](../../docs/candidate310-c309-generic-wording-design.md) |
| C311 | C310の、出力を絞ってよいとする一文から範囲の修飾を外す（「確認のコマンドは、出力を絞って実行してよい。…」） | [設計](../../docs/candidate311-c310-trim-permission-unscoped-design.md) |
| C312 | C311のその一文を「確認のコマンドは、そのコマンド自身の終了コードと、判断に必要な部分の出力（末尾など）だけを受け取る形で実行する。」に置き換える | [設計](../../docs/candidate312-c311-validation-receive-form-design.md) |

## 比較の規則と基準

- #374で比較の部分のコードを直したため、完全一致（`exact`）の規則では、評価コードのSHA-256が違い、C309と比べられなくなった。この変更は計測の動きに触れないので、計測の道具を実効互換の規則（`effective-v1`。評価コードのSHA-256は記録だけの項目とし、代わりにモデルへ渡した課題文の一致を確かめる）に切り替えた。
- 基準のC309（Sonnet low N=5）は、70件を流し直さず、実効互換の規則のプールへ登録し直して集計した（[analysis](c309-claude-sonnet55-low-standard14-n5_2026-10-10-analysis-effective-v1.json)、[selection](c309-claude-sonnet55-low-standard14-n5_2026-10-10-selection-effective-v1.json)）。値は元の集計と同じだった。
- 費用は、比べる両方を単価表`api-standard-2026-10-10-r2`で数え直した。Sonnetの単価は`api-standard-2026-10-09`と同じである。

## 結果

| 指標 | C309 N=5 | C309 累積N=20（参考） | C310 | C311 | C312 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 品質（0〜100） | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 |
| 費用（USD） | 0.6637（0.6443〜0.6918） | 0.6708（0.6443〜0.7253） | 0.6988（0.6665〜0.7287） | 0.6889（0.6365〜0.7449） | 0.6757（0.6324〜0.6834） |
| 経過時間（秒） | 290.06（273.76〜308.29） | 236.44（223.16〜308.29） | 227.21（225.37〜235.66） | 231.90（221.26〜240.42） | 224.22（216.13〜230.33） |
| 生のトークン（参考） | 777,420 | 801,026 | 799,610 | 826,951 | 780,484 |

- C310はC309比で費用+5.28%（幅より上）、C311は+3.80%（幅の中）、C312は+1.81%（幅の中）。C312はC311比で−1.91%（幅の中）。
- 経過時間は、計測した時間帯のモデルの応答の速さの違いが大きい（C309の累積N=20で足した分も223〜248秒）。C310〜C312とC309のN=5の差を、プロンプトの効果として扱わない。
- 比較は`compare-analyses`による（一次アーティファクトを参照）。

## 処理の適切さと機序の診断（合否にしない）

[診断の記録](c310-c312-claude-sonnet55-low-standard14-n5_2026-10-12-diagnostics.json)。

| 項目 | C309 | C310 | C311 | C312 |
| --- | ---: | ---: | ---: | ---: |
| 必須の確認コマンドのうち終了コードを表示したもの | 57 / 81 | 52 / 81 | 55 / 85 | 79 / 81 |
| 必須の確認コマンドのうち出力を絞ったもの | 50 / 81 | 33 / 81 | 42 / 85 | 66 / 81 |
| `main_verify.sh`を出力そのままで実行 | 3 / 20 | 11 / 21 | 7 / 20 | 0 / 20 |
| 出力が退避された回数 | 3 | 11 | 7 | 0 |
| 終了コードを確かめずに報告したrun | 0 | 2 | 2 | 0 |
| 状態の確認を最後の確認と同じ応答で行ったrun | 28 / 32 | 28 / 31 | 27 / 31 | 27 / 31 |
| 状態を確かめずに報告したrun | 0 | 0 | 0 | 0 |
| F06・F07の`git diff --check`の成功 | 10/10 | 10/10 | 10/10 | 10/10 |

- C310：「TaskSpecが」を「依頼や適用中の指示が」に変えると、出力を絞ってよいとする一文の効き目が弱くなった。課題文は「以下のTaskSpecに従って作業してください」と書いており、「TaskSpecが求める確認」は課題文の確認コマンドに直接結びついていたと読める。
- C311：範囲の修飾を外すと一部戻ったが、F07を中心に出力そのままの実行が残った。F07は、C301（一文なし）からC311まで、毎回のように出力そのままで実行していた。出力が退避されて終了コードが見えないまま、「終了コードはこの実行では取得していません」「pytestの最終行が失敗なしだったことで判断しています」と報告したrunがあった。
- C312：許可の文を、させたい形（コマンド自身の終了コードと、判断に必要な部分の出力だけを受け取る）を書く文に置き換えると、終了コードの表示が81件中79件、出力そのままの`main_verify.sh`が0件、出力の退避が0件になった。終了コードを表示しなかった2件は、出力の小さい確認だった。処理方法の指定の遵守率は、この計測で初めて確かめた。
- 状態の確認の置き場所の文（「依頼や適用中の指示が求める確認」）は、言葉を変えてもC309と同じ水準で保たれた。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- C310：[登録結果](df5c9cb9b6314d599bd5045a04b45525.json)・[analysis](c310-claude-sonnet55-low-standard14-n5_2026-10-12-analysis.json)・[selection](c310-claude-sonnet55-low-standard14-n5_2026-10-12-selection.json)・[品質監査](c310-claude-sonnet55-low-standard14-n5_2026-10-12-quality-audit.json)・[発行前の記録](c310-claude-sonnet55-low-standard14-n5_2026-10-12-prepare-receipt.json)・[C309との比較](c310-claude-sonnet55-low-standard14-n5_2026-10-12-c309-comparison.json)
- C311：[登録結果](28b6929192d642d1ba6d887287843de5.json)・[analysis](c311-claude-sonnet55-low-standard14-n5_2026-10-12-analysis.json)・[selection](c311-claude-sonnet55-low-standard14-n5_2026-10-12-selection.json)・[品質監査](c311-claude-sonnet55-low-standard14-n5_2026-10-12-quality-audit.json)・[発行前の記録](c311-claude-sonnet55-low-standard14-n5_2026-10-12-prepare-receipt.json)・[C309との比較](c311-claude-sonnet55-low-standard14-n5_2026-10-12-c309-comparison.json)・[C310との比較](c311-claude-sonnet55-low-standard14-n5_2026-10-12-c310-comparison.json)
- C312：[登録結果](4f2d26c95e784ef1a1922ac971fe4fe7.json)・[analysis](c312-claude-sonnet55-low-standard14-n5_2026-10-12-analysis.json)・[selection](c312-claude-sonnet55-low-standard14-n5_2026-10-12-selection.json)・[品質監査](c312-claude-sonnet55-low-standard14-n5_2026-10-12-quality-audit.json)・[発行前の記録](c312-claude-sonnet55-low-standard14-n5_2026-10-12-prepare-receipt.json)・[C309との比較](c312-claude-sonnet55-low-standard14-n5_2026-10-12-c309-comparison.json)・[C311との比較](c312-claude-sonnet55-low-standard14-n5_2026-10-12-c311-comparison.json)
- C309の実効互換の規則での集計：[analysis](c309-claude-sonnet55-low-standard14-n5_2026-10-10-analysis-effective-v1.json)・[selection](c309-claude-sonnet55-low-standard14-n5_2026-10-10-selection-effective-v1.json)
- 診断：[記録](c310-c312-claude-sonnet55-low-standard14-n5_2026-10-12-diagnostics.json)
