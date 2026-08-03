# Candidate157 / Free 変更前調査一文 Rating v14 Medium F08 N=5比較

## 結論

Candidate157は、Freeの0-byte root `AGENTS.md`へ次の一文だけを追加した。

> 変更前の調査は、変更箇所と方法を一つに決めるために不足している情報だけに絞り、決まった後は、念のための探索、再確認、履歴調査をせず変更へ進む。

F08 N=5では、5 / 5件がscore `4`だった。変更前commandはFreeの`13 / 9 / 10 / 10 / 10`件、中央値`10`件に対し、Candidate157は`8 / 9 / 6 / 6 / 7`件、中央値`7`件だった。品質を維持したまま、変更前command中央値が30%減ったため、この一文が調査の選び方へ影響したと判定する。

all-agent total token中央値はFreeの`424,826`から`307,730`へ`-27.56%`、elapsed中央値は`121.538秒`から`99.606秒`へ`-18.05%`だった。ただし単一case N=5の結果であり、Standard14全体の料金削減へ一般化しない。

## 比較条件

| 項目 | Free | Candidate157 |
| --- | --- | --- |
| root prompt | 0 byte | 214 byte、1文 |
| case | F08 r1 | F08 r1 |
| N | 5 | 5 |
| run | 5 valid | 5 valid、excluded 0 |
| Rating | v14 | v14 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

prompt identity以外の実効条件は実行前preflightで一致した。Candidate157の5件は新規実行し、Freeの保存済みF08 5件は再実行していない。

## 結果

| 指標 | Free | Candidate157 | Free比 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 差0 |
| 変更前command中央値 | 10 | 7 | `-30.00%` |
| all-agent total token中央値 | 424,826 | 307,730 | `-27.56%` |
| elapsed中央値 | 121.538秒 | 99.606秒 | `-18.05%` |

変更前commandは、各runの最初のfile changeより前に完了したcommand executionを数えた。Candidate157は全5件でFree以下となり、4 / 5件でFreeより少なかった。

## 状態境界

- 評価: `targeted_f08_n5_completed`
- 品質gate: `passed`
- 行動条件: `passed`。変更前command中央値`10 → 7`
- 掲載判断: `included_in_supplementary_article`
- Standard14: `not_started`
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`9d512a1910a5411c84c64774ee2ecf4b`、execution archive SHA-256は`6cf9461b2d56b309e78f88092742090d9563547a350bea2a05726fc8406f788b`、final archive SHA-256は`a3c83e199b4ff0c0fadb50b8088e5039312336671b0f85b51ac7816f22819612`である。
