# Candidate242 A02 N=5結果

## 結論

Candidate242は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。開始確認だけを先に完了せず、途中のresultを次の作業選択へ使う前に影響しないreadも選んだのは3 / 5件であり、Candidate241の2 / 5件から動作差は生じた。しかし残る2件では開始確認だけを完了し、そのresultを説明した後にreadを選ぶ経路が残ったため、事前gateの5 / 5件を満たさず`mechanism_failed / stopped`とする。別ケース、追加N、Standard14、採用、release、projectionへ進まない。

## 一次結果

- registered result: `f5f78ea591414f949e33d0c84edf4665`
- prompt identity: `the-caption-3ce91a4-start-check-only-completion-exclusion-r1`
- bundle SHA-256: `685c08b155bff522d20b9110264cdcaf11f894acc790c2df12dbefaddd82b283`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `190,525`
- elapsed中央値: `79.1322882079985`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate242はtoken`+47.60%`、elapsed`+7.84%`だった。

Candidate239比はtoken`+18.37%`、elapsed`+24.90%`、Candidate240比はtoken`-1.50%`、elapsed`-5.15%`、Candidate241比はtoken`+17.61%`、elapsed`+23.93%`だった。機序不通過のため、この差を成立した制御の一般的効果として扱わない。

個別tokenは登録resultのiteration順に`190,525 / 144,825 / 209,903 / 331,071 / 186,989`だった。

## 実際の動作

実行時iteration 2、4、5は、開始確認の完了後に利用者向け説明を挟まず、`run.sh`とcanonical entrypointのreadも選んだ。個別commandの開始・完了は直列に記録された場合があるが、開始確認resultを判断へ使うagent messageはread選択より前に存在しない。

iteration 1と3は開始確認だけを完了し、cleanな開始状態を説明した後に`run.sh`とcanonical entrypointを読んだ。この2件では、Candidate241から残った遅延選択経路が消えていない。

全5件は`run.sh`の同じ一行だけを`src.app.entrypoints.v4_daily_main`へ正しく修正し、構文確認、既存テスト、diff確認を完了した。品質は維持され、対象機序も2 / 5件から3 / 5件へ動いたが、一文による禁止は一貫して働かなかった。

## 状態

`a02_n5_completed / quality_passed / start_check_only_completion_exclusion_passed_3_of_5 / delayed_selection_failed_2_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](f5f78ea591414f949e33d0c84edf4665.json)、個別採点は[品質監査](candidate242-start-check-only-completion-exclusion-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate242-start-check-only-completion-exclusion-a02-n5-mechanism-audit-r1.json)を正本とする。
