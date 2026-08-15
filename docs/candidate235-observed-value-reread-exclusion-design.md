# Candidate235 観測済み値の再read除外設計

## 結論

Candidate235はCandidate147を直接の基準とし、Candidate233で通過した担当起動境界を保持したまま、F02で観測済みの値を行位置特定、狭い再read、同値検索によって取り直す許可だけを閉じる。目的はF02の実行時総使用トークンをC147へ近づけることであり、prompt本文の短文化は行わない。

## 作成前の固定

| 項目 | 固定内容 |
| --- | --- |
| 保存反例 | Candidate233の1 / 5件は、最初の全文readに必要箇所が含まれた後、同じ範囲の`sed`と同じ値の`rg`を追加した |
| 閉じる辺 | 観測済みの値から、正確な行位置、狭いcontext、同値確認を理由に再readまたは検索を発行する許可 |
| 変更 | `EVIDENCE_GATE`で、既存resultに必要値が含まれる場合、所在特定や再確認はmissing observationをbindできず発行不可とする |
| 維持 | Candidate233の担当起動境界、ほか12項目、品質、validation完了待ち |
| 対象外 | 環境起因のnonterminal validation wait、prompt本文の短文化、A02、成功runのtool順 |
| 評価 | F02 N=5。5 / 5 Score `4`、担当名起動0 / 5、観測済み値の再readまたは同値検索0 / 5を必須とする。総使用トークンをC147、Candidate231、Candidate233と比較する |
| 停止 | いずれかの機序または品質に一件でも反例があれば停止する。環境waitは別診断として保持し、prompt成功へ補正しない |

## 境界

- prompt identity: `the-caption-3ce91a4-observed-value-reread-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- Candidate233は保持する機能と反例のsourceでありprompt parentではない

## 現在状態

`design_fixed / candidate_created / f02_n5_completed / quality_passed / mechanism_passed / cost_not_reduced / stopped`

## F02 N=5結果

品質、担当起動、観測済み値の再取得は全5件で通過した。しかし総使用トークン中央値は`171,747`で、Candidate233比`+1.40%`、Candidate231比`+28.50%`、Candidate147比`+33.92%`だった。3 / 5件のnonterminal validation waitが中央値を押し上げており、prompt側の再readを閉じても公式KPIは減らなかったため停止する。
