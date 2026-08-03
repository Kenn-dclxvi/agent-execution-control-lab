# Candidate150 / Free F02・F04・F07 targeted N=5結果

## 結論

Candidate150は15 / 15件がscore 4で、書いた`IMPLEMENTATION / CHANGE`境界に対応する全成果bindも15 / 15件で成立した。Standard14は実施していない。

| gate | 実測 | 判定 |
| --- | ---: | --- |
| valid / rateable | 15 / 15 | pass |
| score 4 | 15 / 15 | pass |
| F02二つのsource effectを同時に接続 | 5 / 5 | pass |
| F04必要変更と既存`colSpan` relationを両立 | 5 / 5 | pass |
| F07 dependency pairを同時に修復 | 5 / 5 | pass |
| required validation完備 | 15 / 15 | pass |
| 部分変更・無変更停止 | 0 / 15 | pass |

## 固定条件

- candidate: `the-caption-3ce91a4-required-outcome-bind-readable-r1`
- bundle SHA-256: `4312aef46bafe0cd198d3e04967c6a55f971171b136c4a81bfb4e1f74171e36f`
- cases: F02 r1 / F04 r2 / F07 dependency r1
- rating / model / reasoning: v14 / `gpt-5.6-sol` / Medium
- CLI / Python / configured M / N: `0.146.0` / `3.14.5` / `24` / 各`5`
- reference: Free result `c8a59dbdc98d46418449557df6958221`
- candidate pool: `a3a0857eeda7e39d8cd42188c7ae8f534d6827b962dc4e4ee90a103d262143f8`
- selection: `93a9ed479cd6481aa8301ac66c1af727`
- registered result: `6417a0bee5ec439aa697ceff25c3fb2f`
- compatibility key: `1a160baf02c918304673639cae670d6d9bad5d235e33e965d641f60fef339d93`
- execution archive SHA-256: `0b8f5bfa06c32b1bff12510d6493a80591f8ace31ef22a861c75f8de21ac887e`
- final compact archive SHA-256: `20213ba5aac43b3ba5609a314be3ae28be932e7eff123b066774069e5d93ff66`

## KPI診断

3 case合計の中央値はCandidate150が711,410 token・263.416秒、Freeが732,360 token・244.153秒だった。差はtoken`-20,950`（`-2.86%`）、elapsed`+19.263秒`（`+7.89%`）であり、N=5のtargeted結果から全体cost改善は主張しない。

## 証拠境界

品質採点後に実行workspaceを一度sealしてからpre-seal observation不足へ気付き、検証済みarchiveから対象15 workspaceだけをlosslessに復元してquality auditを完了した。最終登録後は再度compactし、一次evidenceはarchiveへ保持した。

Candidate149 Standard14の先行campaignは、最終prompt完成前だったため中断した。未採点・未登録であり、本結果にも後続Standard14にも使わない。
