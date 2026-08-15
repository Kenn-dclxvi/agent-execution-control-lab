# Candidate229 A02 N=5結果

## 結論

Candidate229は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。一方、開始状態の結果に影響されないreadを結果受領後まで未発行にした経路が4 / 5件に残った。作成前に固定した停止条件に従い、`mechanism_failed / stopped`とし、Standard14、追加N、採用、release、projectionへ進まない。

「影響しない作業を結果受領後まで発行しないこと自体を許可しない」と書いても、モデルは4件で開始状態を確認し、その結果を受け取ってからreadを別発行した。禁止対象を明示しただけでは、C147の結果影響範囲が持つ発行境界を人間語へ復元できていない。

## 一次結果

- registered result: `671dd3cd50ae4d41bbc4203a797a7e42`
- prompt identity: `the-caption-3ce91a4-c147-direct-human-wait-permission-closure-r1`
- bundle SHA-256: `4ca0c25b38db273f82d6f7555c3f9d70bb69a4a75cdb440ab330ceab3b241c14`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `456,113`
- elapsed中央値: `104.2768694999977`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate229は記述差としてtoken`+253.34%`、elapsed`+42.11%`だった。機序不通過のため、この差を改善効果として扱わない。

## 機序判定

iteration 1〜4では、開始状態を確認するcommandが完了し、モデルへ結果が返った後に`run.sh`のreadを別発行した。iteration 5だけは、開始状態確認とreadが同じ判断から発行され、途中で結果を次の判断へ使っていない。

判定は`1 / 5 passed、4 / 5 failed`である。

## 状態

`a02_n5_completed / quality_passed / result_effect_scope_failed_4_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](671dd3cd50ae4d41bbc4203a797a7e42.json)、個別採点は[品質監査](candidate229-c147-direct-human-wait-permission-closure-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate229-c147-direct-human-wait-permission-closure-a02-n5-mechanism-audit-r1.json)を正本とする。
