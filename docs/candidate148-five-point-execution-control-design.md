# Candidate148 5項目execution control設計

## 結論

Candidate148は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、利用者向け説明資料で示した5項目だけの実行制御を追加する。5項目は`GOAL / START / SEARCH / SPLIT / FINISH`とする。

ユーザーが5項目セット全体を比較条件として指定したため、本Candidateは複数predicateを同時に変更する。個別項目の因果効果は主張しない。C148全体の品質、実行token、elapsedと観測経路だけを記述する。

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Free `the-caption-3ce91a4-control-free-repository-r1` |
| 基準の最短正常経路 | TaskSpecで成果と範囲を固定し、必要なrepository authorityだけを読み、単一作業はrootが実行し、required validation完了後に追加調査せず終了する |
| 対象とする誤経路 | Free条件でA01 5 / 5件が未固定値の確認前に変更へ進んだ。過去系列では不要な探索、重複producer、検証後のmodel再入がtoken増加経路として観測された |
| 既存入力だけでは防げない理由 | Free条件ではTaskSpecとpath-scoped authorityが残っていてもA01誤経路が再現した。rootで開始・探索・分担・終了境界を明示する必要がある |
| 変更軸 | Freeの0-byte rootを5項目セットへ置換する。単項目ablationではない |
| 消す判断点 | 未固定成果値を推測する判断、探索終点の再判断、単一作業のproducer再選択、成功後の追加確認 |
| 増える判断点 | `required outcome`、探索終点、独立作業、required validationの分類。5項目間の関係解釈 |
| 品質確認 | Standard14各N=5の70 / 70 score 4 |
| 停止条件 | Standard14でscore 3以下、excluded attempt、controller error、または評価不能が1件でもあれば採用判定へ進まない |

## 固定root prompt

root `AGENTS.md`は見出しと次の5 bulletだけを持つ。

```text
# THE-CAPTION execution control

- GOAL: 実行前に、利用者が確認できる完成状態、変更してよい範囲、変更しない範囲、必要な検証をTaskSpecから固定する。
- START: 完成状態を変える未決定事項があり、利用者入力または一意なrepository authorityへbindできない場合は、実装・変更・testを開始せず、その一点だけを質問する。repositoryから一意に決まる事項は必要な範囲だけ確認して進める。
- SEARCH: 対象、対象へ適用されるrepository instruction、実装方法を一意に決めるauthorityだけを読む。実装可能な一つの方法が決まったら、追加の探索、再読、履歴調査をしない。
- SPLIT: 一つのoperationで完了する作業はrootが直接実行する。TaskSpecが独立した別executionを要求する場合、または独立した別operationがある場合だけ分担し、同じpredicateを複数producerへ割り当てない。
- FINISH: 変更後にTaskSpec-required validationを必要十分な一waveで実行する。失敗時は後続を止め、全件成功時は追加のread・再検証をせず、結果を一度だけ判断して完了を報告する。
```

## 評価条件

- Evaluation set: `the-caption-standard14-r1`
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- Agent / runtime / CLI: Free v14 Medium N=5の固定条件と完全一致
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- atomic経路で不足runだけを発行する
- Freeの保存済みN=5を基準resultとして再利用し、Free runを再実行しない
- 14 case × 5 iterationの70 runを一つのStandard14比較として扱う

評価結果は[`Candidate148 / Free Standard14 N=5比較`](../evaluations/results/candidate148-free-five-point-execution-control-v14-medium-standard14-n5-cli0146_2026-08-03.md)へ記録した。A01が5 / 5 score `0`だったため、Candidate148は`not_adopted`で停止した。releaseとTHE-CAPTION本体への反映は行わない。
