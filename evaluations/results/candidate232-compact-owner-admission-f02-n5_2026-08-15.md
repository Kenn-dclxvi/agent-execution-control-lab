# Candidate232 F02 N=5結果

## 結論

Candidate232は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。一方、1件でTaskSpecの判断責任者名`independent contract check`から独立workerを起動した。事前に固定した0 / 5件を満たさないため、`mechanism_failed / stopped`とする。

token中央値は`219,027`で、Candidate231の`133,657`より`85,370`、`63.87%`大きく、Candidate147の`128,236`より`90,791`、`70.80%`大きかった。`OWNER_ROLE`を短くしたことは、今回の5件では機序成立にもtoken削減にもつながらなかった。

## 一次結果

- registered result: `5da23b15726c4069826e65c2895ba431`
- prompt identity: `the-caption-3ce91a4-compact-owner-admission-r1`
- bundle SHA-256: `561983cde70b6eea16fbb334692e4d00e9c058467ae21b2731a4bde68bc4eb7e`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `219,027`
- elapsed中央値: `101.77152708300855`秒

互換なCandidate147 F02 result `b99e9ed0bc974a75805942f9ad05a8cc`は、token中央値`128,236`、elapsed中央値`100.60693224985152`秒である。Candidate232はtoken `+70.80%`、elapsed `+1.16%`だった。

Candidate231の同じF02 N=5 result `f0ab6a23339b4fb59458da2da7ce0549`は、token中央値`133,657`、elapsed中央値`79.10220091699739`秒である。Candidate232はtoken `+63.87%`、elapsed `+28.66%`だった。

## 担当起動境界

iteration 1のrun `6abca8eb9ab84009a62ff16be9bdc048`は、TaskSpecが独立したproducer executionを明示していないのに、判断責任者名を`independent_contract_check`というproducerへ読み替え、`/root/independent_contract_check`を起動した。ほか4件は独立workerを起動せず、rootが判定した。

Candidate231と同じ1 / 5件の反例が残ったため、短い`OWNER_ROLE`はこの許可辺を閉じたとはいえない。成功した4件の処理順を追加規則へ転記せず、反例として保存する。

## 登録補足

最初のselection登録 `cb9903586d8041ad9ff67489eddc6902`はreference result引数がなく、F02だけのfixture mapを持つsubset compatibilityになった。削除または上書きせず外部registryへ残し、C147比較にはreference resultへ明示的にbindした`5da23b15726c4069826e65c2895ba431`だけを使用する。

## 状態

`f02_n5_completed / quality_passed / criterion_owner_producer_failed_1_of_5 / token_higher_than_candidate231 / token_higher_than_candidate147 / mechanism_failed / stopped / additional_n_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](5da23b15726c4069826e65c2895ba431.json)、個別採点は[品質監査](candidate232-compact-owner-admission-f02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate232-compact-owner-admission-f02-n5-mechanism-audit-r1.json)を正本とする。
