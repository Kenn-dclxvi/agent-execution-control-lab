# Candidate230 別AI平易日本語翻訳設計

## 結論

Candidate230はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基準とし、利用者が提示した別AIによる平易な日本語訳をroot `AGENTS.md`へ置く。Candidate227からCandidate229までは親にせず、同じ対象ケースで残った失敗経路と比較値だけを使う。

提示文のうち「以下は、rootのAGENTS.mdを」という回答上の前置きはprompt instructionではないため除外し、「前提となる用語」から13項目の末尾までを本文として固定する。本文の表現は評価結果を見る前に変更しない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準promptと正常経路 | Candidate147。13項目で成果値、実行担当、完了、context、証拠、owner、root、独立判定、結果影響、検証、方法、回復を制御する |
| 保存済みの問題経路 | Candidate228はA02待機依存5 / 5件、判断責任者からの担当起動0 / 10件。Candidate229はA02待機依存4 / 5件。いずれも一般化した人間語でC147の発行境界を完全には維持できなかった |
| 問題を許した辺 | こちらで作った翻訳は、C147の`同一model step`と開始identityの局所規則を一般的な待機禁止へ置き換えた。提示された翻訳は「相互非依存invocationは分割しない」「同じmodel stepで発行する」「owner名だけでproducerを選ばない」を残している |
| 変更する条件 | C147の13項目を、提示された用語説明と平易な日本語本文へ全置換する。C147の状態名、対応関係、発行境界、検証閉包は削除せず説明を展開する |
| 実行不能にする経路 | 開始identity結果に影響されないreadを別判断へ分ける経路。criterion ownerの記載だけから独立producerを起動する経路 |
| 維持する正常経路 | drift時に禁止される変更と必須commandだけを待たせ、許可済みreadは止めない。TaskSpecが独立producerを明示した場合だけ起動し、本人の結果を受け取る。ほか11項目もC147との対応を維持する |
| 増える判断と対象外影響 | 新しい制御機能は増やさない。用語説明と展開文によるprompt長増加はtokenとelapsedで観測する。前置き以外の提示文は編集しない |
| 評価 | まずCandidate228と同じA02・F02・F03各N=5、合計15件を評価する。品質15 / 15 Score `4`、A02待機依存0 / 5件、責任者名からの独立担当起動0 / 10件を必須とする。通過した場合だけCandidate147と互換なStandard14各N=5へ進む |
| 仕上げやすさの比較 | 同じ3ケースで、残る失敗機能数、失敗run数、品質、token、elapsedをCandidate228と比較する。失敗機能が少ない方を、現時点で仕上げやすい翻訳とする。同数なら失敗run数、次に品質、最後にtokenとelapsedを記述比較する |
| 停止条件 | targeted 15件で品質または二つの機序に一件でも反例があれば、Standard14、追加N、採用、release、projectionへ進まない。通過後のStandard14でも品質または既知機序の反例一件で停止する |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-reader-ai-plain-japanese-translation-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの17 targetをCandidate147と同一byteで保持
- 提示文source: `/Users/kenn/.codex/attachments/5bb4f7e4-64f2-4804-9fe5-6919e45437ba/pasted-text.txt`
- Candidate227〜Candidate229: 反例と比較対象のみ。prompt本文、bundle identity、評価状態を親として継承しない

## 評価結果

対象15件はすべてvalidかつrateableで、15 / 15件がScore `4`だった。判断責任者名による独立producer起動は0 / 10件だった。A02の不要な待機依存はCandidate228の5 / 5件から2 / 5件へ減ったが、固定した0 / 5件には届かなかった。

同じ3ケースで残る失敗機能数はCandidate228と同じ1機能、失敗run数は5件から2件へ減った。このため、事前に固定した順序ではCandidate230の方が仕上げやすい。停止条件に従い、Standard14は開始しない。

## 現在状態

`targeted_n5_completed / quality_passed / criterion_owner_producer_gate_passed_10_of_10 / result_effect_scope_failed_2_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided`
