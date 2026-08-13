# Candidate208 Standard14 N=5 結果

## 結論

Candidate208はStandard14全14ケースのN=5で70 / 70 valid、70 / 70 Score `4`だった。品質中央値はCandidate206と同じ100.0、全agent token中央値は1,605,899で45,285増（+2.90%）、経過時間中央値は864.158秒で40.618秒減（-4.49%）だった。

したがって、通常経路の品質は維持したが、costはtokenとelapsedが逆方向であり、Candidate206に対する一方向の優位は確認できない。ADR9で残った二つの機序逸脱は解消扱いにせず、Candidate208は引き続き`quality_passed / mechanism_failed`である。採用、releaseおよびruntime projectionは未決定である。

## 実行条件

- result: `7922b5fec056420bb558dd03e502ef66`
- prompt: `the-caption-3ce91a4-result-kind-evidence-domain-r1`
- bundle SHA-256: `be67f9dce76e57ac1b1f7535a4e1128f3f7b9f0b7810e55527d089d1cbd7f15f`
- Evaluation set: `the-caption-standard14-r1` r1
- coverage: 14ケース×5件
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: 24
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- comparison reference: Candidate206 result `0aba77ffad0848e5be7e635f96293070`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

## 品質

- valid: 70 / 70
- excluded attempt: 0
- Score `4`: 70 / 70
- command protocol violation: 0
- 月次reviewの数値位置: exact 5 / 5

owner/producer evidenceは55件で診断上不成立だったが、固定済みv14 contractでは`diagnostic_only`であり、Candidate206も同じ55件である。Candidate208追加文による増分とは扱わない。

## KPI

| prompt | 品質中央値 | 全agent token中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: |
| Candidate206 | 100.0 | 1,560,614 | 904.776秒 |
| Candidate208 | 100.0 | 1,605,899 | 864.158秒 |
| C208 - C206 | 0.0 | +45,285（+2.90%） | -40.618秒（-4.49%） |

外側parallel runnerの70件完了時間は210.202秒であり、分析上のiteration中央値とは別の実行指標である。

## 機序の扱い

Standard14は通常経路の測定として成功したが、Candidate208の明示review result kind境界を単独で識別する試験ではない。review名を持つ2ケース10件でも独立producer evidenceは0件だったが、Candidate206との差はなく、固定ratingでは診断情報である。

この結果はADR9の機序不通過を上書きしない。ADR05-i4の不要な再読とADR09-i5のroot prereadは既知の残差として保持する。

## 状態

- Standard14 quality: `passed`
- Standard14 mechanism diagnostic: `not_decisive`
- ADR9 mechanism: `failed`
- adoption: `not_decided`
- release: `not_decided`
- runtime projection: `not_authorized`
