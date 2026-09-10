# 一般チャットAI採点pilot attempt r1の結果

## 結論

2026年8月20日に固定3件を発行したが、3件とも採点開始前に出力スキーマをAPIから拒否された。このattemptではAI labelが一件も生成されていないため、採点品質、一致率、閾値および正式適格性は未測定のままである。同じpreflightから再発行はしない。

## 固定した実行条件

- 採点対象モデルは`gpt-5.6-sol`
- 採点モデルは独立した3件の`gpt-5.6-terra`、reasoningは`medium`
- runtimeはregistryで固定した`codex-cli 0.148.0`
- 発行数は3件で、追加発行と自動再試行は行っていない

## 観測結果

run resultは`general-chat-semantic-pilot-panel-r1-run-r1`である。3件すべてがexit code 1の`external_failure`となり、`valid_results=0`、`measurement_state=pilot_measurement_not_established`で終了した。

全件に共通したAPI errorは`invalid_json_schema`だった。transport schemaの`independent_context`が`const: true`だけを持ち、必須の`type`を持たないことが最初の拒否箇所として報告された。canonical label schemaには、同じ形の`schema_version`と、型を持たない`label`の`enum`も存在していた。

これは回答内容の判定失敗やgrader間不一致ではない。採点モデルへ有効な要求が到達していないため、このattemptをpilotの意味測定へ含めない。

## 後続処置

transport schema生成時に`const`および同種値だけの`enum`からJSON型を補う。さらに、未対応annotationが残っていないこと、固定値に型があること、objectの全propertyがrequiredであることをpreflight内で検査する。修正後は別identityのpreflightを作り、再発行には別の明示判断を必要とする。

raw JSONL、stderr、固定material、issued receiptおよびrun resultは、repository外の失敗attempt保存先へ一括して保持する。raw実行ログはcommitしない。
