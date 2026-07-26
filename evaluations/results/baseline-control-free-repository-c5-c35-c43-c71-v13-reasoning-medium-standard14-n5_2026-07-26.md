# Baseline / ControlFreeRepository / C5 / C35 / C43 / C71 Medium Rating v13 標準14項目 各5回

## 結論

Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43をreasoning `medium`で新規実行し、既存のCandidate71 `medium`と同じRating v13、標準14項目、各`N=5`、global queue `M=24`へ揃えた。6条件とも70 / 70件がvalidかつrateableで、result登録とfinal compactを完了した。

公式score分布はCandidate43とCandidate71が`4 = 70`だった。ControlFreeRepository、Candidate5、Candidate35は`4 / 0 = 65 / 5`で、score `0`はすべてA01だった。Baselineは`4 / 3 / 1 / 0 = 63 / 2 / 1 / 4`だった。

5反復中央値では、Candidate43が`quality_score = 100.000`、`total_tokens = 2,716,869`、`elapsed_seconds = 1,061.204秒`、Candidate71が`100.000`、`1,923,688`、`948.869秒`だった。Candidate71からCandidate43を引くと、`quality_score = 0.000`、`total_tokens = -793,181`（`-29.19%`）、`elapsed_seconds = -112.335秒`（`-10.59%`）である。

6条件とも既存High比で品質中央値を維持し、token中央値とelapsed中央値が小さかった。ただしreasoning effortはcomparison conditionであり、MediumとHighのcompatibility keyは異なる。この差はLayer 4の互換comparisonではなく記述的な差である。

このresultは3 KPIと診断を保存する。winner、採用、release、THE-CAPTION本体反映は判断しない。

## 固定条件

- evaluation set: `the-caption-standard14-r1` revision `r1`
- quality rating: `outcome-abstract-condition-preserving-owner-diagnostic-v13`
- rating contract SHA-256: `d2dd4096911c35257c2866872d071f2ee5137bb3dcb6a7b279853e3ebe581f1f`
- target repository: `THE-CAPTION@3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.144.0`、Python `3.14.5`、memories `false`
- permission: `workspace-write`、approval `never`
- repetition: 14 case × `N=5` = 70 slot
- schedule: global queue、`M=24`
- token accounting: all-agent / `v1`
- evaluation set identity SHA-256: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- comparison conditions SHA-256: `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb`
- compatibility key: `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8`

6 profileはprompt identity以外のcase、TaskSpec、permission、executor parameter、rating、反復条件を一致させた。5つの新規campaignは同時実行せず、Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43の順に実行した。

## 3 KPI

| 条件 | score分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 70件token合計 | 70件elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 1 / 0 = 63 / 2 / 1 / 4` | 92.857 | 11,977,774 | 3,568.742秒 | 64,096,747 | 18,583.648秒 |
| ControlFreeRepository | `4 / 0 = 65 / 5` | 92.857 | 3,496,976 | 1,250.057秒 | 17,173,925 | 6,225.500秒 |
| Candidate5 | `4 / 0 = 65 / 5` | 92.857 | 8,425,533 | 2,368.815秒 | 44,924,675 | 12,277.277秒 |
| Candidate35 | `4 / 0 = 65 / 5` | 92.857 | 4,920,365 | 1,716.646秒 | 23,912,141 | 8,535.144秒 |
| Candidate43 | `4 = 70` | 100.000 | 2,716,869 | 1,061.204秒 | 13,769,064 | 5,309.023秒 |
| Candidate71 | `4 = 70` | 100.000 | 1,923,688 | 948.869秒 | 9,475,504 | 4,754.179秒 |

Baselineとの差は記述的な差分であり、採用順位ではない。

| 条件 | quality中央値差 | token中央値差 | elapsed中央値差 | token合計差 | elapsed合計差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ControlFreeRepository - Baseline | 0.000 | -8,480,798（-70.80%） | -2,318.685秒（-64.97%） | -46,922,822（-73.21%） | -12,358.148秒（-66.50%） |
| Candidate5 - Baseline | 0.000 | -3,552,241（-29.66%） | -1,199.927秒（-33.62%） | -19,172,072（-29.91%） | -6,306.371秒（-33.94%） |
| Candidate35 - Baseline | 0.000 | -7,057,409（-58.92%） | -1,852.096秒（-51.90%） | -40,184,606（-62.69%） | -10,048.504秒（-54.07%） |
| Candidate43 - Baseline | +7.143 | -9,260,905（-77.32%） | -2,507.538秒（-70.26%） | -50,327,683（-78.52%） | -13,274.625秒（-71.43%） |
| Candidate71 - Baseline | +7.143 | -10,054,086（-83.94%） | -2,619.873秒（-73.41%） | -54,621,243（-85.22%） | -13,829.469秒（-74.42%） |

Candidate71とCandidate43の直接差は、token合計`-4,293,560`（`-31.18%`）、elapsed合計`-554.844秒`（`-10.45%`）だった。

## Highとの記述差

同じpromptごとにMediumから既存Highを引いた。reasoning effortが異なるため、互換comparisonや因果推定には使わない。

| 条件 | quality中央値差 | token中央値差 | elapsed中央値差 |
| --- | ---: | ---: | ---: |
| Baseline Medium - High | 0.000 | -591,059（-4.70%） | -59.805秒（-1.65%） |
| ControlFreeRepository Medium - High | 0.000 | -421,526（-10.76%） | -58.144秒（-4.44%） |
| Candidate5 Medium - High | 0.000 | -3,101,700（-26.91%） | -502.203秒（-17.49%） |
| Candidate35 Medium - High | 0.000 | -534,564（-9.80%） | -59.308秒（-3.34%） |
| Candidate43 Medium - High | 0.000 | -393,030（-12.64%） | -119.775秒（-10.14%） |
| Candidate71 Medium - High | 0.000 | -207,371（-9.73%） | -165.656秒（-14.86%） |

## 低得点

| 条件 | case | 件数 | 保存された主なfailure |
| --- | --- | ---: | --- |
| Baseline | A01 | 4 | 未固定値の確認前に変更・試験へ進行、または要求値未確定のまま終了 |
| Baseline | A02 | 2 | 1件は抽象的な既存test成功証拠不足、1件はcanonical routeと変更pathが未達 |
| Baseline | F07 dependency | 1 | model-visibleに明示されたdependency確認commandを未実行 |
| ControlFreeRepository | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate5 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate35 | A01 | 5 | 未固定値の確認前に変更・試験へ進行 |
| Candidate43 | — | 0 | — |
| Candidate71 | — | 0 | — |

BaselineのF07 canonicalで`command_evidence_incomplete`を4 attempt除外し、同じslotを再実行して70件のvalid resultを得た。他5条件のexcluded attemptは0件だった。

## 診断

診断値は3 KPIへ追加せず、quality scoreを変更しない。

| 条件 | command protocol violation | owner-producer evidence inadmissible | F10 Monthly数値line |
| --- | ---: | ---: | ---: |
| Baseline | 631 | 53 | exact 4 / mismatch 1 |
| ControlFreeRepository | 0 | 55 | exact 5 |
| Candidate5 | 227 | 30 | exact 5 |
| Candidate35 | 8 | 0 | exact 5 |
| Candidate43 | 0 | 55 | exact 3 / mismatch 2 |
| Candidate71 | 0 | 55 | exact 5 |

## 保存artifact

| 条件 | result ID |
| --- | --- |
| Baseline | `107d31cdae9044d08c0768ffc89d3896` |
| ControlFreeRepository | `3fb81b94ef1d4770b52bc202bf0a43d8` |
| Candidate5 | `ba2a17b3edd94ff2b084e2af41f9532c` |
| Candidate35 | `dcc7c7274ebd47e4964e577097c9c419` |
| Candidate43 | `4257136a9a8341c69be7ce2e007c7050` |
| Candidate71 | `267130a37c3544c7bb6e39c94f03c6e4` |

- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- comparison view: `comparison-views/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5-20260726-r1.json`
- campaign root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs`

5つの新規campaignに`batch-001/compact/final-compact-receipt.json`を保存した。既存Candidate71 Mediumにも同receiptがある。raw execution evidenceはrepositoryへcommitしない。
