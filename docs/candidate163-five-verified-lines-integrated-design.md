# Candidate163 確認済み5文統合版 Standard14 N=5試験設計

## 結論

Candidate163は、個別N=5でFreeとの行動差を確認した5文を、Freeの0-byte root `AGENTS.md`へそのまま統合する。Standard14 14 caseを各N=5で実行し、5文セット全体の品質とKPIをFreeの保存済みStandard14 N=5と比較する。

個別試験の効果が統合時にも維持されるとは仮定しない。Standard14の結果から個々の文の因果効果も分離しない。

## 固定root prompt

```text
利用者が決める変更後の動作や値が書かれていない場合は、現在のコードやテストから推測せず、その結果だけを質問する。ファイルの場所や実装方法が未確認なだけなら、プロジェクト内で決めて進める。
変更前に、必要な成果、変更箇所、直し方、維持する動作を一つの方針にまとめ、どれか決まらない間は変更しない。
独立した作業を分ける場合は、開始前に担当、判定対象、必要な結果を対応づけ、担当の完了結果だけを受け取り、同じ判定を別の担当や進捗報告でやり直して補わない。
変更前の調査は、変更箇所と方法を一つに決めるために不足している情報だけに絞り、決まった後は、念のための探索、再確認、履歴調査をせず変更へ進む。
変更後は、必要なテストと差分確認を一つの実行票として先に固定し、実行中は同じ結果だけを待ち、失敗なら後続を止め、全結果がそろったら追加確認せず一度だけ完了を判断する。
```

## 実行前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準 | ControlFreeRepositoryの保存済みRating v14 Medium Standard14 N=5 |
| 変更軸 | root `AGENTS.md`の5文だけ |
| coverage | Standard14 14 case × 5 sample = 70 run |
| 品質gate | 70 / 70 validかつrateable、score `4`。一件でもscore `3`以下ならcostを採用根拠にしない |
| A01確認 | 未指定の変更後値を推測せず、質問して停止する |
| 実行条件 | Python 3.14.5、Codex CLI 0.146.0、`gpt-5.6-sol / medium`、`workspace-write / never`、M=24 |
| 停止条件 | prompt identity以外の不一致、coverage不一致、excluded attempt、controller error、または評価不能があれば結果登録へ進めない |

Freeの保存済み70 runは再実行しない。Candidate163の不足70 runだけをatomic経路で発行する。

## 評価結果

Standard14 N=5は70 / 70件がscore `4`となり、品質gateを通過した。A01は5 / 5件で利用者の指定値を質問して停止した。Free比の中央値は、API価格換算`-14.01%`、all-agent total token`-15.85%`、elapsed`-5.74%`だった。

詳細は[`Candidate163 / Free Standard14 N=5比較`](../evaluations/results/candidate163-free-five-verified-lines-integrated-v14-medium-standard14-n5-cli0146_2026-08-04.md)を正本とする。

## 現在state

`standard14_n5_completed / quality_gate_passed / adoption_not_decided / release_not_created / runtime_not_projected`
