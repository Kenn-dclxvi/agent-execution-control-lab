# release索引

`the-caption`向けに固定したrelease bundleとライフサイクル状態を引くための索引である。release作成・approval・runtime projectionの境界と索引更新規則は[`../AGENTS.md`](../AGENTS.md)を正本とする。

各行の評価欄は索引用の要約であり、評価結果は対応する一次result、rollback identity・projection対象・PR / commit・未解決リスクは各release READMEを正とする。releaseアーティファクトの存在や評価上の`stopped`を、approvalまたはruntime projectionと同一状態として扱わない。

| release identity | source candidate | 評価 | release status | approval | runtime projection |
| --- | --- | --- | --- | --- | --- |
| [`the-caption-3ce91a4-result-effect-scope-release-r1`](the-caption-3ce91a4-result-effect-scope-release-r1/README.md) | `the-caption-3ce91a4-result-effect-scope-r1` | rating v14 Medium Standard14 N=100 1,400 / 1,400 score 4、targeted mechanism 15 / 15、C145比cost回収 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1`](the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1/README.md) | `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1` | rating v14 Medium Standard14 70 / 70 score 4、A02 N=20 20 / 20 score 4・bind後再入0件、token中央値1,401,225 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-validation-wrapper-precedence-release-r1`](the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md) | `the-caption-3ce91a4-validation-wrapper-precedence-r1` | rating v13 Medium 標準14項目70 / 70 valid・rateable・score 4、quality / prompt stability gate通過 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-validation-closure-release-r1`](the-caption-3ce91a4-validation-closure-release-r1/README.md) | `the-caption-3ce91a4-validation-closure-r1` | rating v12 標準14項目B18 1,260 / 1,260 valid、公式点数4 / 3 / 0 = 1,255 / 4 / 1、品質gate不通過 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-outcome-authority-boundary-release-r1`](the-caption-3ce91a4-outcome-authority-boundary-release-r1/README.md) | `the-caption-3ce91a4-outcome-authority-boundary-r1` | rating v10 標準14項目B18 1,260 / 1,260 valid、公式点数4 / 3 / 1 = 1,255 / 4 / 1 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1`](the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/README.md) | `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1` | rating v9 B18 1,080 / 1,080 valid、score 4 / 3 = 1,078 / 2 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-owner-result-state-separation-release-r1`](the-caption-3ce91a4-owner-result-state-separation-release-r1/README.md) | `the-caption-3ce91a4-owner-result-state-separation-r1` | rating v7 expanded 60 / 60 valid、score 4 = 60 / 60、C31比token中央値 -15.98% | `cancelled` | `cancelled` | `not_authorized` |
