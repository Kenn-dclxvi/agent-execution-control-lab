# Candidate110 validation実行票decision boundary設計

## 結論

Candidate110はCandidate108を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

validation実行票の途中状態を既存`DECISION_BOUNDARY`の定義へ接続する。途中状態は未発行invocationの選択を変えるresultではなく、実行票全体のterminal resultだけが次の判断境界を開くものとする。yield値、tool名、待機方法、executor動作は指定しない。

## Identityと状態

- candidate number: Candidate110
- prompt identity: `the-caption-3ce91a4-validation-ticket-decision-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `b9e1140ebdfb79d66c04dd47f478f85ec985122de104f0b08eef25d03fa5cdbe`
- evaluation status: `targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / control_not_demonstrated / result_registered / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。
2. 基準状態の最短正常経路は、`validation_set_ready=true`後に全required validationと完了判定用証拠を一つの実行票として発行し、実行票全体のterminal resultを一度だけ受領して完了判断する経路とする。
3. 保存済み誤経路はCandidate108 Standard14 N=5とする。command protocol対象35件中12件がouter yield `1000ms`を選び、12 / 12件がcell ID付きnonterminal resultを返した。全70 runの`wait`はCandidate107の3回から23回へ増えた。
4. Candidate108はnonterminal resultを完了判定へ使わずwait-onlyで継続するため、terminal前の誤判断、途中message、validation再実行を防ぐ。一方、実行票の途中状態が`DECISION_BOUNDARY`を開くresultかどうかを定義していないため、結果を変えない途中状態を要求してmodelへ再入する選択を残す。TaskSpec、repository authority、repository stateはこのmodel判断を固定しない。
5. 置換する一つのpredicateは`VALIDATION_PLAN`である。実行票の途中状態を`decision_boundary=false`、実行票全体のterminal resultを次の判断入力としてbindする。
6. 消す判断点は、実行票の途中状態を受け取るためにterminal前のmodel判断境界を開くかどうかという選択である。
7. 新しいlabel、runtime state分類、tool固有parameter、例外は追加しない。既存`DECISION_BOUNDARY`の発火条件へvalidation実行票の途中状態を対応付けるだけとする。
8. F03 r2、Rating v14、Medium、N=5で5 / 5 score `4`、required command evidence充足、required validation一回、validation実行票のterminal前model再入0、途中message0を確認する。
9. qualityまたはmechanism条件が5 / 5で成立しなければ停止する。成立時だけ保存済みCandidate108 F03 N=5と比較する。Candidate110のtokenまたはelapsed中央値の一方でも高ければStandard14へ進めず停止する。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限り
toolを追加しない。実行票の途中状態は未発行invocationのtarget / permission / method / stop conditionを
変えないため`DECISION_BOUNDARY`を開かず、実行票全体のterminal resultだけを次の判断へ渡す。
```

## 非目標

- yield値、deadline、tool名、待機方法の指定
- executor、tool result配送、runtime上限の変更
- TaskSpec、required validation、Evaluation set、fixture、ratingの変更
- commandのshell compound化
- Candidate108またはCandidate109の履歴変更
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

F03 N=5は5 / 5 score `4`で、required validationも全件一回だった。一方、実行票全体のterminal前にmodelへ戻らなかったrunは2 / 5件だけだった。残る3件はouter yield `1000ms`を選び、3 / 3件がcell ID付きnonterminal resultを返した。うち2件はwaitより先に進捗messageを出した。

当初の作成前gateではmechanism不通過を理由にKPI比較前で停止した。ユーザー訂正により、prompt制御は手段、3 KPI改善が目的であり、mechanismは原因診断であって主結果ではないと判定した。

保存済みCandidate108 F03 N=5との比較ではquality同値、token中央値`-1,844`（`-1.31%`）、elapsed中央値`-5.384`秒（`-6.99%`）だった。これによりKPIを含めずmechanismだけで結果を閉じた当初判定は訂正する。

一方、狙った制御は2 / 5件でしか成立していない。targeted KPI低下をこの制御の効果とbindできないため、ユーザー判断によりStandard14へ拡大せず停止する。Standard14用preflightは残り65 slotをreadyにしたが、評価slotは0件であり、campaignと未実行profileを撤回した。

詳細は[`Candidate110 F03 atomic N=5結果`](../evaluations/results/candidate110-validation-ticket-decision-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)を正本とする。現在状態は`targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / control_not_demonstrated / result_registered / stopped`である。
