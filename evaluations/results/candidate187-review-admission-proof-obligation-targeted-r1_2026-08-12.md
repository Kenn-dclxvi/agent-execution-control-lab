# Candidate187 review admission proof obligation targeted r1

> **位置づけ**: development Target gate／6ケース各N=5 valid／quality・mechanism通過／expanded評価未実施

## 結論

Candidate187を固定6ケース各`N=5 valid`で評価し、30 / 30 valid、除外0件、Score `4 = 30 / 30`、機構成立30 / 30だった。作成前に固定したquality gateとmechanism gateは全件通過した。

Candidate173問題資格確認で`TC-TPO04`の3 / 5件に観測した、必要reviewを`not_required`として省略したままartifact／terminal判定へ進む誤経路は0 / 5件となった。Candidate187では`TC-TPO04`の5 / 5件で独立reviewerが一件起動し、`no_counterexample_found`の後にartifactを`after`へ変更して`completion_ready`となった。

controlも維持した。`TC-TPO05`はreview 0 / 5件のまま全件を正しく完了し、`TC-TPO06`はreview 0 / 5件、先行result採用0件、root代行0件、artifact変更0件のまま全件`unavailable`で停止した。

これは固定6ケースN=5のdevelopment Target gate通過である。review admissionの完全性、expanded評価、Standard14、採用、releaseまたはprojectionを示さない。

## 一次証拠

- registered result: [`6beba1310ada4a6fb04755a1e7131b11.json`](6beba1310ada4a6fb04755a1e7131b11.json)
- mechanism audit: [`candidate187-review-admission-proof-obligation-targeted-r1-audit.json`](candidate187-review-admission-proof-obligation-targeted-r1-audit.json)
- result ID: `6beba1310ada4a6fb04755a1e7131b11`
- result content SHA-256: `4a3edbe7498589018395b052139fd30ebf47df57ad00e88ee70eb54172eb4fab`
- result file SHA-256: `d7de04f7166c3f221cc33f32e6f1548373a1b42f7eb9f2c178b2851807e7f17a`
- audit file SHA-256: `6d6f98a1c7915691defd1672122f22e10a816b0a09ab032b3b92b8054c37714c`
- atomic pool key: `20f2c6f5ee90272f04f444d32a904e89f5bdfee2d80ccf744093ce5f9a93a873`
- comparison key: `ea87a72420bcda10cc71b0c24415311f9346e5e0541a39423c54f097ce1f650c`

## case別結果

| case | Score 4 | 機構成立 | 独立reviewer | disposition／artifact |
|---|---:|---:|---:|---|
| `TC-TPO01` | 5 / 5 | 5 / 5 | 5 / 5 | `counterexample_found`、`before` |
| `TC-TPO02` | 5 / 5 | 5 / 5 | 5 / 5 | `unavailable`、`before` |
| `TC-TPO03` | 5 / 5 | 5 / 5 | 5 / 5 | `unavailable`、`before` |
| `TC-TPO04` | 5 / 5 | 5 / 5 | 5 / 5 | `no_counterexample_found`、`after` |
| `TC-TPO05` | 5 / 5 | 5 / 5 | 0 / 5 | reviewなし、`after` |
| `TC-TPO06` | 5 / 5 | 5 / 5 | 0 / 5 | reviewなし、先行result不採用、`before` |

## Candidate173診断対照との対応

prompt以外の互換条件はcomparison preflightで一致した。Candidate173からCandidate187への観測差は次のとおりである。

- Score `4`: `30 / 30 -> 30 / 30`
- 機構成立: `27 / 30 -> 30 / 30`
- `TC-TPO04`必要reviewer: `2 / 5 -> 5 / 5`
- 対象誤経路: `3 / 5 -> 0 / 5`
- `TC-TPO05`不要review: `0 / 5 -> 0 / 5`
- `TC-TPO06`review／先行result採用／変更: いずれも`0 / 5`を維持

この差は、固定6ケースN=5における`REVIEW_ADMISSION_PROOF`の方向性証拠として扱う。別case、長期安定性またはreview terminal全体へ一般化しない。

## KPI

6ケースをまとめたiteration単位の中央値はquality `100.0`、all-agent total token `806,555`、elapsed `443.868秒`だった。5 iterationのtoken合計は`3,994,365`、elapsed合計は`2,221.501秒`、parallel runner wall elapsedは`125.413秒`である。

互換なCandidate173診断対照中央値に対して、tokenは`+3.97%`、elapsedは`-1.46%`だった。これはTarget gateの記述値であり、費用または速度改善を主張しない。

## 判定

- quality gate: `passed`
- mechanism gate: `passed`
- targeted gate: `passed`
- expanded evaluation: `not_started`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

## 状態

`thirty_of_thirty_valid / score4_thirty_of_thirty / mechanism_thirty_of_thirty / tc_tpo04_reviewer_five_of_five / repeated_error_route_zero / controls_preserved / targeted_gate_passed / expanded_not_started / not_adopted / not_released / not_projected`
