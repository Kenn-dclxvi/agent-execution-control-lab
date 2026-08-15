# Candidate228 A02・F02・F03 N=5結果

## 結論

Candidate228は15 / 15件がvalidかつrateableで、15 / 15件がScore `4`だった。判断責任者の記載から新しい実行担当を起動する経路は、F02・F03の10 / 10件で閉じた。

一方、A02は5 / 5件すべてで開始状態の確認を完了した後にreadを別発行した。開始状態の結果はreadの対象、許可、方法、停止条件を変えないため、影響しない作業間の待機依存が残っている。作成前に固定した停止条件に従い、`mechanism_failed / stopped`とし、Standard14、追加N、採用、release、projectionへ進まない。

## 一次結果

- registered result: `7ae274532e454377bab8e715c6380b5b`
- prompt identity: `the-caption-3ce91a4-c147-direct-human-permission-boundaries-r1`
- bundle SHA-256: `5d6b1913c31893b14601e94c001082746ef8486528ebbc78cbd896e5108e84b6`
- compatibility key: `ecad7b450511697e60b62d3b93db7b2fe06dacf667ed8634033e42cba0d8b718`
- valid / excluded / error: `15 / 0 / 0`
- Score: `4 = 15`
- all-agent token中央値: `846,261`
- elapsed中央値: `314.45416637600283`秒

互換なCandidate147対象3ケースの参照result `0444608873624c8ab9e39726769f542d`は、token中央値`390,297`、elapsed中央値`238.3117350002285`秒である。Candidate228は記述差としてtoken`+116.82%`、elapsed`+31.95%`だった。機序不通過のため、この差を改善効果として扱わない。

## 機序判定

### 影響しない結果からの待機依存

A02の5件はすべて、`pwd`、branch、HEAD、statusなどの開始状態確認が完了した後に、固定済みの`run.sh` readを別の呼び出しとして開始した。開始状態の結果でreadの対象または許可は変わらない。したがって「互いに影響しない作業の間に、待機や停止への依存関係を作らない」という文だけでは、その依存を実行不能にできなかった。

判定は`0 / 5 passed、5 / 5 failed`である。

### 判断責任者からの担当起動

F02の判断責任者`independent contract check`とF03の判断責任者`independent state check`は、独立した実行担当の指定ではない。10件すべてで新しい担当の起動はなく、rootが作業を完了した。

判定は`10 / 10 passed、0 / 10 failed`である。品質Ratingでは独立担当の結果がないためowner evidenceが診断上`inadmissible`となるが、これは今回閉じる機序では期待どおりの観測であり、Rating v14では診断項目である。

## 状態

`targeted_n5_completed / quality_passed / result_effect_scope_failed_5_of_5 / owner_producer_gate_passed_10_of_10 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](7ae274532e454377bab8e715c6380b5b.json)、個別採点は[品質監査](candidate228-c147-direct-human-permission-boundaries-targeted-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate228-c147-direct-human-permission-boundaries-targeted-n5-mechanism-audit-r1.json)を正本とする。
