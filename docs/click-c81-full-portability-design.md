# Click C81全文水平適用の設計記録

## 結論

Click Bundle Bは、THE-CAPTION Candidate81のroot `AGENTS.md`本文を改変せず、Clickのroot `AGENTS.md` 1 targetへ適用する。比較軸はControl-Freeに対するC81全文の有無である。個別predicateの因果効果は分離せず、確立済みprompt set全体の外部妥当性を検証する。

## Candidate作成前gate

1. 基準prompt setは`click-00e592c-control-free-r1`とする。最短正常経路は、固定TaskSpecとrepository stateから必要な変更を行い、明示されたrequired validationを完了して停止する経路である。
2. Click Control-Free Std14は70 / 70件がscore `4`だった。一方、保存済みF08 5 traceは3 required validationを3回のmodel stepへ分割し、全成功後も追加readを1回行った。
3. TaskSpecはrequired commandを固定するが、promptなしでは、独立commandの同一model step発行、全result受領後の一回判断、成功後の停止を拘束しない。
4. 変更する一つの軸は、空のroot `AGENTS.md`を、THE-CAPTION Candidate81のroot `AGENTS.md`全文へ置換することである。移植時に文面、label、predicateを変更しない。
5. この構成差が消すと想定する判断経路は、THE-CAPTIONで観測された仕様未確定時の先行実行、不要なproducer/context伝播、独立invocation間のmodel再入、検証成功後の追加readである。個別predicateへの効果帰属は行わない。
6. 増えるのは11 labelの読解、operation/producer/result binding、例外条件である。Clickに存在しないrepository固有reference fileやpath-scoped promptは追加しない。
7. 品質は既存C81のTHE-CAPTION targetedおよびStd14で確認済みである。水平適用の主試験はClick `click-standard14-r1`、Rating v10、High、N=5とし、70 / 70 valid・rateable、score `4`分布をControl-Freeと比較する。
8. Std14ではControl-Free比のquality、all-agent token、elapsedの絶対値、差、率を比較する。複数required command caseの1-step closureと、全成功後の追加read / validationは診断として集計する。
9. Click Std14で品質低下、required command欠落、protocol違反、許可外driftのいずれかがあれば、効率値にかかわらずClick向け最適化へ採用しない。個別predicateの原因調査は別試験とする。

## THE-CAPTION参照差

同一Rating v13、Medium、Std14 N=5におけるControl-Free RepositoryからCandidate81への差は次のとおりである。

| KPI | Control-Free | Candidate81 | C81 - Control-Free | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | `92.857` | `100.000` | `+7.143` | `+7.69%` |
| all-agent token中央値 | `3,496,976` | `1,917,979` | `-1,578,997` | `-45.15%` |
| elapsed中央値 | `1,250.057`秒 | `1,003.744`秒 | `-246.313`秒 | `-19.70%` |

Clickではrating contract、reasoning effort、target repositoryが異なるため、この絶対値を同一比較へ混ぜない。方向と効果量を外部妥当性の参照値として扱う。

## 変更境界

- source content: `the-caption-3ce91a4-validation-wrapper-precedence-r1`のroot `AGENTS.md`
- Click baseline: `click-00e592c-control-free-r1`
- target map: root `AGENTS.md` 1件
- 非変更: Click case、TaskSpec、rating v10、runtime r2、model、reasoning High、M=24
- adoption / release / pallets/click projection: 未実施

## Evidence

- [Candidate81設計](candidate81-validation-wrapper-precedence-design.md)
- [THE-CAPTION Candidate81 Std14結果](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [Click Control-Free Std14結果](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
