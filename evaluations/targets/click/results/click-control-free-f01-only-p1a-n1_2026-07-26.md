# click control-free F01-only P1-a N=1

## 結論

P1-aは1 / 1件がvalid・rateableで、score `4`だった。Layer 1 fixture固定、bundle overlay、focused / full gate、all-agent token集計、rating、append-only result登録まで端から端で成立した。

この結果は1 case・`N=1`の成立確認である。ばらつき、prompt間の差、標準14項目相当の品質、採用、release、本体反映を示さない。

## 評価identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-f01-only-global-m24-n1-r2` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-f01-only-r1` |
| set identity SHA-256 | `cc0582d2327088f6790bd4bf2b5e84e9ef5f288b64c35660d0cff4ebf08b0a38` |
| case | `CLICK-F01-ANSI-SEQUENCE-STRIP` r1 |
| model / reasoning | `gpt-5.6-sol` / `high` |
| run ID | `927ecf537d1944c698e9be4d3ce2822b` |
| result ID | `d364f70f4b8a418eb75fec5d7359b720` |
| result content SHA-256 | `f13a591cd7482129a2ad1c07deef23228574aa9e43956080bc27dc4c697d5784` |
| compatibility key | `6db48144ae00b5910f7887ccf765906f39664713c9226a615cc546a441631226` |

## 3 KPI

| KPI | 値 |
| --- | ---: |
| `quality_score` | `100.000`（raw score `4`） |
| all-agent `total_tokens` | `180,871` |
| `elapsed_seconds` | `77.811` |

child sessionは0件で、all-agent値はroot session 1件の最終usageと一致した。excluded attemptは0件だった。

## 成果とgate

変更は`src/click/_compat.py`の1行だけである。CSI除去用の正規表現をparameter byte、intermediate byte、final byteの範囲へ拡張した。最終changed pathはこの1 pathだけで、許可外driftは0件だった。

| required command | exit | 観測結果 |
| --- | ---: | --- |
| `PYTHONPATH=src .venv/bin/python -m pytest tests/test_compat.py tests/test_utils/test_style.py -q` | 0 | `280 passed` |
| `PYTHONPATH=src .venv/bin/python -m pytest -q` | 0 | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |

command evidenceは`the-caption-prompt.all-agent-command-evidence/v5`で2 commandともsuccessfulにbindした。protocol違反、adapter-owned cleanup試行、外部失敗はいずれも0件だった。owner-producer evidenceはcriterion owner指定がないため`not_applicable`であり、rating contractどおりdiagnosticだけに使用した。

## P1-aで判明したartifact修正

最初に固定したr1 profileは、Layer 2開始前のfail-closed検証で`comparison_conditions.executor_parameters.token_accounting must use all_agents/v1`となり、runを生成しなかった。r1は履歴として残した。

r2 profileでは、結果を見ずに次の実行契約だけを追加した。

- all-agent token accounting `all_agents/v1`
- focused / full gateを個別commandとしてbindするcommand evidence protocol v1

r1の失敗は評価runではなく、resultとexcluded attemptは0件である。r2はprompt、case、set、model、reasoning、permission、target ref、`N=1`、`M=24`を変更していない。

## 保存境界

registry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約と固定profileだけを置き、raw run log、session file、fixture workspaceはcommitしない。
