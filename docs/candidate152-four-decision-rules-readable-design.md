# Candidate152 4つの判断ルール試験設計

## 結論

Candidate152はControlFreeRepositoryを直接親とし、外部説明資料へ掲載した4文だけをroot `AGENTS.md`へ追加する。独自caseは作らず、Standard14から選んだ6 caseを各N=5で実行し、品質だけでなく4文に対応する挙動を判定する。

初期計画では、一つでもmechanism gateに失敗した場合はStandard14全体へ進まず、失敗した文だけを改訂した新Candidateを作る方針だった。

## 試験目的の訂正

初期設計は4文だけで各挙動を5 / 5件制御する基準を置いたが、これは短い説明文の実効性を確かめる最初の試験として強すぎた。今回の目的は完全制御ではなく、Freeから行動の選ばれ方が変わり、狙った選択が1回以上出ることの確認へ訂正した。

ただし、Candidate152で狙った選択が出ただけでは効果としない。Freeでも同じ選択が出ている場合は増分効果を判定不能とする。後続の強化版で5 / 5を狙う作業は、この訂正時点で停止した。

## Prompt identity

- identity: `the-caption-3ce91a4-four-decision-rules-readable-r1`
- parent: `the-caption-3ce91a4-control-free-repository-r1`
- changed target: root `AGENTS.md`だけ
- bundle SHA-256: `bcfca3f6bf231fe538c21861c2a99de6755a571e00db5acd7070f230395d3ae6`
- inherited research prompt: なし

## 選択するStandard14 case

| 判断ルール | 使用case | 主な判定対象 |
| --- | --- | --- |
| 仕様を決めるとき | A01 / A02 | 利用者が決める値だけを質問し、repositoryから決められる方法は質問せず解決する |
| 変更を始めるとき | F02 / F04 / F07 | 複数effectまたは複数artifactの関係を把握してから最初の変更を行う |
| 調べるとき | A02 / F01 / F02 / F04 / F07 | 独立した必要readをまとめ、実装確定後のmethod探索と利用先のない再読を行わない |
| 作業を終えるとき | F01 / F02 / F04 / F07 | required validationを先に閉じ、重複実行や成功後の追加確認を行わない |

実行coverageはA01、A02、F01、F02、F04、F07の6 case × N=5、計30 runである。Evaluation set identityはStandard14のままとし、部分coverageであることを保持する。

## 初期の完全制御mechanism gate

以下は実行前に置いた5 / 5基準であり、後から成立したことにはしない。今回の訂正後の判定とは分けて履歴として残す。

### 1. 仕様を決めるとき

- A01 5 / 5でrequired outcome valueを推測しない。
- A01 5 / 5でsource read、test read、artifact変更、test実行を開始せず、その値だけを質問して停止する。
- A02 5 / 5で利用者へ質問せず、repository authorityからcanonical routeを解決する。
- A02 5 / 5で`run.sh`だけを修復し、TaskSpec-required validationを成功させる。

### 2. 変更を始めるとき

- F02 5 / 5で、2 source effectと両経路の関係を確認してから最初のartifact変更を行う。
- F04 5 / 5で、列表示条件と既存table relationを確認してから最初のartifact変更を行う。
- F07 5 / 5で、direct constraintとcompiled provenanceの対を確認してから最初のartifact変更を行う。
- F02 / F04 / F07の15 / 15で、部分変更または未変更停止を起こさずrequired outcome全体を成立させる。

### 3. 調べるとき

- A02 / F01 / F02 / F04 / F07で、同じ先行resultに依存しない最初の必要readを同じmodel stepから発行する。
- implementation choice確定後は、その方法を探すための追加repository readを行わない。
- artifact変更後のreadは、変更により状態が変わったrequired effectの確認だけを許可する。
- 決定済み事項の再確認、念のため、報告材料だけを目的とするreadを0件とする。

### 4. 作業を終えるとき

- F01 / F02 / F04 / F07の20 / 20で、TaskSpec-required validationの全体を最初のvalidation開始前に確定できる実行順で発行する。
- failure resultが出た場合は依存する後続validationを開始しない。
- 同一required validationの根拠のない再実行を0件とする。
- 全required result成功後の追加test、追加diff確認、完了再判断を0件とする。

## Quality gate

- 30 / 30 validかつrateable
- 30 / 30 score `4`
- A01は5 / 5 `awaiting_required_value`、artifact unchanged
- A02とF01 / F02 / F04 / F07は25 / 25でrequired outcome、allowed path、required validationを満たす

quality gateが通っても、4つのmechanism gateのいずれかが失敗した場合は不採用として停止する。token、elapsed、API料金換算はmechanism成立後にだけFreeとの記述比較へ使う。

## 現在のstate

最初の6 case × N=5に加え、差が出やすいF08とF03を各N=5で追加した。「仕様を決める」と「調べる」はFreeと異なる選択を観測した。「変更を始める」と「作業を終える」はCandidate152で狙った選択が出たが、Freeでも同じ選択が出たため増分効果を判定できなかった。

詳細は[`targeted結果`](../evaluations/results/candidate152-free-four-decision-rules-readable-v14-medium-targeted-n5-cli0146_2026-08-03.md)を正本とする。

`targeted_evaluated / effect_observed_2_of_4 / two_rules_not_distinguishable_from_free / stopped / not_adopted / release_not_created / runtime_not_projected`
