# Candidate159 変更開始の一文 F02試験設計

## 結論

Candidate159は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、変更開始前に必要な成果全体を一つの方針へまとめる読みやすい一行だけを追加する。5つの説明項目のうち「いつ変更を始めるか」だけを対象とし、F02をN=5で確認する。

完全遵守は目的にしない。最初の変更前に、必要な成果、変更箇所、直し方、維持する動作を同じ方針へ含める実行がFreeより増えることを確認する。

## 記載目的

読者がそのままコピーした場合に、一部の成果だけを見て編集を始め、後から別の必要成果へ気付いて直し直す行動を減らす。

## 固定root prompt

```text
変更前に、必要な成果、変更箇所、直し方、維持する動作を一つの方針にまとめ、どれか決まらない間は変更しない。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Free `the-caption-3ce91a4-control-free-repository-r1` |
| 対象 | 5つの説明項目のうち「いつ変更を始めるか」だけ |
| case | F02。二つのsource effectと二つのtestを同じ変更で接続する |
| 変更軸 | Freeのrootへ変更開始境界の一行だけを追加する |
| 行動条件 | 最初のfile change前に4要素を含む方針を示す実行がFreeより1件以上増える |
| 品質条件 | score `4`が4 / 5件以上で、部分変更または無変更停止がない |
| 解釈 | 完全遵守を要求せず、変更開始前の方針形成への影響だけを判定する |
| 停止条件 | 行動差0件、score `3`以下が2件以上、部分変更、excluded attempt、controller error、または評価不能があれば掲載せず次案を検討する |

## 評価条件

- Evaluation set identity: `the-caption-standard14-r1`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- runtime / CLI: Python 3.14.5 / Codex CLI 0.146.0
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- Freeの保存済みF02 N=5を基準として再利用する
- Candidate159は不足する5 runだけを発行する

prompt identity以外の実効条件とF02 coverageを実行前に機械照合する。不一致があれば一件も発行しない。

## 評価結果

5 / 5件がscore `4`で、部分変更と無変更停止はなかった。最初のcommand前に、具体的な成果、変更対象・方法、維持する動作を同時に示した実行はFreeの`0 / 5件`からCandidate159の`4 / 5件`へ増えた。最初のfile changeまでには両条件とも`5 / 5件`が方針を形成していたため、確認できた効果は方針を早い段階で明示することに限る。

token中央値は`315,507 → 327,309`、elapsed中央値は`91.418秒 → 104.688秒`であり、cost低下は観測していない。詳細は[`F02 N=5結果`](../evaluations/results/candidate159-free-change-start-readable-v14-medium-f02-n5-cli0146_2026-08-04.md)を正本とする。

## 評価後state

`targeted_f02_n5_evaluated / score4_5_of_5 / initial_plan_0_to_4 / behavior_effect_observed / cost_reduction_not_observed / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
