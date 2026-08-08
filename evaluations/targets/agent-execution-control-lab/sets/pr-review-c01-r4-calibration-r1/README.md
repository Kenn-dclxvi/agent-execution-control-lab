# PRR-C01/r4 calibration r1

- set identity: `pr-review-c01-r4-calibration-r1 / r1`
- membership: `PRR-C01/r4`
- target ref: `8cd97283e60f13393fb1302c601c9a4fe0a5381f`
- purpose: Core Baselineの実行結果を受けたWorkflow Freeと将来のreview体制・model構成の校正
- held-out: false

PRR-C01/r4は過去のCore実行後に作成されたため、品質の最終評価には使わない。校正runでは品質を観測するが、findingのmissだけで後続反復を停止しない。実行または計測が不成立の場合だけ、未発行の反復を停止する。
