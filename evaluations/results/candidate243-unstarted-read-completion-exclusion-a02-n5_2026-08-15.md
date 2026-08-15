# Candidate243 A02 N=5結果

## 結論

Candidate243は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。全5件で、開始確認resultを説明または判断へ使う前に影響しないreadも選ばれ、Candidate242で2 / 5件に残った遅延選択は0件になった。品質と対象機序は通過した。

一方、all-agent token中央値は`151,990`で、事前に固定したCandidate147中央値`129,085`を`17.74%`上回った。事前のコスト停止条件により`targeted_passed / cost_not_reduced / stopped`とし、別ケース、追加N、Standard14、採用、release、projectionへ進まない。

## 一次結果

- registered result: `5523eae9775e42f585fc9e91a02f88b2`
- prompt identity: `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- bundle SHA-256: `229f6edc654c8cd6fd1375774c464d3305885befb8e44b1f9b7e85bdd3668193`
- compatibility key: `59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `151,990`
- elapsed中央値: `72.94628641597228`秒

互換なCandidate147 A02 result `c08d676a0d97424f88dc2ab1d7fe2961`は、token中央値`129,085`、elapsed中央値`73.37932329112664`秒である。Candidate243はtoken`+17.74%`、elapsed`-0.59%`だった。

Candidate239比はtoken`-5.57%`、elapsed`+15.13%`、Candidate240比はtoken`-21.42%`、elapsed`-12.56%`、Candidate241比はtoken`-6.18%`、elapsed`+14.24%`、Candidate242比はtoken`-20.23%`、elapsed`-7.82%`だった。A02 N=5の範囲で対象機序は成立したが、C147比のコスト差は解消していない。

個別tokenは登録resultのiteration順に`186,669 / 130,786 / 131,339 / 151,990 / 182,938`だった。

## 実際の動作

全5件で、開始確認と`run.sh`およびcanonical entrypointのreadが、途中のagent messageによるresult消費を挟まず選ばれた。commandの開始・完了が直列に記録されたrunでも、開始確認resultを説明または次の作業選択へ使うagent messageはread選択より前に存在しない。

全5件は`run.sh`の同じ一行だけを`src.app.entrypoints.v4_daily_main`へ正しく修正し、構文確認、既存テスト、diff確認を完了した。Candidate242の「先に」をread未着手という状態へ直接対応付けたことで、対象の遅延選択は5 / 5件で閉じた。

## 状態

`a02_n5_completed / quality_passed / mechanism_passed / targeted_passed / cost_not_reduced / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](5523eae9775e42f585fc9e91a02f88b2.json)、個別採点は[品質監査](candidate243-unstarted-read-completion-exclusion-a02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate243-unstarted-read-completion-exclusion-a02-n5-mechanism-audit-r1.json)を正本とする。
