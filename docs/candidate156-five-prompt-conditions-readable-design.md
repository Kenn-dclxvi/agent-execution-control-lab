# Candidate156 5文prompt条件 Standard14試験設計・結果

## 結論

Candidate156は、ControlFreeRepositoryの0-byte root `AGENTS.md`へ、利用者が指定した5文だけを追加した。5文セット全体を一つの比較条件とし、Standard14各N=5でFreeとの差を測定した。

5文は複数の判断を同時に扱うため、個々の文へ因果効果を帰属しない。品質、all-agent token、elapsedの差を5文セット全体の記述結果として扱う。

結果はFreeと同じ65 / 70件がscore `4`、A01の5 / 5件がscore `0`だった。Free比の中央値はAPI価格換算`+3.98%`、all-agent token`+3.18%`、elapsed`+14.10%`だった。品質改善がなく効率中央値も改善しなかったため、不採用で停止した。詳細は[`Candidate156 / Free Standard14 N=5比較`](../evaluations/results/candidate156-free-five-prompt-conditions-readable-v14-medium-standard14-n5-cli0146_2026-08-03.md)を正本とする。

## Candidate作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt set | Free `the-caption-3ce91a4-control-free-repository-r1` |
| 基準の最短正常経路 | TaskSpecで成果と範囲を固定し、必要なrepository authorityだけを読み、単一作業はrootが実行し、required validation完了後に追加調査せず終了する |
| 保存済みの誤経路 | Free Standard14 N=5ではA01の5 / 5件が未固定値を推測して変更と試験へ進んだ。Candidate148の別の5項目版でも同経路は5 / 5件残った |
| 既存入力だけでは防げない理由 | FreeではTaskSpecとpath-scoped authorityが存在してもA01誤経路が再現した。変更開始、調査、結果待機、完了の境界もroot promptでは未指定である |
| 変更軸 | Freeの0-byte rootを、利用者指定の5文セットへ置換する。単文ablationではない |
| 消す判断点 | 未固定成果値の推測、部分変更、欠けた結果の補完、利用先のない調査、無関係な待機、成功後の追加確認 |
| 増える判断点 | 利用者成果と実装方法、全成果を含む変更方針、独立作業の結果identity、result effect scope、検証完了の分類 |
| 品質確認 | Standard14各N=5の70 runをRating v14で採点する |
| 停止条件 | score `3`以下、excluded attempt、controller error、または評価不能が一件でもあれば、cost差を改善根拠や採用根拠にせず停止する |

ユーザーが5文セット全体のStandard14試験を明示したため、複数predicateを同時に変更する。結果から個別文の効果を分離しない。

## 固定root prompt

root `AGENTS.md`は、次の5文だけを持つ。

```text
- 利用者が決めるべき成果が不足している場合は、その成果だけを質問し、変更やテストを始めない。実装方法が未確認なだけなら、プロジェクト内の根拠から選ぶ。
- 必要な成果をすべて挙げ、変更箇所、直し方、維持する動作を一つの方針にできた場合だけ変更を始める。
- 独立した作業を分ける場合は、各作業の担当、判定対象、必要な結果を開始前に決める。欠けた結果を進捗報告や別作業の結果で補わない。
- 調査は未完了の成果を決めるものだけに絞る。先の結果で対象、権限、方法、停止条件が変わる作業だけを待たせ、影響を受けない調査はまとめて行う。
- 変更後は必要なテストと差分確認を先に一式決める。失敗したら後続を止め、実行中なら同じ結果を待ち、全結果がそろったら一度だけ完了を判断する。
```

## 評価条件

- Evaluation set: `the-caption-standard14-r1`
- Rating: v14
- model / reasoning: `gpt-5.6-sol / medium`
- Agent / runtime / CLI: Free v14 Medium Standard14 N=5の固定条件と完全一致
- permission: `workspace-write / never`
- token accounting: all-agent v1
- profile `max_workers`: `24`
- atomic経路で不足runだけを発行する
- Freeの保存済みN=5を基準resultとして再利用し、Free runを再実行しない
- 14 case × 5 sampleの70 runを一つのStandard14比較として扱う

評価前にFree基準result、全fixture、TaskSpec、rating、model、reasoning、Agent / runtime / CLI、permission、executor挙動、token accountingを機械照合する。prompt identity以外に不一致があれば、一件も発行しない。

## 評価後state

`standard14_n5_evaluated / quality_gate_failed / a01_question_stop_failed_5_of_5 / efficiency_medians_higher / not_adopted / release_not_created / runtime_not_projected`
