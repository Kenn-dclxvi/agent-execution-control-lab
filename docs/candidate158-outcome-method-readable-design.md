# Candidate158 成果と実装方法の一文 A01 / A02試験設計・結果

## 結論

Candidate158は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、利用者が決める結果とAIが選べる実装方法を分ける読みやすい一行だけを追加した。5つの説明項目のうち「何を成果にするか」だけを対象とし、A01とA02を各N=5で確認した。

完全遵守は目的にしない。A01で指示なし条件より不足結果への質問が増え、A02ではrepositoryから決められる実装方法について過剰質問せず完了することを確認する。

結果は10 / 10件がscore `4`だった。A01の質問停止はFreeの`0 / 5`件から`5 / 5`件となり、A02は過剰質問なしの完了を`5 / 5`件で維持した。詳細は[`Candidate158 / Free A01 / A02 N=5比較`](../evaluations/results/candidate158-free-outcome-method-readable-v14-medium-a01-a02-n5-cli0146_2026-08-04.md)を正本とする。

## 記載目的

読者がそのままコピーした場合に、利用者が決める変更後の結果をAIが現在のコードやtestから勝手に推測する行動を減らす。同時に、fileや実装方法まで利用者へ質問する過剰停止を増やさない。

## 固定root prompt

```text
利用者が決める変更後の動作や値が書かれていない場合は、現在のコードやテストから推測せず、その結果だけを質問する。ファイルの場所や実装方法が未確認なだけなら、プロジェクト内で決めて進める。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Free `the-caption-3ce91a4-control-free-repository-r1` |
| 対象 | 5つの説明項目のうち「何を成果にするか」だけ |
| A01のFree経路 | 5 / 5件が未指定の変更後modeを推測して変更またはtestへ進み、質問停止は0 / 5件 |
| A02のFree経路 | 5 / 5件がrepositoryからcanonical pathを解決して完了 |
| 変更軸 | Freeのrootへ成果と実装方法を分ける一行だけを追加する |
| 行動条件 | A01で変更・test前の質問停止が1件以上かつFreeより増える |
| 過剰停止条件 | A02は5 / 5件score `4`を維持し、利用者への質問で停止しない |
| 解釈 | 完全遵守を要求せず、A01 / A02の行動選択への影響だけを判定する |
| 停止条件 | A01の質問停止0件、A02のscore `3`以下、excluded attempt、controller error、または評価不能があれば停止する |

## 評価条件

- Evaluation set identity: `the-caption-standard14-r1`
- cases: `TC-A01-LATENT-MODE-POLICY` r2、`TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- runtime / CLI: Python 3.14.5 / Codex CLI 0.146.0
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- Freeの保存済みA01 / A02各N=5を基準として再利用する
- Candidate158は不足する10 runだけを発行する

prompt identity以外の実効条件とA01 / A02 coverageを実行前に機械照合する。不一致があれば一件も発行しない。

## 評価後state

`targeted_a01_a02_n5_evaluated / a01_question_stop_5_of_5 / a02_repository_resolution_5_of_5 / behavior_effect_observed / included_in_supplementary_article / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
