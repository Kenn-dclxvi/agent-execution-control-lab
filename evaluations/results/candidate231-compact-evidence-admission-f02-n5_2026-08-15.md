# Candidate231 F02 N=5結果

## 結論

Candidate231は5 / 5件がvalidかつrateableで、5 / 5件がScore `4`だった。token中央値は`133,657`で、Candidate230の`178,886`から`45,229`、`25.28%`減り、Candidate147の`128,236`との差は`+4.23%`まで縮まった。

一方、1件でTaskSpecの判断責任者名`independent contract check`から独立workerを起動した。事前に固定した0 / 5件を満たさないため、コスト差は有効な観測として保存するが、Candidate231を復元差分として採用せず`mechanism_failed / stopped`とする。

## 一次結果

- registered result: `f0ab6a23339b4fb59458da2da7ce0549`
- prompt identity: `the-caption-3ce91a4-compact-evidence-admission-r1`
- bundle SHA-256: `b12b09d692a1ec945ef82593011409e1319272a24ace66b581f8072ea2aef1d7`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- valid / excluded / error: `5 / 0 / 0`
- Score: `4 = 5`
- all-agent token中央値: `133,657`
- elapsed中央値: `79.10220091699739`秒

互換なCandidate147 F02 result `b99e9ed0bc974a75805942f9ad05a8cc`は、token中央値`128,236`、elapsed中央値`100.60693224985152`秒である。Candidate231はtoken `+4.23%`、elapsed `-21.37%`だった。

Candidate230の同じ5件のF02観測はtoken中央値`178,886`、elapsed中央値`104.83013287500944`秒である。Candidate231はtoken `-25.28%`、elapsed `-24.54%`だった。Candidate230は3ケースresultの一部なので、この差は同じF02条件の記述比較として扱う。

## 調査経路

Candidate230では、全文read後に同じ判断の検索または部分readを追加したrunが2 / 5件あった。Candidate231では1 / 5件だった。ほか4件は最初の対象readから追加の変更前検索へ進まなかった。

この簡潔化は調査の往復とtokenを減らす方向へ働いた。ただし、短くなったprompt全体で`OWNER_ROLE`の起動条件が常に維持されたとはいえない。変更したのは`EVIDENCE_GATE`だけであり、担当起動の反例を同じ箇所へ追記して補うことはしない。

## 状態

`f02_n5_completed / quality_passed / token_lower_than_candidate230 / near_candidate147_token / same_decision_additional_investigation_1_of_5 / criterion_owner_producer_failed_1_of_5 / mechanism_failed / stopped / additional_n_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](f0ab6a23339b4fb59458da2da7ce0549.json)、個別採点は[品質監査](candidate231-compact-evidence-admission-f02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate231-compact-evidence-admission-f02-n5-mechanism-audit-r1.json)を正本とする。
