# Candidate162 完了実行票の一文 F03試験設計

## 結論

Candidate162は、Freeの0-byte root `AGENTS.md`へ、必要な検証を実行票として先に固定し、結果がそろった後は追加確認せず完了を一度だけ判断する一行だけを追加する。F03をN=5で確認する。

## 固定root prompt

```text
変更後は、必要なテストと差分確認を一つの実行票として先に固定し、実行中は同じ結果だけを待ち、失敗なら後続を止め、全結果がそろったら追加確認せず一度だけ完了を判断する。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準 | Candidate152で使ったFree F03 N=5 |
| 行動条件 | 最初のcommandより前に、focused test、full validation、差分確認を完了条件として具体的に示すrunがFreeより1件以上増える |
| 閉鎖条件 | 同じrequired validationを根拠なく再実行せず、全結果の受領後に調査目的のcommandを追加しない |
| 品質条件 | score `4`が4 / 5件以上で、required outcomeとrequired validationを欠かさない |
| 停止条件 | 行動差0件、根拠のない再検証、score `3`以下が2件以上、excluded attempt、controller error、または評価不能があれば掲載しない |

prompt identity以外はCandidate152と同じF03 profileへ固定し、Free結果へのpreflightを通してから5 runだけを発行する。

## 評価結果

5 / 5件がscore `4`で、required validationの根拠のない再実行と、最終差分確認後の追加調査はなかった。最初のcommand前にfocused test、full validation、差分確認を具体的な実行票として示した実行はFreeの`0 / 5件`からCandidate162の`5 / 5件`へ増えた。

token中央値は`194,441 → 175,411`、elapsed中央値は`69.153秒 → 76.564秒`だった。tokenは`-9.79%`、elapsedは`+10.72%`であり、単一case N=5から料金全体へ一般化しない。詳細は[`F03 N=5結果`](../evaluations/results/candidate162-free-completion-ticket-readable-v14-medium-f03-n5-cli0146_2026-08-04.md)を正本とする。

## 評価後state

`targeted_f03_n5_evaluated / score4_5_of_5 / initial_completion_ticket_0_to_5 / validation_rerun_0_of_5 / behavior_effect_observed / mixed_cost_result / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
