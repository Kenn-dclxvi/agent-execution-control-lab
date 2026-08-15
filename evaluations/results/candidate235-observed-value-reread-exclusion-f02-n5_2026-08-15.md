# Candidate235 F02 N=5結果

## 結論

Candidate235は5 / 5件がvalidかつScore `4`で、担当名からのworker起動と観測済み値の再read・同値検索はいずれも0 / 5件だった。しかし実行時総使用トークン中央値は`171,747`で、Candidate233の`169,370`より`1.40%`、Candidate231の`133,657`より`28.50%`、Candidate147の`128,236`より`33.92%`大きかった。

3 / 5件では必須full validationがnonterminalになり、同じ処理への`wait`でmodel turnが一回または二回増えた。waitなし2件は`134,702`と`135,181`だったが、環境差でKPIを補正せず、登録中央値`171,747`を正式値とする。

## 一次結果

- result: `c719ce57a9874c37953001d0a05d1deb`
- prompt: `the-caption-3ce91a4-observed-value-reread-exclusion-r1`
- compatibility key: `b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b`
- Score: `4 = 5`
- token中央値: `171,747`
- elapsed中央値: `81.7338061669725`秒

prompt側の余分な再調査は閉じたが、総使用トークン削減は成立しなかった。合法なvalidation完了待ちを禁止したり、runtimeのyieldをCandidate解決策として変更したりせず、`mechanism_passed / cost_not_reduced / stopped`とする。

一次値は[登録result](c719ce57a9874c37953001d0a05d1deb.json)、[品質監査](candidate235-observed-value-reread-exclusion-f02-n5-quality-audit-r1.json)、[機序監査](candidate235-observed-value-reread-exclusion-f02-n5-mechanism-audit-r1.json)を正本とする。
