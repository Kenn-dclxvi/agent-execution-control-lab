# Candidate239 結果依存境界一文設計

## 結論

Candidate239はCandidate147を直接の基準とし、Candidate237で成立した人間語とF02の境界を保持したまま、結果の影響範囲を利用者が示した一文だけで表す。Candidate228とCandidate238は保存反例として使い、prompt本文や評価状態を継承しない。

> 影響しない結果から、待機や停止への依存関係を作らない。

成功runのtool順、同じmodel step、未発行状態、先行条件または次の判断を指示する補足は加えない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate237は保持する人間語と成立済みF02境界のsourceであり、直接基準ではない |
| 基準状態の最短正常経路 | 結果の影響を、その結果によって対象、permission、method、stop conditionが変わり得る作業だけへ限定し、無関係な作業へ待機や停止を伝播させない |
| 保存済み問題経路 | Candidate228 A02の5 / 5件とCandidate238 A02の5 / 5件で、開始状態の結果がreadへ影響しないのに、その結果を受け取ってからreadを別発行した |
| TaskSpec等で防げない理由 | A02のTaskSpecはdrift時にartifact変更とrequired commandを止めるがreadを禁止しない。readの対象とpermissionも開始結果では変わらないが、逐次発行は品質を損なわず実行できる |
| 変更条件 | Candidate237の`DECISION_BOUNDARY`にある共同発行の動作説明を削除し、利用者指定の一文だけで待機・停止の依存関係を制限する |
| 消えることを期待する経路 | 影響しない開始状態の結果からreadへの待機依存を作り、結果受領後にreadを別発行する経路 |
| 維持する正常経路 | drift時に禁止されるartifact変更とrequired commandの停止、結果影響範囲の局所化、Candidate237で成立したF02境界 |
| 新しい判断・参照・例外 | なし。補足説明、手順、tool順、model step、未発行状態、先行条件を追加しない |
| 評価 | A02 N=5。5 / 5件Score `4`、影響しない開始結果を受領した後までreadを未発行にしたrun 0 / 5件を必須とする。all-agent total token中央値をCandidate147、Candidate228、Candidate238と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。通過してもtoken中央値がCandidate147より増えた場合はA02のコスト差を未解消として止める |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-plain-result-dependency-boundary-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate237と同一byteで保持

## 評価結果

A02 N=5は5 / 5件がScore `4`だったが、開始状態の結果を待ってから影響しないreadを別発行した経路が5 / 5件に残った。一文だけでは対象機序を再現できず、停止条件に達した。token中央値は`160,959`で、Candidate238比`-12.29%`、Candidate147比`+24.69%`だった。

## 現在状態

`a02_n5_completed / quality_passed / result_dependency_boundary_failed_5_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
