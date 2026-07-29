# Candidate81 pytest allowlist success delivery Rating v14 Medium F06 N=5

## 結論

focused pytestとfull pytestをexact argvへ固定し、成功rawをadapter localへ保存してmodelへreceiptだけを返すexecutor機構は5 / 5 runで成立した。品質も5 / 5件がscore `4`だった。

all-agent tokenは中央値`179,199`、合計`829,560`だった。elapsedは中央値`91.509`秒、合計`431.612`秒だった。同じruntime・TaskSpec・Ratingでsuccess deliveryだけを外したmatched controlは未取得であるため、F06ではtokenまたはelapsedの削減効果を判定しない。

現在状態を`executor_f02_f06_evaluated / quality_passed / exact_allowlist_mechanism_passed / cost_effect_unmatched / std14_not_started`とする。Std14、採用、release、本体反映は未実施・未判断である。

## Identity

- TaskSpec / set: `the-caption-validation-fast-path-f06-r1` / `r1`
- case: `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2`
- evaluation set identity SHA-256: `4efcb48c2b31280e5eb613962d0367d00b1e151e79c6375cf36a45bf8dcc63a5`
- fixture identity SHA-256: `6bd345bda75157b6d29a373a74ca9d9352f429751e33e5bd9e601cbbef63ef06`
- prompt: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model / reasoning / N / M: `gpt-5.6-sol` / `medium` / `5` / `5`
- runtime: Codex CLI `0.146.0` / Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- result: `69f1aab2e1ac4be3b59301d89aa1b61e`
- compatibility key: `624fd47b5b2cde069ae2fd46f853c6d6bc8e88852d2f0de5554372fcdae4c3fb`

標準14項目F06 r2のmodel-visible TaskSpec、fixture、Candidate81 prompt、rating、model、reasoning、permission、M / Nは変更していない。executorへ`observation-delivery/v1`と`success-delivery/v2`を追加した別compatibility条件であり、通常のprompt比較viewへ混ぜない。

## 3 KPI

| iteration | quality | all-agent token | elapsed |
| ---: | ---: | ---: | ---: |
| 1 | `4` | `192,737` | `91.515`秒 |
| 2 | `4` | `184,065` | `91.509`秒 |
| 3 | `4` | `179,199` | `101.673`秒 |
| 4 | `4` | `160,880` | `73.847`秒 |
| 5 | `4` | `112,679` | `73.068`秒 |
| 中央値 | `4` | `179,199` | `91.509`秒 |
| 合計 | 5 / 5 score `4` | `829,560` | `431.612`秒 |

## Mechanism診断

allowlist対象は各runで次の2件だけである。

1. `.venv/bin/python -m pytest tests/unit/test_market_units_snapshot.py -v`
2. `.venv/bin/python -m pytest tests/ -v`

| 診断 | 結果 |
| --- | ---: |
| exact allowlist mechanism | `5 / 5` |
| required command | 2件ともsuccessful、5 / 5 run |
| local raw evidence | `2件 / run`、計`10件` |
| local raw evidence failures | `0` |
| local raw stdout / stderr bytes | `179,206 / run`、計`896,030` |
| validation raw success markerのmodel-visible流入 | `0 / 5` |
| validation model-visible bytes | 中央値`1,092`、合計`4,802` |
| model-visible result bytes | 中央値`21,029`、合計`101,304` |
| model再入 | 中央値`7`、合計`31` |
| 中間message | 中央値`1`、合計`5`件 |
| 中間message bytes | 中央値`222`、合計`1,167` |

初回auditはrun path中の`pytest`と通常read中の`tests/...`を部分文字列で結合し、validation callを3〜4件と誤検出した。v2 auditをwrapper markerとpolicy上のexact argvで照合するよう修正し、同じ保存済みrolloutを再監査した。初回auditは各runの`audit.pre-exact-v2-fix.json`として残した。runの再実行、TaskSpec変更、resultの置換は行っていない。

## 判定

- quality gate: `passed`（5 / 5 score `4`）
- focused / full pytest exact allowlist gate: `passed`（5 / 5）
- local raw evidence gate: `passed`（各run 2件、failure 0）
- success raw ingress gate: `passed`（raw marker 0 / 5）
- cost effect: `unmatched`。matched control未取得のため改善・悪化を判定しない
- Std14、採用、release、本体反映: 未実施・未判断

F02とF06でtransport対象の種類は確認できた。ただし、F02ではinstruction-based v1比のtoken合計が`+1.87%`で、F06にはmatched controlがない。Std14へ進む前に、同じF06条件から`success_delivery`だけを外したcontrolをN=5で取得し、quality、token中央値・合計、elapsed中央値・合計を比較する。

## 保存証跡

- result content SHA-256: `9a9309cfc075b72f1ccbd7f0b78d6869e4c5cab58b83b2e6577c8f06c4f1bcf4`
- execution archive SHA-256: `ca089256b2cfe2ce86f6feef4dd265cfa2d997b8fdf7f7f0d6b774a752af1419`
- execution seal SHA-256: `09f71b0f0851bbaf614f0af72539a277df1fd78df3c5fcf033ff07179f738cd0`
- final archive SHA-256: `7a412a2282f51973aa024a8aa0a92e8b840971cd9cb790b2fc580d98f74861ad`
