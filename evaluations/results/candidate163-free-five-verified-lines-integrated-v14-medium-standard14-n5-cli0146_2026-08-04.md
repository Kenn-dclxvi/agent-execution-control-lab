# Candidate163 / Free 確認済み5文統合版 Rating v14 Medium Standard14 N=5比較

## 結論

Candidate163は、個別N=5で狙った行動への影響を確認した5文を、Freeの0-byte root `AGENTS.md`へそのまま統合した条件である。Standard14 14 caseを各N=5で比較した。

Candidate163は70 / 70件がscore `4`だった。Freeは65 / 70件がscore `4`で、A01の5件がscore `0`だった。A01ではCandidate163の5 / 5件が、利用者の指定値を推測せず質問して停止した。旧統合版Candidate156で残っていた品質失敗は解消した。

Free比で、API価格換算の中央値は`$5.0833 → $4.3711`、`-14.01%`だった。all-agent total token中央値は`3,488,611 → 2,935,725`、`-15.85%`だった。elapsed中央値は`1,166.296 → 1,099.295秒`、`-5.74%`だった。3指標はすべて5 / 5 iterationで低下した。

ただし、この比較が示すのは5文セット全体の結果である。個々の文の因果効果は、各一文だけを追加した個別試験で判断する。A01で誤実装を質問停止へ変えた作業量差を含むため、`-14.01%`を一般的な料金削減率にはしない。

## 比較条件

| 項目 | Free | Candidate163 |
| --- | --- | --- |
| root prompt | 0 byte | 確認済み5文 |
| Evaluation set | Standard14 r1 | 同左 |
| N | 5 | 5 |
| run | 70 valid、excluded 0 | 70 valid、excluded 0 |
| Rating | v14 | 同左 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

両条件のcompatibility keyは`cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致した。Candidate163はFree bundleのroot `AGENTS.md`以外を変更していない。実行前preflightで互換条件と70 slotのcoverageを確認し、Candidate163の不足70 runだけを新規実行した。Freeの保存済み70 runは再実行していない。

## 一表で見る結果

| 指標 | Free | Candidate163 | Free比 |
| --- | ---: | ---: | ---: |
| API価格換算中央値 | `$5.0833` | `$4.3711` | `85.99%`（`-14.01%`） |
| all-agent total token中央値 | 3,488,611 | 2,935,725 | `84.15%`（`-15.85%`） |
| elapsed中央値 | 1,166.296秒 | 1,099.295秒 | `94.26%`（`-5.74%`） |
| quality中央値 | 92.857 | 100.000 | `+7.143` |
| score `4` | 65 / 70 | 70 / 70 | +5件 |
| score `0` | 5 / 70 | 0 / 70 | -5件 |
| A01の質問停止 | 0 / 5 | 5 / 5 | +5件 |

API価格換算は、通常input `$5.00`、cached input `$0.50`、cache write `$6.25`、output `$30.00` / 100万tokenとして、保存済みusageから計算した。実請求額ではない。

## iteration別

| iteration | Free品質 | C163品質 | Free token | C163 token | token差 | Free換算額 | C163換算額 | 金額差 | Free elapsed | C163 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 92.857 | 100.000 | 3,502,016 | 2,973,702 | `-15.09%` | `$5.0833` | `$4.3711` | `-14.01%` | 1,162.225秒 | 1,087.662秒 | `-6.42%` |
| 2 | 92.857 | 100.000 | 3,488,611 | 2,935,725 | `-15.85%` | `$4.9916` | `$4.2449` | `-14.96%` | 1,166.296秒 | 1,072.595秒 | `-8.03%` |
| 3 | 92.857 | 100.000 | 3,676,560 | 2,881,783 | `-21.62%` | `$5.2531` | `$4.5341` | `-13.69%` | 1,302.663秒 | 1,099.295秒 | `-15.61%` |
| 4 | 92.857 | 100.000 | 3,453,487 | 3,061,642 | `-11.35%` | `$4.9237` | `$4.5734` | `-7.12%` | 1,162.000秒 | 1,133.835秒 | `-2.42%` |
| 5 | 92.857 | 100.000 | 3,445,210 | 2,672,867 | `-22.42%` | `$5.2230` | `$4.1448` | `-20.64%` | 1,180.927秒 | 1,156.387秒 | `-2.08%` |

N=5の記述結果であり、統計的な優位は主張しない。

## 5文と今回の観測範囲

| 5文が狙う境界 | 今回のStandard14で確認できたこと | 読み方 |
| --- | --- | --- |
| 利用者成果が不足した場合の質問停止 | A01質問停止`0 / 5 → 5 / 5`。A02は5 / 5件完了 | 統合後も狙った境界を維持 |
| 全成果を方針へまとめてから変更開始 | 全変更caseがscore `4` | 単独効果はCandidate159で確認 |
| 独立作業の担当・判定対象・必要結果の固定 | Standard14には個別試験D01が含まれない | 単独効果はCandidate161で確認 |
| 変更前調査の限定 | 14 case中10 caseでtoken中央値がFreeより低い | 単独の調査行動はCandidate157で確認 |
| 検証を実行票へ固定した完了判断 | 全変更caseがscore `4` | 単独効果はCandidate162で確認 |

Standard14の総合scoreと効率指標は、5文を同時に追加した一条件を測る。表の2行目から5行目について、総合結果を各一文の追加効果へ割り振らない。

## 状態境界

- 評価: `standard14_n5_completed`
- 品質gate: `passed`。70 / 70件がscore `4`
- A01確認: `passed`。質問停止5 / 5件、変更差分0 / 5件
- cost結果: `descriptively_lower`。3指標とも5 / 5 iterationで低下
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`c498dd3944534631a80e70a814fc8171`、execution archive SHA-256は`6b47ce4c0ffb783ee85065550a4337a6205d0cf4054a07df96f0fb2c39ac566b`、final archive SHA-256は`8adfe0e775be18170885e8610b669749ecced08a3b39d147f2a8005b579c6269`である。
