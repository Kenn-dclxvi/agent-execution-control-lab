# click control-free F02-only N=3

## 結論

Bundle Aで追加したF02 caseは3 / 3件がvalid・rateableで、全件score `4`だった。all-agent token中央値は`303,563`、elapsed中央値は`130.225`秒である。

これは追加case 1件・`N=3`の成立確認である。F01 resultとはsetとrating contractが異なるため同一comparisonへ混ぜない。標準14項目、Bundle間の差、採用、release、本体反映を示さない。

## 評価identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-f02-only-global-m24-n3-r1` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-f02-only-r1` |
| set identity SHA-256 | `783ff900291a595fc087c642a7c1a0db76739c4b92bbc65bbd5aa391999fc3b6` |
| case | `CLICK-F02-STREAM-DEPRECATION-CONTRACT` r1 |
| rating contract | `click-outcome-abstract-condition-preserving-v2` |
| model / reasoning | `gpt-5.6-sol` / `high` |
| result ID | `c990e7adda5e4b43b7ebfb2a3816aa63` |
| result content SHA-256 | `92769c42f2ebe28e7e6505e012f6a69f2bffa78a82d1e85b1b0e06ecf19063f1` |
| compatibility key | `d5962afb950268d277f72cc382ce13d609ec790829608f2045c7e896f6a3189e` |

Bundle AのcontentとidentityはP1-cから変更していない。F02追加によりcase、set、rating contract revision、`N`が変わるため、F01 resultとのcompatibility keyは異なる。

## 3 KPI

| KPI | 中央値 | 最小 | 最大 | range | range / 中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `quality_score` | `100.000` | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent `total_tokens` | `303,563` | `231,319` | `323,075` | `91,756` | `30.23%` |
| `elapsed_seconds` | `130.225` | `95.913` | `133.196` | `37.283` | `28.63%` |

| iteration | run ID | raw score | all-agent token | elapsed秒 |
| ---: | --- | ---: | ---: | ---: |
| 1 | `7647ac223b0041f685c53f03ede1df95` | 4 | 303,563 | 133.196 |
| 2 | `f83ff7c3c6e54828909e9c302abf5718` | 4 | 323,075 | 130.225 |
| 3 | `d2e72ec1375d41a181e740c9817b01e3` | 4 | 231,319 | 95.913 |

child sessionは全runで0件であり、all-agent値はroot session 1件の最終usageと一致した。3 slotはすべて初回attemptでvalidとなり、excluded attemptは0件だった。runner wall elapsed `133.348`秒は並列batchのdiagnosticであり3 KPIには含めない。

## 成果とgate

3 runすべてで`src/click/__init__.py`と`src/click/utils.py`の2 fileを変更し、deprecatedな公開stream accessorと内部private helperの層間contractを復元した。iteration 3はdocstring内のhelper参照もprivate名へ揃えたが、observable outcomeは他2 runと同じである。

| required command | 各runのexit | reference時の観測結果 |
| --- | ---: | --- |
| `PYTHONPATH=src .venv/bin/python -m pytest tests/test_deprecations.py tests/test_testing.py -q` | 0 | `72 passed, 1 skipped` |
| `PYTHONPATH=src .venv/bin/python -m pytest -q` | 0 | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |

required command evidenceは全runで2 / 2 successfulだった。protocol違反、許可外drift、adapter-owned cleanup試行、外部失敗はいずれも0件だった。

## 実行前停止の履歴

最初のcampaign r1は、parallel planの`estimated_seconds=0`が正数制約に反してrunner開始前に停止した。run、attempt、resultはいずれも0件である。profile、case、Bundle Aは変更せず、plan extensionのhintだけを`1.0`へ直したcampaign r2で実行した。

## 次の境界

F02のqualificationと`N=3`成立確認は完了した。次は残り12項目の次caseを同じ手順で追加する。既存F01 / F02をcase追加のたびに再実行せず、14 caseが揃った後にBundle AのClick Std14 `14 × N=5 = 70`を実行する。

## 保存境界

registry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約と固定artifactを置き、raw run log、session file、fixture workspaceはcommitしない。
