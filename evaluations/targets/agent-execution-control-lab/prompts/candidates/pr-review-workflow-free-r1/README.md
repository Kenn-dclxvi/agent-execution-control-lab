# Candidate167

Anthropic由来のレビュー手順を保持したCore Baselineに対し、同じ入力、権限、成果条件、出力契約を保ったまま、レビューの順序、担当分割、並列数、subagent model role、issue別validationの指定を外す校正用promptである。

- base: `claude-code-review-core-r1`
- prompt identity: `pr-review-workflow-free-r1`
- change axis: `workflow_control_removal`
- state: `calibration_candidate / not_executed`
- case: `PRR-C01/r4`。過去実行後に作成されたためheld-out evidenceには使わない

Freeは規則や成果条件を与えない状態ではない。reviewerが必要な入力を同じread-only fixture toolから取得し、review contractを満たす方法だけを自分で選ぶ。品質、全agent合計トークン、経過時間を3 KPIとして記録し、tool call、model step、subagent構成は診断情報として保存する。

このartifactの存在は、品質、採用、release、またはCore Baselineとの正式比較成立を意味しない。
