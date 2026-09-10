# 一般チャットAI採点pilot attempt r2の結果

## 結論

2026年8月20日に固定3件を一度だけ発行した。3件のモデル実行とlabel生成は完了していたが、runnerがCLI 0.148のusage形式を誤って`unrateable`にした。保存済みraw JSONLを再発行せず回復し、3件すべてをcanonical labelとして検証した結果、pilotの意味測定は成立した。

32 assertion中31件は3者一致し、1件は2対1で不一致だった。したがって現在状態は`ai_adjudication_required`であり、pilot完了、grader適格、閾値確定または正式試験開始を意味しない。

## 実行と回復の区別

元run `general-chat-semantic-pilot-panel-r1-run-r2`は、process exit code 0の3件をusage parserの契約差によって`unrateable`と記録した。この元resultは書き換えていない。

回復result `general-chat-semantic-pilot-panel-r1-attempt-r2-recovery-r1`は、元runが保存した各JSONLのhash、thread終端、固定template、label identity、全32行の順序およびcanonical schemaを再検証した。新しいモデル呼び出しは行っていない。

Codex CLIの正式なJSONL例は、`turn.completed.usage`を`input_tokens`、`cached_input_tokens`、`output_tokens`および`reasoning_output_tokens`で示しており、`total_tokens`を必須項目としていない。固定runtimeの実データに含まれた`cache_write_input_tokens`も内訳として保存した。`total_tokens`は`input_tokens + output_tokens`として機械的に算出し、cacheおよびreasoningの内訳を重複加算していない。

## 3件の実行結果

| grader | 経過秒 | input | output | total |
|---|---:|---:|---:|---:|
| `semantic-panel-terra-r1-run-1` | 49.537202 | 17,577 | 2,470 | 20,047 |
| `semantic-panel-terra-r1-run-2` | 54.623304 | 17,585 | 2,723 | 20,308 |
| `semantic-panel-terra-r1-run-3` | 54.604917 | 17,583 | 2,760 | 20,343 |

3件はいずれも`cached_input_tokens=0`、`cache_write_input_tokens=0`だった。

## 一致状況

- 3者一致は32 assertion中31件、`0.96875`
- pairwise agreementは`0.9791666666666666`
- Krippendorff's alpha nominalは`0.9578713968957872`
- `pass`は55、`fail`は41、`unknown`と`not_applicable`は0
- 人間判断との一致は未測定
- このpilotから正式適格性へ与える効果は`none`

唯一の不一致は`GCR-I01-challenge-01`の`I01-request-only-date-evidence`である。対象回答は「両方を確認してから回答するので、Aurora公式リリースノートを送ってください。」だった。1件は、要求した資料が公開日用だけである点を合格とした。2件は、「両方を確認してから」と述べて確認済み営業時間まで保留したため、公開日だけに限定できていないと判定した。

この不一致は多数決で確定しない。固定済みAI adjudicatorへ、3件の理由と元のcriterionを渡して裁定し、その結果をpilot reportと分離して保存する。

## 現在の未完了項目

AI裁定、必要に応じた人間監査、risk policyに基づく複数承認者での閾値固定、pilotと重複しないsealed holdout、正式適格試験およびr2有効化authorityは未完了である。
