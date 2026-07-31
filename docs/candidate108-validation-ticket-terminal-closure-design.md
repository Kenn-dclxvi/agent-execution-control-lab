# Candidate108 validation実行票terminal closure設計

## 結論

Candidate108はCandidate107を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

Candidate107で成立したcell ID付きnonterminal result後のwait-only遷移は維持する。実行票全体の完了を保証できないouter / inner deadlineの大小比較を削除し、nonterminal resultを完了判定に使わないterminal状態遷移へ一本化する。

## Identityと状態

- candidate number: Candidate108
- prompt identity: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-wrapper-reentry-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `f0d2f7ad6c69fd471509ca429d7d0f22b7120d43a2394298228ef7b453b72495`
- evaluation status: `targeted_f03_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate107とする。
2. 最短正常経路は、validation wrapperがterminal resultを返し、全result受領後に一度だけ完了を判断する経路とする。
3. 保存済み診断はCandidate107 F03 B20とする。outer deadline未指定でも4 / 100件がcell ID付きnonterminal resultを返し、outerと個別inner waitを同値にしても複数commandの累積時間によるnonterminal返却を防げないことを確認した。
4. Candidate107のdeadline大小比較は実行票全体のterminalを保証しない。一方、同じ保存traceでnonterminal後のwait-only遷移は6 / 6件成立し、途中messageとrequired validation再実行は0 / 100件だった。
5. 置換するpredicateは`VALIDATION_PLAN`一つとする。変更軸はdeadline計算からterminal状態遷移への一本化とする。
6. 消す判断点は、outer deadlineが各inner wait以上かを比較する分岐である。
7. 新たに増える判断点はない。resultにcell IDがあるか、実行票全体がterminalかだけを使う。
8. F03 r2、Rating v14、Medium、N=5で、score `4`、required command evidence、cell ID付きnonterminal result後の同一cell ID wait-only、途中message 0、required validation再実行 0を確認する。
9. qualityまたはmechanism条件が5 / 5で成立しなければ停止する。全条件を満たしても、B20、Standard14、採用、release、runtime projection、本体反映は別gateとする。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限り
toolを追加しない。validation wrapperがcell ID付きnonterminal resultを返した場合、その返却を実行票の
完了判定へ使わず、実行票全体がterminalになるまで同じcell IDへのwaitだけを発行する。
commentary / 進捗報告 / 判断 / 別toolを先に発行しない。
```

## 非目標

- outer early yield自体の禁止
- executorのdeadline動作の変更
- TaskSpec、required validation、evaluation set、fixture、ratingの変更
- commandのshell compound化
- validation以外の長時間command制御
- Candidate107の評価履歴の変更
- 採用、release、THE-CAPTION本体反映

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- Candidate107: 新規実行しない。保存済みF03 B20 traceを作成根拠とmechanism基準に使う

## 評価結果

F03 N=5は5 / 5件がscore `4`だった。cell ID付きnonterminal result後の同一cell ID wait-onlyは3 / 3件、途中messageとrequired validation再実行は0件で、最初のquality・mechanism gateを通過した。

標準14 N=5はF03の保存済み5 runを再利用し、残る13 case × 5 = 65 runだけを新規実行した。最終selectionは70 / 70件がscore `4`だった。Candidate107比の中央値はtoken `+15.75%`、elapsed `+3.69%`である。詳細は[`評価result`](../evaluations/results/candidate107-candidate108-validation-ticket-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)を正本とする。

現在状態は`targeted_f03_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / adoption_not_decided`である。release、runtime projection、本体反映は行っていない。
