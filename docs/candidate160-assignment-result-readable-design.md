# Candidate160 独立作業の担当と結果の一文 D01試験設計・停止結果

## 結論

Candidate160は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、独立作業の担当、判定対象、必要な結果を開始前に対応づける読みやすい一行だけを追加した。D01では、起動前の対応づけがFreeの1 / 5件から5 / 5件へ増えたが、1件でrootがworkerと同じreviewをやり直した。事前停止条件に従い掲載せず、Candidate161でやり直し防止まで一文へ含める。

完全遵守は目的にしない。指定workerを起動する前に、担当identity、review対象、返すべきfindingを同じ説明へ含める実行がFreeより増えることを確認する。

## 固定root prompt

```text
独立した作業を分ける場合は、作業ごとに担当、判定対象、必要な結果を開始前に対応づけ、欠けた結果を別の担当や進捗報告で補って完了にしない。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 対象 | 5つの説明項目のうち「誰が何を判定するか」だけ |
| case | D01。指定workerがmonthly format bindingをreviewし、findingを返す |
| 変更軸 | Freeのrootへ担当と結果を対応づける一行だけを追加する |
| 行動条件 | 最初のworker起動前に担当identity、判定対象、必要結果を対応づける実行がFreeより1件以上増える |
| 品質条件 | score `4`が4 / 5件以上で、指定worker result欠落とrootによる代替reviewがない |
| 解釈 | 完全遵守を要求せず、独立作業の担当と結果の対応づけへの影響だけを判定する |
| 停止条件 | 行動差0件、score `3`以下が2件以上、worker result欠落、root代替review、excluded attempt、controller error、または評価不能があれば掲載せず次案を検討する |

## 評価条件

- Evaluation set: `tc-d01-explicit-producer-monthly-review-r1`
- case: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW` r1
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- runtime / CLI: Python 3.14.5 / Codex CLI 0.146.0
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- 同じLayer 1をFreeとCandidate160へ適用する
- FreeとCandidate160を各5 runだけ発行する

一件目の発行前にfixture、TaskSpec、rating、model、runtime、permission、executor parameterを固定する。Candidate160はFree結果へprompt identity以外が一致するpreflightを通してから発行する。

## 評価後state

`targeted_d01_n5_evaluated / score4_5_of_5 / assignment_mapping_1_to_5 / duplicate_root_review_1_of_5 / stopped / not_published / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
