# Candidate232 担当起動条件の簡潔化設計

## 結論

Candidate232はCandidate147を直接の基準とし、Candidate231の短い`EVIDENCE_GATE`を維持したまま、`OWNER_ROLE`だけを短くする。判断責任者名は担当情報でありworker起動の許可ではないことを先頭へ置き、TaskSpecが独立実行を明示した場合だけ起動する境界を復元する。

## 作成前の固定

| 項目 | 固定内容 |
| --- | --- |
| 保存反例 | Candidate231はF02のtokenをCandidate147比`+4.23%`まで戻したが、1 / 5件で`independent contract check`という判断責任者名からworkerを起動した |
| 閉じる辺 | criterion owner名からworker operationを作る許可 |
| 変更 | `OWNER_ROLE`だけを簡潔化し、起動禁止と唯一の起動条件を先頭へ出す |
| 維持 | Candidate231の`EVIDENCE_GATE`、ほか11項目、環境非依存の表現、正常な明示delegationとresult照合 |
| 対象外 | workerを常に禁止しない。成功runの手順、tool、command、repository構造を固定しない |
| 評価 | F02 N=5。5 / 5 Score `4`、判断責任者名によるworker起動0 / 5件を必須とする。tokenをCandidate231の`133,657`とCandidate147の`128,236`へ比較する |
| 停止 | 品質または担当起動に一件でも反例があれば停止する。追加N、採用、release、projectionへ自動的に進まない |

## 境界

- prompt identity: `the-caption-3ce91a4-compact-owner-admission-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- root `AGENTS.md`だけを変更
- Candidate231は人間語と反例のsourceでありprompt parentではない

## 現在状態

`design_fixed / candidate_created / f02_n5_completed / quality_passed / criterion_owner_producer_failed_1_of_5 / mechanism_failed / stopped`

## F02 N=5結果

5 / 5件がvalidかつScore `4`だった。しかし1 / 5件で、TaskSpecが独立したproducer executionを明示していないにもかかわらず、判断責任者名`independent contract check`から`/root/independent_contract_check`を起動した。事前に固定した0 / 5件を満たさないため停止する。

token中央値は`219,027`で、Candidate231比`+63.87%`、Candidate147比`+70.80%`だった。`OWNER_ROLE`を311 bytes短くしても、今回の5件ではtoken削減も担当起動境界も再現しなかった。追加N、採用、release、projectionへ進めない。
