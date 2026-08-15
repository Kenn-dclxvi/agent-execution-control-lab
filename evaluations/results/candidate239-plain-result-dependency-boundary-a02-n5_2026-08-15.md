# Candidate239 A02 N=5結果

## 結論

Candidate239は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。しかし、5件すべてで開始状態の確認結果を受け取ってから、影響しない`run.sh`のreadを別に発行した。利用者指定の一文だけでは待機依存を除けなかったため、`mechanism_failed / stopped`とし、次のケース、追加N、Standard14、採用、release、projectionへ進まない。

> 影響しない結果から、待機や停止への依存関係を作らない。

この一文は、Candidate238より総使用トークンを減らしたが、Candidate147の機能は再現しなかった。

## 一次結果

- registered result: `bd3434af2bf74fb289401d31efed32ea`
- prompt identity: `the-caption-3ce91a4-plain-result-dependency-boundary-r1`
- bundle SHA-256: `384a32cc650b4d3c433cdcc459113c1d287da3cde3ecf76f30bac9a464cd085a`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `160,959`
- elapsed中央値: `63.35727637499804`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate239はtoken`+24.69%`、elapsed`-13.66%`だった。

Candidate238のtoken中央値`183,521`、elapsed中央値`71.99136791599449`秒に対しては、token`-12.29%`、elapsed`-11.99%`だった。Candidate228のA02 token中央値`308,007`に対しては`-47.74%`だった。ただし対象機序が不成立なので、これらを成立した制御の改善効果として一般化しない。

個別tokenはiteration順に`133,044 / 124,966 / 160,959 / 188,726 / 173,276`だった。

## 機序判定

iteration 1〜5のすべてで、最初に`pwd`、branch、HEAD、statusの全部または一部を確認し、その結果を受け取った後に`run.sh`を読んだ。開始状態の結果によってreadの対象または許可は変わらない。したがって、影響しない結果とreadの間から待機依存を除く境界は0 / 5件で、5 / 5件が不成立だった。

## 状態

`a02_n5_completed / quality_passed / result_dependency_boundary_failed_5_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](bd3434af2bf74fb289401d31efed32ea.json)、個別採点は[品質監査](candidate239-plain-result-dependency-boundary-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate239-plain-result-dependency-boundary-a02-n5-mechanism-audit-r1.json)を正本とする。
