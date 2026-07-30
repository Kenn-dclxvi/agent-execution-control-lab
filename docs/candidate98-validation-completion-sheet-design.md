# Candidate98 検証実行票の設計

## 結論

Candidate81へ184文字の`VALIDATION_PLAN`一規則だけを追加する。

変更後の検証を始める前に、required validationと、完了判定に必要だと既に分かっているstatus / diff確認を一つの実行票へ固定する。検証結果を受け取るためにmodelへ戻ってからstatus / diffを追加する経路と、同じfull validationを再実行する経路を対象にする。

## Identityと状態

- candidate number: Candidate98
- prompt identity: `the-caption-3ce91a4-validation-completion-sheet-r1`
- direct parent: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- changed target: root `AGENTS.md`
- changed rule: `VALIDATION_PLAN`の追加
- bundle SHA-256: `3f2035cc5ea2de93e196506472f1317130fc16a12c7ad605e162c1cf2b0c6f76`
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前に固定した内容

1. 基準promptはCandidate81とする。
2. 最短正常経路は、変更後にfocused validation、full validation、必要なstatus / diff確認を事前に固定した順序で一度ずつ実行し、全result後に完了を一度判断する経路とする。
3. Candidate81 F02 100件では、84件がfull validation後にstatus / diff確認を別に発行し、5件がfull validationを2回実行した。
4. Candidate81の`VALIDATION_CLOSURE`はrequired validationだけを集合へ固定するため、完了判定用のstatus / diffを検証結果後に追加する経路を禁止しない。
5. 一つの実行票へ事前固定する`VALIDATION_PLAN`だけを追加する。
6. 検証結果後にstatus / diffの要否を再判断する箇所と、完了後にtoolを追加する箇所を消す。
7. 新たに増えるのは、検証開始前に完了判定用証拠を実行票へ含める一つの確認だけである。
8. F02 r1、Rating v14、Mediumで成果品質と実行経路を確認する。
9. 品質、required validation、実行票への事前固定、full validation一回、実行票完了後toolなしのいずれかが成立しなければ停止する。

## 非目標

- 変更前read、command数、message数、token数、推論量の制限
- TaskSpec、required validation、repository authorityの変更
- tool result配送またはexecutorの変更
- Candidate97の改訂または再試験
- 採用、release、本体反映

## 最初の試験

- case: F02 r1
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- 実際の同時実行数: 最大5件。profileの`M`は変更しない
- C81: 新規実行しない

判定条件は次のとおりとする。

- score `4`: 5 / 5
- required command evidence: 5 / 5
- focused / full validation: 各run一回
- status / diff確認: validationと同じtool発行groupへ事前固定
- 実行票完了後の追加tool: 0 / 5

一つでも満たさなければ停止する。全件成立した場合だけ、同じ`M=24`を維持した後続範囲を別途判断する。
