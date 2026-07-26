# Releases

評価済みcandidateを反映判断可能なbundleへ固定して置く。release作成だけでは採用承認またはTHE-CAPTION本体への反映を意味しない。

候補81は明示承認済みで、THE-CAPTIONへの投影待ちである。Rating v13 Medium標準14項目N=5でquality gateとprompt stability gateを通過した評価状態を保持する。

候補71は現在THE-CAPTIONへ投影済みであり、候補81の直接の巻き戻し先として維持する。候補43は過去の投影履歴として維持する。

候補41は直前の投影履歴と候補43の巻き戻し先として維持する。候補34は一旦キャンセルし、不採用または削除にはしていない。

| release identity | source candidate | evaluation | release status | approval | runtime projection |
| --- | --- | --- | --- | --- | --- |
| [`the-caption-3ce91a4-validation-wrapper-precedence-release-r1`](the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md) | `the-caption-3ce91a4-validation-wrapper-precedence-r1` | rating v13 Medium 標準14項目70 / 70 valid・rateable・score 4、quality / prompt stability gate通過 | `approved_for_projection` | `approved` | `not_projected` |
| [`the-caption-3ce91a4-validation-closure-release-r1`](the-caption-3ce91a4-validation-closure-release-r1/README.md) | `the-caption-3ce91a4-validation-closure-r1` | rating v12 標準14項目B18 1,260 / 1,260 valid、公式点数4 / 3 / 0 = 1,255 / 4 / 1、品質gate不通過 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-outcome-authority-boundary-release-r1`](the-caption-3ce91a4-outcome-authority-boundary-release-r1/README.md) | `the-caption-3ce91a4-outcome-authority-boundary-r1` | rating v10 標準14項目B18 1,260 / 1,260 valid、公式点数4 / 3 / 1 = 1,255 / 4 / 1 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1`](the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/README.md) | `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1` | rating v9 B18 1,080 / 1,080 valid、score 4 / 3 = 1,078 / 2 | `projected` | `approved` | `projected` |
| [`the-caption-3ce91a4-owner-result-state-separation-release-r1`](the-caption-3ce91a4-owner-result-state-separation-release-r1/README.md) | `the-caption-3ce91a4-owner-result-state-separation-r1` | rating v7 expanded 60 / 60 valid、score 4 = 60 / 60、C31比token中央値 -15.98% | `cancelled` | `cancelled` | `not_authorized` |
