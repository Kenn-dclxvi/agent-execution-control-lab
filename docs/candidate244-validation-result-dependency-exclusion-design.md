# Candidate244 検証途中結果への発行依存の閉鎖

## 結論

Candidate244はCandidate147を直接の基準とし、検証の途中結果を受け取ってから次の必須検証を発行する依存関係を、短い人間語で閉じる。Candidate243は変更対象外の人間語を保持するsourceとしてだけ使い、直接の親にはしない。

置換する境界は次の五文とする。

> 変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。順に行う必須検証は一つの発行対象とし、途中結果を次の発行判断に使わない。ただし各検証は結果を区別できる個別の実行とし、一つのshell commandへ結合してはならない。失敗または利用不能になった検証に依存する後続は発行せず、必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求や結果の失効がなければ、完了後にreadや検証を追加しない。

これは実行するcommandやtoolの順を案内するものではない。途中結果を次の発行許可へ変換できる辺、個別結果を失う結合、失敗した結果に依存する後続の発行許可だけを削除する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate243は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 変更後に必要な検証を一つの発行対象へ固定し、個別結果を保持したまま全結果を受け取り、一度だけ完了を判断する |
| 保存済み問題経路 | Candidate69のStandard14では、必須検証の途中結果ごとにmodelへ戻り、次の検証を別の発行判断から開始する再入が残った。Candidate71は同じTaskSpecとrequired commandを維持し、model stepを539件から408件へ減らした |
| 問題経路の影響 | 途中結果が次の発行判断の前提となり、Standard14 N=5のall-agent token中央値はCandidate69の`2,691,522`に対しCandidate71で`1,923,837`まで減った。command欠落とprotocol違反はCandidate71で0件だった |
| 許していた依存関係 | 一件の検証結果をmodelへ返した後でなければ次の必須検証を発行できない依存関係と、複数結果を一つのshell結果へ潰せる許可 |
| TaskSpec等で防げない理由 | TaskSpecは必須検証、順序、合格条件を定めるが、途中結果を次の発行許可へ使えるか、個別commandを一つのshell commandへ結合できるかまでは制限しない |
| 置換する条件 | Candidate243の`VALIDATION_CLOSURE`全文だけを上記五文へ置換する。`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は変更しない |
| 消える問題経路 | 途中結果を受け取ってから次の必須検証を新たに選ぶ経路、個別結果を一つのshell結果へ結合する経路、失敗結果に依存する後続を発行する経路 |
| 判断順を変えた場合 | 必須検証の順序をどのように解釈しても、途中結果は次の発行判断の入力にできない。個別結果を維持できないshell結合も許可されない |
| 維持する正常経路 | 各検証は別々に実行して個別結果を保持する。失敗時は依存する後続だけを止める。全結果がそろった後に一度だけ完了を判断する |
| 情報の所在と経路 | TaskSpecが必須検証、順序、合格条件、停止条件を持つ。rootまたは指定producerは各個別結果を受け取る。新しいcarrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 新しいlabel、実行手段、worker判断は増やさない。既存の検証対象、依存関係、結果だけから判定する |
| 評価 | F04 N=5。5 / 5件Score `4`、3 required commandの欠落0件、順序違反0件、shell結合0件、途中結果後の再発行判断0件、失敗後の依存検証発行0件を必須とする。all-agent total token中央値を互換なCandidate147と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過してもtoken中央値がCandidate147より増えた場合はF04のコスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-validation-result-dependency-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-unstarted-read-completion-exclusion-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate243と同一byteで保持

## 現在状態

`design_gate_fixed / candidate_created / f04_n5_completed / quality_passed / mechanism_failed_3_of_5 / cost_increased / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
