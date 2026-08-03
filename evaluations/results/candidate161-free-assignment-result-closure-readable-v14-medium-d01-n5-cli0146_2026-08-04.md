# Candidate161 / Free 担当と結果の閉鎖一文 Rating v14 Medium D01 N=5比較

## 結論

Candidate161は、Freeの0-byte root `AGENTS.md`へ次の一文だけを追加した。

> 独立した作業を分ける場合は、開始前に担当、判定対象、必要な結果を対応づけ、担当の完了結果だけを受け取り、同じ判定を別の担当や進捗報告でやり直して補わない。

D01 N=5では5 / 5件がscore `4`だった。worker起動前に担当identity、判定対象、必要な結果を対応づけた実行はFreeの`1 / 5件`からCandidate161の`5 / 5件`へ増えた。worker result欠落と、受領後にrootが同じreviewをやり直す行動は0 / 5件だった。

したがって、この一文が担当と必要結果を起動前に対応づける選択へ影響したと判定する。tokenとelapsedの低下は観測していない。

## 比較条件

| 項目 | Free | Candidate161 |
| --- | --- | --- |
| root prompt | 0 byte | 1文 |
| Evaluation set / case | D01 r1 | 同左 |
| N | 5 | 5 |
| Rating | v14 | 同左 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

prompt identity以外の実効条件は実行前preflightで一致した。Candidate161の5 runだけを新規発行し、同じ条件のFree 5件を基準にした。

## 結果

| 指標 | Free | Candidate161 | 差 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 0 |
| 起動前の担当・対象・結果対応 | 1 / 5 | 5 / 5 | +4件 |
| worker result欠落 | 0 / 5 | 0 / 5 | 0 |
| rootによる同一reviewのやり直し | 0 / 5 | 0 / 5 | 0 |
| all-agent total token中央値 | 299,897 | 301,810 | `+0.64%` |
| elapsed中央値 | 125.563秒 | 135.255秒 | `+7.72%` |

## 状態境界

- 評価: `targeted_d01_n5_completed`
- 品質gate: `passed`
- 行動条件: `passed`。起動前対応`1 / 5 → 5 / 5`
- 閉鎖条件: `passed`。重複review `0 / 5`
- cost低下: `not_observed`
- 掲載判断: `included_in_supplementary_article`
- Standard14: `not_started`
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`de389fce7adf402fb9c9cf3ce75ca752`、execution archive SHA-256は`7d5cd2b82fa0a2556c0d52d4d812a2067e953dd39399a4f2e8cd212993268fc3`、final archive SHA-256は`d0fce0aeb0018e13faff114c7e02be143794aaf59ee7b5de4fffa298f6ba2916`である。

