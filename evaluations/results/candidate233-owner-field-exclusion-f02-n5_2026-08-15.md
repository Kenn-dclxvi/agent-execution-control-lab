# Candidate233 F02 N=5結果

## 結論

Candidate233は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。判断責任者名`independent contract check`から独立workerを起動したrunは0 / 5件で、事前に固定した担当起動境界を通過した。

token中央値は`169,370`で、Candidate231の`133,657`より`35,713`、`26.72%`大きく、Candidate147の`128,236`より`41,134`、`32.08%`大きかった。機序は復元できたが、C147に近いtokenという点ではCandidate231より後退した。

## 一次結果

- registered result: `670d5536ed5a4baaabbba29d55cc6c0e`
- prompt identity: `the-caption-3ce91a4-owner-field-exclusion-r1`
- bundle SHA-256: `e86424f86b12c2d414eb6eeb1752057b322507788784df5a8d750d47392c9cf4`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `169,370`
- elapsed中央値: `79.6329457089887`秒

互換なCandidate147 F02 result `b99e9ed0bc974a75805942f9ad05a8cc`は、token中央値`128,236`、elapsed中央値`100.60693224985152`秒である。Candidate233はtoken `+32.08%`、elapsed `-20.85%`だった。

Candidate231の同じF02 N=5 result `f0ab6a23339b4fb59458da2da7ce0549`は、token中央値`133,657`、elapsed中央値`79.10220091699739`秒である。Candidate233はtoken `+26.72%`、elapsed `+0.67%`だった。

## 担当起動境界

5件とも、TaskSpecの`criterion owner`欄に`independent contract check`があっても独立producer executionの指定とは扱わず、rootが判定した。`criterion owner`欄の値、`independent`等の名称、独立判定の必要性をworker起動許可から除外し、ownerとは別の実行担当と判定対象の指定だけを許可する境界は、このF02 N=5で成立した。

これはF02 N=5のtargeted結果であり、Standard14全体、追加N、採用、release、projectionを意味しない。

## 状態

`f02_n5_completed / quality_passed / criterion_owner_producer_passed_5_of_5 / mechanism_passed / targeted_passed / token_higher_than_candidate231 / token_higher_than_candidate147 / additional_n_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](670d5536ed5a4baaabbba29d55cc6c0e.json)、個別採点は[品質監査](candidate233-owner-field-exclusion-f02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate233-owner-field-exclusion-f02-n5-mechanism-audit-r1.json)を正本とする。
