# Workflow Free校正設計 r1

## 目的

Anthropic由来の手順を保持したCore Baselineと、レビュー方法をモデルへ委ねる状態を分け、次のレビュー体制とモデル構成を選ぶための校正値を得る。

Core BaselineのGitHub Actions run `31265761721`では、入力、read-only権限、実並列、構造化出力、全agent token、経過時間を観測できた。一方、期待findingは返らなかった。この結果は測定経路の不成立ではなく、固定したレビュー体制で得た品質観測として保持する。

## Freeの定義

Freeは、review対象、適用規則、成果条件、権限、出力契約を除去した状態ではない。次を同じまま保持する。

- PRR-C01/r4のmodel-visible入力とmodel-invisible oracleの境界
- PR metadata、changed paths、diff、規則、対象本文へ到達できるread-only fixture tool
- repository writeとGitHub commentの禁止
- review contract、構造化出力schema、quality rating
- root model、Claude Code Action revision、timeout、token accounting

次のレビュー方法だけを固定しない。

- 入力を取得する順序
- subagentを使うかどうか
- 担当数、並列化、model role
- 要約を独立段階にするかどうか
- 候補findingを検証する方法

実際に選ばれたtool call、subagent構成、model role、並列関係は実行条件へ事後補完せず、診断情報として記録する。

## 判定の分離

一つのrunから、測定が成立したかと、レビュー品質がどうだったかを別々に記録する。

測定成立には、Actionの完了、構造化出力、要求modelとの一致、全agent token、経過時間、fixture access、fixture toolの権限拒否0件を要求する。品質は同じrating contractで採点するが、findingのmissまたはfalse positiveだけでは次の校正反復を止めない。

正式KPIは次の3件である。

- `quality_score`
- all-agent `total_tokens`
- `elapsed_seconds`

tool call、model step、subagent routing、rootとsubagent別のusage recordは、Freeが選んだレビュー方法を説明する診断情報であり、KPIへ追加しない。

## 校正からモデル選択まで

PRR-C01/r4は過去実行後に作成されたため、held-out evidenceには使わない。最初のWorkflow Free N=2は、品質の一般化や勝敗ではなく、制御を外したときのレビュー方法とKPIを観測する。

その後は、Core BaselineとFreeの差から一つの構成軸だけを持つreview体制候補を作る。review体制を固定した後、repository discipline、bug/security、validationなどの役割ごとにmodel構成を校正する。選択した構成を固定してから、チューニングに使っていないcaseでCore Baselineとの比較を行う。
