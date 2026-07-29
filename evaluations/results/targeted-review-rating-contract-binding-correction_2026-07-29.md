# F10 / D01 targeted review rating contract binding訂正

## 結論

F10 / D01用の個別監査scriptが、評価cycleに固定されたrating contract IDを採点関数へ渡さず、既定値のv10で判定していた。v11以降はnumericな`path:line`不一致をdiagnostic-onlyとするため、v13 / v14の2 runを誤ってscore `3`にしていた。

保存済み応答を変更せず、cycleの正しいcontract IDを明示して再評価した。C81 D01 iteration 3とC87 D01 iteration 2は、finding内容、severity、impact、required evidenceを満たし、location mismatchだけが残るため、いずれもscore `4`である。モデル再実行はしていない。tokenとelapsedも変更していない。

## 影響範囲

同じ監査実装を持つv13 / v14 campaignは8件だった。うち7件は実行済みで、合計35 valid runを保存応答から再検査した。35件すべてで正しいcontractによるquality failureは0件だった。

- C81 v14 planning-first D01
- C81 v13 D01
- C81 v13 F10
- C82 v13 D01
- C82 v13 F10
- C83 v14 D01（準備のみ。run / resultなし）
- C86 v14 D01
- C87 v14 D01

公式scoreが変わるのは次の2 runだけである。他の33 runは旧監査でもscore `4`だったため、scoreは変わらない。C83 D01は未実行であり、結果訂正の対象ではない。

| candidate | run ID | 旧result | 旧score | 訂正result | 訂正score |
| --- | --- | --- | ---: | --- | ---: |
| C81 v13 D01 iteration 3 | `f06ed8ebb34745e986d45f749a09ab98` | `d11c7f2b08be4f1088bd684d9a20a51c` | 3 | `b07f9bc31b134b15acd81f378b66a61b` | 4 |
| C87 v14 D01 iteration 2 | `5b1a0ed2c0ef47e2a6fc17e58eb9a4c2` | `06e34a45334343a1ba9d55ba219bae1e` | 3 | `27b73ffe18bf47a99e15541c91c9d6e5` | 4 |

旧resultはimmutable historyとして残す。訂正resultは同じ保存済みexecution evidenceと同じcompatibility keyへappend-only登録した。

| 訂正result | content SHA-256 | compatibility key | score分布 |
| --- | --- | --- | --- |
| `b07f9bc31b134b15acd81f378b66a61b` | `f01bb05b53813813d7d36c88639a7cb69f815dd88df8ec777eec4d3c8a9f2a8b` | `c25f117849daacadaca98d3e1487a269a48c921ac56c8a6990b702a0952f916d` | `4 = 5` |
| `27b73ffe18bf47a99e15541c91c9d6e5` | `e1858ecc50df7f46b64290d7922bea2899339b0acb9cd90469ac0ef3049d356d` | `32332fd9e9d519812fb75613fd7d99d47ecb288253af5479f60c32befb2cf7c6` | `4 = 5` |

## 原因と恒久対策

原因はrating policy自体ではなく、個別監査からpolicyを呼ぶ境界にあった。`monthly_review_failures()`と`monthly_review_rating()`の既定値がv10だったため、cycleがv13 / v14でも古い規則が暗黙適用された。

今後のF10 / D01保存証拠監査は`scripts/targeted_review_quality_audit.py`を使う。このscriptはvalid bindingからcycleのcontract IDを取得し、採点関数のkeyword-only必須引数として渡す。contract ID省略時にv10へfallbackする経路は持たない。

numeric locationは診断情報として保存する。ただしv11以降ではquality scoreを変更しない。exact coordinateをhard requirementにしない既存方針と一致する。

## 状態への影響

- C81 / C82 targeted gate: Candidate82の通過判断は変わらない。C81 D01の品質分布だけを`5 / 5 score 4`へ訂正する。C81のroot再読1件はroute diagnosticとして残す。
- C87 D01: quality gate、producer route、C86比cost gateを通過する。保存済みC81との比較ではtoken中央値`-14,694`（`-10.29%`）、elapsed中央値`+6.606秒`（`+7.12%`）で、両KPI悪化の停止条件には該当しない。
- 訂正時点のC87状態: `targeted_d01_evaluated / qualification_passed / f02_not_run`。

## 後続result

訂正後に既存F02 r1を変更せず実行した。[`F02 result`](candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md)は5 / 5 score `4`でgateを通過し、現在状態は`targeted_d01_f02_evaluated / proceeding_to_f04`である。
