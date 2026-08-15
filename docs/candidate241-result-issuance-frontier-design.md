# Candidate241 結果を受け取る前の着手範囲の固定

## 結論

Candidate241はCandidate147を直接の基準とし、結果を受け取る前に、すでに許可されていてその結果の影響を受けない作業の着手範囲を閉じる。Candidate237は変更対象外の人間語を保持するsource、Candidate240は開始確認だけを先に選べる経路を5 / 5件残した反例としてだけ使い、いずれも直接の親にはしない。

置換する境界は次の五文とする。

> 結果を返す作業を始める時点で、すでに許可され、その結果によって対象、許可、方法、停止条件が変わらない作業を、未着手のまま残してはならない。該当する作業すべてに着手するまでは、返った結果を次の作業の選択や停止に使ってはならない。
>
> 開始状態の確認によって読み取りが禁止されず、その対象や許可も変わらない場合は、確認を始める時点で、許可済みの読み取りを未着手のまま残してはならない。確認結果によって読み取り自体が禁止されるか、その対象または許可が変わり得る場合だけ、読み取りを確認後へ分ける。変更や必須実行が確認結果によって禁止され得る場合は、その結果が返るまで始めない。

これは成功runの実行順を手順として転記するものではない。先に開始確認だけを選び、結果を受け取った後で初めて影響しない読み取りを次の作業として選べる依存関係を閉じる。実行手段や一回の応答内での処理方法は指定せず、結果を判断へ使える時点と、その時点までに着手済みでなければならない範囲だけを固定する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate237は保持する本文のsource、Candidate240は反例であり、直接の親ではない |
| 基準状態の最短正常経路 | 結果を返す確認を始める時点で、すでに許可され、その結果で対象、許可、方法、停止条件が変わらない作業へすべて着手する。これらへ着手する前に返った結果を次の選択や停止へ使わず、結果によって禁止され得る変更や必須実行だけを保留する |
| 保存済み問題経路 | Candidate240 A02の5 / 5件で、モデルは開始状態の確認だけを先に発行して結果を受け取り、その後に`run.sh`の読み取りを別の作業として選んだ |
| 問題経路の影響 | 開始確認の結果を受け取るまで許可済みreadが未着手となり、結果待ちに依存しないreadとの間に往復が一段増えた。Candidate240のtoken中央値はC147比`+49.84%`だった |
| 許していた依存関係 | Candidate240は影響しない作業の保留を禁じたが、どの作業が保留対象になるかを結果受領前に閉じなかった。このため、開始確認だけを先に選び、結果受領後にreadを新たに選ぶ経路は文面に違反しなかった |
| TaskSpec等で防げない理由 | A02のTaskSpecはdrift時にartifact変更とrequired commandを禁止するがreadを禁止しない。readの対象とpermissionも開始結果では変わらないが、TaskSpecとrepository authorityだけでは結果受領前に着手対象を確定する義務を作らない |
| 置換する条件 | Candidate237の`DECISION_BOUNDARY`にある環境依存の共同発行説明を、上記五文の結果受領前の着手範囲、結果利用禁止、開始確認のread境界、read分離例外、影響を受ける作業の保留へ置換する |
| 消える問題経路 | 開始確認だけを先に選んでresultを受け取り、その後で初めて許可済みreadを選ぶ経路。影響しない許可済み作業を未着手にしたまま、一部resultを残りの作業の選択や停止へ使う経路 |
| 判断順を変えた場合 | 先に開始確認だけを選んでも、その確認を始める時点で影響しない許可済み作業を未着手にできない。返った結果を先に見ても、該当作業すべてへ着手するまで次の選択や停止へ使えないため、同じ問題経路は成立しない |
| 維持する正常経路 | 確認結果がread自体を禁止する場合、またはread対象・permissionを変え得る場合はreadを確認後へ分ける。確認結果によって禁止され得るartifact変更とrequired commandは結果受領まで始めない。Candidate237のF02境界と他の12制御群は維持する |
| 情報の所在と経路 | TaskSpecが開始確認の停止条件と許可済みreadを持ち、repository authorityがread対象を定める。rootは両方を既存入力として使い、開始確認とreadの結果を直接受け取る。新しいcarrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 新しいlabel、実行手段、runtime、worker判断は増やさない。新しい判断は結果を返す作業の開始時点で既に許可済みの作業を列挙する一回だけ。例外はC147と同じく、結果がread禁止、read対象またはpermissionを変え得る場合だけ |
| 評価 | A02 N=5。5 / 5件Score `4`、最初の開始確認resultを受領または判断へ使用する前に`run.sh`の許可済みreadへ着手したrun 5 / 5件、resultを使って残る許可済みreadを新たに選んだrun 0 / 5件を必須とする。all-agent total token中央値を互換なCandidate147、Candidate239、Candidate240と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過してもtoken中央値がCandidate147より増えた場合はA02のコスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-result-issuance-frontier-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- counterexample: `the-caption-3ce91a4-portable-result-wait-closure-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate237と同一byteで保持

## 現在状態

`a02_n5_completed / quality_passed / issuance_frontier_passed_2_of_5 / delayed_selection_failed_3_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 評価結果

A02 N=5は5 / 5件がScore `4`だった。結果を次の判断へ使う前に許可済みreadへ着手したrunは2 / 5件まで増えたが、3 / 5件では開始確認のresultを説明へ使った後にreadを選ぶ経路が残った。token中央値は`162,000`でCandidate147比`+25.50%`だったため、事前gateに従い停止した。
