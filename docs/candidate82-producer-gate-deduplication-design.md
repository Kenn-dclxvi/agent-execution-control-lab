# Candidate82: producer gate重複削除

## 結論

Candidate82は、投影済みCandidate81を直接親とし、root `AGENTS.md`の`PRODUCER`からP3一文だけを削除する。明示producer gateの正本は`OWNER_ROLE`へ逐語維持し、委譲可否、producer binding、worker起動、result bindingを変更しない。

このCandidateが消すのは、`PRODUCER`の短いgateと`OWNER_ROLE`の完全なgateの語差を照合する判断だけである。prompt byte削減自体を改善根拠にせず、D01の明示委譲経路とF10 Monthlyのroot-only経路を同じrating v13、Medium、各`N=5`で確認する。

## Identity

| 項目 | Candidate81 | Candidate82 |
| --- | --- | --- |
| prompt identity | `the-caption-3ce91a4-validation-wrapper-precedence-r1` | `the-caption-3ce91a4-producer-gate-deduplication-r1` |
| bundle SHA-256 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` | `a5a8dad8d615f4075bd399938bd621f9906d9b71c9de59425815be63027201cd` |
| full bundle target | 19 path | 19 path |
| changed target | — | root `AGENTS.md`のみ |

削除対象は次の一文だけである。

> TaskSpecが独立したproducer executionを明示した場合だけ、その指定identityをproducer role identityへbindする。

`OWNER_ROLE`の「TaskSpecが独立したproducer executionを明示した場合だけ、起動前にそのexecution identityをtask identityとしてproducerへbindし、predicate前に対応workerを起動する。」は維持する。`PRODUCER`のP1 / P2 / P4 / P5、Candidate81の`VALIDATION_CLOSURE`、残り18 targetも維持する。

## Candidate作成前gate

1. **基準prompt set**: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`を直接親とする。
2. **最短正常経路**: root-only operationではrootを一度bindする。明示委譲operationではTaskSpec指定workerだけをpredicate前に一度spawnし、そのterminal resultをrootが対象criterionへbindする。
3. **保存済み誤経路**: Candidate41以前はcriterion owner語列をworker指定へ読み替え、F05 / F10で不要workerを起動した。
4. **既存入力だけでは防げない理由**: owner metadataとproducer execution指定の変換可否はTaskSpecだけでは決まらないため明示gate自体は必要である。ただし完全なgateは`OWNER_ROLE`へ存在する。
5. **変更predicate**: `PRODUCER`のP3一文だけを削除する。
6. **消す判断点**: `PRODUCER`の短いgateと`OWNER_ROLE`の完全なgateを照合するcross-label判断を一つ消す。委譲可否の判断は消さない。
7. **新規cost**: 新しい判断、参照、例外、labelは追加しない。
8. **品質維持範囲**: D01明示producer正例とF10 Monthly root-onlyを、Candidate81 / Candidate82、rating v13、Medium、各`N=5`で比較する。3 KPIに加え、worker routing、root再読 / result再生成、zero driftをdiagnosticとして記録する。
9. **停止条件**: 不要worker、D01指定worker欠落、rootによるreview再実行、terminal resultの誤binding、required evidence欠落、zero drift違反、score `4`未満が一件でもあれば停止する。意味を補う文は追加しない。

## 評価条件

新しいEvaluation setまたはrating revisionは作らない。既存setを次の二組で使う。

| 経路 | set | 期待するroute |
| --- | --- | --- |
| root-only | `tc-f10-monthly-format-test-review-r3` | child session 0、rootがreviewを一度だけ実行、zero drift |
| 明示producer | `tc-d01-explicit-producer-monthly-review-r1` | 指定worker `/root/monthly_format_review_producer`だけがreviewを実行し、rootはresultを再生成しない |

各pairはprompt identity以外を同一にする。reasoning effortは現行運用基準の`medium`、反復は`N=5`、rating contractは`outcome-abstract-condition-preserving-owner-diagnostic-v13`とする。F10とD01はset identityが異なるため、互いのKPIを一つのcompatibility comparisonへ混ぜない。

## 判定境界

- targeted評価の通過は、P3削除がこの2経路で意味保持した証拠である。
- targeted評価だけでは標準14全体の非回帰、採用、release、THE-CAPTION本体反映を確定しない。
- tokenまたはelapsedが減らなくても、品質とrouteを維持すれば重複削除の意味保持とは両立する。
- bundleの存在は評価済みを意味しない。評価状態は独立resultで更新する。

## 評価結果（2026-07-28）

[`Candidate81 / Candidate82 F10・D01 targeted result`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-f10-d01-n5_2026-07-28.md)を登録した。Candidate82は10 / 10がscore `4`だった。F10は5 / 5 root-only、D01は5 / 5で指定workerだけがreview対象を読み、root再読は0件だったため、`targeted_evaluated / targeted_gate_passed`とする。

token中央値とelapsed中央値はF10、D01の両方でCandidate81を上回ったため、runtime効率改善は主張しない。標準14、採用、release、THE-CAPTION本体反映は未判断、未実施である。

同日、[`標準14項目各N=5`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5_2026-07-28.md)を別resultとして追加した。Candidate82は70 / 70 score `4`、70 / 70 root-only、excluded attempt 0件で、`standard14_evaluated / quality_gate_passed / targeted_gate_passed`となった。token中央値はCandidate81比`+2.28%`、elapsed中央値は`-6.50%`で方向が分かれたため、効率改善は主張しない。採用、release、THE-CAPTION本体反映は引き続き未判断、未実施である。

採用前の長期確認として、同じCandidate82、Rating v13、Medium、標準14項目各`N=5`を新規20 batch、合計1,400件で実行した。[`B20 result`](../evaluations/results/candidate82-producer-gate-deduplication-v13-medium-standard14-continuous-n5-b20_2026-07-28.md)は1,400 / 1,400 valid・rateable、公式score `4 / 1 = 1,399 / 1`だった。score `1`のA01は実際には未固定値を質問して停止した採点偽陰性である。

一方、保存session監査でF02とF04の各1件がcriterion ownerを独立producer指定へ変換し、childを起動した。標準14 TaskSpecは独立producer executionを明示しておらず、設計上の停止条件「不要workerが1件でもあれば停止する」に該当する。現在状態を`standard14_b20_evaluated / stopped`とし、Candidate82へ補助文を追加せず、採用、release、THE-CAPTION本体反映へ進めない。単発N=5の通過結果は当時の履歴として維持する。
