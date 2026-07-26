# click control-free F01-only P1-b N=5

## 結論

P1-bは5 / 5件がvalid・rateableで、全件score `4`だった。同一のBundle A、case、runtime、model、reasoningを固定した1 batch内で、all-agent token中央値は`189,977`、elapsed中央値は`80.475`秒だった。

この結果は1 case・`N=5`のbatch内分布である。batch間の安定性、標準14項目、Bundle間の差、採用、release、本体反映を示さない。

## 評価identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-f01-only-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-f01-only-r1` |
| set identity SHA-256 | `cc0582d2327088f6790bd4bf2b5e84e9ef5f288b64c35660d0cff4ebf08b0a38` |
| case | `CLICK-F01-ANSI-SEQUENCE-STRIP` r1 |
| model / reasoning | `gpt-5.6-sol` / `high` |
| result ID | `d83aab21064c4425b690a922ba0e2877` |
| result content SHA-256 | `6bd06cac99c9b8a184e469113705c98e9bfac60c8aeba660790bc49d16748178` |
| compatibility key | `bc44567542c938534cbdc2dc7520228514e3cdd55c476182b90a549f5fc0a79a` |

P1-aから変更した比較条件は、profile identityと反復数`N=1 → 5`だけである。Bundle Aのcontentとidentityは変更していない。

## 3 KPI

| KPI | 中央値 | 最小 | 最大 | range | range / 中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `quality_score` | `100.000` | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent `total_tokens` | `189,977` | `170,228` | `202,176` | `31,948` | `16.82%` |
| `elapsed_seconds` | `80.475` | `79.323` | `85.443` | `6.120` | `7.61%` |

| iteration | run ID | raw score | all-agent token | elapsed秒 |
| ---: | --- | ---: | ---: | ---: |
| 1 | `16835a154ce44f2694746ddc81edca62` | 4 | 202,176 | 80.475 |
| 2 | `fa4eee3918a9457e81419deec1bb6b2e` | 4 | 170,228 | 79.569 |
| 3 | `102607e7939e4c919c36a2adbce145b9` | 4 | 198,376 | 79.323 |
| 4 | `aadf7b4104dc47a4ab206ad53c8165fd` | 4 | 189,977 | 85.443 |
| 5 | `4de6eb40979e46418d87e1f14678d87e` | 4 | 174,959 | 85.349 |

child sessionは全runで0件であり、all-agent値はroot session 1件の最終usageと一致した。5 slotはすべて初回attemptでvalidとなり、excluded attemptは0件だった。global queueのrunner wall elapsedは`85.669`秒であるが、これは並列batchのdiagnosticであり3 KPIには含めない。

## 成果とgate

全runの最終changed pathは`src/click/_compat.py`だけで、許可外driftは0件だった。4 runはCSI除去用の正規表現を`r"\033\[[0-?]*[ -/]*[@-~]"`、1 runは同じbyte範囲を明示する`r"\033\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]"`として実装した。固定rating contractは意味的に同等な実装を同一成果として扱うため、全件score `4`である。

| required command | 各runのexit | 各runの観測結果 |
| --- | ---: | --- |
| `PYTHONPATH=src .venv/bin/python -m pytest tests/test_compat.py tests/test_utils/test_style.py -q` | 0 | `280 passed` |
| `PYTHONPATH=src .venv/bin/python -m pytest -q` | 0 | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |

command evidenceは全runで2 commandともsuccessfulにbindした。protocol違反、adapter-owned cleanup試行、外部失敗はいずれも0件だった。owner-producer evidenceはcriterion owner指定がないため全runで`not_applicable`であり、rating contractどおりdiagnosticだけに使用した。

## 次の境界

次はP1-cとして、同じBundle A identityと`N=5` profileを変更せず独立resultへ反復し、batch中央値の散らばりを測る。Bundle Bは作らない。Bundle BはBundle Aの標準14項目baselineを確立した後、1軸だけを変更した最初の実Candidateとして固定する。

## 保存境界

registry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約と固定profileだけを置き、raw run log、session file、fixture workspaceはcommitしない。
