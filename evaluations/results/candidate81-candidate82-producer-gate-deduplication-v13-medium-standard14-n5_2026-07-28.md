# Candidate81 / Candidate82 producer gate重複削除 Rating v13 Medium 標準14項目 N=5

## 結論

Candidate82は標準14項目70 / 70件でvalid・rateable・score `4`となり、quality gateを通過した。excluded attempt、quality failure、command protocol違反、workspace driftは0件だった。保存session証跡では70 / 70件がroot-onlyで、`PRODUCER` P3削除による不要worker起動は観測しなかった。

互換な既存Candidate81 resultも70 / 70件がscore `4`、root-onlyだった。Candidate82はtargeted F10 / D01 10 / 10に続き、標準14でも品質とrouteを維持した。したがってCandidate82を`standard14_evaluated / quality_gate_passed / targeted_gate_passed`とする。

3 KPI中央値差はquality `0.000`、all-agent token `+43,774`（`+2.28%`）、elapsed `-65.273秒`（`-6.50%`）だった。tokenとelapsedの方向が分かれ、M=24の別campaign間比較でもあるため、runtime効率改善は主張しない。採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

| 条件 | 値 |
| --- | --- |
| evaluation set | `the-caption-standard14-r1` revision `r1` |
| case | 14項目 |
| repetition | 各`N=5`、計70 slot |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| schedule | global queue、`M=24` |
| command evidence protocol | v1 |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| evaluation set identity SHA-256 | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| comparison conditions SHA-256 | `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb` |
| compatibility key | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` |

Candidate82 profileはCandidate81 profileから`profile_id`と`prompt_set_identity`だけを変更した。既存Candidate81 resultは同じcompatibility keyを持つため再実行せず、固定参照した。

## Prompt identity

| prompt | bundle SHA-256 | root `AGENTS.md` bytes |
| --- | --- | ---: |
| Candidate81 `the-caption-3ce91a4-validation-wrapper-precedence-r1` | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` | 5,525 |
| Candidate82 `the-caption-3ce91a4-producer-gate-deduplication-r1` | `a5a8dad8d615f4075bd399938bd621f9906d9b71c9de59425815be63027201cd` | 5,393 |

Candidate82は`PRODUCER`のP3一文だけを削除した。`OWNER_ROLE`の完全な明示producer gate、Candidate81の`VALIDATION_CLOSURE`、残り18 targetは維持した。

## 一次result

| prompt | result ID | content SHA-256 | valid / rateable | score分布 | excluded attempt |
| --- | --- | --- | ---: | --- | ---: |
| Candidate81 | `d97458bb526b41b094f92a5c35409326` | `ebe4f772ac0d9584ead7a63769a1f2ee13c04590db9b14527ccc76bbdfca09f8` | 70 / 70 | `4 = 70` | 0 |
| Candidate82 | `039b1b1afa6c41ef9012eb93860c594b` | `750822a2e8e481561970f49d3ecf13da0a4492485937ac16cbfec30f5d1ffd62` | 70 / 70 | `4 = 70` | 0 |

Candidate82 campaignは70件を再試行なしで完了し、result登録とfinal compactまで完了した。F10 Monthlyのnumeric locationは5 / 5で`exact`だった。

## 3 KPI

| KPI | Candidate81 | Candidate82 | C82 - C81 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 1,917,979 | 1,961,753 | +43,774 | +2.28% |
| elapsed中央値 | 1,003.744秒 | 938.471秒 | -65.273秒 | -6.50% |
| 70件token合計 | 9,502,252 | 9,740,800 | +238,548 | +2.51% |
| 70件elapsed合計 | 4,993.269秒 | 4,683.066秒 | -310.204秒 | -6.21% |

Candidate82はiteration別elapsedがCandidate81より4 / 5で小さかった。一方、tokenは中央値と合計が増えた。並行campaignのelapsedは環境変動を含むため、今回の値だけからP3削除固有の速度改善とは判断しない。

## Routeと品質診断

| diagnostic | Candidate81 | Candidate82 |
| --- | ---: | ---: |
| root-only | 70 / 70 | 70 / 70 |
| child session | 0 | 0 |
| score `4` | 70 / 70 | 70 / 70 |
| command protocol violation | 0 | 0 |
| F10 Monthly numeric location exact | 5 / 5 | 5 / 5 |
| owner-producer evidence inadmissible | 55 | 55 |

標準14 TaskSpecは独立producer executionを明示しない。両promptとも全70件でchild session 0だったため、P3削除後も明示指定のないoperationをworkerへ誤routingしていない。

`owner-producer-evidence/v1`の非適格55件はRating v13ではdiagnostic onlyである。all-agent usageに固定されたsession集合を直接監査し、worker起動有無を判定した。

## 判定境界

- 事実: Candidate82は標準14項目70 / 70でscore `4`、zero drift、root-onlyを維持した。
- 事実: targeted F10 / D01を含め、P3削除による品質低下またはroute欠落は観測しなかった。
- 事実: token中央値と合計は増え、elapsed中央値と合計は減った。
- 判断: Candidate82はstandard14 quality gateを通過した。
- 未判断: 採用、release、runtime projection。

Candidate82へ補助predicateを追加しない。採用またはreleaseへ進める場合は、この評価resultとは別のapproval operationとして扱う。

## 保存artifact

- Candidate81 result: `d97458bb526b41b094f92a5c35409326`
- Candidate82 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate82-producer-gate-deduplication-v13-reasoning-medium-standard14-global-m24-n5-20260728-r1`
- Candidate82 execution archive SHA-256: `2a635cb0fdd81ddc8206f562de7ff4c3e479a54c2d45bda3bf820be0c552b3d6`
- Candidate82 final archive SHA-256: `a3a47f2092f8f571feac199e178759a5c79582b4a0a4cfdddf31c436ba91bf1e`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5-20260728-r1.json`
- route audit: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate82-producer-gate-deduplication-v13-reasoning-medium-standard14-global-m24-n5-20260728-r1/route-audit-v1.json`
