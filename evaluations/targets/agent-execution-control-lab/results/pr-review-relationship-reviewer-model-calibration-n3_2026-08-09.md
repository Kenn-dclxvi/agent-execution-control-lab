# PRR-C01/r4 関係レビュー役モデル校正 N=3

## 結果

Sonnet条件とOpus条件の全6反復で、root model、関係レビュー役1人、指定したreviewer model、構造化出力、全agent token、経過時間、reviewerによるfixture access、rootのfixture access 0回を確認できた。したがって、6件すべて測定として成立した。

Opus条件のquality scoreは`4 / 4 / 4`、Sonnet条件は`4 / 0 / 4`だった。Sonnet repetition 2は期待findingを検出した一方、model-visibleな`rule_catalog`にないrule identityを使うfindingを2件追加したため、false positive 2件、scope violation 2件、review contract violation 2件となった。

PRR-C01/r4はこの校正に使ったcaseであり、held-out evidenceではない。このN=3だけから一般的なモデル優劣、採用、releaseを決めない。

## 一次result

| reviewer model | repetition | GitHub run | 測定成立 | quality | all-agent tokens | review | execution | fixture access |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Opus | 1 | [31269234142](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269234142) | satisfied | 4 | 570,567 | 169.185秒 | 182.744秒 | reviewer 13回 / root 0回 |
| Opus | 2 | [31269414636](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269414636) | satisfied | 4 | 637,780 | 184.554秒 | 200.322秒 | reviewer 8回 / root 0回 |
| Opus | 3 | [31269611740](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269611740) | satisfied | 4 | 933,211 | 269.832秒 | 285.340秒 | reviewer 3回 / root 0回 |
| Sonnet | 1 | [31269234148](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269234148) | satisfied | 4 | 1,539,180 | 447.768秒 | 460.225秒 | reviewer 14回 / root 0回 |
| Sonnet | 2 | [31269611823](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269611823) | satisfied | 0 | 1,765,770 | 370.624秒 | 384.687秒 | reviewer 21回 / root 0回 |
| Sonnet | 3 | [31269923611](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31269923611) | satisfied | 4 | 1,021,924 | 248.640秒 | 265.408秒 | reviewer 7回 / root 0回 |

- [Opus repetition 1](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-opus-r1-a31269234142.json)、SHA-256 `91cfd9e39bca884e6ccc852e5e4f9fef36b20a05789be74499a2559518db365a`
- [Opus repetition 2](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-opus-r2-a31269414636.json)、SHA-256 `c94b2debeb953211cb8180344a62eb4fa4831138f12e1fa23682d7d161cbe4cd`
- [Opus repetition 3](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-opus-r3-a31269611740.json)、SHA-256 `a942641f8de59e344cb179974a116483069df948662788482ac3a167c8120006`
- [Sonnet repetition 1](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-sonnet-r1-a31269234148.json)、SHA-256 `1a32dc938e816c5b3cacbcc6a1b4e21d09f31aa180218a13284c5da9a66035cb`
- [Sonnet repetition 2](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-sonnet-r2-a31269611823.json)、SHA-256 `39e346297671711b59db73bf2da85e93c43fa6bb8d3684e047fd84c9c322edbb`
- [Sonnet repetition 3](pr-review-relationship-reviewer-model-calibration-r1-prr-c01-relationship-reviewer-sonnet-r3-a31269923611.json)、SHA-256 `954a6abac9dd0baff5c76abf3ddbe0ccac0f7211539abd19b2ed73c784708086`

## 3 KPIの記述値

| reviewer model | quality score | all-agent tokens 平均 / 中央値 | review時間 平均 / 中央値 | execution時間 平均 / 中央値 |
| --- | --- | ---: | ---: | ---: |
| Opus | `4 / 4 / 4` | 713,852.7 / 637,780 | 207.857秒 / 184.554秒 | 222.802秒 / 200.322秒 |
| Sonnet | `4 / 0 / 4` | 1,442,291.3 / 1,539,180 | 355.677秒 / 370.624秒 | 370.107秒 / 384.687秒 |

これらは同じfixtureと固定review体制でreviewer modelだけを変えたN=3の記述値である。小標本であり、分布推定や他caseへの一般化には使わない。fixture tool call数はreviewerの調査挙動を確認する診断情報であり、KPIではない。
