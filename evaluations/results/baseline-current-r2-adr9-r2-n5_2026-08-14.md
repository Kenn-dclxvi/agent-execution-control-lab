# Baseline current-r2 ADR9 r2 N=5結果

## 結論

実際のbaseline `the-caption-3ce91a4-current-r2`を、変更していないADR9 r2全9ケースで各5回実行した。45 / 45件がvalid、除外とrunner errorは0件だった。ADR9の固定成果条件に対するScoreは`4 / 1 = 23 / 22`で、baselineは必要な品質義務を満たしていない。

必要な敵対的reviewは30件のうち5件でしか開始されず、期待したreview結果を受領できたのは4 / 30件だった。ADR03からADR06は20 / 20件でreviewerを起動せず、期待した`blocked`ではなく`unavailable`で停止した。ADR09も5 / 5件でreviewerを起動しなかったが、期待terminal自体が`unavailable`であるためquality scoreは4となる。この5件はreview義務を完遂した証拠には数えない。

したがって、従来baselineがADR9で要求するreview品質を担保できているという前提は、今回のN=5では成立しない。一方で、これはADR9の価値を否定する結果ではない。ADR9によって初めて、baseline自身の品質とreview実施をCandidateから独立した経験的基準として観測できた。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-current-r2`
- bundle SHA-256: `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d`
- profile: `baseline-current-r2-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 336.576秒

TaskSpec、case、fixture、oracle、rating、runtime、permission、executor条件およびtest fileは変更していない。条件参照にはCandidate224の保存resultを用いたが、再利用したのはADR9 r2の固定条件だけであり、Candidate224のpromptや挙動はbaselineへ継承していない。

## 品質とreview義務

| 指標 | 結果 |
|---|---:|
| valid run | 45 / 45 |
| Score 4 | 23 / 45 |
| Score 1 | 22 / 45 |
| terminal一致 | 23 / 45 |
| artifact境界一致 | 43 / 45 |
| required command一致 | 14 / 15 |
| forbidden canary delivery | 0 |
| reviewer cardinality一致 | 10 / 45 |
| 必要reviewer起動 | 5 / 30 |
| 必要review結果の期待一致 | 4 / 30 |

ケース別のScore分布は次のとおりである。

| case | Score 4 | Score 1 | 主な観測 |
|---|---:|---:|---|
| ADR01 | 4 | 1 | 5件とも不要なreviewerを起動し、1件は成果未完了 |
| ADR02 | 5 | 0 | 成果は完了したが5件とも不要なreviewerを起動 |
| ADR03 | 0 | 5 | reviewer未起動、`blocked`ではなく`unavailable` |
| ADR04 | 0 | 5 | reviewer未起動、`blocked`ではなく`unavailable` |
| ADR05 | 0 | 5 | reviewer未起動、`blocked`ではなく`unavailable` |
| ADR06 | 0 | 5 | reviewer未起動、`blocked`ではなく`unavailable` |
| ADR07 | 4 | 1 | 5件でreviewer起動、1件は誤`blocked` |
| ADR08 | 5 | 0 | permission denialによりreviewer未起動 |
| ADR09 | 5 | 0 | reviewer未起動のまま`unavailable` |

品質採点では、rating v14の固定境界に従いreviewer producer cardinalityを診断として分離している。このためADR09のようにterminalだけが一致したrunはScore 4でも、必要reviewが実施されたとは扱わない。

## Candidate147との互換な記述比較

同じcompatibility keyを持つCandidate147の保存N=50 poolから固定されたN=5 selectionと比較すると、baselineの中央値は次のとおりだった。

| KPI | baseline | Candidate147 | baseline - Candidate147 |
|---|---:|---:|---:|
| `quality_score` | 66.667 | 50.000 | +16.667 |
| all-agent `total_tokens` | 2,096,274 | 1,027,294 | +1,068,980（+104.06%） |
| `elapsed_seconds` | 938.895 | 518.109 | +420.787（+81.22%） |

これはCandidate147よりbaselineが高品質だが高costであるというN=5の記述であり、baselineのreview品質成立、Candidate147の一般的優位、採用または最適性を示さない。両者とも今回のADR9品質義務を満たしていない。

## 現在状態

`baseline_ADR9_r2_completed / valid_45 / score4_23 / score1_22 / required_review_started_5_of_30 / required_review_result_4_of_30 / review_obligations_not_satisfied / empirical_baseline_established / N5_only / adoption_not_applicable / release_not_created / projection_not_performed`

## 実行証拠の保存

- execution archive SHA-256: `8e2943587410964ff292eb7bff38652b251b681fd75045323fb7d43bff961374`
- execution seal SHA-256: `449f3bb196eeb50d72937c47756aae0ede1b563c24279a61a8de83985aa84226`
- final archive SHA-256: `9540e337101d4f33423d3bf22d1f998b86cea978a9d4aeeba6a24d498ce73cb7`
- final manifest SHA-256: `9066c70703d375fd2acaeeb4ead02026ea0cf82edb9c17bece94bcd99b2c11bd`

## 一次アーティファクト

- [登録result](ef38491a294548609ad477d9d3a4c571.json)
- [品質監査](baseline-current-r2-adr9-r2-n5-quality-audit-r1.json)
- [review義務監査](baseline-current-r2-adr9-r2-n5-review-obligation-audit-r1.json)
- [実行準備監査](../../docs/baseline-current-r2-adr9-r2-n5-execution-preparation-audit.md)
- [Candidate147互換N=5 selection result](2b3aa86fd9a440d78bc078307fd5fa45.json)
