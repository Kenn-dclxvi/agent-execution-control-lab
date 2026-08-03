# Candidate161 独立作業の担当と結果の閉鎖一文 D01試験設計

## 結論

Candidate161は、Freeの0-byte root `AGENTS.md`へ、独立作業の担当・判定対象・必要結果を対応づけ、担当結果の受領後に同じ判定をやり直さない一行だけを追加する。D01をN=5で確認する。

## 固定root prompt

```text
独立した作業を分ける場合は、開始前に担当、判定対象、必要な結果を対応づけ、担当の完了結果だけを受け取り、同じ判定を別の担当や進捗報告でやり直して補わない。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準 | Candidate160と同じFree D01 N=5 |
| 行動条件 | 起動前の担当・対象・結果の対応づけがFreeより1件以上増える |
| 閉鎖条件 | worker結果後にrootが同じdiffとsourceを再読してreviewしない |
| 品質条件 | score `4`が4 / 5件以上で、worker result欠落がない |
| 停止条件 | 行動差0件、root重複review、score `3`以下が2件以上、worker result欠落、excluded attempt、controller error、または評価不能があれば掲載しない |

prompt identity以外はCandidate160と同じD01 profileへ固定し、Free結果へのpreflightを通してから5 runだけを発行する。

## 評価結果

5 / 5件がscore `4`で、worker result欠落とrootの重複reviewはなかった。worker起動前に担当identity、判定対象、必要な結果を対応づけた実行はFreeの`1 / 5件`からCandidate161の`5 / 5件`へ増えた。

token中央値は`299,897 → 301,810`、elapsed中央値は`125.563秒 → 135.255秒`であり、cost低下は観測していない。詳細は[`D01 N=5結果`](../evaluations/results/candidate161-free-assignment-result-closure-readable-v14-medium-d01-n5-cli0146_2026-08-04.md)を正本とする。

## 評価後state

`targeted_d01_n5_evaluated / score4_5_of_5 / assignment_mapping_1_to_5 / duplicate_review_0_of_5 / behavior_effect_observed / cost_reduction_not_observed / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
