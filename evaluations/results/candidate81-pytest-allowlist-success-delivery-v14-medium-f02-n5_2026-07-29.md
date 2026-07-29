# Candidate81 pytest allowlist success delivery Rating v14 Medium F02 N=5

## 結論

pytest系commandだけをexact argvで許可し、成功rawをadapter localへ保存してmodelへreceiptだけを返すexecutor機構は5 / 5 runで成立した。品質も5 / 5件がscore `4`だった。

一方、直前のinstruction-based success-silent条件比では、all-agent token中央値は`226,326 → 206,751`、`-19,575`（`-8.65%`）だったが、合計は`1,111,067 → 1,131,815`、`+20,748`（`+1.87%`）だった。したがって、機構成立と品質維持は確認したが、token総量の削減は確認していない。

状態を`executor_f02_evaluated / quality_passed / exact_allowlist_mechanism_passed / failure_transport_unit_passed / aggregate_token_reduction_not_demonstrated / f06_not_started`とする。Std14、採用、release、本体反映は未実施・未判断である。

## Identity

- TaskSpec / set: `the-caption-planning-first-f02-r1` / `r1`
- prompt: Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model / reasoning / N / M: `gpt-5.6-sol` / `medium` / `5` / `5`
- runtime: Codex CLI `0.146.0` / Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- treatment result: `7cc11367ced44b4ba2a03b2d2d07692e`
- treatment compatibility key: `b3bcd8fecd9b25e1203f3c1770b026cc138f579f0c02580440a9c3e34dd7e5bf`

TaskSpec、Candidate81 prompt、case revision、fixture、rating、model、reasoning、permission、M / Nは変更していない。直前の[`success-delivery/v1`](candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md)との差はexecutorの`success_delivery`だけである。executor parameterが異なるためcompatibility keyも異なり、通常のprompt比較viewへ混ぜない。

## 3 KPI

| condition | score 4 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| sealed control | 5 / 5 | `275,549` | `1,417,138` | `95.398`秒 | `480.561`秒 |
| instruction-based v1 | 5 / 5 | `226,326` | `1,111,067` | `79.832`秒 | `427.517`秒 |
| pytest exact allowlist v2 | 5 / 5 | `206,751` | `1,131,815` | `83.581`秒 | `400.201`秒 |
| v2 - v1 | `0` | `-19,575`（`-8.65%`） | `+20,748`（`+1.87%`） | `+3.749`秒（`+4.70%`） | `-27.316`秒（`-6.39%`） |
| v2 - sealed control | `0` | `-68,798`（`-24.97%`） | `-285,323`（`-20.13%`） | `-11.816`秒（`-12.39%`） | `-80.360`秒（`-16.72%`） |

| iteration | token | elapsed | model再入 | model-visible result bytes |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `268,434` | `90.763`秒 | `7` | `87,619` |
| 2 | `206,751` | `69.799`秒 | `6` | `63,510` |
| 3 | `259,538` | `86.259`秒 | `7` | `78,041` |
| 4 | `199,359` | `83.581`秒 | `6` | `63,046` |
| 5 | `197,733` | `69.800`秒 | `6` | `58,143` |

v2のmodel-visible result bytesは中央値`63,510`、合計`350,359`だった。v1比は中央値`-694`（`-1.08%`）、合計`-100`（`-0.03%`）であり、model-visible result全体の追加削減はほぼない。model再入もv1と同じ中央値`6`、合計`32`だった。

## Mechanism診断

allowlist対象は各runで次の2件だけである。

1. `.venv/bin/python -m pytest tests/unit/test_collection_history_updater.py tests/unit/test_v4_engine.py -v`
2. `bash scripts/dev/main_verify.sh`

2件目はscript SHA-256 `f714bc5ed1c91c4d9d8a68f85f64a362e4c83681a673536da3be433e0f100f74`も固定した。両commandは5 runすべてで各1回成功した。

| 診断 | v2結果 |
| --- | ---: |
| exact allowlist mechanism | `5 / 5` |
| local raw evidence | `2件 / run`、計`10件` |
| local raw evidence failures | `0` |
| local raw stdout / stderr bytes | `183,079 / run`、計`915,395` |
| validation raw success markerのmodel-visible流入 | `0 / 5` |
| validation model-visible bytes | 中央値`1,125`、合計`5,525` |
| 中間message | 中央値`1`、合計`5`件 |
| 中間message bytes | 中央値`252`、合計`1,248` |

成功時はraw stdout / stderr、byte数、SHA-256、exact argv、exit codeをadapter localに保存し、modelへreceiptだけを返した。allowlist外argvとwrapper identity不一致は実行前に拒否するunit testを通過した。通常のnonzero exitはstdout、stderr、exit code `7`をbyte単位で返し、signal終了もstdout、stderr、signalを維持するsubprocess unit probeを通過した。ただし、実際のF02 taskでpytestを失敗させるrunは実施していない。

## 判定

- quality gate: `passed`（5 / 5 score `4`）
- exact allowlist mechanism gate: `passed`（5 / 5）
- local raw evidence gate: `passed`（各run 2件、failure 0）
- success raw ingress gate: `passed`（raw marker 0 / 5）
- normal nonzero / signal failure transport: `unit probe passed`
- v1比token: 中央値は減少、合計は増加。総量削減は`not demonstrated`
- F06、Std14、採用、release、本体反映: 未実施・未判断

F02はfocused pytestとpinned wrapperのtransport確認である。次はTaskSpecを変えず、focused pytestとdirect full pytestを含むF06でexact allowlistの対象範囲と再現性を確認する。F06成立前にStd14へ拡張しない。

## 実行証跡

実行準備時にrunner planのcycle pathが`source/cycle`を指したため、実行後に実体を予定の`batch-001/cycle`へ移した。未使用precloneはTrashへ退避し、source cycleは同一Layer 1から復元した。run ID、capsule、raw evidence、rating、result identityは変更していない。実行時planは`runner-plan.executed.json`として保持し、修正後planと区別した。

- result content SHA-256: `c5b4e689b681d1810ad0dc898bfa5f1fb51392a9a5e8223070793726d89b1adf`
- execution archive SHA-256: `4216a3e50417d081734a39d2f92e93eb78e3d2d36e8ecd68a018fd95809b8d48`
- execution seal SHA-256: `e6751695a8095690b2abd761112696a01c536248eb7a5e4a69b846d89c3eabff`
- final archive SHA-256: `03180a440a9cfdc675d1e3edfe34d61728e8edbe18649a73d92a14f39f0174e2`
