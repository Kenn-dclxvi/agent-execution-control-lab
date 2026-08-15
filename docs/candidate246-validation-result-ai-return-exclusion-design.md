# Candidate246 検証途中結果のAI返却許可の閉鎖

## 結論

Candidate246はCandidate147を直接の基準とし、順に行う必須検証の途中結果をAIへ返してから残りを実行できる許可を閉じる。Candidate243は変更対象外の人間語を保持するsource、Candidate244とCandidate245は抽象的な発行判断または判断側への依存・返却禁止が誤経路を残した反例としてだけ使い、直接の親にはしない。

置換する境界は次の五文とする。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。順に行う必須検証の途中結果をAIへ返してから、残りの検証を実行してはならない。ただし各検証は結果を区別できる個別の実行とし、一つのshell commandへ結合してはならない。失敗または利用不能になった検証に依存する後続は発行せず、必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求や結果の失効がなければ、完了後にreadや検証を追加しない。

これはcommand、toolまたはwrapperの選び方を指定しない。実行途中のresultをAIへ返せるpermissionだけを閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate243は保持する人間語のsource、Candidate244とCandidate245は反例であり、prompt parentではない |
| 基準状態の最短正常経路 | 必須検証の個別結果を実行側で保持し、成功なら残りを続け、失敗なら依存する後続を止め、残りが確定した後にAIへ結果を返す |
| 保存済み問題経路 | Candidate245 F04の4 / 5件で、全検証を事前に決めたと述べながら、各command resultをAIへ返した後に次のcustom tool callを発行した |
| 問題経路の影響 | Candidate245の総使用token中央値は`337,752`でCandidate147比`123.43%`多く、対象機序も4 / 5件で不成立だった |
| 許していた辺 | Candidate245の「判断側」は実行model自身またはcustom tool resultの返却先へ安定して対応づかず、途中result返却後の別発行が文面上残った |
| TaskSpec等で防げない理由 | TaskSpecとcommand evidence protocolは検証対象、順序、個別実行を定めるが、途中resultをAIへ返せる時点を定めない |
| 置換する条件 | Candidate243の`VALIDATION_CLOSURE`全文だけを上記五文へ置換する。Candidate245の第二文は保持しない。`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は変更しない |
| 消える問題経路 | 成功した途中resultをAIへ返した後に、残りを別のcustom tool callから発行する経路 |
| 判断順を変えた場合 | 後続を事前に決定済みとしても、途中resultをAIへ返した時点で残りを実行する経路が禁止される |
| 維持する正常経路 | 各検証の個別結果、指定順、失敗時の依存後続停止、shell結合禁止、全結果後の一回の完了判断を維持する |
| 情報の所在と経路 | TaskSpecが検証、順序、合格条件、停止条件を持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | AIという既存の依頼実行主体を返却先として明示するだけで、新しい判断、参照、実行手段は増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、required command欠落0件、順序違反0件、shell結合0件、途中resultをAIへ返してから次を別発行したrun 0件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過しても総使用token中央値がCandidate147より多ければコスト差を未解消として停止する。この一文でも機序を通過しなければ、同じ境界の環境非依存な自然文への言い換えを打ち切り、C147の技術的な返却境界を保持する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- counterexample only: Candidate244、Candidate245
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate243と同一byteで保持

## 現在状態

`design_gate_fixed / candidate_created / f04_n5_completed / quality_passed / mechanism_passed_5_of_5 / targeted_passed / cost_not_reduced / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
