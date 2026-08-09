# Candidate170 C02診断測定

Candidate170のpromptを変更せず、PRR-C02/r2を同じSonnet rootとOpus関係レビュー役1人の構成で再実行した。GitHub Actions run [31300109132](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31300109132)はレビュー、結果収集、採点を完了し、測定成立条件を満たした。

## 結果

| 条件 | quality score | all-agent token | execution | reported cost | fixture-tool access |
|---|---:|---:|---:|---:|---:|
| Candidate169 | 4 | 763,825 | 218.789秒 | $1.05153175 | 18 |
| Candidate170 初回 | 4 | 595,146 | 192.789秒 | $1.10362325 | 11 |
| Candidate170 診断 | 1 | 611,050 | 266.321秒 | $0.89759800 | 8 |

今回の診断はCandidate169に対してtokenが20.00%少なく、reported costが14.64%低かった。一方でexecutionは21.73%長い。Candidate170初回に対してはtokenが2.67%、executionが38.14%増え、reported costは18.67%低かった。1回の診断値であるため、これらをCandidate170の安定した効果とは扱わない。

## 品質

関係レビュー役は、別インスタンスのケースを評価setへ混ぜた違反と、正しい`rule_id`、category、severityを返した。しかし、違反成立に必要なREADMEを`related_paths`へ含めず、`members.json`だけをfindingへ結び付けた。oracleはREADMEの比較範囲宣言と`members.json`のmembershipの関係を一つのfindingとして要求するため、期待findingの欠落1件と余分なfinding 1件となり、quality scoreは`1`だった。

Candidate170初回は同じケースでscore `4`だったため、この結果は「違反を発見できない」という固定的な失敗ではない。複数pathの関係を見つけても、最終出力で必要なpath集合を安定して保持できないことが、現在の主な品質上の弱点である。

## 証拠取得

必須7件は一つのbatchで共同発行された。その前後にfixture-tool accessが1件あり、strictなmechanism条件は`unsatisfied`となった。内容非保存の診断記録には、必須7操作の`eligibility / metadata / changed-paths / diff / rules / files / contract`が残った一方、追加1件には既知の操作名が残っていない。

この観測からは、追加1件が変更本文の再読だったとはいえない。fixture-toolの既知subcommandを伴わない使い方確認だった可能性が高いが、生のcommandを保存しない設計のため確定はしない。Candidate170初回の追加4件から今回の1件へ減ったことも、promptの確定的効果ではなく実行間変動として扱う。

## token内訳

all-agent input 610,888の内訳は、通常input 52、cache creation input 90,316、cache read input 520,520だった。cache readが85.21%、cache creationが14.78%を占める。rootはinput全体の29.89%、Opus関係レビュー役は70.11%だった。出力はroot 17、関係レビュー役145、合計162 tokenである。

総tokenだけではreported costの差を説明できない。今回の値はcache read中心であり、Candidate170初回より総tokenが多いのにreported costが低い。ただしCandidate169とCandidate170初回には同じ価格区分の内訳がないため、過去2件との差を価格区分だけへ帰属させない。

## 次の改善範囲

次のCandidateでは、C02の精度を上げながら低コストを維持するため、次の二点だけを同じprompt revisionで扱う価値がある。

1. 7件の正確なfixture-tool subcommandをpromptへ示し、bare invocationによる使い方確認を不要にする。
2. finding候補ごとに、違反の成立に使ったchanged path集合と`path + related_paths`の集合が一致しなければ出力しない、という最終確認を機械的な集合比較として表す。

この変更は結果確認済みのPRR-C02/r2で開発校正し、複数回の品質とtokenを確認する。今回の結果はfresh held-out evidenceではなく、Candidateの採用、release、本体反映を決めない。
