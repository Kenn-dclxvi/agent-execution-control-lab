# Candidate241 A02 N=5結果

## 結論

Candidate241は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。結果を受け取る前に、開始確認の影響を受けない許可済みreadへ着手したのは2 / 5件であり、Candidate240の0 / 5件から動作差は生じた。しかし残る3件では開始確認のresultを判断へ使った後にreadを選ぶ経路が残ったため、事前gateの5 / 5件を満たさず`mechanism_failed / stopped`とする。別ケース、追加N、Standard14、採用、release、projectionへ進まない。

## 一次結果

- registered result: `77fd75c4c3e347778594a6025fa92de6`
- prompt identity: `the-caption-3ce91a4-result-issuance-frontier-r1`
- bundle SHA-256: `68b436c54b81321c639fd512718412d31dc411d612a2969b73f706abc0e9eaa2`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `162,000`
- elapsed中央値: `63.85347620898392`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate241はtoken`+25.50%`、elapsed`-12.98%`だった。

Candidate239比はtoken`+0.65%`、elapsed`+0.78%`、Candidate240比はtoken`-16.24%`、elapsed`-23.46%`だった。機序不通過のため、この差を成立した制御の一般的効果として扱わない。

個別tokenは登録resultのiteration順に`188,975 / 141,970 / 162,000 / 166,812 / 155,850`だった。

## 実際の動作

実行時iteration 2と3は、最初の判断で開始確認、`run.sh`のread、canonical entrypointの限定調査をすべて選び、途中のresultを次の作業選択へ使う前に着手した。iteration 3はreadと限定調査を開始確認より先に発行し、iteration 2は開始確認を先に発行したが、結果を使う説明を挟まず同じ判断内でreadと限定調査も発行した。

iteration 1、4、5は開始確認だけを完了し、そのresultを使ってcleanな開始状態を説明した後に`run.sh`とcanonical entrypointを読んだ。この3件では、C240で確認した遅延選択経路がそのまま残った。

全5件は`run.sh`の同じ一行だけを`src.app.entrypoints.v4_daily_main`へ正しく修正し、構文確認、既存テスト、diff確認を完了した。品質は維持されたが、着手範囲の固定は2 / 5件にとどまった。

## 状態

`a02_n5_completed / quality_passed / issuance_frontier_passed_2_of_5 / delayed_selection_failed_3_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](77fd75c4c3e347778594a6025fa92de6.json)、個別採点は[品質監査](candidate241-result-issuance-frontier-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate241-result-issuance-frontier-a02-n5-mechanism-audit-r1.json)を正本とする。
