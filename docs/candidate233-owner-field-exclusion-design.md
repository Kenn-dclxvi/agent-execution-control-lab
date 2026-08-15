# Candidate233 判断責任者欄の起動許可除外設計

## 結論

Candidate233はCandidate147を直接の基準とし、Candidate231の短い`EVIDENCE_GATE`を維持したまま、`OWNER_ROLE`で判断責任者欄と独立実行の明示を排他的に分ける。判断責任者名に`independent`、`check`、`reviewer`などが含まれていてもworker起動の許可にはならず、ownerとは別に実行担当と判定対象が指定された場合だけ起動できるようにする。

## 作成前の固定

| 項目 | 固定内容 |
| --- | --- |
| 直接基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保存反例 | Candidate231とCandidate232は各1 / 5件で、判断責任者名`independent contract check`を独立producer executionの明示と読み替えた |
| 閉じる辺 | `criterion owner`欄の値や役割名からworker operationを作る許可 |
| 変更 | `OWNER_ROLE`で、owner欄、名称、独立判定の必要性を実行明示の根拠から除外し、ownerとは別の実行担当と判定対象の指定だけを起動条件にする |
| 維持 | Candidate231の`EVIDENCE_GATE`、ほか11項目、環境非依存の表現、正当に明示された分担resultの照合 |
| 対象外 | workerを常に禁止しない。成功runの手順、tool、command、repository構造を固定しない。Candidate232の短い`OWNER_ROLE`を親として継承しない |
| 評価 | F02 N=5。5 / 5 Score `4`、判断責任者名によるworker起動0 / 5件を必須とする。tokenをCandidate231の`133,657`とCandidate147の`128,236`へ比較する |
| 停止 | 品質または担当起動に一件でも反例があれば停止する。追加N、採用、release、projectionへ自動的に進まない |

## 境界

- prompt identity: `the-caption-3ce91a4-owner-field-exclusion-r1`
- root `AGENTS.md`だけを変更
- Candidate231は低tokenの人間語と保持する`EVIDENCE_GATE`のsource、Candidate232は反例であり、どちらもprompt parentではない

## 現在状態

`design_fixed / candidate_created / f02_n5_completed / quality_passed / owner_gate_passed / targeted_passed / additional_n_not_started`

## F02 N=5結果

5 / 5件がvalidかつScore `4`で、判断責任者名から独立workerを起動したrunは0 / 5件だった。Candidate231とCandidate232で残った許可辺は、この範囲では閉じた。

token中央値は`169,370`で、Candidate231比`+26.72%`、Candidate147比`+32.08%`だった。elapsed中央値は`79.6329457089887`秒で、Candidate231比`+0.67%`、Candidate147比`-20.85%`だった。機序は通過したが、C147に近いtokenという点ではCandidate231より後退した。追加N、採用、release、projectionへ自動的に進めない。
