# Candidate171 C02開発測定

Candidate171を、既知のCase PRR-C02/r2、Sonnet root、Opus関係レビュー役1人という固定条件で3回実行した。GitHub Actions run [31302081024](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31302081024)、[31302081051](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31302081051)、[31302081026](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31302081026)は、いずれもレビュー、収集、採点を完了し、測定成立条件を満たした。

## 結果

| repetition | quality score | all-agent token | execution | reported cost | fixture-tool access |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 650,719 | 205.994秒 | $0.71131725 | 6 |
| 2 | 4 | 560,749 | 280.957秒 | $0.81381105 | 13 |
| 3 | 1 | 378,709 | 284.726秒 | $0.88092615 | 8 |

quality scoreは`1 / 4 / 1`で、平均は`2.0`、中央値は`1`だった。all-agent tokenの中央値は`560,749`、executionの中央値は`280.957秒`、reported costの中央値は`$0.81381105`だった。

直接の基準にしたCandidate170診断1件と比べると、Candidate171の中央値はtokenが8.23%少なく、reported costが9.33%低く、executionが5.50%長かった。Candidate169の保存済み1件と比べると、tokenは26.59%、reported costは22.61%低く、executionは28.41%長かった。比較相手はいずれも1件だけであり、この差を安定した効率効果とは扱わない。

## 品質

3回とも、別インスタンスのcaseをevaluation setへ混ぜた違反、正しい`rule_id`、category、severityを返した。差が出たのは、違反を成立させる複数pathのidentityである。

- repetition 2は、`members.json`を`path`、setの`README.md`を`related_paths`として返し、期待findingと一致した。
- repetition 1と3は、`members.json`だけをfindingへ結び付け、`README.md`を`related_paths`へ入れなかった。このため、意味上は同じ違反を指摘していても、採点契約上は期待findingの欠落1件と余分なfinding 1件になった。

Candidate171は、違反成立path集合と`path + related_paths`の一致を最終確認するよう明示している。それでも3回中2回で片方が欠けたため、一般的な証拠取得条件と自己確認の指示だけでは、複数path identityを安定して保持できていない。今回の目標だった「Opusを使いながらC02の精度を低コストで上げる」は達成していない。

## 証拠取得の診断

固定した7件のreadを合否条件にはしていない。fixture-tool accessは`6 / 13 / 8`で、3回とも取得順と操作種別を記録できた。consumer bindingは現行hookでは機械検証できないため、全件を`observed_not_machine_qualified`として保持する。

repetition 2では、一つのtool call内に複数のfixture-tool操作が含まれ、tool call数13に対して認識した操作数は16だった。この二つは同じ単位ではないため、差を追加read数として解釈しない。repetition 3では既知の操作名へ分類できないaccessが1件あった。これらは診断情報であり、3 KPIまたは品質の合否条件ではない。

## 次の改善範囲

次の変更では、read件数を再び固定するのではなく、findingの出力許可を複数path identityの検証結果へ結び付ける必要がある。関係レビュー役が、finding本文とは別に「違反の前提として実際に使ったchanged path集合」を返し、rootがその集合と`path + related_paths`の完全一致だけを検証する。集合が一致しない場合はrootがfindingを補完せず、同じ関係レビュー役へ修正を一度だけ要求する構成が候補になる。

この測定はCandidate171の開発用結果である。PRR-C02/r2は設計に使用済みであり、fresh held-out効果、一般化、採用、release、ターゲット本体への反映を示さない。
