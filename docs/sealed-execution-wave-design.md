# Sealed execution wave 第1版

## 結論

model再入を減らす境界は、出力文字数の指示ではなく、**中間resultをmodelへ配送しないexecutor境界**とする。

第1版は[`sealed_execution_wave.py`](../scripts/sealed_execution_wave.py)として実装した。事前に確定できるcommand群を一つのwaveとして順に実行する。正常な中間stdout / stderrはworkspace外の証跡directoryへ保存し、model-facing stdoutへ返さない。modelへ返すのは、全command完了、最初のpredicate不成立、または結果不明のいずれかを示す一つのterminal receiptだけである。

これはprompt Candidateではない。TaskSpec、prompt bundle、quality rating contractも変更しない。

## 解決する問題

保存済みのCandidate90からCandidate93までのF02 `N=5`では、短文化や結果分類の記述だけでは中間resultの再流入を安定して止められなかった。特にCandidate92は、上限指定が個別readの細分化を誘発し、品質を維持したままtoken `+51.00%`、elapsed中央値`+28.89%`となった。

原因はrawであること自体ではない。次の判断に不要な正常resultまでmodel contextへ入り、その後のmodel stepで会話履歴として再読されることが問題である。

## 配送境界

| operation result | executorの処理 | modelへの配送 |
| --- | --- | --- |
| expected exit code | stdout / stderrを外部保存して次へ進む | 配送しない |
| unexpected exit code | 後続を停止して外部保存する | 4 KiB以下の失敗末尾をterminal receiptへ含める |
| timeout | process groupを停止して外部保存する | `unknown` receiptを返す |
| command起動不能 | 後続を停止して外部保存する | `unknown` receiptを返す |
| 全operation成功 | write-once receiptを外部保存する | terminal receiptを一度だけ返す |

この境界で「成功したので次へ進めるか」という決定的な状態遷移はexecutorが処理する。失敗原因の解釈、対象や方法の変更、permission追加、成果の意味判断が必要な場合だけmodelへ戻す。

## Plan contract

plan schemaは`the-caption-prompt.sealed-execution-wave-plan/v1`である。

```json
{
  "schema_version": "the-caption-prompt.sealed-execution-wave-plan/v1",
  "wave_id": "post-edit-validation",
  "operations": [
    {
      "id": "focused-test",
      "argv": [".venv/bin/python", "-m", "pytest", "tests/test_target.py", "-q"],
      "expected_exit_codes": [0],
      "timeout_seconds": 300
    },
    {
      "id": "full-test",
      "argv": [".venv/bin/python", "-m", "pytest", "-q"],
      "expected_exit_codes": [0],
      "timeout_seconds": 1200
    }
  ]
}
```

`argv`は文字列配列に限定する。shell文字列、暗黙のcommand連結、任意の環境変数差し替えは受け付けない。operationは記載順に実行し、最初の不成立または不明で後続を止める。

実行例は次のとおりである。

```bash
python3 scripts/sealed_execution_wave.py \
  --plan /tmp/post-edit-validation-plan.json \
  --workspace /path/to/fixture-copy \
  --evidence-directory /tmp/post-edit-validation-evidence
```

証跡directoryはworkspace外かつ未作成でなければならない。plan、各operationの完全なstdout / stderr、SHA-256、byte数、terminal receiptをwrite-onceで保存する。公開repositoryへraw出力を保存しない。

## 保証することと、まだ保証しないこと

第1版が保証するのは、一つのCLI invocation内での観測遮断である。正常な中間出力はCLI stdoutへ現れない。このため、呼出側がCLI resultだけをmodelへ渡せば、中間出力はmodel contextへ再入しない。

第1版のCLIだけでは、modelが通常のexecを選んでwaveを迂回することまでは禁止しない。また、source理解、diff判断、GitHub approval、production状態の意味判定を自動化しない。

評価adapterは`comparison_conditions.executor_parameters.observation_delivery`に次の完全一致policyがある場合だけ、Codexの`code_mode`、`code_mode_buffered_exec`、`code_mode_only`を有効にする。通常toolの直接result配送を閉じ、code内のnested tool resultをcodeが返るまでmodelへ配送しないruntime conditionである。

```json
{
  "schema_version": "the-caption-prompt.observation-delivery/v1",
  "mode": "code_mode_only_buffered_exec",
  "direct_tool_result_delivery": "disabled",
  "nested_tool_result_delivery": "code_local_until_return"
}
```

このCodex機能は現行CLIで`under development`である。このため、利用可能というだけではN5の有効性を確定しない。adapterは各runのroot rolloutから`observation-delivery-audit/v1`を作る。直接`function_call_output`が0件で、すべてのmodel-visible tool resultが外側のcode callに対応する場合だけ`mechanism_passed=true`とする。通常resultの直接配送があればmechanism不成立としてKPI解釈から分離する。

後続の[`F02 N=5 executor A/B`](../evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md)で、treatmentは直接result 0件を5 / 5で達成した。一方、model再入はcontrol / treatmentとも中央値`7`、合計`36`で、token中央値は`+1.92%`だった。現在の状態は`mechanism unit verified / adapter flag binding verified / executor_f02_evaluated / no_reentry_reduction / stopped`である。

失敗理由は、`code_mode_only`が直接tool経路を閉じても、modelが外側code callを7〜8回に分けられるためである。次の再開条件は、正常な外側code returnをterminalまで禁止できるruntime境界が存在することとする。promptへの文言追加や同じfeature flagの再試行は行わない。

## N=5での効果測定

次の効果測定は、いつものF02 `N=5`を使う。TaskSpecは変更しない。

固定するものはCandidate81 prompt bundle、F02 case revision、quality rating revision、model、reasoning level、permission、fixture、反復数である。変更するのはexecutorのresult配送だけである。

| condition | result配送 |
| --- | --- |
| control | 現行の各tool result配送 |
| treatment | sealed execution waveによるterminal receipt-only配送 |

品質、all-agent `total_tokens`、`elapsed_seconds`の3 KPIで判定する。model step、tool call、model-visible result byte数、外部保存byte数は原因診断にだけ使用する。

これはprompt Candidate比較ではなくexecutor A/Bである。`comparison_conditions.executor_parameters.observation_delivery`が異なるため、既存Candidate81 resultと同一compatibility keyの勝敗には混ぜない。まずadapter integrationを実装し、5回すべてで通常resultの迂回がないことをmechanism gateとして確認してからKPIを解釈する。
