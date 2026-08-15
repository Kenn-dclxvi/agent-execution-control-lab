# Candidate236 TaskSpec出力境界 F02 N=5結果

## 結論

Candidate236はF02を5 / 5 valid、5 / 5 Score `4`で完了した。対象としたTaskSpec内部値の項目別進捗出力は0 / 5件、判断責任者名からのworker起動も0 / 5件だった。一方、1 / 5件で最初の全文read後に同じ値と行位置を`rg -n -C 10`で再取得し、維持条件を失ったため`mechanism_failed / stopped`とする。

## 一次値

- result: `cfc9678fda814da3a6f8eea818cb4335`
- valid / rateable: `5 / 5`
- quality: Score `4 = 5`
- all-agent total token中央値: `180,024`
- elapsed中央値: `88.17263808398275`秒
- Candidate147比: token `+40.38%`、elapsed `-12.36%`
- Candidate231比: token `+34.69%`
- Candidate233比: token `+6.29%`
- Candidate235比: token `+4.82%`

一次の数値は[登録result](cfc9678fda814da3a6f8eea818cb4335.json)、個別採点は[品質監査](candidate236-taskspec-output-boundary-f02-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate236-taskspec-output-boundary-f02-n5-mechanism-audit-r1.json)を正本とする。

## 機序

- TaskSpec内部値の項目別進捗出力: `0 / 5`件
- 判断責任者名からのworker起動: `0 / 5`件
- 観測済み値の再readまたは同値検索: `1 / 5`件
- nonterminal validation wait: `3 / 5`件
- waitなし実行のtotal token: `136,196`、`180,024`

対象の出力境界は成立したが、Candidate235で成立していた観測済み値の再取得境界を維持できなかった。成功runのtool構成を指示へ転記せず、追加N、採用、release、projectionへ進めない。

## 登録上の注記

最初のresult登録はregistryへの書き込み後、cycle receiptの保存だけに失敗した。同じ固定selectionをreceipt付きで再登録した`cfc9678fda814da3a6f8eea818cb4335`を本記録の正本とする。先に作られた`386a952204ca48baafb9b2ff8a4844d0`は同じselectionと一次値を持つ非採用の重複登録としてregistryに残し、このリポジトリのresult索引へは採用しない。

## 状態

`f02_n5_completed / quality_passed / taskspec_output_gate_passed / criterion_owner_gate_passed / observed_value_reread_failed_1_of_5 / mechanism_failed / token_higher_than_candidate235 / stopped / additional_n_not_started / adoption_not_decided / release_not_created / projection_not_performed`
