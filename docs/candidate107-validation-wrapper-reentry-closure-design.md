# Candidate107 validation wrapper再入closure設計

## 結論

Candidate107はCandidate106を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

Candidate106 F03 B20で再発した一件へ合わせ、validation wrapperのouter early yieldを引数条件で閉じる。万一cell ID付きnonterminal resultが返った場合も、次actionを同じcell IDへの`wait`だけに限定する。

## Identityと状態

- candidate number: Candidate107
- prompt identity: `the-caption-3ce91a4-validation-wrapper-reentry-closure-r1`
- direct parent: `the-caption-3ce91a4-compact-validation-terminal-wait-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `72c6f4b8818065300ca24fd0a42bdf49ce834ae44d4f2406da497f98c064c50d`
- evaluation status: `targeted_f03_b20_evaluated / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate106とする。
2. 最短正常経路は、outerを意図的に早期返却させず、validation wrapper内でrequired validationを順に完了し、全result受領後に一度だけ成否を判断する経路とする。
3. 保存済み誤経路はCandidate106 F03 B20のrun `db37cda875434f2abb2bf64d5c20c232`とする。wrapper内でfull validationを開始した後、outerの`yield_time_ms=1000`が先に満了し、cell ID付きnonterminal result後に進捗messageを挟んだ。
4. Candidate106は「意図的な短時間yieldを使わない」「同じsessionのterminalだけを待つ」と述べるが、outer deadlineの許可条件とcell ID返却後の次actionを直接bindしていないため、この経路を1 / 100件で残した。
5. 置換するpredicateは`VALIDATION_PLAN`一つとする。変更軸はvalidation wrapperのnonterminal再入closure一つとする。
6. 消す判断点は、内部waitより短いouter deadlineの選択と、cell ID付きnonterminal result後に`wait`より先にmessage・判断・別toolを選ぶ分岐である。
7. 新たに増える判断点はない。発行時に観測可能なouter / inner deadlineの大小と、resultにcell IDがあるかだけを使う。
8. F03 r2、Rating v14、Medium、N=5で、score `4`、required command evidence、内部waitより短いouter deadline 0、cell ID付きnonterminal resultとterminal result間のmessage 0、required validation再実行 0を確認する。
9. いずれかが5 / 5で成立しなければ停止し、B20、Standard14、採用以降へ進めない。全条件を満たした場合も、低頻度経路の安定性確認は別のF03 B20 gateとする。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限り
toolを追加しない。validation wrapperのouter yield deadlineは未指定にするか、内部required commandの
wait deadline以上にする。cell ID付きnonterminal result後は、terminalまで同じcell IDへのwaitだけを
発行する。commentary / 進捗報告 / 判断 / 別toolを先に発行しない。
```

## 非目標

- TaskSpec、required validation、evaluation set、fixture、ratingの変更
- commandのshell compound化
- tool result配送、output cap、executor hookの変更
- validation以外の長時間command制御
- Candidate106の評価履歴の変更
- 採用、release、THE-CAPTION本体反映

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- Candidate106: 新規実行しない。保存済みB20 traceを作成根拠として使う

## 評価結果

F03 N=5は5 / 5件がscore `4`で、内部waitより短いouter deadline、cell ID付きnonterminal result、途中message、required validation再実行はすべて0 / 5だった。

続くF03 B20は100 / 100件がscore `4`だった。required validation間の途中messageとrequired validation再実行は0 / 100である。cell ID付きnonterminal resultは6件あり、6 / 6件とも直後に同じcell IDへの`wait`を発行した。一方、内部waitより短いouter deadlineが4 / 100件あったため、作成前zero gateは不通過である。

当時の状態を`targeted_f03_b20_evaluated / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`とした。詳細は[`Candidate107 F03 N=5 B20 result`](../evaluations/results/candidate107-validation-wrapper-reentry-closure-v14-medium-f03-continuous-n5-b20-cli0146_2026-07-30.md)を正本とする。このgateから自動的にStandard14、採用、release、runtime projection、本体反映へ進めない。

## 明示再開したStandard14

2026-07-31にユーザーがStandard14 N=5だけを明示的に再開した。C106の保存済み互換resultを参照し、C107の不足70 atomic runだけをM=24のglobal queueで実行した。70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。

C107 minus C106の5 sample中央値差はquality `0.000`、token `-181,469`（`-10.65%`）、elapsed `+74.332`秒（`+8.53%`）だった。方向が分かれたため効率改善は主張しない。F03 B20のouter deadline違反4 / 100件は失効しない。現在状態は`targeted_f03_b20_evaluated / standard14_evaluated_by_explicit_reopen / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`とする。詳細は[`Candidate106 / Candidate107 Standard14 atomic N=5 result`](../evaluations/results/candidate106-candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146_2026-07-31.md)を正本とする。
