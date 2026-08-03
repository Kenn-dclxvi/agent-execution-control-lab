# Candidate160 / Free 担当と結果一文 Rating v14 Medium D01 N=5停止結果

## 結論

Candidate160では、worker起動前に担当identity、判定対象、必要な結果を対応づけた実行がFreeの`1 / 5件`から`5 / 5件`へ増えた。5 / 5件はscore `4`だった。

ただしCandidate160の1 / 5件で、worker result受領後にrootが同じdiffとsourceを再読し、同じreviewをやり直した。事前停止条件に従い、この文は読者向け例へ掲載しない。Candidate161では、担当の完了結果だけを受け取り、同じ判定をやり直さない条件まで一文へ含めた。

## 固定した一文

> 独立した作業を分ける場合は、作業ごとに担当、判定対象、必要な結果を開始前に対応づけ、欠けた結果を別の担当や進捗報告で補って完了にしない。

## 結果

| 指標 | Free | Candidate160 |
| --- | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 |
| 起動前の担当・対象・結果対応 | 1 / 5 | 5 / 5 |
| rootによる同一reviewのやり直し | 0 / 5 | 1 / 5 |
| all-agent total token中央値 | 299,897 | 319,765 |
| elapsed中央値 | 125.563秒 | 120.532秒 |

FreeとCandidate160は同じD01 Layer 1、TaskSpec、rating、model、runtime、permission、executor parameterへ固定した。Free result IDは`64d4fa1491844bd0897ba9b28a7700a2`、Candidate160 result IDは`b1b50aa4498f4b4d8db8992370e7ce48`である。

## 状態境界

`targeted_d01_n5_evaluated / score4_5_of_5 / assignment_mapping_1_to_5 / duplicate_root_review_1_of_5 / stopped / not_published / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`

