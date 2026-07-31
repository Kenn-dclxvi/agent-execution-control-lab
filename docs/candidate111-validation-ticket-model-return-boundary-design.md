# Candidate111 validation実行票model return boundary設計

## 結論

Candidate111はCandidate108を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

制御対象は、途中messageやnonterminal resultの受領後処理ではなく、実行票の発行時点でmodelへ途中resultを返す必要性を選ぶ判断とする。受領resultが未発行invocationのtarget、permission、method、stop conditionを変え得る場合だけmodel returnの必要性が成立する。実行票の継続待機以外の判断を生まない途中状態にはreturnの必要性がない。yield値、tool名、待機時間、executor動作は指定しない。

## Identityと状態

- candidate number: Candidate111
- prompt identity: `the-caption-3ce91a4-validation-ticket-model-return-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- evaluation status: `targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / model_return_gate_failed / result_registered / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。
2. 基準状態の最短正常経路は、`validation_set_ready=true`後に全required validationと完了判定用証拠を一つの実行票として発行し、途中で新しい判断を必要としない限り、実行票全体のresultを一度だけmodelへ返して完了判断する経路とする。
3. 保存済み誤経路はCandidate110 F03 N=5の3件とする。3件とも発行前には全実行票の完了後に判断すると宣言したが、外側へ`1000ms`の早期return条件を選び、3 / 3件がcell ID付きnonterminal resultを返した。その後、同じ実行票を待つためだけにmodelが再入した。
4. Candidate110は受領した途中状態を`DECISION_BOUNDARY`の外へ置いたが、途中状態をmodelへ返す必要性を発行時に判定していない。TaskSpec、repository authority、repository stateも、このmodel判断を固定しない。
5. 置換する一つのpredicateは`VALIDATION_PLAN`である。model returnの必要性を既存`DECISION_BOUNDARY`と同じ直接観測可能な条件へbindする。
6. 消す判断点は、未発行invocationを変えない途中状態を得るためにmodel returnを要求するかどうかという選択である。
7. 新しいlabel、runtime state分類、tool固有parameter、時間閾値、executor分岐、例外は追加しない。executorが独自にnonterminal resultを返した場合のCandidate108の継続規則は維持する。
8. F03 r2、Rating v14、Medium、N=5で、5 / 5 score `4`、required command evidence充足、required validation一回を確認する。mechanism診断では、modelが判断価値のない途中returnを明示的に要求した件数、実際のterminal前model再入、再入後の判断内容、中間messageを分けて記録する。
9. 保存済みCandidate108 F03 N=5との3 KPI比較は、mechanism診断と分けて必ず主結果へ含める。qualityが5 / 5で成立しない場合は停止する。modelが判断価値のない途中returnを一件でも明示的に要求した場合、またはterminal前再入後に実行票の継続待機だけを行うrunが一件でもあれば、KPI差を狙った制御の効果へbindせずStandard14へ進めない。制御成立時もtokenまたはelapsed中央値の一方でも高ければ停止する。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票の処理中にmodelへresultを返す必要性は、受領resultが
未発行invocationのtarget / permission / method / stop conditionを変え得る場合だけ成立する。実行票の
継続待機以外の判断を生まない途中状態にはmodel returnの必要性がない。executorからnonterminal resultが
返った場合は完了判定に使わず、実行票全体がterminalになるまで同じcell IDへwait-onlyで継続する。
実行票完了後はTaskSpec追加要求またはresult失効がない限りtoolを追加しない。
```

## 非目標

- yield値、deadline、tool名、待機時間の指定
- executor、tool result配送、runtime上限の変更
- 中間表示を直接禁止する規則
- TaskSpec、required validation、Evaluation set、fixture、ratingの変更
- commandのshell compound化
- Candidate108からCandidate110までの履歴変更
- 採用、release、THE-CAPTION本体反映

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- reference: Candidate108の保存済みF03 N=5

## 評価結果と現在状態

F03 N=5は5 / 5 score `4`で、required validationも全件一回だった。Candidate108比の中央値はtoken `-1,394`（`-0.99%`）、elapsed `-7.193`秒（`-9.34%`）だった。

一方、modelが外側のreturn horizonを明示したrunは4 / 5件だった。`1000ms`を選んだ2件は2 / 2件がnonterminalとなり、判断を追加せず同じcell IDへwaitするためだけにmodelへ再入した。`30000ms`を選んだ2件はterminal前に時間条件へ到達しなかっただけで、return要求自体は残った。中間messageは0件だった。

狙った制御は成立せず、KPI低下をその効果へbindできない。Standard14は発行せず、現在状態を`targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / model_return_gate_failed / result_registered / stopped`とする。詳細は[`Candidate111 F03 atomic N=5結果`](../evaluations/results/candidate111-validation-ticket-model-return-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)を正本とする。
