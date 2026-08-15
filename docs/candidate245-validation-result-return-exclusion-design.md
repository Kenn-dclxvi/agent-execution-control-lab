# Candidate245 検証途中結果の返却許可の閉鎖

## 結論

Candidate245はCandidate147を直接の基準とし、順に行う必須検証の途中結果を、残りの検証が未確定のまま判断側へ返せる許可を閉じる。Candidate243は変更対象外の人間語を保持するsource、Candidate244は途中結果を別発行の条件にしないだけでは返却自体を3 / 5件で止められなかった反例としてだけ使い、どちらも直接の親にはしない。

置換する境界は次の五文とする。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。順に行う必須検証の途中結果は、残りがすべて実行済みになるか、その結果によって後続の実行が禁止されるまで、判断側へ返してはならない。ただし各検証は結果を区別できる個別の実行とし、一つのshell commandへ結合してはならない。失敗または利用不能になった検証に依存する後続は発行せず、必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求や結果の失効がなければ、完了後にreadや検証を追加しない。

これはcommand、toolまたはwrapperの選び方を指定しない。途中結果を返せる時点だけを制限し、成功した途中結果を判断側へ返してから残りを別に発行できる経路を消す。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate243は保持する人間語のsource、Candidate244は反例であり、prompt parentではない |
| 基準状態の最短正常経路 | 変更後に必要な検証を一つの実行境界へ入れ、各結果を区別したまま、成功なら残りを続け、失敗なら依存する後続を止め、返却後に一度だけ完了を判断する |
| 保存済み問題経路 | Candidate244 F04の3 / 5件で、`npm ci`、`npm run lint`、`npm run build`が別々の発行となり、各途中結果が判断側へ返ってから次が発行された |
| 問題経路の影響 | Candidate244の総使用token中央値は`281,762`でCandidate147の`151,170`より`86.39%`多く、対象機序も3 / 5件で不成立だった |
| 許していた辺 | Candidate244は途中結果を「次の発行判断に使う」ことを禁じたが、後続を既に決めたものとして途中結果を判断側へ返す許可を閉じなかった |
| TaskSpec等で防げない理由 | TaskSpecとcommand evidence protocolは検証対象、順序、個別実行を定めるが、成功した途中結果を残りの検証前に判断側へ返せる時点を定めない |
| 置換する条件 | Candidate243の`VALIDATION_CLOSURE`全文だけを上記五文へ置換する。Candidate244の第二文は保持しない。`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は変更しない |
| 消える問題経路 | 成功した途中結果を、残りの検証が未実行の状態で判断側へ返し、その後に残りを別発行する経路 |
| 判断順を変えた場合 | 後続を事前に決定済みと解釈しても、返却可能時点は変わらず、残りが実行済みまたは失敗により発行禁止になる前には返せない |
| 維持する正常経路 | 各検証の個別結果、指定順、失敗時の依存後続停止、shell結合禁止、全結果後の一回の完了判断を維持する |
| 情報の所在と経路 | TaskSpecが検証、順序、合格条件、停止条件を持つ。実行主体は各結果を保持し、返却可能条件を満たした後に判断側へ返す。新しいcarrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 新しいrepository read、label、worker判断、実行手段は増やさない。返却可能時点だけを既存の実行済み状態または停止条件へ対応づける |
| 評価 | F04 N=5。5 / 5件Score `4`、required command欠落0件、順序違反0件、shell結合0件、途中結果を判断側へ返してから次を別発行したrun 0件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過しても総使用token中央値がCandidate147より多ければ、F04のコスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-validation-result-return-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- counterexample only: `the-caption-3ce91a4-validation-result-dependency-exclusion-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate243と同一byteで保持

## 現在状態

`design_gate_fixed / candidate_created / f04_n5_completed / quality_passed / mechanism_failed_4_of_5 / cost_increased / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
