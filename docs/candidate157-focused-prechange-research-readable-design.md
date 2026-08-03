# Candidate157 変更前調査一文 F08試験設計・結果

## 結論

Candidate157は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、変更前調査を不足情報だけへ絞る一文だけを追加した。5つの説明項目のうち「何を調べるか」だけを対象とし、F08各N=5でFreeとの差を確認した。

この一文は完全遵守や実運用版と同じ料金削減率を目的にしない。品質を悪化させず、変更前commandがFreeより減るという行動への影響を確認する。

結果は5 / 5件がscore `4`だった。変更前command中央値はFreeの`10`件から`7`件へ減り、token中央値は`-27.56%`、elapsed中央値は`-18.05%`だった。狙った行動への影響を確認した。詳細は[`Candidate157 / Free F08 N=5比較`](../evaluations/results/candidate157-free-focused-prechange-research-readable-v14-medium-f08-n5-cli0146_2026-08-04.md)を正本とする。

## 記載目的

読者がそのままコピーした場合に、変更箇所と方法が決まった後の念のための探索、再確認、履歴調査を減らす。

## 固定root prompt

```text
変更前の調査は、変更箇所と方法を一つに決めるために不足している情報だけに絞り、決まった後は、念のための探索、再確認、履歴調査をせず変更へ進む。
```

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Free `the-caption-3ce91a4-control-free-repository-r1` |
| 対象 | 5つの説明項目のうち「何を調べるか」だけ |
| 基準の誤経路 | Free F08では変更前commandが各反復`13 / 9 / 10 / 10 / 10`件、中央値`10`件だった |
| 既存の影響証拠 | Candidate152の4文版ではF08の変更前commandが`12 / 8 / 7 / 7 / 7`件、中央値`7`件だった |
| 変更軸 | Freeのrootへ変更前調査の一文だけを追加する |
| 品質条件 | F08 5 / 5件でscore `4`を維持する |
| 行動条件 | 変更前command中央値がFreeの`10`件を下回る |
| 解釈 | tokenとelapsedを記述するが、単一case N=5から料金全体へ一般化しない |
| 停止条件 | score `3`以下、excluded attempt、controller error、評価不能、または変更前command中央値が`10`件以上なら停止する |

## 評価条件

- Evaluation set identity: `the-caption-standard14-r1`
- case: `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` r1だけ
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- runtime / CLI: Python 3.14.5 / Codex CLI 0.146.0
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- Freeの保存済みF08 N=5を基準として再利用する
- Candidate157は不足する5 runだけを発行する

prompt identity以外の実効条件とF08 coverageを実行前に機械照合する。不一致があれば一件も発行しない。

## 評価後state

`targeted_f08_n5_evaluated / quality_gate_passed / prechange_command_median_10_to_7 / behavior_effect_observed / included_in_supplementary_article / standard14_not_started / adoption_not_decided / release_not_created / runtime_not_projected`
