# Success-silent delivery 第1版

## 結論

結果本文を意味圧縮せず、deterministicな成功resultだけをmodelへ配送しない。失敗、unknown、permission要求はtool resultを変更せずmodelへ返す。TaskSpec、Candidate81 prompt、case、rating contractは変更しない。

比較対象は保存済みの[`sealed observation delivery F02 N=5`](../evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md)である。新しいtreatmentとの差は`comparison_conditions.executor_parameters.success_delivery`だけとする。

## 保存traceから確認した削減対象

sealed condition 5回では、中間messageが25件・`7,635` bytesだった。required validation、identity、scope、mutation receiptなど、成功後にmodel判断を変えないmodel-visible resultは`216,685` bytesだった。discovery read `350,173` bytesと最終回答は削減対象にしない。

同じrun内のsource readには、nested command output `452,334` bytes中`61,443` bytes（`13.58%`）の正規化同一行があった。ただし第1版ではread内容を圧縮・遮断しない。まず成功経路だけを分離する。

## Executor policy

```json
{
  "schema_version": "the-caption-prompt.success-delivery/v1",
  "mode": "success_silent_failure_unchanged",
  "deterministic_success_delivery": "command_and_exit_code_only",
  "failure_delivery": "unchanged_tool_result",
  "intermediate_status_delivery": "start_blocking_or_60s_only"
}
```

required validationは一つのcode call内で列挙順に個別発行する。各resultはcode localに保持する。全commandのexit codeが0なら、完全なcommand文字列とexit codeだけを一度modelへ返す。stdout / stderrはmodelへ返さない。nonzero、unknown、permission要求なら後続を止め、該当tool resultを変更せず返す。

中間messageは開始時、blocking / unknown発生時、または60秒を超える場合だけに限定する。identity一致、正常差分、validation成功の説明を独立messageとして再入力しない。

## 事前gate

F02 `N=5`で次を確認する。

- quality: 5 / 5 score `4`
- required validation: 既存command evidenceが完全
- validation wave: 1 outer code call
- success receipt: 4,096 bytes以下、raw pytest markerなし
- intermediate message: 2件以下、合計1,024 bytes以下
- KPI: all-agent token中央値と合計、elapsed中央値と合計

mechanism gateを1件でも満たさない場合はF04と標準14へ進めない。mechanismを満たしてもtoken中央値または合計が減らなければ、成功result配送を主要因と扱わず停止する。

## F02 N=5結果

[`F02 N=5 result`](../evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`、mechanism 5 / 5だった。sealed control比でtoken中央値`-17.86%`、合計`-21.60%`、elapsed中央値`-16.32%`、model-visible result bytes合計`-38.18%`である。

現在状態は`executor_f02_evaluated / quality_passed / mechanism_passed / cost_reduced / f04_not_started`である。単一caseから一般化せず、次の評価はF04の互換control / treatmentとする。
