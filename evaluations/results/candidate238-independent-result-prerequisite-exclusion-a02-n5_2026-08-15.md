# Candidate238 A02 N=5結果

## 結論

Candidate238は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。一方、開始状態の確認結果に影響されないreadを、その結果の受領後まで未発行にした経路が5 / 5件に残った。作成前に固定した停止条件に従い、`mechanism_failed / stopped`とし、追加N、Standard14、採用、release、projectionへ進まない。

「確認結果はreadの先行条件ではない」と依存関係を否定しても、モデルは5件すべてで開始状態を先に確認し、その結果を受け取ってからreadを別発行した。Candidate229の待機禁止より依存関係を具体化しても、C147の結果影響範囲が持つ発行境界は復元できなかった。

## 一次結果

- registered result: `d4cd0d9aec174d2fabf6743deb32d65c`
- prompt identity: `the-caption-3ce91a4-independent-result-prerequisite-exclusion-r1`
- bundle SHA-256: `1dfca2ca29c0a66af6c11f956c231c80622322c0e5a008d9bf6f35d13152f8f9`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `183,521`
- elapsed中央値: `71.99136791599449`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate238はtoken`+42.17%`、elapsed`-1.89%`だった。

保存反例Candidate229のtoken中央値`456,113`、elapsed中央値`104.2768694999977`秒に対しては、Candidate238がtoken`-59.76%`、elapsed`-30.96%`だった。ただし機序不通過のため、この差を成立した改善効果として一般化しない。

個別tokenはiteration順に`183,521 / 190,087 / 179,955 / 153,315 / 301,569`だった。

## 機序判定

iteration 1〜4は、開始状態を確認するcommandが完了してから`run.sh`のreadを発行した。iteration 5も、`pwd`、HEAD、branchの結果を受け取った後に`run.sh`を読み、残る`git status --short`はそのreadより後へ分割した。開始状態の確認と影響しないreadの間から待機依存を除く境界は0 / 5件で、5 / 5件すべてが不成立だった。

## 状態

`a02_n5_completed / quality_passed / result_prerequisite_exclusion_failed_5_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](d4cd0d9aec174d2fabf6743deb32d65c.json)、個別採点は[品質監査](candidate238-independent-result-prerequisite-exclusion-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate238-independent-result-prerequisite-exclusion-a02-n5-mechanism-audit-r1.json)を正本とする。
