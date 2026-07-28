# Candidate81 / Candidate82 producer gate重複削除 Rating v13 Medium F10 / D01 N=5

## 結論

Candidate82は、Candidate81のroot `AGENTS.md`から`PRODUCER` P3の短い再記述だけを削除し、F10 root-onlyとD01明示producerのtargeted gateを通過した。Candidate82の10 / 10 runはscore `4`、zero drift、excluded attempt 0件だった。F10は5 / 5でchild session 0、D01は5 / 5でTaskSpec指定worker `/root/monthly_format_review_producer`を一度だけ起動し、rootによるreview対象の再読は0件だった。

同時実行したCandidate81はF10 5 / 5がscore `4`だった。D01はscore `4 / 3 = 4 / 1`で、score `3`の1件だけrootがreview対象を再読した。Candidate82ではこの低得点と誤経路を再現しなかった。削除したP3の意味欠落は、今回の2経路では観測しなかった。

Candidate82は`targeted_evaluated / targeted_gate_passed`とする。token中央値とelapsed中央値は両scopeで増えたため、runtime効率改善は主張しない。この結果はF10 r3とD01 r1、rating v13、reasoning effort `medium`、各`N=5`に限定する。標準14、採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 静的差分

| 項目 | Candidate81 | Candidate82 | 差 |
| --- | ---: | ---: | ---: |
| prompt identity | `the-caption-3ce91a4-validation-wrapper-precedence-r1` | `the-caption-3ce91a4-producer-gate-deduplication-r1` | — |
| bundle SHA-256 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` | `a5a8dad8d615f4075bd399938bd621f9906d9b71c9de59425815be63027201cd` | — |
| root `AGENTS.md` bytes | 5,525 | 5,393 | -132（-2.39%） |
| bundle target | 19 | 19 | 0 |

変更targetはroot `AGENTS.md`だけである。`OWNER_ROLE`の完全な明示producer gate、`PRODUCER`の残りのpredicate、Candidate81の`VALIDATION_CLOSURE`、残り18 targetは逐語維持した。

## 固定条件

| 条件 | 値 |
| --- | --- |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| model | `gpt-5.6-sol` |
| reasoning effort | `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| runtime / Codex CLI | `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0` |
| capability catalog SHA-256 | `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e` |
| memories / apps / plugins / plugin sharing | disabled |
| token accounting | all-agent / `v1` |
| repetition | 各scope、各prompt `N=5` |
| excluded attempt | 0 |

各pairは`profile_id`と`prompt_set_identity`以外を一致させた。F10とD01はEvaluation setが異なるため、別のcompatibility comparisonとして登録した。

| scope | Evaluation set | compatibility key |
| --- | --- | --- |
| F10 | `tc-f10-monthly-format-test-review-r3` | `8ed423934833a50267bdcddfe92b56402ad5a459f1dc4925edd4dc3ae563214d` |
| D01 | `tc-d01-explicit-producer-monthly-review-r1` | `c25f117849daacadaca98d3e1487a269a48c921ac56c8a6990b702a0952f916d` |

## 一次resultと品質

| scope | prompt | result ID | content SHA-256 | valid / rateable | score分布 |
| --- | --- | --- | --- | ---: | --- |
| F10 | Candidate81 | `f63d261635c64d82860628f4f0875a5f` | `37a266c16e14c4575a72d563c245a3bc1646656d2e97c71b5f4682396bc9e805` | 5 / 5 | `4 = 5` |
| F10 | Candidate82 | `67f7687ba8c944408422e705b5e90e01` | `d4eb10afcc12d16f515f38f80ea883a491a24624953ad8014fd2d3eb2698c2d1` | 5 / 5 | `4 = 5` |
| D01 | Candidate81 | `d11c7f2b08be4f1088bd684d9a20a51c` | `44b27a79defa4b964bdf9c8565070cd52388dc29a4be003f1062ba12615c7554` | 5 / 5 | `4 = 4 / 3 = 1` |
| D01 | Candidate82 | `513a3cd0f0d14223a174b82271a6340a` | `7ef619698e49f0b950e16b2f935f50f89edf3fccf29ca71d271b12bdd6c610c6` | 5 / 5 | `4 = 5` |

Candidate81 D01 iteration 3は、主要findingを特定したが指摘位置が実変更行と一致せずscore `3`だった。required command protocol違反も同じ1件にだけ記録された。Candidate82は10 runすべてでquality failureとcommand protocol違反が0件だった。

## 3 KPI

### F10 root-only

| KPI | Candidate81 | Candidate82 | C82 - C81 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 76,177 | 78,979 | +2,802 | +3.68% |
| elapsed中央値 | 58.300秒 | 67.572秒 | +9.273秒 | +15.90% |
| all-agent token合計 | 432,728 | 430,039 | -2,689 | -0.62% |
| elapsed合計 | 315.109秒 | 342.626秒 | +27.517秒 | +8.73% |

### D01 explicit producer

| KPI | Candidate81 | Candidate82 | C82 - C81 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 209,865 | 212,674 | +2,809 | +1.34% |
| elapsed中央値 | 118.337秒 | 125.476秒 | +7.139秒 | +6.03% |
| all-agent token合計 | 1,051,386 | 1,084,601 | +33,215 | +3.16% |
| elapsed合計 | 560.841秒 | 641.221秒 | +80.380秒 | +14.33% |

Candidate82のtoken中央値とelapsed中央値は両scopeで増えた。削除の目的は重複判断点の除去であり、targeted品質とrouteを維持すれば意味保持とは両立するが、今回の値からruntime効率改善は主張しない。

## 保存rolloutのroute診断

| route | Candidate81 | Candidate82 |
| --- | ---: | ---: |
| F10 child session 0 | 5 / 5 | 5 / 5 |
| D01 sessionがroot + 指定workerだけ | 5 / 5 | 5 / 5 |
| D01 `monthly_format_review_producer`を1回spawn | 5 / 5 | 5 / 5 |
| D01 childがreview対象をreadしてterminal resultを返却 | 5 / 5 | 5 / 5 |
| D01 rootのreview対象read 0 | 4 / 5 | 5 / 5 |

Candidate81でroot readが発生したのはscore `3`と同じrun `f06ed8ebb34745e986d45f749a09ab98`だった。Candidate82では指定worker欠落、追加worker、root再読、terminal result欠落を観測しなかった。

標準`owner-producer-evidence/v1`は、criterion ownerの語列とagent pathの一致を要求するため、汎用owner表記を持つF10 / D01を全20 runで`inadmissible`とした。これはrating v13ではdiagnostic onlyである。route判定は、all-agent usageに固定されたsession parent / child identityと、そのSHA-256を記録した保存rolloutのtool callを直接監査した。collectorの非適格をworker欠落へ読み替えていない。

## 判定境界

- 事実: Candidate82は対象2経路の10 / 10でscore `4`、期待route、zero driftを満たした。
- 事実: P3削除後も`OWNER_ROLE`の完全なgateだけでroot-onlyと明示producerを分離できた。
- 事実: token中央値とelapsed中央値は両scopeで増え、効率改善は確認しなかった。
- 判断: P3削除のtargeted意味保持gateは通過した。
- 未判断: 標準14全体の非回帰、採用、release、runtime projection。

Candidate82へ意味を補う文は追加しない。次へ進める場合は、今回のtargeted resultを変更せず、標準14を別profile・別resultとして実施する。

## 後続result

2026-07-28に[`標準14項目各N=5`](candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5_2026-07-28.md)を別resultとして実施した。Candidate82は70 / 70でscore `4`、root-onlyを維持し、standard14 quality gateを通過した。本targeted resultのidentity、数値、判定境界は変更しない。

## 登録証跡

| scope | prompt | execution archive SHA-256 |
| --- | --- | --- |
| F10 | Candidate81 | `6ff957c128040f566b2ecf6a97c8ab16b01263840931555d69d34fd23a5b2650` |
| F10 | Candidate82 | `aa0d12afea6c64c6b223ce354e3755dee2d9429b437c1a8970e8692c1bc4a389` |
| D01 | Candidate81 | `2967bea4aa7fc27c19631b7682cf79e5228ceac09fc113748346e74f589d4bcd` |
| D01 | Candidate82 | `cdc7255c004a1333272d41fa55b6dce024ac061d13524baecd5dc0e2cfaab64b` |

comparison views:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate82-producer-gate-deduplication-v13-medium-f10-n5-20260728-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate82-producer-gate-deduplication-v13-medium-d01-n5-20260728-r1.json`

derived route audit:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate82-producer-gate-deduplication-v13-reasoning-medium-fixed-evidence-review-f10-global-m10-n5-catalog-fixed-20260728-r1/route-audit-v1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate82-producer-gate-deduplication-v13-reasoning-medium-explicit-producer-d01-global-m5-n5-catalog-fixed-20260728-r1/route-audit-v1.json`
