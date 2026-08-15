# Candidate240 A02 N=5結果

## 結論

Candidate240は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。しかし5件すべてで、開始状態の確認結果を受け取るまで許可済みreadを保留し、その結果を使ってreadを次に発行した。環境依存語を除いた四文でもC147の結果待機境界は再現できなかったため、`mechanism_failed / stopped`とし、別ケース、追加N、Standard14、採用、release、projectionへ進まない。

## 一次結果

- registered result: `e878ab6593f448fab3b8353bc16b9895`
- prompt identity: `the-caption-3ce91a4-portable-result-wait-closure-r1`
- bundle SHA-256: `aed214874743be48960901f58902f007e564bf4e6d3e9db95809aba3884a2103`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `193,418`
- elapsed中央値: `83.42730224999832`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate240はtoken`+49.84%`、elapsed`+13.69%`だった。

Candidate239比はtoken`+20.17%`、elapsed`+31.68%`、Candidate238比はtoken`+5.39%`、elapsed`+15.89%`だった。機序不通過のため、この差を成立した制御の効果として一般化しない。

個別tokenはiteration順に`288,316 / 186,045 / 193,418 / 225,238 / 187,791`だった。

## 実際の動作

iteration 1は`pwd`、branch、HEAD、statusを一件ずつ完了させ、全結果を説明へ使ってから`run.sh`を読んだ。iteration 2〜5は開始確認を一つのcommandへまとめたが、そのcommandのterminal resultを受け取った後に`run.sh`のreadを別発行した。5件すべての最初の説明も「まず開始状態を確認し、その後読む」という逐次方針だった。

したがって、開始結果受領後までreadを保留しない境界は0 / 5件、一部の開始結果を残るreadの選択へ使わない境界も0 / 5件だった。全件で`run.sh`の同じ一行を正しく修正したが、対象の待機依存は変わらなかった。

iteration 1では、全テスト出力が大きく最終diff/status結果が応答から欠落したとして、diff check、diff、statusを再実行した。これは対象外の追加コストとして公式tokenへ補正せず含めた。

## 状態

`a02_n5_completed / quality_passed / wait_closure_failed_5_of_5 / partial_result_barrier_failed_5_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](e878ab6593f448fab3b8353bc16b9895.json)、個別採点は[品質監査](candidate240-portable-result-wait-closure-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate240-portable-result-wait-closure-a02-n5-mechanism-audit-r1.json)を正本とする。
