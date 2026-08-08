# PRR-C01/r4 Workflow Free calibration N=2

## 結論

Workflow Freeの2反復は、どちらも固定入力への到達、要求model、構造化出力、全agent token、経過時間、権限境界を確認でき、測定として成立した。Freeは両方ともsubagentを使わず、`claude-sonnet-5`のrootだけでレビューした。品質は1回目がscore `4`、2回目がscore `1`であり、同じ構成でも期待findingの検出が反復間で変わった。

このN=2は、PRR-C01/r4を使った校正結果であり、held-out品質、Core Baselineとの勝敗、採用、releaseを示さない。

## 一次result

| repetition | GitHub run | 測定成立 | quality | all-agent tokens | review | execution | 実際の構成 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | [31267762618](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31267762618) | satisfied | 4 | 3,412,444 | 273.019秒 | 292.323秒 | rootのみ、subagent 0、fixture tool 6回 |
| 2 | [31268027384](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31268027384) | satisfied | 1 | 2,247,776 | 259.356秒 | 275.600秒 | rootのみ、subagent 0、fixture tool 6回 |

- repetition 1: [`run result`](pr-review-workflow-free-calibration-r1-prr-c01-r1-a31267762618.json)、SHA-256 `8249c2c7d3a1b62ce39c9c167538acc7c2e873b0449fdec14741a1860f819500`
- repetition 2: [`run result`](pr-review-workflow-free-calibration-r1-prr-c01-r2-a31268027384.json)、SHA-256 `5db6a3ed775d0f083f3e01d91cd5b4b59e86915d2e8573c6348ff33cf3f63a35`

## 観測範囲

2反復のall-agent token合計は`5,660,220`、1反復平均は`2,830,110`である。review時間の平均は`266.188秒`、workflow executionの平均は`283.962秒`である。平均値はN=2の記述値であり、分布の推定には使わない。

Core Baselineのrun `31265761721`は、固定された複数agent構成でscore `1`、all-agent token `3,338,635`、review `563.788秒`だった。Freeの2反復は同runより短時間だったが、実際のsubagent構成とmodel mixが異なるため、厳密なprompt-only KPI比較として扱わない。

## 次の校正

今回の結果から、固定4 reviewer構成がなくても期待findingを検出できる一方、root単独の同一modelでも見逃しが再現することが分かった。次は、単純にagent数を増やすのではなく、複数pathと適用規則の関係を確認するreview roleを固定し、そのroleのmodelを比較する。eligibility、入力収集、bug/security、validationのmodel選択は別の構成軸として扱う。
